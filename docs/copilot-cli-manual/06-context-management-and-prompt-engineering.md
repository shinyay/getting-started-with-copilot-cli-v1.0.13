# Chapter 6: Context Management & Prompt Engineering

Every interaction with Copilot CLI happens inside a **context window** — a finite
budget of tokens that determines what the AI model knows about your project, your
conversation, and your intent. Mastering context management is the single most
impactful skill for getting consistently excellent results from Copilot CLI.

This chapter covers every mechanism Copilot CLI provides for controlling what goes
into that window, how to keep it healthy over long sessions, and how to write
prompts that make the most of every token.

---

## Understanding the Context Window

The context window is the total amount of text — measured in **tokens** — that the
AI model can process in a single interaction. Think of it as the model's working
memory: everything it can "see" at once when generating a response.

### What Is a Token?

A token is roughly ¾ of a word. The word `function` is one token; the word
`concatenation` is broken into multiple tokens. Code tends to consume more tokens
per line than prose because of syntax characters, indentation, and special symbols.

### What Fills the Context Window?

Every request you send to Copilot CLI assembles a context payload from multiple
sources:

| Source | Description | Typical Size |
|--------|-------------|--------------|
| System prompt | Internal instructions that define Copilot's behavior | ~1,000–3,000 tokens |
| Custom instructions | Your `copilot-instructions.md`, `.github/copilot-instructions.md` | ~200–1,000 tokens |
| Conversation history | All previous turns in the current session | Grows over time |
| `@`-mentioned files | Files you explicitly reference in your prompt | ~500–5,000 per file |
| Tool results | Output from bash, grep, file reads, etc. | Varies widely |
| `#`-referenced items | GitHub issues, PRs, discussions pulled in | ~200–2,000 per item |
| MCP sampling responses | LLM inference results requested by MCP servers *(v1.0.13)* | Varies per request |
| Your current prompt | The message you just typed | ~50–500 tokens |

### Why Context Management Matters

- **More relevant context = better answers.** The model produces higher-quality
  output when it has access to the right files, patterns, and history.
- **Irrelevant context = wasted budget.** Including files or history that are not
  related to your current task dilutes the model's attention.
- **Context overflow = truncation.** When the total context exceeds the model's
  limit, older content is silently dropped or aggressively summarized — and you
  lose important details.

> 💡 Think of context like a desk: keep only what you need for the current task
> within arm's reach. Archive everything else.

> ⚠️ Different models have different context limits. Switching models mid-session
> may cause unexpected compaction if the new model has a smaller window.

---

## `@` File Mentions

The `@` symbol is your primary tool for bringing specific file contents into the
context window. When you type `@` followed by a path, Copilot CLI reads that file
and includes its full contents in your prompt.

### Syntax

```
@path/to/file.ts
@relative/path/from/cwd/module.py
@src/routes/events.ts
@package.json
```

Paths are resolved relative to your **current working directory**. You do not need
quotes or backticks around the path.

### Autocomplete

When you type `@` and begin typing a path, Copilot CLI offers interactive
autocomplete:

1. Type `@` to trigger the file picker
2. Start typing the filename or path segment
3. Use **arrow keys** to navigate suggestions
4. Press **Tab** to accept the highlighted suggestion

> 💡 Since v0.0.397, directories appear in autocomplete results. You can
> `@`-mention a directory to include a listing of its contents, giving the model
> structural awareness without loading every file.

> 💡 Since v0.0.422, autocomplete always reflects the current working directory
> state — including files recently created or moved during your session.

### Files Created by the CLI

Files that Copilot CLI creates during your session (via tool calls or code
generation) are immediately available for `@`-mention without restarting the
session (since v0.0.384). This enables workflows like:

```
Create a new utility module for date formatting
```

Then immediately:

```
@src/utils/dateFormatter.ts — add unit tests for this module
```

### Image File Support

You can `@`-mention image files (PNG, JPEG, GIF, WebP). The image content is
sent to the model as a visual input, allowing the model to analyze screenshots,
diagrams, mockups, or error captures:

```
@docs/wireframe.png — implement this layout using Tailwind CSS
```

> ⚠️ Image tokens are more expensive than text tokens. A single image can
> consume 1,000–3,000 tokens depending on resolution. Use images purposefully.

### Multiple `@`-Mentions

You can include multiple files in a single prompt:

```
@src/routes/events.ts @src/services/eventService.ts — refactor the
event creation flow to validate dates before saving
```

### Best Practices for `@`-Mentions

| Practice | Why |
|----------|-----|
| Be specific — mention exact files | Avoids loading unnecessary content |
| Prefer small, focused files | Large files consume thousands of tokens |
| Use directory mentions for structure | Shows layout without loading all code |
| Mention test files alongside source | Helps model match patterns and naming |
| Avoid `@`-mentioning generated files | `dist/`, `node_modules/` waste context |

> 📋 For managing which files are visible to Copilot, also see
> [Chapter 7: Custom Instructions & Configuration](./07-custom-instructions-and-configuration.md).

---

## `#` GitHub Reference Picker

Since v0.0.420, typing `#` in your prompt opens a **GitHub reference picker**
that lets you browse and select issues, pull requests, and discussions from your
repository.

### How It Works

1. Type `#` to trigger the reference picker
2. A search interface appears showing recent issues and PRs
3. Type keywords to filter results
4. Select an item to include its title, body, labels, and comments in your context

### Use Cases

```
#42 — summarize this issue and suggest an implementation approach
```

```
Fix the bug described in #108, following the pattern established in #95
```

The `#` picker pulls in structured data from the GitHub API, giving the model
rich context about requirements, discussion history, and related changes.

> 💡 Since v0.0.421, API errors from the GitHub reference picker are handled
> gracefully — if the lookup fails (e.g., rate limiting, network issues), you
> get a clear error message instead of a crash.

> ⚠️ Each referenced issue or PR adds tokens to your context. A long issue
> thread with many comments can consume 2,000+ tokens. Be selective about
> which references you include.

---

## `/context` Command

The `/context` command provides a **visual overview** of your current token
usage (since v0.0.372). It shows how much of your context budget is consumed
and how much space remains.

### Usage

```
/context
```

### What It Shows

```
Context usage: ████████████░░░░░░░░ 62% (78,400 / 128,000 tokens)

  System prompt:         2,100 tokens  ( 1.6%)
  Custom instructions:     840 tokens  ( 0.7%)
  Conversation history: 61,200 tokens  (47.8%)
  File contents:        12,400 tokens  ( 9.7%)
  Tool results:          1,860 tokens  ( 1.5%)
```

### When to Check Context

| Situation | Action |
|-----------|--------|
| Session has been running for 30+ minutes | Run `/context` to check utilization |
| Model responses seem to lose earlier context | Check if you are near the limit |
| About to `@`-mention a large file | Verify there is room in the budget |
| Planning to include multiple `#` references | Check remaining capacity first |
| Responses suddenly become less accurate | Context overflow may have triggered truncation |

> 💡 Make `/context` a habit at the start of complex tasks. Knowing your budget
> helps you decide whether to compact first or proceed.

---

## Auto-Compaction

When your context reaches **95% of the model's token limit**, Copilot CLI
automatically triggers compaction (since v0.0.374). This process summarizes older
conversation history to free up space while preserving essential information.

### How Auto-Compaction Works

1. Context usage crosses the 95% threshold
2. Copilot CLI begins compaction **in the background** — your conversation is not
   blocked (since v0.0.380)
3. Older conversation turns are replaced with a condensed summary
4. A **checkpoint summary** is created, capturing the key state at that point
5. The compacted context is used for subsequent interactions

### What Auto-Compaction Preserves

Auto-compaction is not a blunt truncation. The algorithm specifically preserves:

