// =============================================================================
// REFERENCE FILE — This standalone hook is for documentation purposes.
// The actual hook is registered in extensions/scaffolder-ext/extension.mjs.
// Copilot CLI loads hooks through extensions, not from standalone files.
// See Exercise 5 for how to modify the hook in the extension.
// =============================================================================

// preCompact Hook — Saves context summary before compaction
// This hook fires before Copilot compresses conversation context.
// Exercise 5 teaches learners how to configure and modify this hook.

import { joinSession } from "@github/copilot-sdk/extension";
import { writeFileSync } from "node:fs";

export default await joinSession({
  hooks: {
    preCompact: async (session, { summary }) => {
      const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
      const filename = `context_summary_${timestamp}.md`;

      try {
        writeFileSync(filename, `# Context Summary\n\n${summary}\n`);
        console.log(`[preCompact] Saved context summary to ${filename}`);
      } catch (err) {
        console.error(`[preCompact] Failed to save summary: ${err.message}`);
      }
    },
  },
});
