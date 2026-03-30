# Chapter 5: Complete Slash Commands Reference

Slash commands control Copilot CLI behavior during an interactive session. Type
`/` at the prompt to enter command mode — a fuzzy-searchable picker appears.
You can also type the full command directly.

> 📋 This reference reflects features through **v1.0.13**. Run `/help` or
> `/changelog` to verify availability in your installed version.

## Quick Reference: All Commands

| Command | Aliases | Category | Since |
|---------|---------|----------|-------|
| `/add-dir` | — | Permission | — |
| `/agent` | — | Agent Environment | — |
| `/allow-all` | `/yolo` | Permission | v0.0.399 |
| `/changelog` | — | Help & Feedback | v0.0.406 |
| `/chronicle` | — | Other (experimental) | v0.0.419 |
| `/clear` | `/new` | Help & Feedback | — |
| `/compact` | — | Session | v0.0.374 |
| `/context` | — | Session | v0.0.372 |
| `/copy` | — | Session | v0.0.422 |
| `/cwd` | `/cd` | Permission | — |
| `/delegate` | — | Other | v0.0.353 |
| `/diff` | — | Code | v0.0.389 |
| `/exit` | `/quit` | Other | — |
| `/extensions` | — | Agent Environment | v1.0.5 |
| `/experimental` | — | Help & Feedback | v0.0.396 |
| `/feedback` | — | Help & Feedback | — |
| `/fleet` | — | Models & Subagents | v0.0.411 |
| `/help` | — | Help & Feedback | — |
| `/ide` | — | Code | v0.0.409 |
| `/init` | — | Agent Environment | v0.0.396 |
| `/instructions` | — | Help & Feedback | v0.0.407 |
| `/list-dirs` | — | Permission | — |
| `/login` | — | Other | — |
| `/logout` | — | Other | — |
| `/lsp` | — | Code | — |
| `/mcp` | — | Agent Environment | — |
| `/model` | `/models` | Models & Subagents | v0.0.329 |
| `/new` | — | Session | v1.0.13 |
| `/plan` | — | Other | — |
| `/plugin` | — | Agent Environment | v0.0.392 |
| `/pr` | — | Code | v1.0.5 |
| `/rename` | — | Session | v0.0.392 |
| `/research` | — | Other | v0.0.417 |
| `/reset-allowed-tools` | — | Permission | — |
| `/restart` | — | Other | v1.0.3 |
| `/resume` | — | Session | v0.0.386 |
| `/review` | — | Code | v0.0.388 |
| `/rewind` | — | Session | v1.0.13 |
| `/session` | — | Session | — |
| `/share` | — | Session | v0.0.359 |
| `/skills` | — | Agent Environment | — |
| `/streamer-mode` | — | Help & Feedback | v0.0.408 |
| `/tasks` | — | Models & Subagents | v0.0.404 |
| `/terminal-setup` | — | Code | — |
| `/theme` | — | Help & Feedback | v0.0.400 |
| `/update` | — | Help & Feedback | v0.0.412 |
| `/usage` | — | Session | v0.0.333 |
| `/user` | — | Other | — |
| `/version` | — | Help & Feedback | v1.0.5 |

---

## Agent Environment Commands

### `/init`

**Initialize Copilot instructions for a repository.** *(since v0.0.396)*

| Syntax | Description |
|--------|-------------|
| `/init` | Scan repo and generate `.github/copilot-instructions.md` |
| `/init suppress` | Suppress per-repo init suggestions *(since v0.0.410)* |

```
> /init
```

> Expected: Copilot detects your tech stack and generates a structured
> instructions file with project conventions.

> 📋 See [Chapter 7](./07-custom-instructions-and-repository-configuration.md) for writing effective instruction files.

---

### `/agent`

**Browse and select available agents.** Opens a fuzzy-search picker listing all
registered agents — specialized configurations combining instructions, tools,
and model settings.

> 📋 See [Chapter 8](./08-agents.md) for creating custom agents.

---

### `/skills`

