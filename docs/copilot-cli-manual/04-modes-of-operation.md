# Chapter 4: Modes of Operation

GitHub Copilot CLI provides five distinct modes of operation, each designed for
a different interaction style. Understanding when and how to use each mode is
the key to working efficiently — choosing the right mode for the task at hand
can save significant time and reduce risk.

This chapter covers every mode in detail: how to activate it, how it behaves,
when to use it, and when to avoid it.

---

## Overview

| Mode | Purpose | Activation | AI Involvement |
|------|---------|------------|----------------|
| **Interactive** | Turn-by-turn conversation | Default mode | Per-turn response |
| **Plan** | Collaborative implementation planning | `Shift+Tab` cycle or `/plan` | Planning only |
| **Autopilot** | Autonomous task completion | `Shift+Tab` cycle | Fully autonomous |
| **Customize** | Section-level system prompt configuration | `/customize` | Configuration only |
| **Shell** | Direct shell command execution | `!` prefix | None |

### Cycling Between Modes

You cycle through modes using keyboard shortcuts:

| Shortcut | Direction |
|----------|-----------|
| `Shift+Tab` | Forward through modes (Interactive → Plan → Autopilot) |
| `Tab` | Backward through modes (Autopilot → Plan → Interactive) |

> 💡 Shell mode is **not** part of the `Shift+Tab` cycle (since v0.0.410).
> Access it exclusively by prefixing your input with `!`.

The current mode is displayed in the input prompt area. Switching modes does not
clear your conversation history — your full context is preserved.

### Mode Persistence Across /clear

Since v0.0.412, the `/clear` command preserves your current mode. If you are in
Plan mode and run `/clear`, the conversation resets but you remain in Plan mode.
Prior to this version, `/clear` would reset you to Interactive mode.

```
# You are in Plan mode
/clear

# Conversation cleared — still in Plan mode
```

> ⚠️ While `/clear` preserves mode, it does clear all conversation context,
> the plan panel contents, and any in-flight tool approvals.

---

## Interactive Mode (Default)

Interactive mode is the default mode when you start Copilot CLI. It provides a
turn-by-turn conversational experience where you submit a prompt, Copilot
responds, and you guide the conversation iteratively.

### How It Works

1. You type a prompt and press `Enter`
2. Copilot processes your request, potentially calling tools (file reads, shell
   commands, code edits)
3. Each tool invocation requires your explicit approval (unless you have
   session-approved the tool)
4. Copilot presents its response
5. You review, follow up, or start a new request

### Tool Approval in Interactive Mode

Every tool call requires your approval before execution:

```
Copilot wants to run: cat src/routes/events.ts
[y] Yes  [n] No  [a] Always allow this tool  [d] Deny always
```

| Response | Effect |
|----------|--------|
| `y` | Allow this single invocation |
| `n` | Deny this single invocation |
| `a` | Allow this tool for the rest of the session (session-approve) |
| `d` | Deny this tool for the rest of the session |

> 💡 Session-approving common read-only tools like file reads saves
> significant time without increasing risk. Use `a` for `view` and `grep`
> early in your session.

### Steering While the Agent Thinks

Since v0.0.380, you can send messages while Copilot is processing a response.
This lets you steer the agent mid-task without waiting for it to finish:

```
You: Refactor the authentication middleware to use JWT

# While Copilot is working...
You: Also make sure to add proper error messages for expired tokens

# Copilot incorporates your guidance into its current work
```

You can also queue slash commands alongside steering messages using `Ctrl+D`:

```
# While Copilot is working...
Ctrl+D    # Opens command queue
/compact  # Queued — will execute after current turn completes
```

### When to Use Interactive Mode

| Scenario | Why Interactive? |
|----------|-----------------|
| Exploring unfamiliar code | You control the pace and direction |
| Learning Copilot CLI | See each tool call and understand the workflow |
| Sensitive code changes | Review every edit before it is applied |
| Debugging with Copilot | Iterative hypothesis → test → refine cycle |
| Code review assistance | Ask targeted questions about specific files |

