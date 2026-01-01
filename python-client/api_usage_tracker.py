#!/usr/bin/env python3
"""
Anthropic API Usage Tracker
Monitors API usage to stay within rate limits and spending limits
"""

import os
import json
import time
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class APICall:
    """Single API call record"""
    timestamp: str
    endpoint: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    success: bool
    error: Optional[str] = None


@dataclass
class UsageLimits:
    """API usage limits"""
    # Rate limits (per minute)
    max_requests_per_minute: int = 50
    max_tokens_per_minute: int = 40000

    # Daily limits
    max_requests_per_day: int = 1000
    max_tokens_per_day: int = 1000000

    # Spending limits
    daily_budget_usd: float = 10.0
    monthly_budget_usd: float = 100.0

    # Alert thresholds (percentage)
    alert_threshold: float = 0.8  # Alert at 80% usage


class APIUsageTracker:
    """
    Track API usage and enforce limits
    """

    # Anthropic pricing (as of 2026-01-01)
    PRICING = {
        'claude-opus-4': {'input': 0.015, 'output': 0.075},  # per 1K tokens
        'claude-sonnet-4': {'input': 0.003, 'output': 0.015},
        'claude-haiku-4': {'input': 0.00025, 'output': 0.00125},
        'claude-3-5-sonnet': {'input': 0.003, 'output': 0.015},
        'claude-3-5-haiku': {'input': 0.001, 'output': 0.005}
    }

    def __init__(self, storage_dir: str = None, limits: Optional[UsageLimits] = None):
        """Initialize usage tracker"""
        self.storage_dir = Path(storage_dir or os.path.expanduser("~/.claude_api_usage"))
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.usage_file = self.storage_dir / "usage_log.json"
        self.limits_file = self.storage_dir / "limits.json"
        self.alerts_file = self.storage_dir / "alerts.json"

        self.limits = limits or self._load_limits()
        self.calls: List[APICall] = self._load_calls()
        self.alerts: List[Dict] = self._load_alerts()

    def _load_limits(self) -> UsageLimits:
        """Load usage limits"""
        if self.limits_file.exists():
            with open(self.limits_file, 'r') as f:
                return UsageLimits(**json.load(f))
        return UsageLimits()

    def _load_calls(self) -> List[APICall]:
        """Load API call history"""
        if self.usage_file.exists():
            with open(self.usage_file, 'r') as f:
                data = json.load(f)
                return [APICall(**call) for call in data]
        return []

    def _load_alerts(self) -> List[Dict]:
        """Load alerts"""
        if self.alerts_file.exists():
            with open(self.alerts_file, 'r') as f:
                return json.load(f)
        return []

    def _save_calls(self):
        """Save API calls to disk"""
        with open(self.usage_file, 'w') as f:
            json.dump([asdict(call) for call in self.calls], f, indent=2)

    def _save_limits(self):
        """Save limits to disk"""
        with open(self.limits_file, 'w') as f:
            json.dump(asdict(self.limits), f, indent=2)

    def _save_alerts(self):
        """Save alerts to disk"""
        with open(self.alerts_file, 'w') as f:
            json.dump(self.alerts, f, indent=2)

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost for API call

        Args:
            model: Model name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Cost in USD
        """
        # Find matching price model
        pricing = None
        for key, price in self.PRICING.items():
            if key in model.lower():
                pricing = price
                break

        if not pricing:
            pricing = self.PRICING['claude-sonnet-4']  # Default

        input_cost = (input_tokens / 1000) * pricing['input']
        output_cost = (output_tokens / 1000) * pricing['output']

        return input_cost + output_cost

    def record_call(self, endpoint: str, model: str, input_tokens: int,
                   output_tokens: int, success: bool = True,
                   error: Optional[str] = None) -> APICall:
        """
        Record an API call

        Args:
            endpoint: API endpoint
            model: Model used
            input_tokens: Input tokens
            output_tokens: Output tokens
            success: Whether call succeeded
            error: Error message if failed

        Returns:
            Recorded API call
        """
        cost = self.calculate_cost(model, input_tokens, output_tokens)

        call = APICall(
            timestamp=datetime.datetime.now().isoformat(),
            endpoint=endpoint,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            success=success,
            error=error
        )

        self.calls.append(call)
        self._save_calls()

        # Check limits after recording
        self._check_limits()

        return call

    def can_make_request(self, estimated_tokens: int = 4000) -> tuple[bool, str]:
        """
        Check if we can make another request

        Args:
            estimated_tokens: Estimated tokens for request

        Returns:
            (can_proceed, reason)
        """
        now = datetime.datetime.now()

        # Check rate limits (per minute)
        minute_ago = now - datetime.timedelta(minutes=1)
        recent_calls = [
            c for c in self.calls
            if datetime.datetime.fromisoformat(c.timestamp) > minute_ago
        ]

        if len(recent_calls) >= self.limits.max_requests_per_minute:
            return False, f"Rate limit: {self.limits.max_requests_per_minute} requests/minute exceeded"

        recent_tokens = sum(c.input_tokens + c.output_tokens for c in recent_calls)
        if recent_tokens + estimated_tokens > self.limits.max_tokens_per_minute:
            return False, f"Token limit: {self.limits.max_tokens_per_minute} tokens/minute exceeded"

        # Check daily limits
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_calls = [
            c for c in self.calls
            if datetime.datetime.fromisoformat(c.timestamp) > today_start
        ]

        if len(today_calls) >= self.limits.max_requests_per_day:
            return False, f"Daily limit: {self.limits.max_requests_per_day} requests/day exceeded"

        today_tokens = sum(c.input_tokens + c.output_tokens for c in today_calls)
        if today_tokens + estimated_tokens > self.limits.max_tokens_per_day:
            return False, f"Daily token limit: {self.limits.max_tokens_per_day} tokens/day exceeded"

        # Check spending limits
        today_cost = sum(c.cost_usd for c in today_calls)
        estimated_cost = self.calculate_cost('claude-sonnet-4', estimated_tokens // 2, estimated_tokens // 2)

        if today_cost + estimated_cost > self.limits.daily_budget_usd:
            return False, f"Daily budget: ${self.limits.daily_budget_usd:.2f} exceeded"

        # Check monthly budget
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_calls = [
            c for c in self.calls
            if datetime.datetime.fromisoformat(c.timestamp) > month_start
        ]
        month_cost = sum(c.cost_usd for c in month_calls)

        if month_cost + estimated_cost > self.limits.monthly_budget_usd:
            return False, f"Monthly budget: ${self.limits.monthly_budget_usd:.2f} exceeded"

        return True, "OK"

    def _check_limits(self):
        """Check if approaching limits and create alerts"""
        now = datetime.datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        today_calls = [
            c for c in self.calls
            if datetime.datetime.fromisoformat(c.timestamp) > today_start
        ]

        # Check daily request limit
        daily_requests = len(today_calls)
        if daily_requests >= self.limits.max_requests_per_day * self.limits.alert_threshold:
            self._create_alert(
                f"Approaching daily request limit: {daily_requests}/{self.limits.max_requests_per_day}"
            )

        # Check daily token limit
        daily_tokens = sum(c.input_tokens + c.output_tokens for c in today_calls)
        if daily_tokens >= self.limits.max_tokens_per_day * self.limits.alert_threshold:
            self._create_alert(
                f"Approaching daily token limit: {daily_tokens:,}/{self.limits.max_tokens_per_day:,}"
            )

        # Check daily budget
        daily_cost = sum(c.cost_usd for c in today_calls)
        if daily_cost >= self.limits.daily_budget_usd * self.limits.alert_threshold:
            self._create_alert(
                f"Approaching daily budget: ${daily_cost:.2f}/${self.limits.daily_budget_usd:.2f}"
            )

    def _create_alert(self, message: str):
        """Create an alert"""
        alert = {
            'timestamp': datetime.datetime.now().isoformat(),
            'message': message
        }

        # Don't duplicate recent alerts
        recent_alerts = [
            a for a in self.alerts
            if a['message'] == message and
            datetime.datetime.fromisoformat(a['timestamp']) >
            datetime.datetime.now() - datetime.timedelta(hours=1)
        ]

        if not recent_alerts:
            self.alerts.append(alert)
            self._save_alerts()
            print(f"⚠️  ALERT: {message}")

    def get_usage_stats(self, period: str = 'today') -> Dict[str, Any]:
        """
        Get usage statistics

        Args:
            period: 'today', 'week', 'month', or 'all'

        Returns:
            Usage statistics
        """
        now = datetime.datetime.now()

        if period == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'week':
            start = now - datetime.timedelta(days=7)
        elif period == 'month':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start = datetime.datetime.min

        period_calls = [
            c for c in self.calls
            if datetime.datetime.fromisoformat(c.timestamp) > start
        ]

        total_cost = sum(c.cost_usd for c in period_calls)
        total_tokens = sum(c.input_tokens + c.output_tokens for c in period_calls)
        total_input = sum(c.input_tokens for c in period_calls)
        total_output = sum(c.output_tokens for c in period_calls)

        # By model
        by_model = defaultdict(lambda: {'calls': 0, 'tokens': 0, 'cost': 0.0})
        for call in period_calls:
            by_model[call.model]['calls'] += 1
            by_model[call.model]['tokens'] += call.input_tokens + call.output_tokens
            by_model[call.model]['cost'] += call.cost_usd

        # Success rate
        successful = sum(1 for c in period_calls if c.success)
        success_rate = (successful / len(period_calls) * 100) if period_calls else 0

        return {
            'period': period,
            'total_calls': len(period_calls),
            'successful_calls': successful,
            'success_rate': success_rate,
            'total_tokens': total_tokens,
            'input_tokens': total_input,
            'output_tokens': total_output,
            'total_cost_usd': total_cost,
            'by_model': dict(by_model),
            'limits': {
                'daily_requests_used': len([
                    c for c in period_calls
                    if datetime.datetime.fromisoformat(c.timestamp).date() == now.date()
                ]),
                'daily_requests_limit': self.limits.max_requests_per_day,
                'daily_budget_used': sum(
                    c.cost_usd for c in period_calls
                    if datetime.datetime.fromisoformat(c.timestamp).date() == now.date()
                ),
                'daily_budget_limit': self.limits.daily_budget_usd
            }
        }

    def generate_report(self, period: str = 'today') -> str:
        """Generate usage report"""
        stats = self.get_usage_stats(period)

        report = []
        report.append("=" * 80)
        report.append(f"API USAGE REPORT - {period.upper()}")
        report.append("=" * 80)
        report.append(f"\n📊 Overview:")
        report.append(f"  Total Calls: {stats['total_calls']:,}")
        report.append(f"  Success Rate: {stats['success_rate']:.1f}%")
        report.append(f"  Total Tokens: {stats['total_tokens']:,}")
        report.append(f"    Input: {stats['input_tokens']:,}")
        report.append(f"    Output: {stats['output_tokens']:,}")
        report.append(f"  Total Cost: ${stats['total_cost_usd']:.4f}")

        report.append(f"\n💰 Budget Status:")
        daily_pct = (stats['limits']['daily_budget_used'] / stats['limits']['daily_budget_limit']) * 100
        report.append(f"  Daily: ${stats['limits']['daily_budget_used']:.2f} / ${stats['limits']['daily_budget_limit']:.2f} ({daily_pct:.1f}%)")

        report.append(f"\n📈 Rate Limits:")
        req_pct = (stats['limits']['daily_requests_used'] / stats['limits']['daily_requests_limit']) * 100
        report.append(f"  Daily Requests: {stats['limits']['daily_requests_used']} / {stats['limits']['daily_requests_limit']} ({req_pct:.1f}%)")

        if stats['by_model']:
            report.append(f"\n🤖 By Model:")
            for model, data in sorted(stats['by_model'].items(), key=lambda x: x[1]['cost'], reverse=True):
                report.append(f"  {model}:")
                report.append(f"    Calls: {data['calls']}")
                report.append(f"    Tokens: {data['tokens']:,}")
                report.append(f"    Cost: ${data['cost']:.4f}")

        # Recent alerts
        recent_alerts = [
            a for a in self.alerts
            if datetime.datetime.fromisoformat(a['timestamp']) >
            datetime.datetime.now() - datetime.timedelta(days=1)
        ]

        if recent_alerts:
            report.append(f"\n⚠️  Recent Alerts ({len(recent_alerts)}):")
            for alert in recent_alerts[-5:]:
                report.append(f"  • {alert['message']}")

        report.append("\n" + "=" * 80)

        return "\n".join(report)

    def set_limits(self, **kwargs):
        """Update usage limits"""
        for key, value in kwargs.items():
            if hasattr(self.limits, key):
                setattr(self.limits, key, value)

        self._save_limits()

    def reset_stats(self, period: str = 'all'):
        """Reset statistics"""
        if period == 'all':
            self.calls = []
            self.alerts = []
        else:
            # Implement partial reset if needed
            pass

        self._save_calls()
        self._save_alerts()


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Anthropic API Usage Tracker")
    parser.add_argument('command', choices=['record', 'check', 'stats', 'report', 'set-limits', 'reset'])
    parser.add_argument('--model', default='claude-sonnet-4')
    parser.add_argument('--input-tokens', type=int, default=1000)
    parser.add_argument('--output-tokens', type=int, default=1000)
    parser.add_argument('--period', default='today', choices=['today', 'week', 'month', 'all'])
    parser.add_argument('--daily-budget', type=float)
    parser.add_argument('--monthly-budget', type=float)

    args = parser.parse_args()

    tracker = APIUsageTracker()

    if args.command == 'record':
        call = tracker.record_call(
            endpoint='/v1/messages',
            model=args.model,
            input_tokens=args.input_tokens,
            output_tokens=args.output_tokens
        )
        print(f"Recorded call: {call.cost_usd:.4f} USD")

    elif args.command == 'check':
        can_proceed, reason = tracker.can_make_request(args.input_tokens + args.output_tokens)
        if can_proceed:
            print(f"✅ Can make request: {reason}")
        else:
            print(f"❌ Cannot make request: {reason}")

    elif args.command == 'stats':
        stats = tracker.get_usage_stats(args.period)
        print(json.dumps(stats, indent=2))

    elif args.command == 'report':
        print(tracker.generate_report(args.period))

    elif args.command == 'set-limits':
        updates = {}
        if args.daily_budget:
            updates['daily_budget_usd'] = args.daily_budget
        if args.monthly_budget:
            updates['monthly_budget_usd'] = args.monthly_budget

        tracker.set_limits(**updates)
        print(f"Limits updated: {updates}")

    elif args.command == 'reset':
        tracker.reset_stats(args.period)
        print(f"Stats reset for period: {args.period}")


if __name__ == "__main__":
    main()