| Preserved Element | Since | Why It Matters |
|-------------------|-------|----------------|
| Tool call sequences | v0.0.386 | Maintains the history of commands run and their outputs |
| Extended thinking | v0.0.390 | Reasoning chains are not lost during summarization |
| Skills effectiveness | v0.0.399 | Custom skill context is retained accurately |
| Essential context summary | — | Key decisions, file states, and goals survive compaction |

### Compaction Status

Since v0.0.393, compaction events are shown as **timeline messages** in your
session — you can see when compaction happened and what checkpoint was created:

```
── Context compacted (checkpoint #3) ─────────────────────
   Summarized 47 turns into checkpoint summary.
   Context usage: 42% (53,760 / 128,000 tokens)
```

> ⚠️ While auto-compaction preserves key context, very specific details from
> early in a session (like exact variable names discussed 50 turns ago) may be
> lost. If certain details are critical, re-state them in your prompt or use
> `@`-mentions to bring the relevant file back into context.

---

## `/compact` Manual Compaction

You do not have to wait for the 95% threshold. The `/compact` command lets you
manually trigger compaction at any time.

### Usage

```
/compact
```

### When to Use Manual Compaction

- **Before switching tasks** — compact the context from Task A before starting
  Task B to give the model a clean slate
- **After a long debugging session** — remove the noise of failed attempts and
  keep only the resolution
- **Before a complex operation** — free up context space before a multi-step
  plan or large code generation

### Interaction During Compaction

| Feature | Since | Behavior |
|---------|-------|----------|
| Cancel with Esc | v0.0.385 | Press Esc to abort compaction if started accidentally |
| Auto-queued messages | v0.0.389 | Messages you type during compaction are queued and sent after completion |
| Checkpoint summary hints | v0.0.399 | Clearer hints on how to view checkpoint summaries after compaction |

> 💡 You can type your next prompt while compaction is running. It will be
> queued and processed as soon as compaction finishes — no need to wait.

### preCompact Hook

Since v1.0.5, the **`preCompact`** hook fires before context compaction begins —
whether triggered automatically at the 95% threshold or manually via `/compact`.
Use this hook to save summaries, archive context to external storage, or log the
pre-compaction state before older turns are condensed.

| Hook | Trigger | Since | Use Case |
|------|---------|-------|----------|
| `preCompact` | Before compaction starts | v1.0.5 | Save summaries, archive context, log state |

---

## Infinite Sessions

Since v0.0.385, Copilot CLI supports **infinite sessions** — sessions that can
run indefinitely without hitting a hard context limit. This is made possible by
the compaction checkpoint system.

### How Infinite Sessions Work

1. You start a session and work through multiple tasks
2. As context grows, auto-compaction creates checkpoints at regular intervals
3. Each checkpoint summarizes the preceding conversation segment
4. The active context always contains the most recent turns plus checkpoint
   summaries, keeping total usage within the model's window

### Performance

- **Faster session loads** — sessions with large conversation history load
  more efficiently (since v0.0.380)
- **SDK support** — the underlying SDK manages infinite sessions with
  auto-compaction natively (since v0.0.394)

### Best Practices for Long Sessions

| Practice | Benefit |
|----------|---------|
| Run `/compact` when switching tasks | Separates concerns cleanly in checkpoints |
| Re-state important context periodically | Ensures critical details survive compaction |
| Use `@`-mentions instead of relying on memory | Files are always fresh; history may be summarized |
| Check `/context` before complex operations | Verify you have room for the task |
| Start a new session for unrelated work | Avoids cross-contamination of context |

> 💡 Infinite sessions are powerful for long coding sessions, but a fresh
> session is still preferable when your task is completely unrelated to the
> previous conversation.

---

## Extended Thinking & Reasoning

Copilot CLI can show the model's internal reasoning process, giving you
visibility into **how** it arrives at its answers — not just the final output.

### Toggling Reasoning Display

| Action | Shortcut | Since | Notes |
|--------|----------|-------|-------|
| Toggle reasoning on/off | **Ctrl+T** | v0.0.384 | Setting persists across sessions |