### When to Avoid Interactive Mode

- **Repetitive batch tasks** — Autopilot is faster
- **You already have a clear plan** — Plan mode then Autopilot is more efficient
- **Simple shell commands** — Shell mode (`!`) avoids AI overhead

### Detailed Workflow Example: Interactive Bug Investigation

```
You: I'm seeing a 500 error on POST /api/events. Help me debug this.

Copilot: I'll look at the events route handler. Let me read the relevant files.
         [Tool: view src/routes/events.ts] → Approved
         [Tool: view src/services/eventService.ts] → Approved

         The POST handler calls eventService.create() but doesn't validate
         the request body. If `title` is missing, the service throws an
         unhandled error. Here's what's happening:
         ...

You: Can you show me the error handling middleware too?

Copilot: [Tool: view src/middleware/errorHandler.ts] → Approved

         The error handler catches AppError instances but this is a raw
         TypeError, so it falls through to the generic 500 response...

You: Add validation for the POST body using the Zod schema pattern.

Copilot: [Tool: edit src/routes/events.ts] → Approved
         [Tool: edit src/middleware/validation.ts] → Approved

         I've added a validateBody(createEventSchema) middleware to the
         POST route. Now invalid requests return a 400 with details...
```

> 📋 For a complete reference of slash commands available in Interactive mode,
> see [Chapter 5: Slash Commands Reference](./05-slash-commands-reference.md).

---

## Plan Mode

Plan mode is designed for collaborative planning — you and Copilot build an
implementation plan **before** any code is written. This is critical for
complex tasks where writing code without a plan leads to rework.

### How It Works

1. Switch to Plan mode via `Shift+Tab` or the `/plan` command
2. Describe the task or feature you want to implement
3. Copilot analyzes the codebase and drafts an implementation plan
4. The plan appears in a **dedicated plan panel** in the terminal
5. You review, suggest changes, or approve the plan
6. Once approved, you switch to Interactive or Autopilot to implement

### Activating Plan Mode

There are two ways to enter Plan mode:

```
# Method 1: Cycle with keyboard shortcut
Shift+Tab    # Cycles forward: Interactive → Plan

# Method 2: Slash command (works from any mode)
/plan
```

### The Plan Panel

Plan mode uses a dedicated panel separate from the conversation area. The plan
is a structured markdown document that typically includes:

- **Problem statement** — what you are solving
- **Approach** — high-level strategy
- **Files to modify** — specific files and what changes each needs
- **Key decisions** — trade-offs and architectural choices
- **Implementation order** — suggested sequence of steps

### Editing the Plan Directly

Since v0.0.412, you can edit the plan in your terminal editor using `Ctrl+Y`:

```
Ctrl+Y    # Opens plan in $EDITOR (or vi/nano if unset)
```

This opens the plan as a markdown file. Edit it, save, and close — your changes
are reflected in the plan panel immediately.

> 💡 On WSL and in devcontainers, plan files automatically open in VS Code
> instead of the terminal editor, giving you a richer editing experience.

### Plan Approval Flow

When Copilot finishes drafting the plan, it uses the `exit_plan_mode` tool to
present it for your review. You see an action menu:

```
Plan ready for review:

• Overall approach: Add JWT authentication to the Event API
• Files to change: src/middleware/auth.ts, src/routes/events.ts, src/models/user.ts
• Key decision: Use RS256 algorithm for token signing

[1] ✅ Accept (recommended)
[2] 📄 View full plan
[3] 💬 Suggest changes
```

| Action | What Happens |
|--------|--------------|
| **Accept** | Plan is locked in; you proceed to implementation |
| **View full plan** | Opens the complete plan document for detailed review |
| **Suggest changes** | You provide feedback; Copilot revises the plan |

Since v0.0.415, the action menu is model-curated — Copilot highlights the
recommended action based on context (usually "Accept" for well-formed plans).

