// =============================================================================
// REFERENCE FILE — This standalone hook is for documentation purposes.
// The actual hook is registered in extensions/scaffolder-ext/extension.mjs.
// Copilot CLI loads hooks through extensions, not from standalone files.
// See Exercise 5 for how to modify the hook in the extension.
// =============================================================================

// subagentStart Hook — Injects project context into subagent prompts
// This hook fires when a subagent is launched (e.g., explore, task agents).
// Exercise 5 teaches learners how to configure and modify this hook.

import { joinSession } from "@github/copilot-sdk/extension";

export default await joinSession({
  hooks: {
    subagentStart: async (session, { prompt }) => {
      const projectContext = [
        "Project: Scaffolder CLI",
        "Language: Python 3.8+ (stdlib only)",
        "Convention: snake_case functions, PascalCase classes",
        "Convention: docstrings on all public functions",
        "Convention: type hints encouraged",
      ].join("\n");

      return {
        additionalContext: `\n## Project Context\n${projectContext}\n`,
      };
    },
  },
});
