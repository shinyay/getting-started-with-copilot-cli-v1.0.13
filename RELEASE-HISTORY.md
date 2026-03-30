# GitHub Copilot CLI — Release History

> Last updated: 2026-03-30
> Source: [github/copilot-cli/changelog.md](https://github.com/github/copilot-cli/blob/main/changelog.md)

---

## Timeline at a Glance

| Period | Versions | Milestone |
|--------|----------|-----------|
| Sep 2025 | 0.0.328 – 0.0.330 | Public Preview launch, Sonnet 4.5 default |
| Oct 2025 | 0.0.331 – 0.0.354 | Streaming, parallel tools, custom agents, GitHub Universe |
| Nov 2025 | 0.0.355 – 0.0.364 | GPT-5.1 family, ripgrep bundling, image support |
| Dec 2025 | 0.0.365 – 0.0.373 | GPT-5.2, auto-compaction, sub-agents, web_fetch |
| Jan 2026 | 0.0.374 – 0.0.400 | Plan mode, /review, /diff, memory, plugins, autopilot (exp.) |
| Feb 2026 | 0.0.401 – 0.0.420 | GA release 🎉, alt-screen, Claude Opus 4.6, /research |
| Mar 2026 | 0.0.421 – 0.0.423, **1.0.2** – **1.0.13** | Major version bump, Extensions, /pr, /rewind, personal skills, MCP sampling |

---

## 2026

### 1.0.13 — 2026-03-28

**Highlights:** /rewind, /new, CLAUDE.md/GEMINI.md instruction sources, MCP sampling

- Add `/rewind` command to undo last conversation turn and revert associated file changes
- Add `/new` command to start a fresh conversation while preserving settings and environment
- Add `/quit` as an alias for `/exit`
- Instruction sources now include `CLAUDE.md` and `GEMINI.md` files (in addition to existing sources)
- Add `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` environment variable for specifying additional instruction directories
- Add `/session` subcommands for session management
- Improved `/instructions` toggle with individual file control
- MCP servers can now request LLM inference (sampling) with user approval
- Remove Gemini-3-Pro-preview model support

### 1.0.12 — 2026-03-26

**Highlights:** .claude/settings.json config, /allow-all subcommands, template variables, intra-line diffs

- Read `.claude/settings.json` and `.claude/settings.local.json` as configuration sources
- Support `.mcp.json` at git root as MCP configuration source
- `/allow-all` now supports `on`, `off`, and `show` subcommands
- `/yolo` path permissions persist after `/clear`
- Support `{{project_dir}}` and `{{plugin_data_dir}}` template variables in hook/plugin configurations
- Plugin hooks now receive `CLAUDE_PROJECT_DIR` and `CLAUDE_PLUGIN_DATA` environment variables
- `Ctrl+Y` in plan mode opens the latest research report if no plan exists
- OSC 8 hyperlinks now clickable in VS Code terminals
- Intra-line diff highlighting improvements in `/diff` view
- Model display header shows the active reasoning effort level
- `/session rename` auto-generates session name from conversation history
- Removed `--alt-screen` flag — alt-screen now always enabled
- `@` file picker no longer shows `.git` contents
- Resilient handling of high-volume shell command output (no more crashes)
- Session resume restores previously selected custom agent
- User prompt appears in conversation immediately after pressing Enter

### 1.0.11 — 2026-03-23

**Highlights:** Personal skills directory, org MCP policy enforcement

- Add `~/.agents/skills/` as personal skill discovery directory (matches VS Code Copilot extension)
- Organization policy for third-party MCP servers now enforced for all users
- Warning displayed when MCP servers are blocked by allowlist enforcement
- Models always appear in picker; model names displayed where possible
- MCP servers in `.mcp.json` start correctly when working directory is git root
- Clipboard copy fixes for Windows with non-system `clip.exe`

### 1.0.10 — 2026-03-22

**Highlights:** Session management fixes, error feedback

- Session management stability improvements
- Improved error feedback for common failure scenarios
- Incremental fixes between v1.0.9 and v1.0.11

### 1.0.9 — 2026-03-21

**Highlights:** Usability and stability improvements

- Usability and stability improvements across CLI
- Bug fixes for session handling and terminal rendering

### 1.0.8 — 2026-03-19

**Highlights:** Session file restore fixes

- Fix session file restore issues on resume
- Incremental stability improvements

### 1.0.7 — 2026-03-17

**Highlights:** gpt-5.4-mini, customize mode, subagentStart hook, enhanced color contrast

- Add `gpt-5.4-mini` model support
- Add "customize" mode for section-level system prompt configuration
- Add `subagentStart` hook for injecting context into subagent prompts
- Improved CLI theme color contrast for readability
- User messages now have a subtle background for easier differentiation
- Tab bar uses more compact `[label]` style
- Double-Esc: first clears input, second triggers undo — hint shown after first Esc
- Branch indicator in header differentiates unstaged (`*`), staged (`+`), and untracked (`%`) files
- Session resume robustness improvements for sessions from older versions
- Experimental session SDK APIs: list and manage skills, MCP servers, and plugins
- Pro and trial users now see all entitled models in the model picker
- Fix CLI restart resending `-i/--interactive` prompt
- Fix Windows auto-update leaving incomplete packages

### 1.0.6 — 2026-03-14

**Highlights:** Filesystem and MCP fixes

- Case-insensitive filesystem handling improvements (fixes trusted folder prompts on macOS/Windows)
- MCP server startup fixes for various configurations
- Incremental stability improvements from v1.0.5

### 1.0.5 — 2026-03-13

**Highlights:** /pr command, /extensions, /version, @-mentions outside project, /diff syntax highlighting

- Introducing `/pr` to create and view PRs, fix CI failures, address review feedback, and resolve merge conflicts
- Add `/extensions` command to view, enable, and disable CLI extensions
- Add `/version` command to display CLI version and check for updates from within the session
- `@` file mentions now support paths outside the project: absolute paths (`@/usr/...`), home directory (`@~/...`), and relative parent paths (`@../...`)
- Syntax highlighting in `/diff` with support for 17 programming languages
- Send follow-up messages to background agents with the `write_agent` tool for multi-turn conversations
- Add experimental embedding-based dynamic retrieval of MCP and skill instructions per turn
- Add `preCompact` hook to run commands before context compaction starts
- `/changelog` supports `last <N>`, `since <version>`, and `summarize` to browse and summarize multiple release notes at once
- Toggling experimental mode with `/experimental on|off` automatically restarts the CLI
- Hooks config files that omit the version field are now accepted by the CLI
- Terminal title resets to default after running `/clear` or `/new`
- Block network (UNC) paths to prevent credential leakage via SMB authentication
- Setting claude-sonnet-4.6 as the default model is now preserved correctly
- Show a clear error when a classic PAT (`ghp_`) is set in environment variables
- Session reports an authentication error instead of hanging when the token is invalid

### 1.0.4 — 2026-03-11

**Highlights:** Adaptive themes, --reasoning-effort, configure-copilot agent, OpenTelemetry

- Add `--reasoning-effort` CLI flag to set reasoning effort level
- Add `configure-copilot` sub-agent for managing MCP servers, custom agents, and skills via the task tool
- Adaptive color engine with dynamic color modes and interactive theme picker
- Enables OpenTelemetry instrumentation for observability into agent sessions, LLM calls, and tool executions
- Replace `/pr open` with `/pr view [local|web]` to view PR status locally or open in browser
- Extensions can now be written as CommonJS modules (`extension.cjs`)
- Show loaded extensions count in the Environment loaded startup message
- Support `disableAllHooks` flag to disable all hooks from a configuration file
- Hooks can now request user confirmation before tool execution with 'ask' permission decision
- Path permission dialog offers a one-time approval option in addition to adding the path to the allowed list
- Show individual instruction file names in `/instructions` picker with [external] labels for injected files
- `/update` command automatically restarts to apply updates instead of requiring manual exit
- Add `session.shell.exec` and `session.shell.kill` RPC methods for streaming shell output
- OAuth authentication now handles Microsoft Entra ID and other OIDC servers reliably
- Autopilot mode stops continuing after API errors instead of looping indefinitely
- Terminal properly resets when CLI crashes, preventing shell corruption

### 1.0.3 — 2026-03-09

**Highlights:** Extensions (experimental), /restart, MCP from devcontainer.json

- Extensions are now available as an experimental feature — ask Copilot to write custom tools and hooks via `@github/copilot-sdk`
- Add `/restart` command to hot restart the CLI while preserving your session
- Read MCP server configuration from `.devcontainer/devcontainer.json`
- Document `GH_HOST`, `HTTP_PROXY`, `HTTPS_PROXY`, `NO_COLOR`, and `NO_PROXY` environment variables in help
- Add `--binary-version` flag to query the CLI binary version without launching
- Background task notifications display in timeline with expandable detail
- Type 'quit' to exit the CLI, in addition to 'exit'
- Add Windows Terminal support to `/terminal-setup` command
- `/reset-allowed-tools` now fully undoes `/allow-all` and re-triggers the autopilot permission dialog
- `/add-dir` directories persist across session changes like `/clear` and `/resume`
- Suppress `/init` suggestion when `.github/instructions/` contains instructions
- Rename `merge_strategy` config to `mergeStrategy` for consistency
- Trust safe `sed` commands to run without confirmation

### 1.0.2 — 2026-03-06 🏆

_Major version bump to celebrate General Availability!_

- Type `exit` as a bare command to close the CLI
- `ask_user` form submits with Enter and allows custom responses in enum fields
- Support `command` field as cross-platform alias for bash/powershell in hook configs
- Hook configurations accept `timeout` as alias for `timeoutSec`
- Fix handling of meta with control keys (including shift+enter from `/terminal-setup`)

### 0.0.423 — 2026-03-06

- Security: prompt users for shell commands with dangerous expansion/substitution
- Block `/share gist` for EMU and GHE Cloud users with clear error messaging
- Elicitation fields require Enter to confirm (✓ confirmed vs ❯ browsing cursor)
- MCP servers can request users to visit a URL for OAuth/API key flows
- Improved explore agent precision and large repository support
- Diff mode displays cleanly on Windows with CRLF line endings

### 0.0.422 — 2026-03-05

**Highlights:** GPT-5.4 model, reverse history search (Ctrl+R), JSONL output mode, startup hooks

- Add support for **GPT-5.4** model
- Display request ID in auth error messages
- Load personal hooks from `~/.copilot/hooks`
- Timeline shows question box; "Making best guess on autopilot" indicator
- Plugin cache auto-recovers from corruption
- Add `copy_on_select` config option for alt-screen
- CJK IME candidate windows at correct cursor position
- Mouse scroll in `/diff` alt-screen mode
- Add `/copy` command
- Add `--output-format json` for JSONL in prompt mode
- Press **Ctrl+R** for reverse incremental history search
- Startup prompt hooks to auto-submit prompts at session start
- Rename `launch_messages` → `companyAnnouncements`
- Rename `.github/copilot/config.json` → `settings.json`
- Support `enabledPlugins` in config for auto-install at startup
- Support installing plugins from `ssh://` URLs
- Session usage metrics persisted to `events.jsonl`

### 0.0.421 — 2026-03-03

**Highlights:** MCP Elicitations (experimental), AUTO theme, clickable PR links

- Autopilot permission dialog on first prompt, not on mode switch
- AUTO theme reads terminal's ANSI color palette directly
- Structured form input via MCP Elicitations (experimental)
- Plugin commands read `extraKnownMarketplaces` from `.claude/settings.json`
- Git hooks detect Copilot CLI via `COPILOT_CLI=1` env var
- Fix Python MCP server timeouts (buffered stdout)
- Display clickable PR reference in status bar
- Add `--plugin-dir` flag for local plugin loading
- Linux primary selection buffer support (middle-click paste)
- Markdown tables with proper column widths and Unicode borders

### 0.0.420 — 2026-02-27

- Auto-update now also updates the binary executable
- Plugin repos update correctly after force-pushes
- 502 errors retried automatically
- Type `#` to reference GitHub issues, PRs, and discussions

### 0.0.419 — 2026-02-27

**Highlights:** `/chronicle` command (experimental), external editor shortcut

- Add `/chronicle` command (standup, tips, improve) powered by session history
- Add **Ctrl+G** for editing prompts in external editor
- Add `--mouse`/`--no-mouse` flag
- Home/End keys for alt-screen scroll buffer
- MCP server env vars auto-included; npm-style server names supported

### 0.0.418 — 2026-02-25 🎉

**General Availability!**

- 🎉 Copilot CLI is now [generally available](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available)
- Agent protected from accidentally killing itself
- Remove `--disable-parallel-tools-execution` flag

### 0.0.417 — 2026-02-25

- Add `/research` command for deep research with exportable reports
- Plugin agents and skills available immediately after install
- Alt+backspace registers correctly

### 0.0.416 — 2026-02-24

- Expanded `--help` with descriptions, examples, sorted flags
- Block third-party MCP servers when policy disallows
- Status line two-line layout on narrow terminals
- Undo operations always require confirmation

### 0.0.415 — 2026-02-23

- Add `show_file` tool for presenting code and diffs
- Env loading indicator for skills, MCPs, plugins
- Plan approval menu with model-curated actions
- `/mcp show` groups servers by User/Workspace/Plugins/Built-in
- Ctrl+A/E cycle through visual lines in wrapped input

### 0.0.414 — 2026-02-21

- Explore agent can use GitHub MCP tools
- Permission elevation dialog when accepting a plan with autopilot

### 0.0.413 — 2026-02-20

- Add support for **Claude Opus 4.6** (display heading content from reasoning)
- Increase LSP request timeout 30s → 90s
- Alt-screen mode enabled by default with `--experimental`
- Auto-migrate from claude-sonnet-4.5 to current default model
- Configurable status line via custom shell scripts

### 0.0.412 — 2026-02-19

**Highlights:** Cross-session memory (experimental), `/update` command, user-level instructions

- Add cross-session memory: ask about past work across sessions (experimental)
- Add `/update` command
- Add `exit_plan_mode` tool with plan approval dialog
- Support `~/.copilot/instructions/*.instructions.md` for user-level instructions
- Edit plan with Ctrl+Y; edit prompt with Ctrl+X Ctrl+E
- Double-click word / triple-click line selection in alt-screen
- `/fleet` mode dispatches more subagents in parallel
- Deprecate `gpt-5` model
- Sign Windows native prebuilds with Authenticode
- Add `--bash-env` flag
- `/clear` preserves agent mode

### 0.0.411 — 2026-02-17

- Add support for **Claude Sonnet 4.6**
- Autopilot mode and `/fleet` command available to all users
- Add `include_coauthor` config to control Co-authored-by trailer
- SDK APIs for plan mode, autopilot, fleet, workspace files
- Terminal bell rings once when agent finishes

### 0.0.410 — 2026-02-14

**Focus:** Memory optimization, Ctrl+Z suspend/resume

- Fixed multiple high memory usage issues (rapid logging, large sessions, rapid shell output)
- Add Ctrl+Z suspend/resume on Unix
- Page Up/Page Down in alt-screen
- Add `/init suppress` per repository
- Shell mode removed from Shift+Tab cycle (access via `!` only)
- Exit with Ctrl+D on empty prompt
- Shift+Enter newlines with Kitty keyboard protocol
- Add Copilot co-authored-by trailer to git commits

### 0.0.409 — 2026-02-12

- CLI integrates with VS Code (`/ide` command)
- Quick help overlay: press `?` for grouped shortcuts
- `/diff` uses full screen in alt-screen
- Include default plugin marketplaces (copilot-plugins, awesome-copilot)

### 0.0.408 — 2026-02-12

- Add `/streamer-mode`
- Mouse text selection in `--alt-screen`
- Large `!` command output no longer crashes

### 0.0.407 — 2026-02-11

**Highlights:** Alt-screen mode (experimental), `/instructions` command, permanent tool permissions

- Add experimental **alt-screen buffer mode** (`--alt-screen`)
- Add `/instructions` command to view/toggle custom instruction files
- Theme picker with live preview, colorblind/tritanopia variants
- Option to approve tool permissions permanently for a location
- Add workspace-local MCP via `.vscode/mcp.json`
- Tab cycles modes forward, Shift+Tab backward; shell is now a mode
- Streaming responses auto-retry on server errors

### 0.0.406 — 2026-02-07

- Add support for **Claude Opus 4.6 Fast (Preview)**
- Add `/changelog` command
- Commands from plugins translated into skills
- MCP tool responses include structured content (images, resources)

### 0.0.405 — 2026-02-05

- Plugins can bundle LSP server configurations
- `/experimental` shows help listing features

### 0.0.404 — 2026-02-05

- Add support for **Claude Opus 4.6**
- Add `/tasks` command for background task management
- Enable background agents for all users
- `/allow-all` and `/yolo` execute immediately

### 0.0.403 — 2026-02-04

- Security check preventing use of modules outside application bundle
- Reasoning summaries enabled by default
- Support comma-separated tools in custom agent frontmatter

### 0.0.402 — 2026-02-03

- ACP server supports agent and plan session modes
- Plugins can provide hooks for session lifecycle events

### 0.0.401 — 2026-02-03

- Support `.agents/skills` directory for auto-loading
- Support Claude-style `.mcp.json` format
- Add `copilot login` subcommand
- Add `agentStop` and `subagentStop` hooks
- `/diff` dual column layout with accurate line numbers

### 0.0.400 — 2026-01-30

**Highlights:** Autopilot mode (experimental), theme picker, MCP server instructions

- Add **autopilot mode** for autonomous task completion (experimental)
- Add `/theme` command with GitHub Dark/Light themes
- MCP server instructions support
- Remove bundled LSP servers (TypeScript, Python)
- Add fuzzy search to model picker
- Add `launch_messages` config for startup announcements
- Code Review tool handles large changesets (100-file limit)

### 0.0.399 — 2026-01-29

- Add `/diff` command to review session changes
- Add `/allow-all` and `/yolo` commands
- Add LSP tool for code intelligence (experimental)
- Undo/rewind to previous states with double-Esc
- Support `.claude/commands/` single-file commands
- Sessions get AI-generated names

### 0.0.398 — 2026-01-28

- Fix "Invalid session id" regression for agent shell calls

### 0.0.397 — 2026-01-28

- `/mcp show <server-name>` for server details
- Add `--acp` flag for Agent Client Protocol server mode
- Directories in `@`-mention autocomplete
- Content >30 KB auto-saved to workspace files

### 0.0.396 — 2026-01-27

**Highlights:** Agent creation wizard, `/init` command, plugin system

- Create custom agents through interactive CLI wizard
- Add `/init` command to generate Copilot instructions
- Add `/experimental` command and `--experimental` flag
- Add `/plugin install` (GitHub repos, URLs, local paths)
- Plugins can provide custom agents
- `preToolUse` hooks can deny/modify tool execution

### 0.0.395 — 2026-01-26

- Add commenting to `/diff` mode
- Plugin skills usable by agent
- Load local shell configuration in agent sessions

### 0.0.394 — 2026-01-24

- Add GHE Cloud (`*.ghe.com`) support in `/delegate`
- `/delegate` accepts optional prompt
- SDK supports infinite sessions with auto-compaction
- Press `/` to search sessions in `/resume`

### 0.0.393 — 2026-01-23

- Add Esc-Esc to undo file changes to any previous snapshot
- GHE Cloud remote custom agents support
- Show compaction status as timeline messages

### 0.0.392 — 2026-01-22

- Add `/plugin` command for marketplace management
- Add `/rename` command
- Edit tool displays diffs in timeline

### 0.0.390 — 2026-01-22

- Preserve extended thinking after compaction
- Enable steering during plan mode

### 0.0.389 — 2026-01-22

**Highlights:** MSI installer, OAuth MCP, `/diff` command, MIT license

- Add MSI installer for Windows
- MCP servers authenticate via OAuth 2.0 with auto token management
- Plugins can bundle MCP servers
- Invoke skills using `/skill-name` slash commands
- Add `/diff` command to review session changes
- Shell commands (`!`) run in parallel while agent works
- **Change license to MIT License**

### 0.0.388 — 2026-01-20

- Add `/review` command to analyze code changes
- `--enable-all-github-mcp-tools` flag for read-write GitHub MCP
- Redesign CLI header with branded mascot

### 0.0.387 — 2026-01-20

- Add `ask_user` tool for interactive clarification
- Add **plan mode** with dedicated panel

### 0.0.386 — 2026-01-19

- Add `/resume` command to switch sessions

### 0.0.385 — 2026-01-19

**Highlights:** Infinite sessions, memory, intent in terminal title

- Enable **infinite sessions** with automatic compaction checkpoints
- Combine all custom instruction files (not priority-based fallbacks)
- Display current intent in terminal tab title
- `store_memory` tool for repository memory

### 0.0.384 — 2026-01-16

**Highlights:** Extended thinking, memory injection, reasoning persistence

- Enable **extended thinking** for Anthropic Claude models
- Inject repo memories; add memory storage tool
- Add `&` prefix shortcut for `/delegate`
- Add `/cd` alias for `/cwd`
- Configure reasoning effort for GPT models
- Selecting "approve for session" auto-approves parallel requests of same type

### 0.0.382 — 2026-01-14

- Add support for **GPT-5.2-Codex**
- Add `--config-dir` flag

### 0.0.381 — 2026-01-13

- Add `--allow-all` and `--yolo` flags
- Shell mode history filters by prefix (`!git` + ↑)

### 0.0.380 — 2026-01-13

- Auto-compaction runs in background without blocking
- Inline feedback when rejecting tool permissions
- `web-fetch` rejects `file://` URLs

### 0.0.377 — 2026-01-08

- Large file messages encourage `view_range` incremental reading

### 0.0.376 — 2026-01-08

- Remote session loading via GraphQL ID
- Task tool subagents process images
- Large tool outputs written to disk

### 0.0.375 — 2026-01-07

- Add **Ctrl+T** to toggle reasoning summaries
- Add `--share` and `--share-gist` flags for non-interactive mode

### 0.0.374 — 2026-01-02

- Add `/compact` command and auto-compaction at 95% token limit
- **Built-in sub-agents** for exploring and managing tasks
- Built-in `web_fetch` tool

---

## 2025

### 0.0.373 — 2025-12-30

- Enable Copilot Spaces tools in GitHub MCP Server
- Tab completion for path args in `/cwd`, `/add-dir`

### 0.0.372 — 2025-12-19

- Add `/context` command (token usage visualization)
- Add `--resume` flag for remote sessions
- URL permission controls for shell commands
- Enable disabled models directly when selecting them

### 0.0.371 — 2025-12-18

- Normal text respects terminal default foreground color

### 0.0.370 — 2025-12-18

- Load CA certificates from system and environment
- Diff display uses configured git pager (delta, diff-so-fancy)
- SHA256 checksums published for CLI executables
- Add `--available-tools` and `--excluded-tools` flags

### 0.0.369 — 2025-12-11

- Add support for **GPT-5.2**

### 0.0.368 — 2025-12-10

- Add `grep` tool for Codex models
- Numpad keys work with Kitty protocol

### 0.0.367 — 2025-12-04

- **GPT-5.1-Codex-Max** now available

### 0.0.366 — 2025-12-03

- Add `infer` property for custom agent tool visibility
- CLI executables in GitHub release artifacts
- Add `apply_patch` toolchain for OpenAI Codex models

### 0.0.365 — 2025-11-25

- Add `--silent` option for scripting

### 0.0.364 — 2025-11-25

- Syntax highlighting for diffs

### 0.0.363 — 2025-11-24

- **Opus 4.5**, **GPT-4.1**, and **GPT-5-Mini** now available
- Image data paste prioritizes file contents over icons
- Support `GITHUB_ASKPASS` for authentication
- MCP servers work in `--prompt` mode

### 0.0.362 — 2025-11-20

- Paste image data from clipboard into CLI
- Shell commands excluded from Bash/PowerShell history

### 0.0.360 — 2025-11-18

- Fix file operations timing out on permission wait

### 0.0.359 — 2025-11-17

**Highlights:** Image drag & drop, `/share` command

- Image support via drag & drop and path pasting
- Add `/share` command (markdown file or GitHub gist)
- `copilot -p` no longer prompts for permissions
- Enable `USE_BUILTIN_RIPGREP` env var

### 0.0.358 — 2025-11-14

- Recovery: fix GPT-5.1, GPT-5.1-Codex, GPT-5.1-Codex-Mini availability

### 0.0.356 — 2025-11-13

- **GPT-5.1**, **GPT-5.1-Codex**, and **GPT-5.1-Codex-Mini** now available

### 0.0.355 — 2025-11-12

**Highlights:** Bundled ripgrep, self-documentation

- Agent can read its own `/help` and README for capability questions
- Bundled **ripgrep** with `grep` and `glob` tools
- Improved `.agent.md` parsing for VS Code custom agents

### 0.0.354 — 2025-11-03

- Support for MCP server tool notifications
- `COPILOT_GITHUB_TOKEN` env var (precedence over `GH_TOKEN`)
- `/delegate` command works without local changes
- Exit with nonzero code on `-p` mode LLM failures

### 0.0.353 — 2025-10-28

**Highlights:** Custom agents, `/delegate` command

- **Custom agents** from `~/.copilot/agents`, `.github/agents`, or org `.github` repo
- `/agent` slash command and `--agent` flag
- Add `/delegate` command to delegate tasks to Copilot coding agent (branch + PR)

### 0.0.352 — 2025-10-27

- Improve MCP tools with slashes

### 0.0.351 — 2025-10-24

- Major path detection improvements to reduce unnecessary permission prompts
- 👀 See you at GitHub Universe!

### 0.0.350 — 2025-10-23

**Highlights:** Curated GitHub MCP tools, bundled sharp

- Limited default GitHub MCP server tools to conserve context window
- Added `--enable-all-github-mcp-tools` flag
- Bundled `sharp` dependency (Windows startup fix)

### 0.0.349 — 2025-10-22

- **Parallel tool calling** enabled (with `--disable-parallel-tools-execution` opt-out)
- Add `/quit` alias for `/exit`
- Added temp directory to default allowed paths

### 0.0.348 — 2025-10-21

**Highlights:** Token-by-token streaming

- **Streaming output** enabled (`--stream off` to disable)
- Bundled `node-pty`
- Memory footprint improvements for large shell outputs

### 0.0.347 — 2025-10-20

- Fix incorrect PRU consumption stats display

### 0.0.346 — 2025-10-19

- Fix model config not accounted for in PRU estimation

### 0.0.345 — 2025-10-18

- Fix premium request overcounting bug

### 0.0.344 — 2025-10-17

- GitHub MCP server in prompt mode
- Detached process support in bash tool
- Session abort handling cleanup

### 0.0.343 — 2025-10-16

- Add **Haiku 4.5** model
- Add `--additional-mcp-config` flag (inline JSON or file)
- Shimmer effect on "Thinking..." indicator
- Prompt for `/terminal-setup` if needed

### 0.0.342 — 2025-10-15

**Highlights:** New session format, Kitty protocol default, multi-line input

- Overhauled session logging format (`~/.copilot/session-state`)
- **Kitty keyboard protocol** enabled by default → multi-line input via Shift+Ctrl
- `/terminal-setup` for VS Code multi-line support
- Non-interactive GHE logins via `GH_HOST`
- Persistent `log_level` config option

### 0.0.341 — 2025-10-14

- Add `/terminal-setup` command
- Model premium request multipliers in `/model` list

### 0.0.340 — 2025-10-13

- Removed "Windows support is experimental" warning
- Improved debugging with Copilot API request IDs
- Changed MCP env vars to literal values (use `${VAR}` for references)
- Prompt to approve new paths in `-p` mode

### 0.0.339 — 2025-10-10

- Improved MCP server argument input in `/mcp add`
- Kitty protocol fix for `u` paste issue (behind `COPILOT_KITTY` env var)

### 0.0.338 — 2025-10-09

- Kitty protocol moved behind `COPILOT_KITTY` env var due to regressions

### 0.0.337 — 2025-10-08

- MCP server name validation
- Ctrl+B / Ctrl+F cursor movement
- Multi-line input for Kitty protocol terminals

### 0.0.336 — 2025-10-07

**Highlights:** Major performance improvements

- **Proxy support** via HTTPS_PROXY/HTTP_PROXY regardless of Node version
- Significantly reduced token consumption and round trips
- Improved file write performance (especially Windows)
- Screen reader persistent preference prompt

### 0.0.335 — 2025-10-06

- File diffs shown in timeline by default
- Slash command argument hints
- Display improvements for narrow windows (<80 columns)

### 0.0.334 — 2025-10-03

- Compact paste display (>10 lines → `[Paste #1 - 15 lines]`)
- Context approaching ≤20% warning

### 0.0.333 — 2025-10-02

**Highlights:** Image support, shell bypass, `/usage` command

- **Image support** via `@`-mention
- Direct shell commands with `!` prefix
- Add `/usage` command (PRU stats, session time, code changes)
- Add `--continue` flag to resume last session

### 0.0.332 — 2025-10-01

- Switch to per-subscription Copilot API endpoints
- Fix `/user` commands across auth modes

### 0.0.331 — 2025-10-01

- Improved file read/edit timeline density
- Model list shows only accessible models
- Scrollbar in `@` file picker

### 0.0.330 — 2025-09-29

- Reverted default model back to **Sonnet 4** (4.5 not yet fully rolled out)

### 0.0.329 — 2025-09-29

**Highlights:** Sonnet 4.5, `/model` command

- Add **Claude Sonnet 4.5** as default model
- Add `/model` slash command
- Display current model above input
- Scrollable multi-line input (10-line limit)
- Glob matching in shell rules (`--allow-tool`, `--deny-tool`)
- Improved `/resume` interface with relative time

### 0.0.328 — 2025-09-26

_First version tracked in the public changelog._

- Improved error when blocked by organization policy
- Improved PAT error for missing "Copilot Requests" permission
- PowerShell parsing improvements

---

## Model Availability Timeline

| Date | Model | Event |
|------|-------|-------|
| 2025-09-29 | Claude Sonnet 4.5 | Added (briefly default) |
| 2025-10-16 | Claude Haiku 4.5 | Added |
| 2025-11-13 | GPT-5.1, GPT-5.1-Codex, GPT-5.1-Codex-Mini | Added |
| 2025-11-24 | Claude Opus 4.5, GPT-4.1, GPT-5-Mini | Added |
| 2025-12-04 | GPT-5.1-Codex-Max | Added |
| 2025-12-11 | GPT-5.2 | Added |
| 2026-01-14 | GPT-5.2-Codex | Added |
| 2026-02-05 | Claude Opus 4.6 | Added |
| 2026-02-07 | Claude Opus 4.6 Fast (Preview) | Added |
| 2026-02-17 | Claude Sonnet 4.6 | Added |
| 2026-02-19 | GPT-5 | Deprecated |
| 2026-03-05 | GPT-5.4 | Added |

---

## Key Feature Milestones

| Feature | Version | Date |
|---------|---------|------|
| Public Preview launch | 0.0.328 | 2025-09-26 |
| `/model` slash command | 0.0.329 | 2025-09-29 |
| Image support (`@`-mention) | 0.0.333 | 2025-10-02 |
| Token-by-token streaming | 0.0.348 | 2025-10-21 |
| Parallel tool calling | 0.0.349 | 2025-10-22 |
| Custom agents + `/delegate` | 0.0.353 | 2025-10-28 |
| Bundled ripgrep (`grep`/`glob` tools) | 0.0.355 | 2025-11-12 |
| `/share` command | 0.0.359 | 2025-11-17 |
| Auto-compaction + sub-agents | 0.0.374 | 2026-01-02 |
| Plan mode + `ask_user` | 0.0.387 | 2026-01-20 |
| `/review` command | 0.0.388 | 2026-01-20 |
| Plugin system + `/plugin` | 0.0.392 | 2026-01-22 |
| MIT License | 0.0.389 | 2026-01-22 |
| `/init` + agent creation wizard | 0.0.396 | 2026-01-27 |
| Autopilot mode (experimental) | 0.0.400 | 2026-01-30 |
| Alt-screen mode (experimental) | 0.0.407 | 2026-02-11 |
| VS Code integration (`/ide`) | 0.0.409 | 2026-02-12 |
| Cross-session memory (experimental) | 0.0.412 | 2026-02-19 |
| 🎉 General Availability | 0.0.418 | 2026-02-25 |
| `/research` command | 0.0.417 | 2026-02-25 |
| Major version bump → **1.0.2** | 1.0.2 | 2026-03-06 |
