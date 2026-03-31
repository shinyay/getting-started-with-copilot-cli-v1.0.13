---
layout: cheatsheet
title: "Level 7 — Quick Reference Card"
parent_step: 7
permalink: /cheatsheet/7/
---

# Level 7 Cheat Sheet — Customization & Configuration

## Custom Instructions Location

| Level | File | Scope |
|-------|------|-------|
| Organization | GitHub org settings (web UI) | All repos in org |
| Repository | `.github/copilot-instructions.md` | All contributors |
| User (cross-repo) | `~/.copilot/instructions/*.instructions.md` | All your repos (v0.0.412+) |
| Personal | `~/.copilot/copilot-instructions.md` | Your sessions |
| Session | Conversation context | Current session only |
| `CLAUDE.md` | Repository root | Cross-tool compatibility (v1.0.13) |
| `GEMINI.md` | Repository root | Cross-tool compatibility (v1.0.13) |
| `.claude/settings.json` | Repository root | Cross-tool config (v1.0.12) |
| `.mcp.json` | Git root | Simplified MCP config (v1.0.12) |
| `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Environment variable | Additional instruction directories (v1.0.13) |

> **Priority (most specific wins):** Session > COPILOT_CUSTOM_INSTRUCTIONS_DIRS > CLAUDE.md/GEMINI.md > .github/instructions/** > .github/copilot-instructions.md > ~/.copilot/instructions/ > ~/.copilot/copilot-instructions.md > Organization

## Writing Good Instructions

```markdown
# Good — specific, actionable, with examples
- Use `AppError.badRequest("message", "ERROR_CODE")` for 400 errors
- Import the logger: `import { logger } from '../utils/logger'`
- Never use `console.log` — always use `logger.info()` with context

# Bad — vague, no examples
- Handle errors properly
- Use the logger
- Follow best practices
```

### Instruction Template

```markdown
## Project: [Name] ([Language] + [Framework])

### Code Style
- [naming convention]
- [import style]
- [const vs let rules]

### Error Handling
- [error class/pattern]
- [what NOT to do]

### API Responses
- [response wrapper type]
- [pagination pattern]

### Testing
- [test framework + style]
- [what NOT to do]

### Architecture
- [layer descriptions]
- [what goes where]

### Excluded Files
- [directories to ignore]
```

## `.copilotignore` Syntax

```gitignore
# Auto-generated
generated/
dist/
build/

# Third-party
node_modules/
vendor/

# Large / irrelevant
package-lock.json
yarn.lock
*.map
*.min.js
coverage/

# Data
*.sql
*.csv
*.sqlite
```

## Context Optimization

| Task | Load These | Skip These |
|------|-----------|------------|
| New service function | Service file + model file | Routes, middleware |
| New route handler | Route file + service file | Utils, models |
| New test | Test file + source file | Other tests |
| Bug fix | Buggy file + its test | Unrelated files |
| Refactoring | File being refactored | Everything else |

## MCP Configuration

```json
// .github/copilot/mcp.json (project-level)
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {}
    }
  }
}
```

| MCP Command / Config | Purpose |
|----------------------|---------|
| `/mcp` | Show configured MCP servers |
| `/mcp show` | Groups servers by User/Workspace/Plugins/Built-in (v0.0.415+) |
| `/mcp reload` | Reload MCP configuration without restarting (v0.0.412+) |
| `.github/copilot/mcp.json` | Project-level MCP config (shared via repo) |
| `.vscode/mcp.json` | Workspace-local MCP config alternative (v0.0.407+) |
| `.devcontainer/devcontainer.json` | Dev Container / Codespaces MCP config (v1.0.3+) |
| `.mcp.json` (git root) | Simplest MCP config (v1.0.12) |
| `configure-copilot` agent | Manage MCP/agents/skills conversationally via task tool (v1.0.4+) |

## Session Commands

| Command | Effect |
|---------|--------|
| `copilot` | New session |
| `copilot --continue` | Resume last session |
| `copilot --resume` | Pick from recent sessions |
| `/clear` | Reset context in current session |
| `/context` | Show loaded context |
| `/rewind` | Undo last turn + revert files (v1.0.13) |
| `/new` | Fresh conversation, keep settings (v1.0.13) |
| `/session` | Session metadata and management (v1.0.13) |
| `/instructions` | View/toggle loaded instruction files (v1.0.13) |
| `/copy` | Copy last response to clipboard (v0.0.422+) |
| `/update` | Update CLI to latest version (v0.0.412+) |
| `/restart` | Hot-restart CLI preserving current session (v1.0.3+) |
| `/version` | Display CLI version and check for updates (v1.0.5+) |
| `/extensions` | View, enable, or disable CLI extensions (v1.0.5+) |
| `/terminal-setup` | Configure shell integration |
| `Ctrl+C` | Cancel current generation |
| `Ctrl+D` | Exit |

## Prompt Templates

### New Service Function
```
@ [service-file] @ [model-file]
Add a [functionName] function to [service-file]:
- [requirement 1]
- [requirement 2]
Follow error handling and logging conventions from instructions.
```

### New Endpoint
```
@ [route-file] @ [service-file]
Add a [METHOD] /api/[path] endpoint:
- Validate with [schema]
- Call [serviceFunction]
- Return respondSuccess/respondPaginated
```

### Bug Fix
```
@ [buggy-file] @ [test-file]
Bug: [description]
1. Explain the root cause
2. /plan the fix
3. Implement
4. Write regression test
5. /diff then /review
```

## Configuration ROI (setup priority)

1. 🔴 **Custom instructions** — 15 min setup, highest impact
2. 🟡 **`.copilotignore`** — 5 min, cleaner context
3. 🟡 **Prompt templates** — 10 min, team consistency
4. 🟢 **MCP servers** — 20 min, project-dependent
5. 🟢 **Terminal setup** — 2 min, nice-to-have

## Hooks

| Hook / Config | Purpose |
|---------------|---------|
| `preExec` | Run before a command executes |
| `postExec` | Run after a command executes |
| `preCompact` | Run before context compaction (v1.0.5+) |
| `disableAllHooks` | Flag to disable all hooks from a config file (v1.0.4+) |
| `ask` permission | Hook can request user confirmation before proceeding (v1.0.4+) |

## Tips

- **Test instructions by generating code** — don't assume, verify
- **Iterate on instructions** — every convention violation = add/clarify instruction
- **Context is a budget** — load minimum needed, not everything
- **Share prompt templates** — put them in `docs/` for the team
- **Audit quarterly** — conventions evolve, instructions should follow
- **`@` paths (v1.0.5):** File mentions now support `@~/` (home), `@../` (relative), and `@/abs/` (absolute) paths for flexible context loading