When enabled, you see a collapsible "Thinking…" section before the model's
response, showing its chain-of-thought reasoning.

### Model-Specific Behavior

| Model Family | Behavior | Since |
|--------------|----------|-------|
| Anthropic Claude | Full extended thinking with reasoning blocks | v0.0.384 |
| GPT models | Heading content from reasoning displayed | v0.0.413 |
| GPT models | Configurable reasoning effort level | v0.0.384 |
| All supporting models | Reasoning summaries enabled by default | v0.0.403 |

> 💡 Extended thinking is especially valuable for complex debugging,
> architecture decisions, and security reviews. Enable it when you want to
> understand and verify the model's logic.

> ⚠️ Extended thinking adds tokens to the context. For simple tasks (renaming
> variables, formatting code), disabling it saves context budget.

### Fixed Issues

- Since v0.0.375: responses with reasoning no longer cause duplicate messages
  in the conversation history

---

## Image Support

Copilot CLI supports visual input through multiple methods, allowing the model
to analyze images alongside your text prompts.

### Input Methods

| Method | How | Since |
|--------|-----|-------|
| `@`-mention | `@screenshot.png` in your prompt | v0.0.333 |
| Drag and drop | Drag image file onto the CLI window | v0.0.359 |
| Clipboard paste | Copy image, then paste into CLI | v0.0.362 |

### Behavior Details

| Feature | Since | Description |
|---------|-------|-------------|
| File content priority | v0.0.363 | Pasting image data prioritizes file contents over OS icon data |
| Sub-agent processing | v0.0.376 | Task tool sub-agents can view and analyze images |
| SVG as text | v0.0.375 | SVG files are treated as text (XML source), not rasterized images |

### Use Cases for Image Input

```
@error-screenshot.png — what does this error mean and how do I fix it?
```

```
@ui-mockup.png — create React components that match this design
```

```
@architecture-diagram.png — explain the data flow in this system
```

> 💡 For SVG files, `@`-mentioning them gives the model access to the raw XML
> markup, which is often more useful than a rendered image — the model can read
> and modify the SVG source directly.

> ⚠️ Image resolution affects token consumption. Resize large screenshots before
> including them if context budget is tight.

---

## Steering the Agent

Copilot CLI is not a one-shot tool — you can actively steer its behavior during
execution, redirect its approach, and provide real-time feedback.

### Sending Messages While Copilot Is Thinking

Since v0.0.380, you can type and send messages while Copilot is actively
generating a response or executing tool calls. These messages are queued and
influence the model's next action.

**Example workflow:**

1. You ask: `Refactor the auth module to use JWT`
2. Copilot begins working — reading files, planning changes
3. You notice it is heading toward a pattern you don't want
4. You type: `Use RS256 algorithm, not HS256` (sent while Copilot is working)
5. Copilot adjusts its approach based on your steering message

### Queue Management

| Feature | Shortcut | Since | Description |
|---------|----------|-------|-------------|
| Queue messages | (just type) | v0.0.380 | Messages sent during processing are queued |
| Queue slash commands | **Ctrl+D** | v0.0.394 | Queue a slash command to run after current operation |
| Steering in plan mode | — | v0.0.390 | Provide feedback during plan generation |

### Aborting Operations

Press **Esc** at any time to abort the current operation. This stops tool
execution and returns control to you. Useful when:

- The model is going down a wrong path
- A tool call is taking too long
- You want to rephrase your request

### Inline Feedback on Tool Permissions

Since v0.0.380, when you **reject a tool permission** (e.g., denying a file
edit), you can type an inline explanation of why. This feedback is included in
the context, helping the model adjust its approach:

```
[Deny] — Don't modify that file, it's auto-generated. Edit the template instead.
```

> 💡 Steering is most effective when you are specific. Instead of "no, do it
> differently," say "use the factory pattern instead of the builder pattern."

---

## Paste Handling

Copilot CLI intelligently handles large pastes to keep your conversation
readable and your context budget under control.

### Compact Display for Large Pastes

