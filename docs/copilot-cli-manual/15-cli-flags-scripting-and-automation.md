# Chapter 15: CLI Flags, Scripting & Automation

Everything covered in the preceding fourteen chapters assumes a human sitting at
a terminal, typing prompts, reviewing diffs, and approving tool calls one at a
time. But Copilot CLI was designed from the start to be **scriptable**. Every
interactive feature has a non-interactive counterpart — a flag, an environment
variable, or a hook — so you can embed Copilot in shell scripts, CI/CD
pipelines, Git hooks, and custom developer tooling without ever touching a
keyboard.

This chapter is the definitive reference for every CLI flag, every environment
variable, the hooks system, and the ACP server mode. It closes with five
end-to-end scripting recipes you can copy, adapt, and ship today.

> 📋 For interactive-mode commands and slash commands, see
> [Chapter 5: Slash Commands Reference](./05-slash-commands-reference.md). For
> custom instructions that influence both interactive and non-interactive runs,
> see [Chapter 7: Custom Instructions & Configuration](./07-custom-instructions-and-configuration.md).

---

## Complete CLI Flags Reference

The table below lists every flag accepted by `copilot` as of the latest
release, organized by category. Flags marked **Launch** shipped with the
initial public preview; all others note the version that introduced them.

### Session & Prompt Flags

| Flag | Short | Description | Since |
|------|-------|-------------|-------|
| `--prompt <text>` | `-p` | Run a single prompt in non-interactive mode and exit | Launch |
| `--model <name>` | | Select the AI model for this session | Launch |
| `--agent <name>` | | Use a specific custom agent (interactive mode since v0.0.380) | v0.0.353 |
| `--continue` | | Resume the most recent session | v0.0.333 |
| `--resume [id]` | | Resume a specific session by ID | v0.0.372 |
| `--banner` | | Show the animated startup banner | Launch |
| `--experimental` | | Enable experimental features for this session | v0.0.396 |
| `--no-experimental` | | Disable experimental features for this session | v0.0.406 |
| `--reasoning-effort <level>` | | Set reasoning depth: `low`/`medium`/`high`/`xhigh` | v1.0.4 |
| `--binary-version` | | Print the native binary version and exit | v1.0.3 |

> 💡 `--continue` and `--resume` are mutually exclusive. Use `--continue` when
> you simply want "pick up where I left off" and `--resume <id>` when you have
> a specific session ID (visible in the status bar or via `copilot help`).

### Display & Accessibility Flags

| Flag | Description | Since |
|------|-------------|-------|
| `--alt-screen on\|off` | Toggle alternate screen buffer mode | v0.0.411 |
| `--mouse` / `--no-mouse` | Enable or disable mouse interaction mode | v0.0.419 |
| `--stream off` | Disable token-by-token streaming (print complete responses) | v0.0.348 |
| `--screen-reader` | Optimize output for screen readers | Launch |

> ⚠️ `--stream off` changes the perceived behavior substantially. The CLI will
> appear to "hang" while the model generates its full response, then print
> everything at once. This is useful for piping output but confusing in an
> interactive terminal.

### Permission Flags

| Flag | Description | Since |
|------|-------------|-------|
| `--allow-all` / `--yolo` | Grant all permissions automatically | v0.0.381 |
| `--allow-all-paths` | Approve all file-system path access | v0.0.340 |
| `--allow-tool <pattern>` | Allow a specific tool; supports glob patterns | Launch |
| `--deny-tool <pattern>` | Deny a specific tool; supports glob patterns | Launch |
| `--available-tools` | Filter the set of tools available to the agent | v0.0.370 |
| `--excluded-tools` | Exclude specific tools from the available set | v0.0.370 |

Permission flags are the backbone of automation. In an interactive session the
CLI pauses to ask "Allow this tool call?" — in a script that pause becomes a
deadlock. Always pair `-p` with at least `--allow-all-paths` and the specific
`--allow-tool` patterns your script needs:

```bash
# Minimal permissions: only allow reading and editing files
copilot -p "Refactor utils.ts" \
  --allow-all-paths \
  --allow-tool "read_file" \
  --allow-tool "edit_file"
```

```bash
# Maximum permissions (use only in trusted environments)
copilot -p "Fix all lint errors and commit" --allow-all
```