**Manage skills: add, remove, view.**

| Subcommand | Description |
|------------|-------------|
| `/skills` | List active skills |
| `/skills add [path]` | Add skill from directory containing `SKILL.md` |
| `/skills remove [name]` | Remove a skill |

> 💡 Since **v0.0.407**, skill changes take effect immediately.

> 📋 See [Chapter 10](./10-skills-and-plugins.md) for creating `SKILL.md` files.

---

### `/mcp`

**Manage MCP server configuration.** MCP servers give Copilot CLI access to
external tools — databases, APIs, and custom services.

| Subcommand | Description | Since |
|------------|-------------|-------|
| `/mcp add` | Register a new MCP server | — |
| `/mcp show` | List servers grouped by User/Workspace/Plugins/Built-in | v0.0.415 |
| `/mcp show <name>` | Show details and tools for a server | v0.0.415 |
| `/mcp enable <name>` | Enable a disabled server | — |
| `/mcp disable <name>` | Disable without removing | — |
| `/mcp reload` | Reload all configurations | — |

> ⚠️ Disabling preserves configuration — re-enable with `/mcp enable`.

> 📋 See [Chapter 9](./09-mcp-servers.md) for `mcp.json` configuration.

---

### `/plugin`

**Manage plugins and marketplaces.** *(since v0.0.392)*

| Subcommand | Description |
|------------|-------------|
| `/plugin install <source>` | Install from GitHub repo, URL, local path, or SSH |
| `/plugin update [name]` | Update one or all plugins |
| `/plugin list` | List installed plugins |
| `/plugin uninstall <name>` | Remove a plugin |
| `/plugin marketplace add` | Register a plugin marketplace |

Supported sources: GitHub repos (`owner/repo`), HTTPS URLs, local paths, SSH URLs.

> 📋 See [Chapter 10](./10-skills-and-plugins.md) for authoring and distributing plugins.

---

## Models & Subagents Commands

### `/model`

**Select the AI model.** *(since v0.0.329, alias `/models` since v0.0.389)*

| Syntax | Description |
|--------|-------------|
| `/model` | Open fuzzy-search picker (two-column layout with multipliers) |
| `/model <name>` | Set model directly: `/model claude-sonnet-4` |

Multipliers shown in the picker indicate PRU consumption rate (1×, 2×, 0.5×).
Model selection persists for the session only — use `--model` on startup for defaults.

> 📋 See [Chapter 13](./13-model-selection.md) for model comparison strategies.

---

### `/fleet`

**Enable fleet mode for parallel subagent execution.** *(since v0.0.411)*

Dispatches multiple subagents that work in parallel on different parts of a
task. An orchestrator validates subagent work and can dispatch more as needed
*(both since v0.0.412)*.

```
> /fleet
```

> ⚠️ Fleet mode increases resource consumption — each subagent uses its own
> context window and consumes PRUs independently. Monitor with `/usage`.

---

### `/tasks`

**View background tasks, subagents, and shell sessions.** *(since v0.0.404)*

Displays a dashboard of running and recently completed work with consistent
icons *(since v0.0.410)*:

| Icon | Status |
|------|--------|
| 🔄 | Running |
| ✅ | Completed |
| ❌ | Failed |
| ⏸️ | Paused |

Shows Recent Activity for background agents *(since v0.0.407)*.

---

## Code Commands

### `/ide`

**Connect to an IDE workspace (VS Code).** *(since v0.0.409)*

Establishes a connection so Copilot CLI can access open files, editor
selections, and diagnostics. Shows a file selection indicator in the status bar.

> 💡 IDE connection enables richer context — Copilot sees your open file,
> cursor position, and active diagnostics.

---

### `/diff`

**Review changes in the current directory.** *(since v0.0.389)*

Full-screen alt-screen diff viewer with syntax highlighting. Uses your
configured git pager (`delta`, `diff-so-fancy`, etc.).

