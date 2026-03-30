# Level 8 Cheat Sheet — Advanced Features

## CLI Permission Flags

| Flag | Effect |
|------|--------|
| `--allow-tool "view"` | Auto-approve `view` tool (no prompts) |
| `--deny-tool "bash"` | Completely block `bash` tool |
| `--allow-url "https://api.github.com/*"` | Allow specific URL patterns |
| `--deny-url "*"` | Block all network access |
| `--reasoning-effort low\|medium\|high\|xhigh` | Set reasoning depth — `low` for quick lookups, `xhigh` for complex tasks (v1.0.4) |
| `/allow-all on\|off\|show` | Enable, disable, or check permission state — replaces binary `/allow-all` (v1.0.12) |
| `--binary-version` | Query CLI binary version without launching a session (v1.0.3) |

### Common Permission Presets

```bash
# Read-only (safest)
copilot --allow-tool "view" --allow-tool "grep" --allow-tool "glob" \
        --deny-tool "bash" --deny-tool "edit" --deny-tool "create"

# Edit but no execute
copilot --allow-tool "view" --allow-tool "edit" --allow-tool "grep" \
        --deny-tool "bash"

# Full trust (fastest)
copilot --allow-tool "view" --allow-tool "edit" --allow-tool "bash" \
        --allow-tool "create" --allow-tool "grep" --allow-tool "glob"

# Locked down (production)
copilot --deny-tool "bash" --deny-tool "edit" --deny-tool "create" \
        --deny-url "*"
```

## Programmatic Mode

```bash
# Basic (with conversational output)
copilot -p "Explain this file"

# Silent (script-friendly, clean output)
copilot -p "Summarize this code" -s

# JSON output for programmatic integrations (v0.0.422)
copilot -p "Analyze this code" --output-format json

# Pipe input
cat file.py | copilot -p "Review this code" -s

# Capture output
RESULT=$(copilot -p "What does main.py do?" -s)

# Loop over files
for f in src/*.ts; do
  copilot -p "One-line summary of $f" -s
done
```

### Programmatic & Session Flags

| Flag | Purpose | Since |
|------|---------|-------|
| `-p "prompt"` | Non-interactive single prompt | — |
| `-s` | Silent / script-friendly output | — |
| `--output-format json` | Emit JSONL in prompt mode for programmatic integrations | v0.0.422 |
| `--plugin-dir <path>` | Load plugin from local directory | v0.0.421 |
| `--mouse` / `--no-mouse` | Enable/disable mouse mode in interactive sessions | v0.0.419 |
| `--bash-env` | Source `BASH_ENV` in shell sessions | v0.0.412 |

## Session Management

| Command | Effect |
|---------|--------|
| `copilot` | New session |
| `copilot --continue` | Resume last session |
| `copilot --resume` | Pick from recent sessions |
| `/clear` | Reset context (keep session) |
| `/context` | Show loaded context |
| `/pr` | PR workflow: create, view status, fix CI, address review feedback, resolve conflicts (v1.0.5) |
| `/extensions` | View, enable, or disable CLI extensions (v1.0.5) |
| `/version` | Display version and check for updates (v1.0.5) |
| `/rewind` | Undo last turn + revert files (v1.0.13) |
| `/new` | Fresh conversation, keep settings (v1.0.13) |
| `/session` | Session metadata and management (v1.0.13) |
| `/restart` | Hot restart preserving session state (v1.0.3) |
| `Ctrl+C` / `/exit` | Exit session |

## Environment Variables

| Variable | Purpose | Since |
|----------|---------|-------|
| `COPILOT_CLI=1` | Set automatically in Copilot CLI subprocesses; useful for git hooks to detect CLI context | v0.0.421 |

## Hooks

| Location | Scope | Description |
|----------|-------|-------------|
| `~/.copilot/hooks` | Personal | User-wide hooks applied to all sessions (v0.0.422) |
| `.github/hooks` | Repository | Repo-level hooks shared with the team |

### Hook Types