> ⚠️ `--yolo` is an alias for `--allow-all`. It grants **every** permission
> including shell execution, file deletion, and network access. Never use it in
> CI on untrusted code (e.g., PRs from forks).

### MCP & Plugin Flags

| Flag | Description | Since |
|------|-------------|-------|
| `--enable-all-github-mcp-tools` | Enable all GitHub MCP tools in read-write mode | v0.0.350 |
| `--disable-mcp-server <name>` | Disable a specific MCP server for this session | v0.0.370 |
| `--additional-mcp-config <json\|@file>` | Add MCP server configuration inline or from file | v0.0.343 |
| `--plugin-dir <path>` | Load a plugin from a local directory | v0.0.421 |

```bash
# Add an MCP server from a JSON file
copilot -p "Query the staging database" \
  --additional-mcp-config @mcp-staging.json \
  --allow-all
```

> 📋 For a full treatment of MCP servers and plugin architecture, see
> [Chapter 9: MCP (Model Context Protocol)](./09-mcp-model-context-protocol.md)
> and [Chapter 10: Plugins & Skills](./10-plugins-and-skills.md).

### Output & Logging Flags

| Flag | Description | Since |
|------|-------------|-------|
| `--output-format json` | Emit structured JSONL output in prompt mode | v0.0.422 |
| `--silent` | Suppress statistics and status output (clean for piping) | v0.0.365 |
| `--share` | Export session as markdown to stdout (non-interactive) | v0.0.375 |
| `--share-gist` | Export session as a GitHub Gist (non-interactive) | v0.0.375 |
| `--log-level <level>` | Set logging verbosity | Launch |

### Advanced & Server Flags

| Flag | Description | Since |
|------|-------------|-------|
| `--config-dir <path>` | Override the configuration directory | v0.0.382 |
| `--bash-env` | Source `BASH_ENV` file in shell sessions | v0.0.412 |
| `--acp` | Start the CLI as an Agent Client Protocol server | v0.0.397 |

---

## Non-Interactive (Prompt) Mode

Prompt mode is the foundation of all Copilot CLI automation. Pass `-p` (or
`--prompt`) with a quoted string and the CLI executes exactly one turn, prints
the response, and exits.

### Basic Usage

```bash
copilot -p "Explain the main function in app.py"
```

The agent reads your working directory context, generates a response, and
prints it to stdout. No interactive prompt appears, no tool-call confirmations
are shown, and the process exits with a status code.

### Combining Flags

Most flags compose naturally with `-p`. The most common combinations:

```bash
# Fix a bug with full permissions and a specific model
copilot -p "Fix the bug in auth.ts" \
  --allow-all \
  --model claude-opus-4.6

# Run the test suite with scoped permissions
copilot -p "Run the test suite and report failures" \
  --allow-all-paths \
  --allow-tool "shell(npm test)"

# Generate API documentation silently
copilot -p "Generate API docs for src/routes/" \
  --model claude-sonnet-4.6 \
  --silent
```

### JSONL Output for Programmatic Consumption

Since v0.0.422, `--output-format json` causes the CLI to emit one JSON object
per line (JSONL). Each object represents a discrete event — a text chunk, a
tool call, a tool result, or a completion signal:

```bash
copilot -p "List all TODO comments in src/" \
  --output-format json \
  --silent \
  > todos.jsonl
```

```jsonl
{"type":"text","content":"Found 3 TODO comments:\n"}
{"type":"tool_call","tool":"grep","args":{"pattern":"TODO","path":"src/"}}
{"type":"tool_result","tool":"grep","result":"src/app.ts:42: // TODO: add validation"}
{"type":"text","content":"1. `src/app.ts:42` — add validation\n"}
{"type":"done","exit_code":0}
```

> 💡 Pipe JSONL output through `jq` for filtering:
> `copilot -p "..." --output-format json | jq 'select(.type == "text") | .content'`

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success — the agent completed its task |
| `1` | General failure (LLM error, network timeout) |
| `2` | Authentication failure (invalid or expired token) |
| `3` | Quota exceeded |

Non-zero exit codes were standardized in **v0.0.354**. Prior versions returned
`1` for all failure modes.

### Prompt Mode Behavior Notes

