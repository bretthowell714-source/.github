/**
 * Integration Skill Template
 * Copy this file to create an integration skill
 *
 * Integration skills connect to external services:
 * - REST APIs
 * - Databases
 * - Cloud services
 * - Third-party APIs
 */

module.exports = {
  name: "my-integration-skill",
  description: "Integrate with external service",
  version: "1.0.0",

  // Service configuration
  service: {
    name: "external-service",
    baseUrl: "${SERVICE_URL}", // Use environment variable
    timeout: 30000
  },

  // Required dependencies
  dependencies: ["axios", "dotenv"],

  /**
   * Optional: Initialize skill (setup connections, load config)
   */
  init: async (config) => {
    // Initialize service connection
    // Load credentials from environment
    // Setup any required state
    console.log("Integration skill initialized");
  },

  input: {
    type: "object",
    properties: {
      action: {
        type: "string",
        description: "Action to perform",
        enum: ["get", "post", "update", "delete"]
      },
      endpoint: {
        type: "string",
        description: "API endpoint"
      },
      data: {
        type: "object",
        description: "Data to send"
      }
    },
    required: ["action", "endpoint"]
  },

  output: {
    type: "object",
    properties: {
      success: { type: "boolean" },
      data: { type: "object" },
      error: { type: "string" }
    }
  },

  /**
   * Execute integration request
   */
  execute: async (input, context) => {
    try {
      const axios = require("axios");

      const { action, endpoint, data } = input;
      const baseUrl = process.env.SERVICE_URL || "http://localhost:3000";

      const headers = {
        "Authorization": `Bearer ${process.env.SERVICE_TOKEN}`,
        "Content-Type": "application/json"
      };

      let response;

      switch (action.toLowerCase()) {
        case "get":
          response = await axios.get(`${baseUrl}${endpoint}`, { headers });
          break;

        case "post":
          response = await axios.post(`${baseUrl}${endpoint}`, data, { headers });
          break;

        case "update":
          response = await axios.put(`${baseUrl}${endpoint}`, data, { headers });
          break;

        case "delete":
          response = await axios.delete(`${baseUrl}${endpoint}`, { headers });
          break;

        default:
          throw new Error(`Unknown action: ${action}`);
      }

      return {
        success: true,
        action,
        endpoint,
        data: response.data,
        status: response.status,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        details: error.response?.data || null,
        timestamp: new Date().toISOString()
      };
    }
  },

  /**
   * Optional: Cleanup (close connections, etc.)
   */
  cleanup: async () => {
    console.log("Integration skill cleaned up");
  }
};
