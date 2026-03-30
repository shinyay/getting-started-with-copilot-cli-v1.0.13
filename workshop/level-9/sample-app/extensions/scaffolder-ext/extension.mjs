// Scaffolder Extension — Custom Copilot CLI tool with hooks
// This extension registers tools AND lifecycle hooks.
// Exercise 2 asks students to add more tools.
// Exercise 5 asks students to modify the hooks.

import { joinSession } from "@github/copilot-sdk/extension";
import { writeFileSync } from "node:fs";

export default await joinSession({
  tools: [
    {
      name: "list_templates",
      description: "List available project scaffold templates with descriptions",
      parameters: {},
      execute: async () => {
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify({
                templates: [
                  { name: "python", description: "Python project with src layout, tests, and CI" },
                  { name: "typescript", description: "TypeScript project with src layout and Jest" },
                  { name: "bash", description: "Bash script project with tests and CI" },
                  { name: "mixed", description: "Multi-language project (Python + TypeScript + Bash)" },
                ],
                total: 4,
              }, null, 2),
            },
          ],
        };
      },
    },
    // TODO: Exercise 2 — Add a "scaffold_project" tool here that:
    // 1. Accepts parameters: { name: string, template: string }
    // 2. Validates the project name (lowercase, hyphens, underscores only)
    // 3. Returns the list of files that would be created
    // Hint: Use child_process to call: python3 -m scaffolder.cli info <template>
  ],
  hooks: {
    // preCompact hook — saves context summary before compaction
    // Exercise 5 asks students to enhance this hook
    preCompact: async (session, context) => {
      const summary = context?.summary || "No summary available";
      const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
      const filename = `context_summary_${timestamp}.md`;

      try {
        writeFileSync(filename, `# Context Summary\n\n${summary}\n`);
        console.log(`[preCompact] Saved context summary to ${filename}`);
      } catch (err) {
        console.error(`[preCompact] Failed to save summary: ${err.message}`);
      }
    },

    // subagentStart hook — injects project context into subagent prompts
    // Exercise 5 asks students to customize this context injection
    subagentStart: async (session, context) => {
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
  slashCommands: [],
});