| Hook | When It Fires | Use Case |
|------|---------------|----------|
| Startup prompt | Session start | Auto-submit commands or set context at launch |
| `preToolUse` | Before a tool runs | Deny or modify tool calls (e.g., block dangerous commands) |
| `preCompact` | Before context compaction | Save state or snapshots before the context window is compressed (v1.0.5) |
| `agentStop` | Agent completes | Post-processing after the main agent finishes |
| `subagentStop` | Sub-agent completes | Post-processing after a delegated sub-agent finishes |

> 💡 Use the `command` field (v1.0.2) as a cross-platform alias instead of separate `bash` / `powershell` fields.

> 💡 Set `disableAllHooks: true` (v1.0.4) in your config to temporarily disable all hooks without removing them — useful for debugging or bypassing automation.

> 💡 Hooks can request user confirmation by specifying the `ask` permission (v1.0.4), adding a human-in-the-loop checkpoint before the hook executes.

---

## Security — Defense in Depth

```
Layer 1: .copilotignore             ← Exclude sensitive files from context
Layer 2: --deny-tool "bash"         ← Block command execution
Layer 3: --deny-url "*"             ← Block network access
Layer 4: Custom instructions        ← "Never display credentials"
Layer 5: Org MCP policy             ← Enterprise-enforced tool restrictions (v1.0.11)
```

### `.copilotignore` for Security

```gitignore
# Credentials
config/production.env
*.pem
*.key
.env.production

# Secrets
**/secrets/
**/credentials/

# Safe to include
!config/development.env
!.env.example
```

## Copilot Coding Agent Workflow

```
1. Create Issue     ← Clear title + acceptance criteria
2. Assign @copilot  ← Agent starts working
3. Agent → Branch   ← Creates implementation
4. Agent → PR       ← Opens pull request
5. You → Review     ← Standard code review
6. Iterate          ← Comment for changes
7. Merge            ← When satisfied
```

### Good vs Bad Issues for the Agent

| Good Issue | Bad Issue |
|------------|-----------|
| "Add GET /users endpoint with pagination" | "Make the API better" |
| "Fix: login returns 500 when email is null" | "Fix all the bugs" |
| Clear acceptance criteria | No success definition |
| Specific files listed | "Figure out where" |
| Test expectations included | "Make sure it works" |

## Delegation Decision Tree

```
Is it well-defined with clear criteria?
├── No → CLI interactive (refine requirements)
└── Yes → Does it need real-time judgment?
    ├── Yes → CLI interactive
    └── No → Is it repeatable/batch?
        ├── Yes → Automation script (copilot -p)
        └── No → Single task with PR needed?
            ├── Yes → Coding Agent
            └── No → CLI interactive
```

## CI/CD Integration

```yaml
# Key pattern: copilot -p "prompt" -s in GitHub Actions
- name: AI Review
  run: |
    DIFF=$(git diff origin/main...HEAD)
    copilot -p "Review: $DIFF" -s > review.md
    gh pr comment $PR --body-file review.md
```

## Automation Script Template

```bash
#!/usr/bin/env bash
set -euo pipefail

INPUT="${1:?Usage: $0 <input>}"

# Gather data
DATA=$(some-command "$INPUT")

# Ask Copilot
RESULT=$(copilot -p "Analyze: $DATA" -s)

# Use result
echo "$RESULT"
```

## The Complete Ecosystem

| Tool | Mode | Best For |
|------|------|----------|
| **CLI** | Interactive | Exploration, planning, coding |
| **CLI -p** | Programmatic | Automation, scripts, CI |
| **Coding Agent** | Autonomous | Issues → PRs |
| **IDE Copilot** | Inline | Code completion, chat |
| **MCP Servers** | Extension | External tools |
| **SDK** | Build | Custom integrations |
| **`configure-copilot` agent** | Built-in sub-agent | Manage MCP servers, custom agents, and skills (v1.0.4) |
| **CLI Extensions** | Extensibility | Custom tools & hooks via `@github/copilot-sdk` (v1.0.3+, `/extensions` v1.0.5) |

## 8 Key Principles (One Per Level)

1. **Observe first** — read before writing
2. **Understand deeply** — ask why, not just what
3. **Plan before coding** — think, then implement
4. **Verify every change** — `/diff` after every edit
5. **Interpret, don't just run** — understand command output
6. **Follow the cycle** — plan → implement → test → review
7. **Configure for your project** — instructions > defaults
8. **Delegate wisely** — right tool for right task