| Version | Feature |
|---------|---------|
| v0.0.389 | Initial `/diff` command |
| v0.0.395 | Commenting on specific lines |
| v0.0.396 | Shows entire repo changes from subdirectories |
| v0.0.399 | Full-screen alt-screen mode, mouse scroll |

**Navigation:** `↑`/`↓` scroll, `←`/`→` navigate files (carousel, up to 5),
`c` comment on line, `q`/`Esc` exit.

> ⚠️ Since v0.0.396, `/diff` shows changes from the **entire repository**, even
> when launched from a subdirectory.

---

### `/review`

**Run the code review agent.** *(since v0.0.388)* Analyzes changes and reports
only genuine issues — bugs, security, logic errors. Handles up to 100 files;
ignores build artifacts.

> 💡 The review agent is intentionally conservative. No findings = clean changes.

---

### `/lsp`

**Manage Language Server Protocol configuration.** Shows configured servers
including plugin-contributed ones, with status and handled file types.

> 📋 See [Chapter 12](./12-language-server-integration.md) for LSP setup and troubleshooting.

---

### `/terminal-setup`

**Configure terminal for multiline input (Shift+Enter).** Detects your terminal
type and provides or applies the appropriate configuration, including VS Code
integrated terminal support.

---

## Permission Commands

### `/allow-all`

**Enable all permissions for the session.** *(since v0.0.399, alias `/yolo`)*

Removes all confirmation prompts for tool execution and file access. Executes
immediately without confirmation *(since v0.0.404)*.

| Subcommand | Description | Since |
|------------|-------------|-------|
| `/allow-all` or `/allow-all on` | Enable all permissions | v0.0.399 |
| `/allow-all off` | Revoke all permissions (restore defaults) | v1.0.12 |
| `/allow-all show` | Display current permission state | v1.0.12 |

Since **v1.0.12**, permissions granted via `/allow-all` (or `/yolo`) persist
after `/clear` — previously, clearing the conversation also reset permissions.

> ⚠️ **Use with caution.** This removes all safety gates. Only use when you
> trust the operations Copilot may perform in a recoverable environment.

---

### `/add-dir`

**Add a directory to the allowed file access list.** Paths can be absolute or
relative (resolved from cwd).

```
> /add-dir /home/user/shared-libs
```

---

### `/list-dirs`

**Display all allowed directories** — the working directory plus any added
with `/add-dir`.

---

### `/cwd`

**Change or show working directory.** *(alias `/cd` since v0.0.384)*

| Syntax | Description |
|--------|-------------|
| `/cwd` or `/cd` | Show current working directory |
| `/cwd <path>` or `/cd <path>` | Change working directory |

> 💡 Tab completion for path arguments since **v0.0.373**.

---

### `/reset-allowed-tools`

**Reset allowed tools list to defaults.** Reverts `/allow-all` and per-tool
grants. Can run during agent execution *(since v0.0.412)*.

---

## Session Commands

### `/resume`

**Switch to a different session.** *(since v0.0.386)*

Opens a session picker — press `/` to search. Supports remote sessions via
GraphQL ID *(since v0.0.376)* for cross-device workflows.

---

### `/rename`

**Rename current session.** *(since v0.0.392, alias for `/session rename`)*

```
> /rename feature-auth-implementation
```

---

### `/context`

**Show context window token usage visualization.** *(since v0.0.372)*

Displays token allocation across conversation history, system instructions,
tool results, and available capacity with percentage bars.

> 💡 When context is nearly full, use `/compact` to reclaim space.

---

### `/usage`

**Display session usage metrics.** *(since v0.0.333)*

| Metric | Description |
|--------|-------------|
| PRU consumption | Premium request units used |
| Session duration | Wall-clock time since start |
| Code changes | Lines added, modified, deleted |
| Per-model tokens | Input/output counts by model |
| Sub-agent tokens | Subagent consumption *(since v0.0.399)* |

---

### `/session`

**Session management and info.** Displays ID, name, creation time,
working directory, active model, and workspace config. Improved visual hierarchy
*(since v0.0.389)*.