| Behavior | Details | Since |
|----------|---------|-------|
| No interactive permission prompts | Tool calls either succeed (if allowed) or are silently skipped | v0.0.359 |
| MCP servers available | MCP-connected tools work in prompt mode | v0.0.363 |
| Custom agent skills | `--agent` flag works with `-p` | v0.0.403 |
| Markdown in output | Response includes markdown formatting by default | v0.0.406 |
| Tool call display | Completed tool calls printed to stderr | v0.0.395 |
| `--allow-all-paths` recommended | Prevents silent file-access denials in automation | v0.0.340 |

---

## CLI Subcommands

Beyond the main `copilot [flags]` invocation, the CLI exposes several
subcommands for administration and troubleshooting:

```bash
copilot help                # General help and quick-start guide
copilot help config         # Configuration file reference
copilot help environment    # Environment variable reference
copilot help logging        # Log levels and log file locations
copilot help permissions    # Permission system deep-dive
copilot version             # Print current CLI version (since v0.0.396)
copilot update              # Check for and install updates (since v0.0.396)
copilot login               # Authenticate with GitHub (since v0.0.401)
copilot plugin install      # Install a plugin from a registry (since v0.0.400)
copilot plugin list         # List installed plugins
copilot plugin update       # Update all installed plugins
```

> 💡 `copilot help <topic>` is the fastest way to check flag syntax without
> leaving the terminal. The output is always up-to-date with your installed
> version.

---

## Hooks System

Hooks let you inject custom logic at specific points in the CLI lifecycle
without modifying the CLI itself. They are shell scripts or executables that
the CLI calls automatically when certain events occur.

### Hook Locations

| Level | Path | Scope |
|-------|------|-------|
| Personal | `~/.copilot/hooks/` | Applies to all your sessions everywhere (since v0.0.422) |
| Repository | `.github/hooks/` | Applies to everyone working in this repo |

Repository hooks take precedence over personal hooks when both define handlers
for the same event. Hooks are discovered automatically — no registration step
is needed.

### Hook Types

#### Startup Prompt Hooks

Startup hooks fire when a new session begins (since v0.0.422). They can submit
an initial prompt or slash command, automating session setup:

```json
{
  "startup": {
    "command": "echo '/compact on'",
    "timeout": 5
  }
}
```

Use cases: auto-enable compact mode, load a context file, run a health check.

#### `preToolUse` Hooks

The most powerful hook type. Fires **before** every tool execution and can:

- **Deny** the tool call (exit code 1 → tool call is skipped)
- **Modify** tool arguments (write modified JSON to stdout)
- **Log** tool usage for auditing

```json
{
  "preToolUse": {
    "command": "node scripts/lint-check.js",
    "timeout": 30,
    "tools": ["edit"]
  }
}
```

The hook receives the tool name and arguments as JSON on stdin. To deny
execution, exit with code `1`. To approve, exit with code `0`.

> ⚠️ A slow `preToolUse` hook adds latency to **every** tool call. Keep hook
> scripts fast (< 1 second) or scope them to specific tools with the `tools`
> array.

#### `preCompact` Hooks

Fires **before** context compaction occurs (since v1.0.5). Can be used to
save or export the full conversation history before it is summarized:

```json
{
  "preCompact": {
    "command": "bash scripts/save-history.sh",
    "timeout": 10
  }
}
```

#### `agentStop` / `subagentStop` Hooks

These hooks fire when the main agent or a sub-agent finishes its work (since
v0.0.401):

```json
{
  "agentStop": {
    "command": "bash scripts/auto-commit.sh",
    "timeout": 60
  }
}
```

Common patterns: auto-commit changes, run a test suite, post a Slack
notification, update a tracking system.

#### `subagentStart` Hooks

The `subagentStart` hook fires **before** a sub-agent begins execution (since
v1.0.7). It receives the sub-agent's name and prompt as JSON on stdin and can
inject additional context into the sub-agent's prompt by writing modified JSON
to stdout:

```json
{
  "subagentStart": {
    "command": "node scripts/inject-context.js",
    "timeout": 10
  }
}
```

Use cases: inject team-specific coding standards, add project context from
external systems, log sub-agent invocations for audit.

### Hook Configuration Fields

