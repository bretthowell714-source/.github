/**
 * Text Formatter Skill
 * Example of a simple utility skill
 *
 * Usage: Format text in various ways
 * - Convert case
 * - Reverse text
 * - Count words/characters
 * - Trim whitespace
 */

module.exports = {
  name: "text-formatter",
  description: "Format and manipulate text in various ways",
  version: "1.0.0",
  category: "Utility",

  input: {
    type: "object",
    properties: {
      text: {
        type: "string",
        description: "Text to format"
      },
      format: {
        type: "string",
        description: "Format type",
        enum: ["uppercase", "lowercase", "reverse", "analyze", "all"]
      }
    },
    required: ["text"]
  },

  output: {
    type: "object",
    properties: {
      success: { type: "boolean" },
      original: { type: "string" },
      formatted: { type: "object" }
    }
  },

  execute: async (input) => {
    try {
      const { text, format = "all" } = input;

      if (!text || typeof text !== "string") {
        throw new Error("Text must be a non-empty string");
      }

      const results = {
        original: text,
        length: text.length,
        wordCount: text.split(/\s+/).filter(w => w).length,
        lineCount: text.split("\n").length,
        formatted: {}
      };

      // Apply requested formats
      if (["uppercase", "all"].includes(format)) {
        results.formatted.uppercase = text.toUpperCase();
      }

      if (["lowercase", "all"].includes(format)) {
        results.formatted.lowercase = text.toLowerCase();
      }

      if (["reverse", "all"].includes(format)) {
        results.formatted.reversed = text.split("").reverse().join("");
      }

      if (["analyze", "all"].includes(format)) {
        results.formatted.analysis = {
          hasNumbers: /\d/.test(text),
          hasSpecialChars: /[^a-zA-Z0-9\s]/.test(text),
          firstWord: text.split(/\s+/)[0],
          lastWord: text.split(/\s+/).pop(),
          averageWordLength: Math.round(
            text.replace(/\s+/g, "").length /
            text.split(/\s+/).filter(w => w).length
          )
        };
      }

      return {
        success: true,
        data: results,
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
