/**
 * Data Processor Skill
 * Example of a domain-specific skill
 *
 * Usage: Process and validate JSON data
 * - Validate JSON structure
 * - Extract fields
 * - Transform data
 * - Generate reports
 */

module.exports = {
  name: "data-processor",
  description: "Process, validate, and transform data structures",
  version: "1.0.0",
  category: "Data",

  input: {
    type: "object",
    properties: {
      data: {
        type: "object | array | string",
        description: "Data to process"
      },
      operation: {
        type: "string",
        description: "Operation to perform",
        enum: ["validate", "extract", "transform", "analyze"]
      },
      options: {
        type: "object",
        description: "Operation-specific options"
      }
    },
    required: ["data", "operation"]
  },

  execute: async (input) => {
    try {
      const { data, operation, options = {} } = input;

      if (!data) {
        throw new Error("Data is required");
      }

      let result;

      switch (operation) {
        case "validate":
          result = validateData(data);
          break;

        case "extract":
          result = extractFields(data, options);
          break;

        case "transform":
          result = transformData(data, options);
          break;

        case "analyze":
          result = analyzeData(data);
          break;

        default:
          throw new Error(`Unknown operation: ${operation}`);
      }

      return {
        success: true,
        operation,
        result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }
};

/**
 * Validate data structure
 */
function validateData(data) {
  const errors = [];
  const warnings = [];

  // Check if valid JSON
  if (typeof data === "string") {
    try {
      JSON.parse(data);
    } catch (e) {
      errors.push(`Invalid JSON: ${e.message}`);
    }
  }

  // Check for required fields
  if (typeof data === "object" && data !== null) {
    if (Array.isArray(data) && data.length === 0) {
      warnings.push("Array is empty");
    }
    if (!Array.isArray(data) && Object.keys(data).length === 0) {
      warnings.push("Object is empty");
    }
  }

  return {
    isValid: errors.length === 0,
    errors,
    warnings,
    dataType: Array.isArray(data) ? "array" : typeof data,
    itemCount: Array.isArray(data) ? data.length :
              typeof data === "object" && data ? Object.keys(data).length : 0
  };
}

/**
 * Extract specific fields
 */
function extractFields(data, options = {}) {
  const { fields = [] } = options;

  if (Array.isArray(data)) {
    return data.map(item => {
      const extracted = {};
      fields.forEach(field => {
        extracted[field] = item[field];
      });
      return extracted;
    });
  } else if (typeof data === "object") {
    const extracted = {};
    fields.forEach(field => {
      extracted[field] = data[field];
    });
    return extracted;
  }

  return data;
}

/**
 * Transform data structure
 */
function transformData(data, options = {}) {
  const { toArray = false, flatten = false } = options;

  let result = data;

  if (toArray && !Array.isArray(result)) {
    result = [result];
  }

  if (flatten && typeof result === "object") {
    result = flattenObject(result);
  }

  return result;
}

/**
 * Analyze data
 */
function analyzeData(data) {
  const analysis = {
    type: Array.isArray(data) ? "array" : typeof data,
    size: calculateSize(data),
    depth: calculateDepth(data),
    summary: generateSummary(data)
  };

  return analysis;
}

/**
 * Flatten nested object
 */
function flattenObject(obj, prefix = "") {
  const flattened = {};

  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const value = obj[key];
      const newKey = prefix ? `${prefix}.${key}` : key;

      if (value !== null && typeof value === "object" && !Array.isArray(value)) {
        Object.assign(flattened, flattenObject(value, newKey));
      } else {
        flattened[newKey] = value;
      }
    }
  }

  return flattened;
}

/**
 * Calculate object size
 */
function calculateSize(obj) {
  if (Array.isArray(obj)) {
    return obj.length;
  } else if (typeof obj === "object" && obj !== null) {
    return Object.keys(obj).length;
  }
  return 1;
}

/**
 * Calculate object depth
 */
function calculateDepth(obj) {
  if (typeof obj !== "object" || obj === null) {
    return 0;
  }

  let maxDepth = 0;

  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const depth = 1 + calculateDepth(obj[key]);
      maxDepth = Math.max(maxDepth, depth);
    }
  }

  return maxDepth;
}

/**
 * Generate summary
 */
function generateSummary(data) {
  if (Array.isArray(data)) {
    return {
      itemCount: data.length,
      sample: data.slice(0, 3)
    };
  } else if (typeof data === "object" && data !== null) {
    return {
      keyCount: Object.keys(data).length,
      keys: Object.keys(data).slice(0, 5)
    };
  }

  return { value: data };
}