| Field | Type | Description | Since |
|-------|------|-------------|-------|
| `command` | string | Cross-platform command (bash on Unix, PowerShell on Windows) | v1.0.2 |
| `bash` | string | Unix-only command (legacy, prefer `command`) | v0.0.396 |
| `powershell` | string | Windows-only command (legacy, prefer `command`) | v0.0.396 |
| `timeout` | number | Seconds before the hook is killed (alias for `timeoutSec`) | v1.0.2 |
| `timeoutSec` | number | Seconds before the hook is killed (original name) | v0.0.396 |
| `tools` | string[] | Limit hook to specific tool names (for `preToolUse`) | v0.0.396 |
| `disableAllHooks` | boolean | Disable all hooks globally (in config file) | v1.0.4 |

> 💡 The `COPILOT_CLI=1` environment variable is set in all hook subprocesses
> (since v0.0.421), so your scripts can detect whether they are being called by
> Copilot or invoked manually.

---

## Environment Variables — Complete Reference

Environment variables control authentication, configuration paths, runtime
behavior, and network settings. They are the primary mechanism for configuring
Copilot CLI in headless environments.

### Authentication Variables

| Variable | Description | Precedence |
|----------|-------------|------------|
| `COPILOT_GITHUB_TOKEN` | Dedicated Copilot auth token | Highest |
| `GH_TOKEN` | GitHub CLI token (shared with `gh`) | Medium |
| `GITHUB_TOKEN` | Standard GitHub token (used in CI/CD) | Lower |
| `GITHUB_ASKPASS` | Path to an auth helper program | Fallback |
| `GH_HOST` | GitHub Enterprise Server hostname | — |

The CLI checks these variables in the order listed. If `COPILOT_GITHUB_TOKEN`
is set, all others are ignored. In GitHub Actions, `GITHUB_TOKEN` is
automatically available and sufficient for most use cases.

> ⚠️ Never commit tokens to source control. In CI, use encrypted secrets
> (`${{ secrets.GITHUB_TOKEN }}`). Locally, let `gh auth login` manage your
> credentials — the CLI reads them automatically.

### Configuration Variables

| Variable | Description |
|----------|-------------|
| `XDG_CONFIG_HOME` | Override the base configuration directory (default `~/.config`) |
| `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Colon-separated list of additional instruction directories (since v1.0.13) |
| `BASH_ENV` | Path to bash environment file (sourced with `--bash-env` flag) |

### Runtime Variables

| Variable | Description |
|----------|-------------|
| `COPILOT_CLI` | Set to `1` in all CLI subprocesses and hooks |
| `CLAUDE_PROJECT_DIR` | Project directory available to plugin hooks (since v1.0.12) |
| `COPILOT_KITTY` | Toggle legacy Kitty terminal protocol support |
| `USE_BUILTIN_RIPGREP` | Set to `0` to use system ripgrep instead of bundled |
| `NODE_ENV` | Explicitly excluded from shell tool environment for safety |
| `GITHUB_WORKSPACE` | MCP server working directory in GitHub Actions |

### Network & Proxy Variables

| Variable | Description |
|----------|-------------|
| `HTTPS_PROXY` | HTTPS proxy URL (also supports `https_proxy`) |
| `HTTP_PROXY` | HTTP proxy URL (also supports `http_proxy`) |

> 💡 In corporate environments behind a proxy, set **both** `HTTPS_PROXY` and
> `HTTP_PROXY`. The CLI makes HTTPS calls to GitHub APIs and HTTP calls to some
> local MCP servers.

---

## CI/CD Integration Patterns

### GitHub Actions — AI-Powered Code Review

```yaml
name: AI Code Review
on:
  pull_request:
    types: [opened, synchronize]

permissions:
  contents: read
  pull-requests: write

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Copilot CLI
        run: curl -fsSL https://gh.io/copilot-install | bash

      - name: Run AI Review
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          copilot -p "Review the diff between origin/main and HEAD. \
            Focus on bugs, security issues, and performance problems. \
            Output a markdown summary." \
            --model claude-sonnet-4.6 \
            --allow-all \
            --silent > review.md

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const body = fs.readFileSync('review.md', 'utf8');
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: body
            });
```

> ⚠️ Always pin `--model` in CI workflows. The default model may change between
> CLI versions, and you want reproducible results.

### Batch Processing Multiple Files

```bash
#!/usr/bin/env bash
set -euo pipefail