Since v0.0.334, pasting more than **10 lines** of text triggers a compact
display:

```
You: Here's the error log:
[Paste #1 - 47 lines]

What's causing this crash?
```

The full content is still sent to the model — only the display is collapsed.

### Auto-Save for Very Large Pastes

Since v0.0.397, content exceeding **30 KB** is automatically saved to a
workspace file instead of being inlined in the conversation:

```
You: Analyze this data:
[Paste #2 - saved to .copilot/workspace/paste-2.txt (142 KB)]
```

The model receives a reference to the file and can read it using tool calls.

### Platform-Specific Fixes

| Platform | Fix | Since |
|----------|-----|-------|
| Windows | Right-click paste works correctly | v0.0.421 |
| All platforms | Large multi-line pastes work correctly | v0.0.401 |

---

## Prompt Engineering Best Practices

The quality of Copilot CLI's output is directly proportional to the quality of
your input. Here are field-tested techniques for writing effective prompts.

### The Anatomy of a Great Prompt

A well-structured prompt typically includes:

1. **Context** — what system/module/file you are working with
2. **Intent** — what you want to accomplish
3. **Constraints** — boundaries, patterns to follow, things to avoid
4. **Expected behavior** — what the result should look like

### Good vs Bad Prompts

| ❌ Bad Prompt | ✅ Good Prompt | Why It's Better |
|--------------|---------------|-----------------|
| `fix the bug` | `@src/services/eventService.ts — the createEvent function throws a TypeError when the date field is missing. Add validation to return a 400 error instead.` | Specifies the file, function, symptom, and desired fix |
| `write tests` | `@src/routes/events.ts — write Jest unit tests for the GET /events endpoint, covering: empty list, single event, pagination, and invalid query params. Follow the pattern in @src/routes/__tests__/health.test.ts.` | Names the target, specifies scenarios, and references a pattern file |
| `refactor this` | `@src/middleware/auth.ts — extract the token validation logic into a separate validateToken utility function in @src/utils/. Keep the middleware thin — it should only call the utility and handle the HTTP response.` | Describes the refactoring goal, target location, and design intent |
| `make it faster` | `@src/services/searchService.ts — the findEvents function scans all events on every call. Add an in-memory index by date to make date-range queries O(1) lookup instead of O(n) scan.` | Identifies the bottleneck and specifies the optimization strategy |
| `add error handling` | `@src/routes/events.ts — wrap the POST handler in try/catch. Use AppError.badRequest() for validation failures and AppError.notFound() for missing resources. Follow the error pattern in @src/middleware/errorHandler.ts.` | Names the error classes, specifies which errors to handle, references the pattern |

### Prompt Patterns That Work

**The "Follow the Pattern" prompt:**
```
@src/routes/events.ts @src/routes/users.ts — create a new route file
for /api/v1/venues following the same patterns used in the events and
users routes. Include CRUD endpoints with validation middleware.
```

**The "Explain Then Fix" prompt:**
```
@src/services/eventService.ts — first explain what the updateEvent
function does step by step, then fix the bug where updating a recurring
event only modifies the first occurrence.
```

**The "Constrained Generation" prompt:**
```
Create a date utility module at src/utils/dateHelpers.ts. Requirements:
- Use only the built-in Date API (no external libraries)
- Export functions for: parseISO, formatISO, isInRange, addDays
- Include JSDoc comments with @param and @returns tags
- Follow the TypeScript strict mode conventions in tsconfig.json
```

**The "Compare and Decide" prompt:**
```
@src/services/cacheService.ts — I need to add TTL-based expiration.
Compare two approaches: (1) setTimeout per entry vs (2) periodic
sweep of a sorted expiry list. Recommend which is better for our
use case of ~1000 cached items with 5-minute TTLs.
```

> 💡 The more specific your prompt, the less the model needs to guess — and
> guessing is where most errors originate.

> ⚠️ Avoid prompt anti-patterns: "Do everything," "Make it perfect," or "Fix
> all bugs." These give the model no direction and produce unfocused results.