#### Permission Elevation on Accept

Since v0.0.414, when you accept a plan and choose to implement with Autopilot,
a permission elevation dialog appears:

```
You are about to run in Autopilot mode.
Copilot will make changes autonomously.

Allow Copilot to proceed? [y/N]
```

This extra confirmation prevents accidental autonomous execution of plans that
were only meant for review.

### Steering During Plan Mode

Since v0.0.390, you can steer Copilot while it is drafting a plan — you do not
have to wait for the full plan to be generated before providing feedback:

```
You: Implement rate limiting for the API

# While Copilot drafts the plan...
You: Use a token bucket algorithm, not sliding window

# Copilot adjusts the plan mid-generation
```

### When to Use Plan Mode

| Scenario | Why Plan? |
|----------|-----------|
| Multi-file refactors | See the full scope before making changes |
| New feature implementation | Agree on architecture before coding |
| Team alignment | Share the plan with teammates for review |
| Complex bug fixes | Map out root cause and fix strategy |
| Unfamiliar codebase | Let Copilot analyze and propose an approach first |

### When to Avoid Plan Mode

- **Quick single-file edits** — Interactive is faster
- **You already know exactly what to do** — Skip straight to implementation
- **Exploratory questions** — Interactive mode is better for Q&A

### Detailed Workflow Example: Plan → Review → Implement

```
# Step 1: Switch to Plan mode
Shift+Tab    # Now in Plan mode

# Step 2: Describe the task
You: Add pagination support to the GET /api/events endpoint.
     It should support page and limit query parameters with
     sensible defaults. Include total count in the response.

# Step 3: Copilot drafts a plan
Copilot: [Analyzing codebase...]

Plan:
─────────────────────────────────────
## Add Pagination to Events API

### Approach
Add cursor-based pagination with page/limit parameters.
Default: page=1, limit=20, max limit=100.

### Files to Modify
1. src/routes/events.ts — Add query param extraction
2. src/services/eventService.ts — Add pagination logic
3. src/models/types.ts — Add PaginationParams interface
4. src/utils/response.ts — respondPaginated already exists ✓
5. tests/events.test.ts — Add pagination test cases

### Implementation Order
1. Types first (models)
2. Service logic (business layer)
3. Route wiring (HTTP layer)
4. Tests (verification)
─────────────────────────────────────

[1] ✅ Accept (recommended)
[2] 📄 View full plan
[3] 💬 Suggest changes

# Step 4: Suggest a change
You: 3    # Suggest changes

You: Add input validation — reject page < 1 and limit > 100.
     Also add an X-Total-Count response header.

# Step 5: Copilot revises
Copilot: [Updated plan with validation and header...]

[1] ✅ Accept (recommended)
...

# Step 6: Accept and implement
You: 1    # Accept

# Step 7: Switch to Autopilot for implementation
Shift+Tab    # Now in Autopilot mode

You: Implement the approved pagination plan.
```

> 📋 For details on `Ctrl+Y` and other keyboard shortcuts, see
> [Chapter 3: Interface and Navigation](./03-interface-and-navigation.md).

---

## Autopilot Mode

Autopilot mode enables Copilot to work autonomously on tasks with minimal
human intervention. Instead of approving every tool call, Copilot executes a
multi-step workflow on its own and notifies you when it is done.

### How It Works

1. Switch to Autopilot mode via `Shift+Tab`
2. Describe the task
3. Copilot works through the task autonomously — reading files, making edits,
   running commands — without asking for approval at each step
4. A terminal bell rings when Copilot finishes (since v0.0.411)
5. You review the results

### Availability

Autopilot mode was introduced as an experimental feature in v0.0.400 and
became available to all users in v0.0.411. No feature flag or opt-in is
required.

### Activating Autopilot Mode

```
# Cycle forward from Interactive
Shift+Tab    # Interactive → Plan
Shift+Tab    # Plan → Autopilot

# Or cycle backward from Interactive
Tab          # Interactive → Autopilot (wraps around)
```

