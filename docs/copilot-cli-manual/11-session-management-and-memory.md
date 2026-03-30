# Chapter 11: Session Management & Memory

Every interaction with GitHub Copilot CLI takes place inside a **session** — a
persistent, named container that holds your conversation history, tool call
results, compaction checkpoints, and usage metrics. Understanding how sessions
work — and how cross-session memory ties them together — unlocks truly
continuous, long-running workflows where context is never lost.

> 📋 For context-window mechanics, see
> [Chapter 6: Context Management & Prompt Engineering](./06-context-management-and-prompt-engineering.md).

---

## Session Lifecycle

A session begins the moment you launch the CLI and ends when you exit or start
a new one. Between those two events, every message, tool call, file edit, and
agent delegation is recorded as part of that session's history.

### Session Creation

| Trigger | What Happens |
|---------|-------------|
| `copilot` (bare launch) | Creates a new session with a temporary ID |
| `/clear` | Ends the current session, starts a fresh one |
| `/new` | Starts a fresh conversation preserving settings, working directory, and environment (since v1.0.13) |
| Cancel the `/resume` picker | Starts a new session (since v0.0.404) |

> 💡 The `/clear` command preserves your current agent mode (Interactive, Plan,
> or Autopilot) since v0.0.412. You no longer need to re-select your mode after
> clearing a session.

> 💡 Since **v1.0.12**, `/yolo` (permission) decisions also persist after `/clear`.
> You no longer need to re-enable `/allow-all` after resetting your conversation
> context.

### AI-Generated Session Names

Since **v0.0.399**, Copilot generates a descriptive session name from your first
message, replacing opaque UUIDs. The name appears in the session picker, the
footer bar, and shared exports.

### Session Storage

| Path | Purpose | Since |
|------|---------|-------|
| `~/.copilot/session-state/` | Current session format | v0.0.342 |
| `~/.copilot/history-session-state/` | Legacy format (pre-v0.0.342) | Deprecated |

Legacy sessions are **auto-migrated** when you resume them. The new format
supports compaction checkpoints, cross-session memory, and structured event logs.

> ⚠️ Do not manually edit files in `~/.copilot/session-state/`. The internal
> format is not a stable API. Use `/share` to export session content.

### Session Info in the Footer

In alt-screen mode, the footer bar shows the current session name, mode, and
model — a persistent anchor so you always know which session you are in.

---

## The `/session` Command

The `/session` command displays information about your current session —
workspace summary, file counts, and conversation statistics.

```
> /session
```

| Version | Improvement |
|---------|-------------|
| v0.0.389 | Improved visual hierarchy with colored section headers |
| v0.0.397 | Accurate line counts for edited files |
| v1.0.13 | Subcommands: view metadata, rename sessions, manage lifecycle |

### `/session` Subcommands (since v1.0.13)

The `/session` command now supports subcommands for granular session management:

| Subcommand | Purpose |
|------------|---------|
| `/session` | View current session metadata (original behavior) |
| `/session rename` | Rename the current session (auto-generates name from history since v1.0.12) |
| `/session info` | Display detailed session metadata |

---

## Resuming Sessions

There are three distinct mechanisms for resuming sessions, each suited to a
different workflow.

### The `/resume` Command

Opens an interactive session picker listing all saved sessions. Use it when you
are inside Copilot CLI and want to **switch** to a different session.

```
> /resume
```

**Session picker features:**

| Feature | Description | Since |
|---------|-------------|-------|
| Relative timestamps | "2 hours ago", "3 days ago" | v0.0.329 |
| Message counts | Shows total turns per session | v0.0.329 |
| Search with `/` | Press `/` inside the picker to filter by name | v0.0.394 |
| Instant rendering | Picker opens without loading flash | v0.0.412 |
| Cancel to start new | Press `Esc` to abandon resume and start fresh | v0.0.404 |

**Navigating the picker:**

```
┌─ Resume Session ───────────────────────────────────────┐
│  ❯ Fix Express auth middleware       8 turns · 12m ago │
│    Add pagination to events API      23 turns · 2h ago │
│    Debug failing Jest tests          5 turns · 1d ago  │
│    Refactor logger utility           14 turns · 3d ago │
│                                                        │
│  ↑↓ navigate  / search  Enter select  Esc cancel       │
└────────────────────────────────────────────────────────┘
```

> 💡 If you have dozens of sessions, use the `/` search filter to narrow the
> list quickly. It matches against AI-generated session names and raw content.

### The `--resume` Flag

Resume a session at **launch time**, before the CLI is fully interactive.

| Usage | Behavior |
|-------|----------|
| `copilot --resume` | Opens the session picker at launch |
| `copilot --resume <session-id>` | Resumes a specific session by UUID |
| `copilot --resume <graphql-id>` | Loads a remote session via GraphQL ID (since v0.0.376) |

