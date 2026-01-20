/**
 * File Processor Tool
 * Process files: convert formats, extract metadata, transform content
 */

module.exports = {
  name: "file-processor",
  description: "Process files - convert formats, extract metadata, transform content",
  parameters: {
    type: "object",
    properties: {
      filepath: {
        type: "string",
        description: "Path to file to process"
      },
      operation: {
        type: "string",
        description: "Operation to perform on the file",
        enum: ["metadata", "convert", "extract", "transform", "validate"],
        default: "metadata"
      },
      targetFormat: {
        type: "string",
        description: "Target format for conversion (json, yaml, csv, markdown, etc.)",
        default: null
      },
      options: {
        type: "object",
        description: "Additional options for the operation",
        properties: {
          includeStats: { type: "boolean" },
          deep: { type: "boolean" },
          validate: { type: "boolean" }
        }
      }
    },
    required: ["filepath", "operation"]
  },

  execute: async (params, context) => {
    const fs = require("fs").promises;
    const path = require("path");

    try {
      const filepath = params.filepath;
      const stat = await fs.stat(filepath);
      const ext = path.extname(filepath).toLowerCase();
      const content = await fs.readFile(filepath, "utf-8");

      const result = {
        filepath,
        operation: params.operation,
        timestamp: new Date().toISOString()
      };

      switch (params.operation) {
        case "metadata":
          result.metadata = extractMetadata(filepath, content, stat, ext);
          break;

        case "convert":
          result.converted = convertFormat(content, ext, params.targetFormat);
          break;

        case "extract":
          result.extracted = extractContent(content, ext, params.options);
          break;

        case "transform":
          result.transformed = transformContent(content, ext, params.options);
          break;

        case "validate":
          result.validation = validateContent(content, ext);
          break;

        default:
          throw new Error(`Unknown operation: ${params.operation}`);
      }

      return {
        success: true,
        result
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
};

function extractMetadata(filepath, content, stat, ext) {
  const lines = content.split("\n").length;
  const words = content.split(/\s+/).length;
  const chars = content.length;

  return {
    path: filepath,
    extension: ext,
    size: stat.size,
    sizeHuman: formatFileSize(stat.size),
    created: stat.birthtime,
    modified: stat.mtime,
    lines,
    words,
    characters: chars,
    averageLineLength: Math.round(chars / lines),
    type: determineFileType(ext),
    encoding: "utf-8"
  };
}

function determineFileType(ext) {
  const types = {
    // Code
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".py": "Python",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    // Web
    ".html": "HTML",
    ".css": "CSS",
    ".json": "JSON",
    ".xml": "XML",
    ".yaml": "YAML",
    ".yml": "YAML",
    // Documents
    ".md": "Markdown",
    ".txt": "Text",
    ".csv": "CSV",
    ".pdf": "PDF"
  };

  return types[ext] || "Unknown";
}

function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + " " + sizes[i];
}

function convertFormat(content, fromExt, toFormat) {
  // JSON to YAML
  if (fromExt === ".json" && toFormat === "yaml") {
    try {
      const data = JSON.parse(content);
      return {
        format: "yaml",
        content: convertToYAML(data),
        preview: convertToYAML(data).split("\n").slice(0, 10).join("\n")
      };
    } catch (e) {
      throw new Error("Invalid JSON");
    }
  }

  // CSV to JSON
  if (fromExt === ".csv" && toFormat === "json") {
    const lines = content.split("\n");
    const headers = lines[0].split(",");
    const data = lines.slice(1).map(line => {
      const values = line.split(",");
      return headers.reduce((obj, header, i) => {
        obj[header.trim()] = values[i]?.trim();
        return obj;
      }, {});
    });
    return {
      format: "json",
      content: JSON.stringify(data, null, 2)
    };
  }

  throw new Error(`Conversion from ${fromExt} to ${toFormat} not supported`);
}

function convertToYAML(obj, indent = 0) {
  let yaml = "";
  const spaces = "  ".repeat(indent);

  for (const [key, value] of Object.entries(obj)) {
    if (typeof value === "object" && value !== null) {
      yaml += `${spaces}${key}:\n`;
      yaml += convertToYAML(value, indent + 1);
    } else {
      yaml += `${spaces}${key}: ${value}\n`;
    }
  }

  return yaml;
}

function extractContent(content, ext, options = {}) {
  const extracted = {
    imports: [],
    functions: [],
    classes: [],
    comments: []
  };

  if ([".js", ".ts", ".jsx", ".tsx"].includes(ext)) {
    // Extract imports
    const importMatches = content.match(/import\s+.*from\s+['"].*['"]/g) || [];
    extracted.imports = importMatches.map(m => m.trim());

    // Extract functions
    const functionMatches = content.match(/function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\(/g) || [];
    extracted.functions = functionMatches.map(m => m.trim()).slice(0, 10);

    // Extract classes
    const classMatches = content.match(/class\s+\w+/g) || [];
    extracted.classes = classMatches.map(m => m.trim());

    // Extract comments
    const commentMatches = content.match(/\/\*[\s\S]*?\*\/|\/\/.*/g) || [];
    extracted.comments = commentMatches.slice(0, 5);
  }

  return extracted;
}

function transformContent(content, ext, options = {}) {
  let transformed = content;

  // Trim whitespace
  transformed = transformed.trim();

  // Normalize line endings
  transformed = transformed.replace(/\r\n/g, "\n");

  // Remove trailing spaces
  transformed = transformed
    .split("\n")
    .map(line => line.trimEnd())
    .join("\n");

  return {
    original: {
      lines: content.split("\n").length,
      chars: content.length
    },
    transformed: {
      lines: transformed.split("\n").length,
      chars: transformed.length
    },
    content: transformed.substring(0, 500) + "..." // Preview
  };
}

function validateContent(content, ext) {
  const validation = {
    valid: true,
    errors: [],
    warnings: []
  };

  // JSON validation
  if (ext === ".json") {
    try {
      JSON.parse(content);
    } catch (e) {
      validation.valid = false;
      validation.errors.push(`JSON parse error: ${e.message}`);
    }
  }

  // Check for empty content
  if (content.trim().length === 0) {
    validation.warnings.push("File is empty");
  }

  // Check for very long lines
  const lines = content.split("\n");
  const longLines = lines.filter(l => l.length > 120);
  if (longLines.length > 0) {
    validation.warnings.push(`${longLines.length} lines exceed 120 characters`);
  }

  return validation;
}