### Permission Dialog

Since v0.0.421, the permission dialog appears when you **submit your first
prompt** in Autopilot mode — not when you switch to it. This means you can
safely cycle to Autopilot mode to inspect it without triggering any
confirmation dialogs.

```
# Switching to Autopilot — no dialog yet
Shift+Tab  Shift+Tab

# Submitting a prompt — dialog appears
You: Fix all failing unit tests in the events module

Autopilot mode: Copilot will work autonomously.
Tool calls will be executed without individual approval.
Continue? [y/N]
```

### Tool Permissions in Autopilot

Even in Autopilot mode, tool permissions are enforced unless you explicitly
opt out:

| Flag | Effect |
|------|--------|
| (default) | Copilot requests tool approval per category |
| `--allow-tool <tool>` | Pre-approve a specific tool |
| `--allow-all` / `--yolo` | Pre-approve all tools (maximum risk) |

```bash
# Pre-approve specific tools
copilot-cli --allow-tool bash --allow-tool edit

# Pre-approve everything (use with caution)
copilot-cli --yolo
```

> ⚠️ The `--yolo` flag disables all safety confirmations. Use it only in
> disposable environments (CI containers, throwaway branches) or when you
> have full confidence in the task scope. **Never** use `--yolo` on
> production code without a safety net like version control.

### "Making Best Guess on Autopilot"

When Copilot encounters an `ask_user` situation in Autopilot mode (a point
where it would normally ask you a question), it auto-responds with its best
guess and continues working. You will see:

```
[Autopilot] Making best guess: Using Express Router pattern for consistency
```

This keeps the workflow unblocked but means Copilot may make assumptions you
would have answered differently. Review the output carefully.

### Terminal Bell Notification

Since v0.0.411, Copilot rings the terminal bell once when an Autopilot task
completes. This is useful when you switch to another terminal or application
while Copilot works:

```
# Most terminals display a visual or audible notification
# Configure your terminal to handle BEL character (\a)
```

> 💡 If you don't hear the bell, check your terminal's notification settings.
> Many terminals support desktop notifications on bell — enable this for the
> best Autopilot experience.

### When to Use Autopilot Mode

| Scenario | Why Autopilot? |
|----------|----------------|
| Well-defined implementation | Task is clear, risk of wrong direction is low |
| Batch operations | Apply the same change across many files |
| CI/CD fix iteration | Fix → test → fix cycle benefits from autonomy |
| Implementing an approved plan | Plan mode already validated the approach |
| Boilerplate generation | Creating repetitive scaffolding code |
| Test writing | Adding tests for existing, well-understood code |

### When NOT to Use Autopilot Mode

| Scenario | Why Not? | Use Instead |
|----------|----------|-------------|
| Unfamiliar codebase | Copilot may make incorrect assumptions | Interactive |
| Destructive operations | Database migrations, file deletions | Interactive |
| Learning Copilot CLI | You miss the educational tool-call feedback | Interactive |
| Vague requirements | "Make it better" gives poor results | Plan → Autopilot |
| Security-sensitive code | Auth, encryption, access control need review | Interactive |

### Detailed Workflow Example: Autopilot for Test Coverage

```
# Step 1: Switch to Autopilot mode
Shift+Tab  Shift+Tab    # Interactive → Plan → Autopilot

# Step 2: Give a well-defined task
You: Write unit tests for src/services/eventService.ts.
     Cover all public methods. Use Jest with describe/it blocks.
     Follow the patterns in the existing test files.
     Target 90%+ line coverage for this file.

# Step 3: Copilot works autonomously
Copilot: [Reading src/services/eventService.ts...]
         [Reading existing test patterns in tests/...]
         [Creating tests/services/eventService.test.ts...]
         [Writing test: describe('EventService')...]
         [Writing test: it('should create event with valid data')...]
         [Writing test: it('should throw NotFound for missing event')...]
         [Running: npx jest tests/services/eventService.test.ts...]
         [Fixing: missing mock for data store...]
         [Re-running tests...]
         [All 14 tests passing ✓]

🔔 # Terminal bell rings

# Step 4: Review the results
You: Show me the test file you created

# Or switch to Interactive for follow-up
Tab    # Autopilot → Interactive (backward cycle)
You: Are there any edge cases we should add?
```