| Subcommand | Description | Since |
|------------|-------------|-------|
| `/session` | Show session info and workspace summary | — |
| `/session list` | List recent sessions | v1.0.13 |
| `/session rename <name>` | Rename current session | v0.0.392 |
| `/session export` | Export session to file | v1.0.13 |
| `/session delete <id>` | Delete a saved session | v1.0.13 |

---

### `/rewind`

**Undo last conversation turn and revert file changes.** *(since v1.0.13)*

Reverts the most recent conversation turn and all associated file modifications.
Unlike `Esc Esc` (which only reverts file snapshots), `/rewind` also removes
the turn from conversation history.

```
> /rewind
```

> Expected: Copilot shows which files would be reverted, asks for confirmation,
> then removes the last turn and restores files to their prior state.

> 💡 Call `/rewind` multiple times to undo several consecutive turns.

> 📋 See [Chapter 4](./04-modes-of-operation.md#the-rewind-command-v1013) for
> how `/rewind` interacts with different modes.

---

### `/new`

**Start a fresh conversation.** *(since v1.0.13)*

Clears all conversation history while preserving your current settings,
environment, permissions, working directory, and model selection. Equivalent
to `/clear` but semantically emphasizes starting new work rather than resetting.

```
> /new
```

> 💡 `/new` and `/clear` are interchangeable — both preserve mode, permissions,
> and session configuration.

---

### `/compact`

**Summarize conversation history.** *(since v0.0.374)*

Compresses history into a concise summary, freeing context window tokens.

| Version | Behavior |
|---------|----------|
| v0.0.374 | Initial support |
| v0.0.385 | Cancellable with `Esc` |
| v0.0.389 | Messages during compaction auto-queued |

> ⚠️ Compaction is **lossy** — detailed history is replaced with a summary.
> Key decisions are retained but specific phrasing may be lost.

---

### `/share`

**Share session to markdown or GitHub gist.** *(since v0.0.359)*

| Variant | Output |
|---------|--------|
| `/share` | Copy session as markdown to clipboard |
| `/share gist` | Create a GitHub gist with session content |

> ⚠️ `/share gist` is **blocked** for EMU accounts and GHE Cloud orgs with
> data residency requirements. Use `/share` (clipboard) instead.

---

### `/copy`

**Copy last response to clipboard.** *(since v0.0.422)*

Copies the most recent Copilot response in its original markdown format.

---

## Help & Feedback Commands

### `/help`

**Show help for interactive commands.** Displays a categorized list of all
available slash commands with brief descriptions.

---

### `/changelog`

**Display changelog for CLI versions.** *(since v0.0.406)* Shows release notes
with version numbers, dates, and categorized changes.

---

### `/feedback`

**Provide feedback** — survey, bug report, or feature request. Opens an
interactive menu with feedback categories.

---

### `/theme`

**View or configure terminal theme.** *(since v0.0.400)* Without arguments shows
the current theme; with a name switches to it.

---

### `/update`

**Update CLI to latest version.** *(since v0.0.412)* Checks for updates,
downloads the latest version, and prompts for restart.

---

### `/experimental`

**Show/toggle experimental features.** *(since v0.0.396)*

Displays experimental features with their enabled/disabled state.

> 💡 Disable all experimental features at startup with `--no-experimental`
> *(since v0.0.406)*:
>
> ```bash
> copilot-cli --no-experimental
> ```

---

### `/clear`

**Clear conversation history.** *(alias `/new` since v0.0.381; `/new` also
available as a standalone command since v1.0.13)*

Resets history while keeping session configuration (cwd, permissions, model).
Preserves agent mode *(since v0.0.412)*.

---

### `/instructions`

**View and toggle custom instruction files.** *(since v0.0.407)*

Shows detected instruction files with source, active/inactive status, and token
count. Full-screen alt-screen view when enabled *(since v0.0.412)*.

Since **v1.0.13**, the toggle supports individual file control — you can enable
or disable specific instruction files without affecting others:

| Syntax | Description | Since |
|--------|-------------|-------|
| `/instructions` | List all instruction files with status | v0.0.407 |
| `/instructions toggle` | Toggle all instructions on/off | v0.0.407 |
| `/instructions toggle <path>` | Toggle a specific instruction file | v1.0.13 |
| `/instructions show <path>` | Display contents of an instruction file | v1.0.13 |

---

### `/streamer-mode`

**Toggle streamer mode.** *(since v0.0.408)* Hides sensitive information (file
paths, environment variables) — useful when screen-sharing or streaming.

---

## Other Commands

### `/exit` / `/quit`

**Exit the CLI.** `/quit` is a dedicated alias *(since v1.0.13)*. Typing bare
`exit` (without `/`) also works *(since v1.0.2)*.

---

### `/restart`

**Restart the CLI session.** *(since v1.0.3)* Reloads configuration and
restarts the agent without exiting the process. Useful after changing
custom instructions or MCP server configuration.

---

### `/extensions`

**Manage CLI extensions.** *(since v1.0.5)* Browse, install, and manage
extensions that add new capabilities to Copilot CLI.

---

### `/pr`

**Interact with pull requests.** *(since v1.0.5)* View, review, and manage
pull requests directly from the CLI. Integrates with the GitHub MCP server
for full PR context.

---

### `/version`

**Display the current CLI version.** *(since v1.0.5)* Shows the installed
version and checks if a newer version is available.

---

### `/login` / `/logout`

**Manage GitHub authentication.** `/login` initiates OAuth device flow;
`/logout` revokes the current token.

---

### `/plan`

**Create an implementation plan before coding.** Switches to planning mode —
subsequent prompts generate structured plans for review before execution.

---

### `/research`

**Deep research with exportable reports.** *(since v0.0.417)* Performs
multi-step investigation on a topic with progress updates and produces an
exportable structured report.

---

### `/user`

**Manage GitHub user list.**

| Subcommand | Description |
|------------|-------------|
| `/user list` | Show all authenticated users |
| `/user show` | Display current user details |
| `/user switch` | Switch to a different account |

---

### `/delegate`

**Delegate task to the Copilot coding agent.** *(since v0.0.353)* Creates a
branch, implements changes, and opens a PR in the background.

| Version | Enhancement |
|---------|-------------|
| v0.0.353 | Initial support |
| v0.0.394 | Inline prompt, GHE Cloud support |
| v0.0.422 | Prompts for target remote in multi-remote repos |

> ⚠️ Runs on GitHub's infrastructure, not locally. Review the resulting PR.

---

### `/chronicle` (Experimental)

**Standup summaries, tips, and workflow improvements.** *(since v0.0.419)*

| Subcommand | Description |
|------------|-------------|
| `/chronicle standup` | Generate standup summary from session history |
| `/chronicle tips` | Personalized tips based on usage patterns |
| `/chronicle improve` | Suggestions for improving your Copilot workflow |

> ⚠️ Experimental — enable with `/experimental` first.

---

### `/models`

**Alias for `/model`.** *(since v0.0.389)* Opens the model selection picker.

---

## Command Cheat Sheet

**Starting a session:**

| Step | Command |
|------|---------|
| Set the model | `/model claude-sonnet-4` |
| Grant permissions | `/allow-all` |
| Check instructions | `/instructions` |

**During development:**

| Action | Command |
|--------|---------|
| Review your changes | `/diff` |
| Get a code review | `/review` |
| Plan before coding | `/plan` |
| Check context usage | `/context` |

**Managing long sessions:**

| Action | Command |
|--------|---------|
| Free context space | `/compact` |
| Check usage | `/usage` |
| Rename session | `/rename my-feature-work` |
| Share session | `/share gist` |

**Getting help:**

| Action | Command |
|--------|---------|
| See all commands | `/help` |
| Check what's new | `/changelog` |
| Report a bug | `/feedback` |
| Update CLI | `/update` |

---

Next: [Chapter 6: Context Management & Prompt Engineering](./06-context-management-and-prompt-engineering.md)
