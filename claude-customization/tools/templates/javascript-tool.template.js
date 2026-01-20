/**
 * JavaScript Tool Template
 * Copy this file to create a new custom tool
 */

module.exports = {
  // Unique identifier for the tool
  name: "my-tool",

  // Description shown to Claude
  description: "Brief description of what this tool does",

  // JSON Schema for tool parameters
  parameters: {
    type: "object",
    properties: {
      param1: {
        type: "string",
        description: "Description of parameter 1"
      },
      param2: {
        type: "number",
        description: "Description of parameter 2",
        default: 0
      },
      param3: {
        type: "array",
        description: "Description of parameter 3",
        items: {
          type: "string",
          enum: ["option1", "option2", "option3"]
        }
      }
    },
    // List required parameters
    required: ["param1"]
  },

  /**
   * Execute the tool
   * @param {object} params - Tool parameters from Claude
   * @param {object} context - Claude execution context
   * @returns {object} Result with success status and data
   */
  execute: async (params, context) => {
    try {
      // Validate inputs
      if (!params.param1) {
        throw new Error("param1 is required");
      }

      // Implement your tool logic here
      const result = await performAction(params);

      // Return success response
      return {
        success: true,
        data: result,
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
 * Implement your tool's functionality
 */
async function performAction(params) {
  // TODO: Replace with your implementation

  // Example implementation:
  return {
    input: params.param1,
    param2: params.param2,
    param3: params.param3,
    processed: true
  };
}