---

## Customize Mode (v1.0.7+)

Customize mode provides a dedicated interface for editing section-level system
prompt configuration. Rather than manually editing instruction files, you can
interactively adjust how Copilot behaves for specific sections of your project.

### How It Works

1. Enter Customize mode via the `/customize` command
2. Copilot presents the current system prompt sections (coding style, tool
   preferences, response format, etc.)
3. You select a section to modify and provide new instructions
4. Changes are applied immediately to the active session
5. Optionally persist changes to your instruction files

### When to Use Customize Mode

| Scenario | Example |
|----------|---------|
| **Adjusting coding style** | "Use tabs instead of spaces for this project" |
| **Setting response preferences** | "Always show file paths relative to project root" |
| **Tool configuration** | "Prefer `npm` over `yarn` for package operations" |
| **Language-specific rules** | "Use strict TypeScript with no `any` types" |

> 💡 Customize mode is **not** part of the `Shift+Tab` cycle. Access it
> exclusively via the `/customize` command.

> 📋 For writing persistent instruction files, see
> [Chapter 7](./07-custom-instructions-and-repository-configuration.md).

---

## Shell Mode

Shell mode lets you run shell commands directly, bypassing Copilot's AI
entirely. It is the fastest way to execute commands you already know.

### How It Works

Prefix any input with `!` to execute it as a shell command:

```
!git status
!npm test
!cat src/routes/events.ts | head -20
```

The command runs in your shell and output is displayed inline. No AI
processing, no tool approval, no conversation context consumed.

### Activating Shell Mode

Since v0.0.410, Shell mode is **not** part of the `Shift+Tab` / `Tab` cycle.
It is accessed exclusively via the `!` prefix:

```
# This is a shell command
!ls -la src/

# This is a prompt to Copilot (even if it looks like a command)
ls -la src/
```

> ⚠️ Without the `!` prefix, Copilot interprets your input as a natural
> language prompt and may attempt to run it as part of a larger workflow.
> Always use `!` for direct shell execution.

### History Navigation with Prefix Filtering

Since v0.0.381, history navigation filters by prefix when you start typing.
This is particularly powerful in Shell mode:

```
# Type a partial command, then press ↑ to find matching history
!git ↑    # Scrolls through only commands starting with "!git"
!npm ↑    # Scrolls through only commands starting with "!npm"
```

| Keystroke | Behavior |
|-----------|----------|
| `↑` (empty input) | Navigate through all history |
| `↑` (after typing) | Navigate through history matching typed prefix |
| `↓` | Navigate forward through filtered history |

### Parallel Execution with Agent Work

Since v0.0.389, shell commands can run in parallel while Copilot processes a
prompt in another mode. This means you can:

1. Submit a prompt to Copilot in Interactive or Autopilot mode
2. While Copilot works, run shell commands with `!`
3. Both execute concurrently

```
# Submit a prompt
You: Analyze the test coverage of the events module

# While Copilot is analyzing... run a shell command
!git log --oneline -10

# Both produce output independently
```

> 💡 This is invaluable during long-running agent tasks — you can continue
> your normal development workflow (checking git status, reading logs, running
> quick tests) without interrupting Copilot.

### History Exclusion

Since v0.0.362, commands run through Shell mode are **excluded** from your
Bash and PowerShell history files. They exist only in Copilot CLI's internal
session history.

This means:

- `!secret-command` does not appear in `~/.bash_history`
- Pressing `↑` in a regular terminal will not reveal shell mode commands
- Copilot CLI's own `↑` history within the session still includes them

> 💡 This is useful for commands involving sensitive values — they stay
> within the Copilot CLI session and do not leak to shell history on disk.

