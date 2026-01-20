/**
 * Code Analyzer Tool
 * Analyzes code files for metrics, complexity, and quality
 */

module.exports = {
  name: "code-analyzer",
  description: "Analyze code files for metrics, complexity, and quality issues",
  parameters: {
    type: "object",
    properties: {
      filepath: {
        type: "string",
        description: "Path to the code file to analyze"
      },
      metrics: {
        type: "array",
        description: "Metrics to calculate: complexity, coverage, duplication, security",
        items: {
          type: "string",
          enum: ["complexity", "coverage", "duplication", "security", "performance"]
        },
        default: ["complexity", "security"]
      }
    },
    required: ["filepath"]
  },

  execute: async (params, context) => {
    const fs = require("fs").promises;
    const path = require("path");

    try {
      // Read file
      const content = await fs.readFile(params.filepath, "utf-8");
      const lines = content.split("\n");

      const analysis = {
        file: params.filepath,
        timestamp: new Date().toISOString(),
        metrics: {}
      };

      // Analyze each requested metric
      for (const metric of params.metrics || ["complexity", "security"]) {
        switch (metric) {
          case "complexity":
            analysis.metrics.complexity = analyzeComplexity(content, lines);
            break;
          case "coverage":
            analysis.metrics.coverage = analyzeCoverage(content);
            break;
          case "duplication":
            analysis.metrics.duplication = analyzeDuplication(content);
            break;
          case "security":
            analysis.metrics.security = analyzeSecurityIssues(content, lines);
            break;
          case "performance":
            analysis.metrics.performance = analyzePerformance(content);
            break;
        }
      }

      return {
        success: true,
        analysis: analysis
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
};

function analyzeComplexity(content, lines) {
  const functions = (content.match(/\bfunction\b|\b(const|let|var)\s+\w+\s*=\s*(?:async\s*)?\(/g) || []).length;
  const conditionals = (content.match(/\bif\b|\belse\b|\bswitch\b|\bcase\b/g) || []).length;
  const loops = (content.match(/\bfor\b|\bwhile\b|\bforeach\b/g) || []).length;

  // Cyclomatic complexity
  const cyclomaticComplexity = Math.max(1, conditionals + loops);

  return {
    functions,
    conditionals,
    loops,
    cyclomaticComplexity,
    linesOfCode: lines.length,
    averageComplexityPerFunction: Math.round(cyclomaticComplexity / Math.max(1, functions) * 100) / 100
  };
}

function analyzeCoverage(content) {
  const tests = (content.match(/\b(describe|it|test|expect|assert)\b/g) || []).length;
  const assertions = (content.match(/\b(expect|assert|should|ok)\b/g) || []).length;

  return {
    hasTests: tests > 0,
    testCount: tests,
    assertionCount: assertions,
    estimatedCoverage: tests > 0 ? "High" : "Low"
  };
}

function analyzeDuplication(content) {
  const lines = content.split("\n");
  const lineFrequency = {};

  lines.forEach(line => {
    const trimmed = line.trim();
    if (trimmed.length > 20) {
      lineFrequency[trimmed] = (lineFrequency[trimmed] || 0) + 1;
    }
  });

  const duplicates = Object.values(lineFrequency).filter(count => count > 1);
  const duplicationRatio = duplicates.length / lines.length;

  return {
    duplicateLines: duplicates.reduce((a, b) => a + b, 0),
    duplicationPercentage: Math.round(duplicationRatio * 100),
    severity: duplicationRatio > 0.1 ? "High" : duplicationRatio > 0.05 ? "Medium" : "Low"
  };
}

function analyzeSecurityIssues(content, lines) {
  const issues = [];

  // Check for common security issues
  if (content.includes("eval(")) {
    issues.push({ type: "eval-usage", severity: "Critical", line: findLine(lines, "eval") });
  }

  if (content.includes("dangerouslySetInnerHTML")) {
    issues.push({ type: "dangerouslySetInnerHTML", severity: "High", line: findLine(lines, "dangerouslySetInnerHTML") });
  }

  if (content.includes("sql") && !content.includes("parameterized")) {
    issues.push({ type: "sql-injection-risk", severity: "High", line: findLine(lines, "sql") });
  }

  if (content.match(/password\s*=\s*["'].*["']/i)) {
    issues.push({ type: "hardcoded-password", severity: "Critical", line: findLine(lines, "password") });
  }

  if (content.includes("process.env")) {
    // This is fine, just tracking
  }

  return {
    issuesFound: issues.length,
    criticalIssues: issues.filter(i => i.severity === "Critical").length,
    highIssues: issues.filter(i => i.severity === "High").length,
    issues: issues.slice(0, 5) // First 5 issues
  };
}

function analyzePerformance(content) {
  const issues = [];

  if (content.includes("Object.keys") && content.includes("for")) {
    issues.push("Possible inefficient looping");
  }

  if ((content.match(/\.\w+\(\)/g) || []).length > 20) {
    issues.push("High number of method calls");
  }

  return {
    performanceIssues: issues,
    hasAsyncAwait: content.includes("async") || content.includes("await"),
    hasErrorHandling: content.includes("try") && content.includes("catch")
  };
}

function findLine(lines, text) {
  const index = lines.findIndex(line => line.includes(text));
  return index >= 0 ? index + 1 : -1;
}