```bash
# Resume interactively
copilot --resume

# Resume a specific session
copilot --resume a3f8c1d2-7e9b-4f1a-b5c6-d8e0f2a3b4c5
```

**Remote session loading (since v0.0.376):** You can resume sessions created by
the GitHub coding agent in the cloud. This brings the full conversation — file
edits, tool calls, plan state — into your local environment.

> ⚠️ Remote sessions may reference files that do not exist locally. The CLI
> displays history, but tool calls that depended on the remote environment
> cannot be re-executed.

**Session creation with UUID (since v0.0.407):** Passing a UUID that does not
match any session creates a **new** session with that ID — useful for scripting.

**Alt-screen rendering (since v0.0.411):** `--resume` no longer causes a visual
flash when loading sessions in alt-screen mode.

**Session resume robustness (since v1.0.7):** Improved handling of sessions
created by older CLI versions. Sessions from earlier releases are loaded
gracefully without errors or data loss.

### The `--continue` Flag

Reopens the **most recently closed session** without presenting a picker.

```bash
copilot --continue
```

| Aspect | Detail |
|--------|--------|
| Available since | v0.0.333 |
| Equivalent to | Selecting the top item in `copilot --resume` |

> 💡 Alias it for instant resumption: `alias cpc='copilot --continue'`

---

## The `/rename` Command

Rename the current session to something more descriptive. This is especially
useful when the AI-generated name does not capture the actual focus of your work.

```
> /rename Refactor auth middleware with Zod validation
```

The `/rename` command is an alias for `/session rename` (since v0.0.392).

Since **v1.0.12**, running `/session rename` (or `/rename`) without arguments
auto-generates a descriptive session name from the conversation history — no
manual input required.

---

## Context Compaction

As sessions grow, they consume the model's context window. **Compaction**
summarizes older history to free space while preserving essential information.

### How Compaction Works

Compaction generates a condensed summary capturing key decisions, files
modified, outstanding tasks, relevant tool results, and resolved errors. This
summary replaces original messages, freeing tokens for new work.

### Auto-Compaction

Auto-compaction triggers automatically when your session reaches **95% of the
model's token limit** (since v0.0.374). It runs in the background without
blocking your input (since v0.0.380), so you can continue typing while the
compaction completes.

| Aspect | Detail | Since |
|--------|--------|-------|
| Trigger threshold | 95% of context window | v0.0.374 |
| Blocking behavior | Non-blocking (background) | v0.0.380 |
| Tool call preservation | Correctly preserves tool call sequences | v0.0.386 |
| Extended thinking | Preserved across compaction | v0.0.390 |
| Skills effectiveness | Maintained after compaction | v0.0.399 |
| Status display | Timeline messages show compaction progress | v0.0.393 |
| Infinite sessions | SDK supports unlimited session length | v0.0.394 |

> 💡 Auto-compaction is transparent — you will see a brief status message in the
> timeline, but the session continues seamlessly. The model "remembers" what
> matters and gracefully forgets what does not.

### The `/compact` Command

Manually trigger compaction — useful when pivoting to a different task within
the same session.

```
> /compact
```

| Feature | Detail | Since |
|---------|--------|-------|
| Cancel with `Esc` | Abort a running compaction | v0.0.385 |
| Message queuing | Messages typed during compaction are auto-queued | v0.0.389 |
| Checkpoint hints | Clearer hints about checkpoint summaries | v0.0.399 |

> ⚠️ Compaction is lossy by nature — fine-grained details from earlier in the
> conversation may be simplified or dropped. If a specific piece of information
> is critical, re-state it after compaction to ensure it stays in context.

### Compaction Checkpoints

Checkpoints are periodic snapshots that preserve essential context across
multiple compaction cycles (since v0.0.385), enabling **truly infinite sessions**.

```
Session Start
    ├── Messages 1–50    → Checkpoint 1
    ├── Messages 51–120  → Checkpoint 2
    └── Messages 121–... → Current (live context)
```

Each checkpoint contains a structured summary, file paths, key decisions, and
unresolved items. Sessions with large histories load faster since v0.0.380.

---

## Cross-Session Memory (Experimental)

> ⚠️ Cross-session memory is an **experimental feature** added in v0.0.412.
> Its behavior, storage format, and availability may change in future releases.

Cross-session memory allows Copilot CLI to recall information from **previous
sessions**. When enabled, you can ask "What files did I edit last week?" and
receive answers drawn from your session history.

### The `store_memory` Tool

Copilot stores memories using the `store_memory` tool, which captures structured
facts about your codebase and development patterns:

| Field | Purpose | Example |
|-------|---------|---------|
| `subject` | Topic keyword (1–2 words) | `"authentication"` |
| `fact` | Concise statement (< 200 chars) | `"Use JWT with 1h expiry for API auth"` |
| `citations` | Source reference | `"src/auth/middleware.ts:42"` |

Since **v0.0.411**, stored memories appear in the session timeline with their
subject, fact, and citations displayed for transparency.

### How Memory Is Injected

Repository-scoped memories are automatically injected into new session prompts
(since v0.0.384). When you start a session in a git repository, the CLI loads
relevant memories from its local store and includes them in the system context.

**Memory loading behavior:**

| Scenario | Behavior | Since |
|----------|----------|-------|
| Inside a git repo | Loads repo-scoped memories | v0.0.384 |
| Outside a git repo | Runs normally, no memories loaded | v0.0.393 |
| Memory loading fails | Handles error gracefully, no user warning | v0.0.394 |
| Feature disabled | Memories not included in prompts | v0.0.385 |

> 💡 Memory is opt-in. It is only included in your prompts when the feature is
> enabled for your account. Check your Copilot settings to verify.

### Querying Past Sessions

With cross-session memory enabled, ask natural-language questions about your
development history:

```
What bugs did I fix in the auth module last week?
```

```
Which PRs did I work on in this repository?
```

---

## Usage Tracking

Copilot CLI provides granular visibility into resource consumption, critical for
managing **Premium Request Units (PRUs)** and understanding token costs.

### The `/usage` Command

Displays a comprehensive breakdown of session resource consumption (since
v0.0.333).

```
> /usage

Session: 47 min · 12 turns · 3.2 PRUs
Tokens: claude-sonnet-4 — 38k in / 12k out
        claude-haiku-4.5 (sub-agents) — 8k in / 3k out
Code:   4 files · +127 -43 lines
```

| Feature | Detail | Since |
|---------|--------|-------|
| Basic usage display | Duration, turns, PRUs | v0.0.333 |
| Per-model breakdown | Token counts by model | v0.0.333 |
| Sub-agent tokens | Includes delegated agent consumption | v0.0.399 |
| Accurate exit summary | Correct totals shown when exiting | v0.0.394 |

### The `/context` Command

Visual overview of current token usage relative to the context window (since
v0.0.372).

```
> /context

Context Window: ████████████████░░░░░░░░░░░  62% used
Used: 124,000 / 200,000 · Compaction at 190,000 (95%)
```

> 💡 Run `/context` before starting large tasks. If close to the threshold,
> run `/compact` first to maximize available space.

### Session Usage Persistence

Since **v0.0.422**, session usage metrics are persisted to an `events.jsonl`
file after each session ends. This enables offline analysis of your Copilot
usage patterns over time.

| Aspect | Detail | Since |
|--------|--------|-------|
| Persistence format | `events.jsonl` (newline-delimited JSON) | v0.0.422 |
| Exit stats cleanup | On-exit usage no longer pollutes session history | v0.0.334 |

---

## Sharing Sessions

Sessions capture problem-solving approaches and architectural decisions.
Copilot CLI provides two mechanisms for sharing this knowledge.

### The `/share` Command

The `/share` command exports your current session as a readable markdown file or
publishes it as a GitHub Gist (since v0.0.359).

| Subcommand | Behavior | Since |
|------------|----------|-------|
| `/share` | Exports session as markdown to a local file | v0.0.359 |
| `/share gist` | Publishes session as a GitHub Gist | v0.0.359 |

```
> /share
Saved session to: ~/copilot-session-fix-express-auth.md

> /share gist
Created gist: https://gist.github.com/user/abc123def456
```

**Non-interactive sharing (since v0.0.375):**

```bash
# Share as markdown file at the end of a non-interactive run
copilot -p "Analyze this repo" --share

# Share as a gist
copilot -p "Analyze this repo" --share-gist
```

| Fix | Detail | Since |
|-----|--------|-------|
| Nested codeblocks | Shared sessions correctly render nested fenced code | v0.0.370 |
| EMU/GHE restriction | `/share gist` blocked for EMU and GHE Cloud with data residency | v0.0.423 |

> ⚠️ If your organization uses GitHub Enterprise Managed Users (EMU) or GHE
> Cloud with data residency enabled, the `/share gist` subcommand is blocked to
> prevent data leakage. Use `/share` to export to a local file instead.

### The `/copy` Command

The `/copy` command copies the **last assistant response** to your system
clipboard (since v0.0.422). This is useful for pasting Copilot's output into
documentation, PRs, or chat messages.

```
> /copy
Copied last response to clipboard.
```

> 💡 In alt-screen mode, text selection persists after copying — you do not
> lose your visual selection when using `/copy`.

---

## Session Events & Timeline