### Detached Process Support

Since v0.0.344, Shell mode supports detached processes that persist after the
Copilot CLI session ends:

```
# Start a server that persists after you exit Copilot CLI
!nohup node server.js &

# Start a background watcher
!npx tsc --watch &
```

Detached processes continue running independently. They are not terminated
when the Copilot CLI session closes.

### Common Shell Mode Uses

| Command Pattern | Purpose |
|-----------------|---------|
| `!git status` | Check working tree state |
| `!git diff --stat` | See changed files summary |
| `!npm test` | Run test suite |
| `!cat file.ts \| head -30` | Quick file peek |
| `!find src -name "*.test.ts"` | Locate test files |
| `!docker ps` | Check running containers |
| `!curl localhost:3000/api/health` | Test API endpoint |
| `!wc -l src/**/*.ts` | Count lines of code |

---

## The `/rewind` Command (v1.0.13)

The `/rewind` command provides a slash-command alternative to the `Esc Esc`
keyboard shortcut for undoing changes. It is available in **all modes** and
reverts the last conversation turn along with any associated file changes.

### Syntax

```
/rewind
```

### Behavior

| Aspect | Details |
|--------|---------|
| **Scope** | Reverts the last conversation turn and all file changes from that turn |
| **Availability** | All modes (Interactive, Plan, Autopilot, Customize, Shell) |
| **Confirmation** | Shows affected files and requires explicit confirmation |
| **Repeatability** | Can be called multiple times to rewind through several turns |

### `/rewind` vs. `Esc Esc`

| Feature | `/rewind` | `Esc Esc` |
|---------|-----------|-----------|
| Trigger | Slash command (typed) | Keyboard shortcut (double-tap) |
| Reverts | Last turn + file changes | File changes to previous snapshot |
| Conversation history | Removes the turn from history | Preserves conversation history |
| Discoverability | Visible in `/help` | Requires knowing the shortcut |

> 💡 Use `/rewind` when you want to completely undo a turn as if it never
> happened. Use `Esc Esc` when you only need to revert file changes but want
> to keep the conversation context.

---

## Mode Comparison Table

The following table provides a comprehensive comparison of all five modes
across every relevant dimension:

| Feature | Interactive | Plan | Autopilot | Customize | Shell |
|---------|------------|------|-----------|-----------|-------|
| **Activation** | Default mode | `Shift+Tab` / `/plan` | `Shift+Tab` | `/customize` | `!` prefix |
| **In Tab cycle** | Yes | Yes | Yes | No | No (since v0.0.410) |
| **AI involvement** | Per-turn | Planning only | Fully autonomous | Configuration | None |
| **Tool approval** | Per use or session-approved | Plan review only | Per use or `--yolo` | N/A | N/A |
| **Steering** | Yes — send messages mid-turn | Yes — edit plan mid-draft | Limited — best guess | Yes — section selection | N/A |
| **Best for** | Learning, careful edits | Complex planning | Batch tasks, CI fixes | Tuning behavior | Quick shell commands |
| **Risk level** | 🟢 Low | 🟢 Low | 🟠 Medium–High | 🟢 Low | 🔵 Varies |
| **Preserves context** | Yes | Yes (plan panel) | Yes | Yes | No (standalone) |
| **Completion signal** | Response appears | Plan presented | Terminal bell 🔔 | Config confirmed | Command output |
| **Parallel commands** | No | No | Yes (with `!`) | No | Yes |
| **History filtered** | Yes | Yes | Yes | Yes | Yes (prefix-based) |

### Choosing the Right Mode — Decision Flowchart

```
Start
  │
  ├─ Do you know exactly what shell command to run?
  │    └─ Yes → Shell Mode (!)
  │
  ├─ Is the task well-defined with clear success criteria?
  │    ├─ Yes, and low risk → Autopilot Mode
  │    └─ Yes, but complex/multi-file → Plan Mode first, then Autopilot
  │
  ├─ Are you exploring or learning?
  │    └─ Yes → Interactive Mode
  │
  └─ Unsure? → Start in Interactive Mode (you can always switch)
```

