/**
 * Simple Skill Template
 * Copy this file to create a new simple skill
 *
 * A simple skill is a single-purpose utility that does one thing well.
 * Typical use cases:
 * - Text processing
 * - Data formatting
 * - Simple calculations
 * - Input validation
 */

module.exports = {
  // Required: Unique skill identifier
  name: "my-simple-skill",

  // Required: Clear description
  description: "Brief description of what this skill does",

  // Optional: Skill metadata
  version: "1.0.0",
  author: "Your Name",
  tags: ["category", "tags"],
  category: "Utility",

  // Optional: Document input/output
  input: {
    type: "string | object | array",
    description: "What input this skill expects",
    examples: ["example-input-1", "example-input-2"]
  },

  output: {
    type: "object",
    properties: {
      success: { type: "boolean" },
      result: { type: "string | object" },
      error: { type: "string" }
    }
  },

  /**
   * Main skill execution
   *
   * @param {any} input - The input data to process
   * @param {object} context - Claude execution context (optional)
   * @returns {object} Result object with success status and data
   *
   * @example
   * execute("hello world")
   * // Returns: { success: true, result: "processed data" }
   */
  execute: async (input, context) => {
    try {
      // Validate input
      if (!input) {
        throw new Error("Input is required");
      }

      // Implement your skill logic here
      const result = processData(input);

      // Return successful response
      return {
        success: true,
        result: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      // Return error response
      return {
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }
};

/**
 * Implement your skill's functionality here
 */
function processData(input) {
  // TODO: Replace with your implementation
  return input;
}