# Add docstrings to all Python files missing them
for file in $(grep -rL '"""' src/*.py); do
  echo "Processing: $file"
  copilot -p "Add Google-style docstrings to all functions in @$file \
    that are missing them. Do not change any logic." \
    --allow-all \
    --silent
done
```

### Pipeline Integration — Test Failure Analysis

```bash
#!/usr/bin/env bash
set -euo pipefail

# Capture test output, then analyze failures with Copilot
TEST_OUTPUT=$(npm test 2>&1 || true)
EXIT_CODE=${PIPESTATUS[0]}

if [ "$EXIT_CODE" -ne 0 ]; then
  echo "$TEST_OUTPUT" | copilot -p \
    "Analyze these test failures. For each failure: explain the root cause, \
     identify the file and line, and suggest a fix." \
    --silent \
    --output-format json > analysis.jsonl
  echo "::error::Tests failed. See analysis.jsonl for AI-generated diagnostics."
  exit 1
fi
```

---

## ACP (Agent Client Protocol) Server Mode

The Agent Client Protocol turns the CLI into an **embeddable AI engine**. Instead
of running as a standalone terminal application, the CLI starts as a server that
other programs communicate with over a structured protocol.

```bash
copilot --acp
```

### What ACP Enables

| Capability | Description |
|------------|-------------|
| Session management | Load, resume, and manage multiple sessions programmatically |
| Model switching | Change models mid-session via protocol messages |
| Permission control | Set `--allow-tool` / `--deny-tool` flags via the SDK |
| Mode selection | Switch between interactive, plan, and autopilot modes |
| Terminal auth | Authenticate through terminal-based OAuth flow (since v0.0.401) |
| Context exposure | Session context (files, history) available via SDK (since v0.0.407) |

### ACP Use Cases

- **IDE integration** — VS Code, JetBrains, and other editors embed Copilot
  via ACP rather than spawning terminal windows
- **Custom developer tools** — Build bespoke interfaces that use Copilot as
  the AI backend
- **Workflow orchestration** — Chain multiple agent runs with shared context
- **CI/CD pipelines** — Long-running Copilot server processing multiple
  prompts without repeated startup overhead

> 📋 ACP is an advanced topic primarily relevant to tool authors and platform
> engineers. Most automation needs are better served by prompt mode (`-p`).

---

## Logging & Debugging

When automation goes wrong, logs are your first stop.

### Configuration

Set `log_level` in your config file (`~/.copilot/config.json`)
or pass `--log-level` at invocation:

```bash
copilot -p "Debug this issue" --log-level debug --allow-all
```

### Log Levels

| Level | What It Captures |
|-------|------------------|
| `none` | Nothing |
| `error` | Errors only (auth failures, crashes) |
| `warning` | Warnings + errors |
| `info` | Informational messages + above |
| `debug` | Detailed traces including model calls, MCP messages |
| `all` | Everything, including raw request/response bodies |
| `default` | Equivalent to `warning` |

### Log File Location

Logs are written to `~/.copilot/` by default. Each session generates a
separate log file named with the session ID.

### Debugging Tips

- **Auth issues**: Set `--log-level debug` and look for token resolution
  messages — the log shows which environment variable or credential store
  was used
- **MCP errors**: Debug-level logs include the full JSON-RPC message exchange
  between the CLI and each MCP server
- **Request IDs**: Since v0.0.422, every error message includes a request ID.
  Include this ID when filing bug reports or contacting support

> 💡 In CI, redirect log output to an artifact:
> `copilot -p "..." --log-level debug 2> copilot-debug.log`

---

## Auto-Update Behavior

The CLI manages its own updates to ensure you always have the latest features
and security patches.

| Behavior | Details | Since |
|----------|---------|-------|
| Automatic check on startup | CLI checks for newer versions at launch | Launch |
| Binary + JS update | Both the native binary and JS package are updated | v0.0.420 |
| CI auto-update disabled | Updates are skipped when `CI=true` is set | v0.0.407 |
| Old version cleanup | Previous package versions are removed after update | v0.0.388 |
| Safe cleanup | Old versions are no longer removed unexpectedly mid-session | v0.0.394 |
| Consistent install path | Always uses `~/.copilot/pkg/` | v0.0.421 |

> ⚠️ Pin your CLI version in CI. Auto-update is disabled by default in CI
> environments, but if you install via `curl`, you get the latest version on
> each run. For reproducibility, cache the installation or pin a version.

---

## Scripting Recipes

### Recipe 1: Automated Code Documentation Generation

Generate documentation for an entire source tree, one module at a time:

```bash
#!/usr/bin/env bash
set -euo pipefail

OUTPUT_DIR="docs/api"
mkdir -p "$OUTPUT_DIR"

for file in src/**/*.ts; do
  module=$(basename "$file" .ts)
  echo "Documenting: $module"
  copilot -p "Generate comprehensive API documentation in markdown for @$file. \
    Include: module overview, each exported function with parameters and return \
    types, usage examples, and edge cases." \
    --allow-all-paths \
    --silent > "$OUTPUT_DIR/${module}.md"
done

echo "Documentation generated in $OUTPUT_DIR/"
```

### Recipe 2: Batch File Migration

Convert a directory of JavaScript files to TypeScript:

```bash
#!/usr/bin/env bash
set -euo pipefail

for file in src/**/*.js; do
  ts_file="${file%.js}.ts"
  echo "Converting: $file → $ts_file"
  copilot -p "Convert @$file from JavaScript to TypeScript. Add proper type \
    annotations, replace require() with import statements, and add an interface \
    for any object literal used as a function parameter. Write the result to \
    $ts_file." \
    --allow-all \
    --silent
done

echo "Running type check..."
npx tsc --noEmit
```

### Recipe 3: Git Pre-Push Hook

Catch issues before they reach the remote:

```bash
#!/usr/bin/env bash
# Save as .git/hooks/pre-push and chmod +x
set -euo pipefail

CHANGED_FILES=$(git diff --name-only HEAD~1 -- '*.ts' '*.tsx')

if [ -z "$CHANGED_FILES" ]; then
  exit 0
fi

echo "Running AI review on changed files..."
copilot -p "Review these changed files for bugs, security issues, and \
  violations of our coding standards: $CHANGED_FILES. \
  Exit with a non-zero code if you find critical issues." \
  --allow-all-paths \
  --allow-tool "read_file" \
  --allow-tool "grep" \
  --silent

echo "AI review passed."
```

### Recipe 4: CI/CD Review Pipeline with JSONL Processing

Parse structured output for integration with other tools:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Generate structured review
copilot -p "Review src/ for security vulnerabilities. For each finding, \
  output the severity (critical/high/medium/low), file path, line number, \
  and description." \
  --output-format json \
  --allow-all-paths \
  --silent > findings.jsonl

# Count critical findings
CRITICAL=$(jq -s '[.[] | select(.type == "text") | .content | test("critical"; "i")] | length' findings.jsonl)

if [ "$CRITICAL" -gt 0 ]; then
  echo "::error::Found $CRITICAL critical security issues"
  exit 1
fi

echo "Security review passed."
```

### Recipe 5: Project Scaffolding

Bootstrap a new project from a template description:

```bash
#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="${1:?Usage: scaffold.sh <project-name>}"
mkdir -p "$PROJECT_NAME" && cd "$PROJECT_NAME"

copilot -p "Scaffold a new Express.js + TypeScript project in the current \
  directory. Include: tsconfig.json, package.json with scripts, src/index.ts \
  with a health-check endpoint, src/routes/ directory, Jest config, .gitignore, \
  and a README.md. Use strict TypeScript settings and ES2020 target." \
  --allow-all \
  --silent

echo "Project scaffolded in $PROJECT_NAME/"
echo "Next steps: cd $PROJECT_NAME && npm install && npm run dev"
```

> 💡 All recipes above use `--silent` to suppress the CLI's statistics line.
> Remove it during development to see token usage and timing information.

---

## Quick Reference Card

| Task | Command |
|------|---------|
| One-shot prompt | `copilot -p "..."` |
| Prompt with full perms | `copilot -p "..." --allow-all` |
| Specific model | `copilot -p "..." --model claude-opus-4.6` |
| JSON output | `copilot -p "..." --output-format json` |
| Silent for piping | `copilot -p "..." --silent` |
| Resume last session | `copilot --continue` |
| Resume by ID | `copilot --resume abc123` |
| Check version | `copilot version` |
| Update CLI | `copilot update` |
| Start ACP server | `copilot --acp` |
| Debug logging | `copilot --log-level debug` |

---

This concludes the GitHub Copilot CLI Manual. Return to the [Index](./00-index.md).