---

## Real-World Workflow Examples

### Example 1: Bug Fix with Plan Mode

**Scenario:** A user reports that event deletion returns 200 but the event
still appears in list responses. You need to find and fix the bug.

```
# 1. Start in Interactive to understand the bug
You: I have a bug where DELETE /api/events/:id returns 200 success
     but the event is not actually deleted. Help me understand why.

Copilot: [Reads route, service, and store files...]
         The deleteEvent method in eventService.ts calls store.remove()
         but store.remove() has a filter condition that never matches
         because it compares string IDs with numeric IDs.

# 2. Switch to Plan mode for the fix
Shift+Tab    # → Plan mode

You: Fix the event deletion bug. The root cause is ID type mismatch
     in the store layer. Also add a test to prevent regression.

Copilot: [Generates plan...]
Plan:
  1. Fix store.remove() to normalize ID types before comparison
  2. Add type-safe ID handling in eventService.ts
  3. Add test: "deleted event should not appear in list"

[1] ✅ Accept (recommended)

# 3. Accept and implement
You: 1

Shift+Tab    # → Autopilot mode

You: Implement the approved plan for the deletion bug fix.

Copilot: [Edits store.ts, eventService.ts, creates test...]
         [Runs tests... all passing ✓]
🔔
```

### Example 2: Feature Implementation with Autopilot

**Scenario:** You need to add a health check endpoint to the Event API. The
requirements are simple and well-defined.

```
# 1. Switch directly to Autopilot (task is well-defined)
Shift+Tab  Shift+Tab    # → Autopilot

You: Add a GET /api/health endpoint that returns:
     { "status": "ok", "timestamp": "<ISO 8601>", "version": "<from package.json>" }
     Add it as a separate route file following the existing patterns.
     Include a test file.

# 2. Copilot works autonomously
Copilot: [Reading existing route patterns...]
         [Creating src/routes/health.ts...]
         [Registering route in src/app.ts...]
         [Creating tests/routes/health.test.ts...]
         [Running tests...]
         [All tests passing ✓]
🔔

# 3. Quick verification via Shell mode
!curl localhost:3000/api/health 2>/dev/null | jq .
{
  "status": "ok",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "version": "1.0.0"
}
```

### Example 3: Interactive Exploration of Unfamiliar Code

**Scenario:** You've just joined the project and want to understand the Event
API's architecture before making changes.

```
# Stay in Interactive mode (default)

You: Give me an overview of this project's architecture.
     What frameworks does it use? How are files organized?

Copilot: [Reads package.json, tsconfig.json, src/ directory...]
         This is a TypeScript/Express REST API...
         Architecture follows routes → services → store pattern...

You: How does error handling work? Show me the error flow.

Copilot: [Reads middleware/errorHandler.ts, utils/AppError.ts...]
         Errors use a custom AppError class with factory methods...
         The global error handler catches AppError and formats...

You: What's the testing strategy? Show me one test file as example.

Copilot: [Reads test files...]
         Tests use Jest with describe/it blocks...
         Here's the pattern from tests/events.test.ts...

You: Thanks. Now I understand the codebase well enough to contribute.
```

> 💡 Interactive exploration is the safest way to learn a new codebase with
> Copilot. You maintain full control and build understanding incrementally.

### Example 4: Mixed Mode Workflow — Full Feature Lifecycle

**Scenario:** You need to add event search functionality. This involves
planning, implementing, testing, and verifying — a natural use of multiple modes.