---

## Context Budget Tips

Understanding the token cost of different content types helps you make informed
decisions about what to include in your context.

### Approximate Token Costs

| Content Type | Approximate Tokens | Notes |
|--------------|--------------------|-------|
| Average source file (100 lines) | ~500–1,000 | Varies by language verbosity |
| Large source file (500 lines) | ~2,500–5,000 | Consider mentioning specific sections |
| Very large file (1,000+ lines) | ~5,000–15,000 | Avoid `@`-mentioning; use grep first |
| Image (screenshot/diagram) | ~1,000–3,000 | Resolution-dependent |
| Single conversation turn | ~100–500 | Both your message and the response |
| Long conversation turn (with code) | ~500–2,000 | Code-heavy responses cost more |
| Custom instructions file | ~200–1,000 | Loaded automatically every turn |
| GitHub issue (short) | ~200–500 | Title + body + labels |
| GitHub issue (long thread) | ~1,000–3,000 | Multiple comments add up quickly |
| Tool result (file read) | ~500–5,000 | Depends on file size |
| Tool result (bash output) | ~100–2,000 | Long outputs are truncated by the CLI |

> 💡 Since v1.0.12, the CLI is resilient to extremely long shell command output —
> previously, very large outputs could cause crashes. Long results are now safely
> truncated and the session continues without interruption.

### Budget Management Strategies

| Strategy | When to Use | How |
|----------|-------------|-----|
| **Selective `@`-mentions** | Always | Only include files directly relevant to your task |
| **Manual compaction** | Before switching tasks | Run `/compact` to clean up old context |
| **Fresh sessions** | For unrelated work | Start a new session with `copilot` instead of reusing |
| **Grep before reading** | Looking for specific code | Ask Copilot to grep for a pattern instead of loading entire files |
| **Checkpoint reviews** | After compaction | Review summaries to ensure critical info was preserved |
| **Smaller images** | Including screenshots | Resize or crop images to show only the relevant area |
| **Specific line references** | Large files | Reference functions by name instead of loading entire files |

### The 80/20 Rule of Context

In most tasks, **80% of the useful context comes from 20% of the files.** Before
loading your entire `src/` directory, ask yourself:

1. Which 2–3 files are directly involved in this change?
2. Is there a pattern file the model should follow?
3. What type definitions or interfaces constrain the implementation?

Start with these, and add more only if the model's output shows it needs
additional context.

> 💡 Run `/context` before and after adding files to see the impact on your
> token budget. This builds intuition about costs over time.

> 💡 If the model produces incorrect output that references "missing" context,
> add the specific file it needs rather than adding everything.

> ⚠️ Custom instructions (`copilot-instructions.md`) are loaded on **every
> turn**. Keep them concise — a 1,000-token instruction file costs 1,000 tokens
> per interaction, not just once.

---

## Quick Reference: Context Management Commands & Shortcuts

| Command / Shortcut | Purpose | Section |
|---------------------|---------|---------|
| `@path/to/file` | Include file contents in prompt | [@ File Mentions](#-file-mentions) |
| `#` | Browse and include GitHub issues/PRs | [# GitHub Reference Picker](#-github-reference-picker) |
| `/context` | Show current token usage | [/context Command](#context-command) |
| `/compact` | Manually trigger compaction | [/compact Manual Compaction](#compact-manual-compaction) |
| **Ctrl+T** | Toggle reasoning display | [Extended Thinking](#extended-thinking--reasoning) |
| **Esc** | Abort current operation / cancel compaction | [Steering the Agent](#steering-the-agent) |
| **Ctrl+D** | Queue a slash command | [Steering the Agent](#steering-the-agent) |

---

> 📋 This chapter covered how context flows into and out of the model's working
> memory. The next chapter builds on this foundation by showing how to **pre-load
> context automatically** through custom instructions, workspace configuration,
> and instruction layering.

**Next: [Chapter 7: Custom Instructions & Configuration](./07-custom-instructions-and-configuration.md)**