The session timeline is the scrollable history of everything that has happened
in your current session. Over recent releases, the timeline has been refined for
clarity and reduced noise.

| Improvement | Detail | Since |
|-------------|--------|-------|
| Tool call display | Completed tool calls shown in prompt mode | v0.0.395 |
| Startup noise reduction | Startup messages hidden to reduce clutter | v0.0.394 |
| Concise events | Session event messages shortened | v0.0.388 |
| Visual cleanup | Cleaner formatting and consistent styling | v0.0.388 |

The timeline displays several categories of events:

| Event Type | Icon | Example |
|------------|------|---------|
| User message | `>` | `> Fix the broken test` |
| Tool execution | `●` | `● bash  npm test` |
| File edit | `●` | `● edit  src/auth.ts  (+5 -2)` |
| Compaction | `◐` | `◐ Context compacted (checkpoint 3)` |
| Memory stored | `◆` | `◆ Memory stored: authentication` |
| Agent delegation | `▸` | `▸ explore agent: 3 files searched` |

---

## ACP Server Mode

The **Agent Client Protocol (ACP)** server mode exposes Copilot CLI as a
programmable backend for external applications (since v0.0.397).

```bash
copilot --acp
```

### ACP Capabilities

| Capability | Detail | Since |
|------------|--------|-------|
| Basic server mode | `--acp` flag launches ACP server | v0.0.397 |
| Session loading | Load existing sessions into ACP | v0.0.410 |
| Model switching | Change models mid-session | v0.0.400 |
| Permission flags | `--yolo`, `--allow-all` respected in ACP | v0.0.400 |
| Agent and plan modes | Full mode support (Interactive, Plan, Autopilot) | v0.0.402 |
| Reasoning effort | Configurable via session config | v0.0.421 |
| Terminal auth | Authentication via terminal flow | v0.0.401 |

> ⚠️ ACP mode is for tool integrations — it does not render a terminal UI.

---

## The `/rewind` Command

The `/rewind` command (since **v1.0.13**) provides the simplest undo mechanism
in Copilot CLI — it undoes the last conversation turn and reverts all associated
file changes in a single action.

```
> /rewind
```

Unlike `Double-Esc` (which opens a multi-snapshot picker), `/rewind` always
targets exactly one turn back. This makes it ideal for quick corrections during
iterative coding — if the agent's last edit was wrong, `/rewind` removes both
the response and its file modifications instantly.

| Aspect | Detail |
|--------|--------|
| Scope | Undoes the last conversation turn |
| File changes | All file modifications from that turn are reverted |
| Conversation | The last assistant response is removed from history |
| Cumulative | Run `/rewind` multiple times to undo successive turns |

> 💡 Use `/rewind` for quick single-step undo. Use `Double-Esc` when you need
> to jump back to an arbitrary earlier point in the session.

---

## Quick Reference: Session Commands

| Command / Flag | Purpose | Context |
|----------------|---------|---------|
| `/session` | Show current session info (subcommands since v1.0.13) | Inside CLI |
| `/rewind` | Undo last turn and revert associated file changes | Inside CLI |
| `/new` | Start fresh conversation preserving settings and environment | Inside CLI |
| `/resume` | Switch to a different session | Inside CLI |
| `/rename <name>` | Rename the current session (auto-generates if no name given) | Inside CLI |
| `/compact` | Manually trigger context compaction | Inside CLI |
| `/usage` | Display session usage metrics | Inside CLI |
| `/context` | Show token usage and remaining capacity | Inside CLI |
| `/share` | Export session as markdown | Inside CLI |
| `/share gist` | Publish session as a GitHub Gist | Inside CLI |
| `/copy` | Copy last response to clipboard | Inside CLI |
| `/clear` | End session and start a new one | Inside CLI |
| `--resume` | Resume a session at launch | CLI flag |
| `--resume <id>` | Resume a specific session at launch | CLI flag |
| `--continue` | Resume the most recent session at launch | CLI flag |
| `--share` | Export session after non-interactive run | CLI flag |
| `--share-gist` | Publish gist after non-interactive run | CLI flag |
| `--acp` | Start in ACP server mode | CLI flag |

---

## Best Practices

1. **Name sessions early** — use `/rename` if the AI-generated name is vague
2. **Compact before pivoting** — run `/compact` when switching tasks mid-session
3. **Use `--continue` as default launch** — alias it: `alias cpc='copilot --continue'`
4. **Monitor with `/context`** — proactive `/compact` beats auto-compaction mid-thought
5. **Share meaningful sessions** — bug fixes and complex features make great onboarding docs
6. **Let memory build organically** — Copilot stores memories when it finds patterns worth keeping

---

Next: [Chapter 12: Code Review, Diff & Development Workflows](./12-code-review-diff-and-workflows.md)