```
# Phase 1: Plan (Plan mode)
Shift+Tab    # → Plan mode

You: Add full-text search to the events API. Users should be able to
     search events by title and description via GET /api/events?q=term.
     Support case-insensitive partial matching.

Copilot: [Analyzes codebase, drafts plan...]
Plan:
  1. Add SearchParams interface to models/types.ts
  2. Add search method to eventService.ts with filtering logic
  3. Update GET /api/events route to accept `q` query param
  4. Add search-specific tests
  5. Update API documentation

[1] ✅ Accept
You: 1

# Phase 2: Implement (Autopilot mode)
Shift+Tab    # → Autopilot

You: Implement the search feature from the approved plan.

Copilot: [Working autonomously...]
         [Creates types, service method, route updates, tests...]
🔔

# Phase 3: Verify (Shell mode)
!npm test -- --coverage

# Phase 4: Debug a failing test (Interactive mode)
Tab  Tab    # → Interactive

You: The search test for partial matching is failing. The test expects
     "meet" to match "Team Meeting" but it doesn't. Why?

Copilot: [Reads the search implementation and test...]
         The search uses indexOf which is case-sensitive. The test
         expects case-insensitive matching. Let me fix the service
         to use toLowerCase() before comparison.

# Phase 5: Apply fix (Autopilot mode)
Shift+Tab  Shift+Tab    # → Autopilot

You: Fix the case-insensitive search bug and re-run the tests.

Copilot: [Fixes service, runs tests... all passing ✓]
🔔

# Phase 6: Final verification (Shell mode)
!npm test -- --verbose
!git diff --stat
```

---

## Mode-Specific Tips and Best Practices

### Interactive Mode Tips

> 💡 Start every new project exploration in Interactive mode. Build context
> and understanding before switching to more autonomous modes.

> 💡 Use session-approval (`a` at tool prompts) for read-only tools early in
> your session. This significantly speeds up exploration without risk.

> ⚠️ If Copilot starts heading in the wrong direction, steer it immediately
> with a follow-up message rather than waiting for it to finish.

### Plan Mode Tips

> 💡 Write clear, specific task descriptions. "Add pagination" produces a
> weaker plan than "Add offset-based pagination with page/limit params,
> defaults of page=1 and limit=20, max limit=100, and X-Total-Count header."

> 💡 Use `Ctrl+Y` to edit the plan directly when you want to restructure it
> significantly rather than describing changes conversationally.

> ⚠️ Don't skip the plan review step. A few minutes reviewing the plan saves
> hours of rework from an incorrect implementation.

### Autopilot Mode Tips

> 💡 Autopilot works best immediately after Plan mode — the approved plan
> gives Copilot clear direction and reduces guesswork.

> 💡 Keep your task descriptions atomic. "Fix the login bug" is better than
> "Fix the login bug, add tests, update docs, and refactor the auth module."

> ⚠️ Always review Autopilot's output before committing. Check `git diff`
> to understand every change that was made.

> ⚠️ Watch for "Making best guess" messages — they indicate points where
> Copilot made assumptions. Verify each one.

### Shell Mode Tips

> 💡 Use shell mode for quick verifications between AI-assisted tasks:
> `!git diff`, `!npm test`, `!cat file | grep pattern`.

> 💡 Leverage prefix-filtered history (`!git ↑`) to quickly replay recent
> commands — this is faster than re-typing.

> ⚠️ Remember that shell commands run in Copilot CLI's shell environment.
> Directory context, environment variables, and shell aliases may differ
> from your regular terminal.

---

## Summary

| Mode | One-Sentence Summary |
|------|---------------------|
| **Interactive** | Full control, turn-by-turn — the safe default for any task |
| **Plan** | Think before you code — collaborative planning with AI |
| **Autopilot** | Hands-off execution — let Copilot drive for well-defined tasks |
| **Customize** | Tune Copilot's behavior — section-level system prompt editing |
| **Shell** | Direct command execution — bypass AI when you know the command |

The most effective Copilot CLI users fluidly switch between modes during a
single session, matching the mode to the task at hand. Start with Interactive
to understand, switch to Plan for complex tasks, execute with Autopilot for
well-defined work, and drop into Shell for quick commands.

---

Next: [Chapter 5: Slash Commands Reference](./05-slash-commands-reference.md)
