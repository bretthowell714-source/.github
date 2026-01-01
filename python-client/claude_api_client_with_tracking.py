#!/usr/bin/env python3
"""
Claude API Client with Automatic Usage Tracking
Wraps Anthropic API with usage monitoring and limit enforcement
"""

import os
from typing import Optional, List, Dict, Any
from anthropic import Anthropic
from api_usage_tracker import APIUsageTracker


class TrackedClaudeClient:
    """
    Claude API client with automatic usage tracking and limit enforcement
    """

    def __init__(self, api_key: Optional[str] = None, tracker: Optional[APIUsageTracker] = None):
        """
        Initialize tracked client

        Args:
            api_key: Anthropic API key
            tracker: Optional existing tracker
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key required")

        self.client = Anthropic(api_key=self.api_key)
        self.tracker = tracker or APIUsageTracker()

    def create_message(self, model: str, max_tokens: int, messages: List[Dict[str, str]],
                      **kwargs) -> Any:
        """
        Create a message with automatic usage tracking

        Args:
            model: Model to use
            max_tokens: Maximum tokens
            messages: List of messages
            **kwargs: Additional arguments

        Returns:
            API response

        Raises:
            RuntimeError: If usage limits would be exceeded
        """
        # Estimate tokens (rough estimate)
        estimated_input = sum(len(m.get('content', '')) // 4 for m in messages)
        estimated_total = estimated_input + max_tokens

        # Check if we can make the request
        can_proceed, reason = self.tracker.can_make_request(estimated_total)

        if not can_proceed:
            raise RuntimeError(f"Usage limit exceeded: {reason}")

        try:
            # Make the actual API call
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=messages,
                **kwargs
            )

            # Record successful call
            self.tracker.record_call(
                endpoint='/v1/messages',
                model=model,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                success=True
            )

            return response

        except Exception as e:
            # Record failed call
            self.tracker.record_call(
                endpoint='/v1/messages',
                model=model,
                input_tokens=estimated_input,
                output_tokens=0,
                success=False,
                error=str(e)
            )
            raise

    def get_usage_report(self, period: str = 'today') -> str:
        """Get usage report"""
        return self.tracker.generate_report(period)

    def get_remaining_budget(self) -> Dict[str, Any]:
        """Get remaining budget and limits"""
        stats = self.tracker.get_usage_stats('today')

        return {
            'daily_budget_remaining': self.tracker.limits.daily_budget_usd - stats['limits']['daily_budget_used'],
            'daily_requests_remaining': self.tracker.limits.max_requests_per_day - stats['limits']['daily_requests_used'],
            'total_spent_today': stats['limits']['daily_budget_used'],
            'total_cost_this_month': self.tracker.get_usage_stats('month')['total_cost_usd']
        }


# Example usage
if __name__ == "__main__":
    client = TrackedClaudeClient()

    print("Current Budget Status:")
    budget = client.get_remaining_budget()
    print(f"  Daily budget remaining: ${budget['daily_budget_remaining']:.2f}")
    print(f"  Requests remaining today: {budget['daily_requests_remaining']}")
    print(f"  Spent today: ${budget['total_spent_today']:.2f}")
    print(f"  Spent this month: ${budget['total_cost_this_month']:.2f}")

    print("\n" + client.get_usage_report('today'))
