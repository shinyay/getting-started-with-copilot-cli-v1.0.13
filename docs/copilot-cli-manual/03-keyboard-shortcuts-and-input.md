# Chapter 3: Keyboard Shortcuts & Input

Mastering keyboard shortcuts is the single fastest way to accelerate your
Copilot CLI workflow. This chapter provides an exhaustive reference for every
shortcut, input mechanism, and navigation technique available in the CLI. Each
section groups related shortcuts by context so you can build muscle memory
incrementally — start with the global shortcuts you'll use every session, then
layer in editing, history, and advanced input techniques as your comfort grows.

> 📋 For a condensed, printable version of the most common shortcuts, see
> [Chapter 2: Installation & Configuration](./02-installation-and-configuration.md).
> This chapter is the **complete** reference.

---

## Complete Shortcut Reference

Copilot CLI shortcuts fall into several categories depending on context: global
shortcuts available at any prompt, editing shortcuts for manipulating your input
text, navigation shortcuts for scrolling and history, and context-specific
shortcuts that activate within particular UI states (alt-screen views, pickers,
plan mode). The tables below cover every documented shortcut as of the current
CLI release.

---

## Global Shortcuts

These shortcuts are available whenever the Copilot CLI prompt is active and
waiting for input. They control high-level behavior — switching modes, managing
operations, and accessing special input features.

| Shortcut | Action | Notes |
|----------|--------|-------|
| `@` | Mention files; include their contents in context | Opens autocomplete picker; see [@ File Mentions](#-file-mentions) |
| `#` | Reference GitHub issues, PRs, discussions | Opens GitHub reference picker; since v0.0.420 |
| `!` | Execute shell command directly (bypass Copilot) | Input is passed to your shell verbatim |
| `Ctrl+S` | Run command while preserving input | Useful for iterating on a prompt without retyping |
| `Shift+Tab` | Cycle modes forward | Interactive → Plan → Autopilot (round-robin) |
| `Tab` | Cycle modes backward | Autopilot → Plan → Interactive |
| `Ctrl+T` | Toggle model reasoning display | Persists across sessions; shows chain-of-thought |
| `Ctrl+O` | Expand recent timeline | Only active when input is empty |
| `Ctrl+E` | Expand all timeline | Only active when input is empty; overloaded with editing shortcut |
| `↑` / `↓` | Navigate command history | Prefix-filtered in shell mode (`!`) |
| `Esc` | Cancel the current operation | Single press cancels generation or dismisses UI; clears input if text present (v1.0.7+) |
| `Esc Esc` | Undo / rewind to previous file snapshot | Double-tap; first Esc clears input (with hint), second triggers undo (v1.0.7+); see [Undo / Rewind](#undo--rewind) |
| `Ctrl+C` | Cancel operation / clear input / exit | Press twice quickly to exit the CLI entirely |
| `Ctrl+D` | Shutdown / queue slash commands alongside messages | Sends EOF; can combine `/command` with free text |
| `Ctrl+L` | Clear the screen | Redraws the prompt on a fresh terminal |
| `Ctrl+Z` | Suspend / resume | Unix only; since v0.0.410; use `fg` to resume |
| `Ctrl+R` | Reverse incremental history search | Since v0.0.422; Bash-style interactive search |
| `?` | Quick help overlay | Shows contextual shortcut hints |

> 💡 **Tip:** `Shift+Tab` and `Tab` for mode cycling are the shortcuts you'll
> use most often. Internalizing these eliminates the need for `/plan` and
> `/autopilot` slash commands in most situations.

> ⚠️ **Warning:** `Ctrl+E` is context-dependent. When you have text in the
> input buffer, it moves the cursor to the end of the line. When the input is
> empty, it expands the full timeline. Be aware of this overloaded behavior.

---

## Editing Shortcuts

These shortcuts manipulate text within the Copilot CLI input box. They follow
familiar Emacs/readline conventions that many terminal users already know,
making them intuitive for experienced CLI users.

| Shortcut | Action | Notes |
|----------|--------|-------|
| `Ctrl+A` | Move to beginning of line | Cycles through visual lines in wrapped input |
| `Ctrl+E` | Move to end of line | Active when text is present in input buffer |
| `Ctrl+H` | Delete previous character | Equivalent to `Backspace` |
| `Ctrl+W` | Delete previous word | Deletes back to the previous whitespace boundary |
| `Ctrl+U` | Delete from cursor to beginning of line | Clears everything before the cursor |
| `Ctrl+K` | Delete from cursor to end of line | At end of line, joins with the next line |
| `Meta+←` / `Meta+→` | Move cursor by word | `Meta` is typically `Alt` or `Option` |
| `Ctrl+B` | Move cursor backward one character | Available on all platforms |
| `Ctrl+F` | Move cursor forward one character | Available on all platforms |
| `Ctrl+N` | Move cursor down (next line) | Alternative to `↓` arrow key |
| `Ctrl+P` | Move cursor up (previous line) | Alternative to `↑` arrow key |
| `Ctrl+G` | Edit prompt in external editor / dismiss UI | Opens `$EDITOR`; also dismisses overlays |
| `Ctrl+X Ctrl+E` | Edit prompt in terminal editor | Two-key chord; opens current input in `$EDITOR` |
| `Ctrl+Y` | Edit plan in terminal editor / open research report | In Plan mode: opens editor; if no plan exists, opens latest `/research` report (v1.0.12+) |
| `Home` | Navigate within visual line | In alt-screen: jump to scroll buffer top |
| `End` | Navigate within visual line | In alt-screen: jump to scroll buffer bottom |
| `Ctrl+Home` | Jump to beginning of text | Moves cursor to first character of entire input |
| `Ctrl+End` | Jump to end of text | Moves cursor past last character of entire input |
| `Page Up` | Scroll alt-screen view up | Active in paged output (diffs, long responses) |
| `Page Down` | Scroll alt-screen view down | Active in paged output (diffs, long responses) |
| `Ctrl+F` / `Ctrl+B` | Page down / page up in alt-screen | Overloaded: character movement at prompt, paging in alt-screen |

> 💡 **Tip:** If you're comfortable with Vim keybindings rather than Emacs, use
> `Ctrl+G` or `Ctrl+X Ctrl+E` to open your input in `$EDITOR`. Set
> `EDITOR=vim` in your shell profile and you get full Vim editing for complex
> multi-line prompts.

> ⚠️ **Warning:** `Ctrl+F` and `Ctrl+B` behave differently depending on
> context. At the normal prompt they move the cursor one character. Inside
> alt-screen views (like diff output or long responses), they page down and up
> respectively. This dual behavior can be surprising at first.

### Platform-Specific Editing Notes

| Platform | Behavior Difference |
|----------|-------------------|
| macOS | `Meta` key is `Option`; ensure "Use Option as Meta key" is enabled in your terminal |
| Linux | `Meta` is typically `Alt`; most terminals support this by default |
| Windows | `Meta` shortcuts may require terminal-specific configuration (Windows Terminal recommended) |
| VS Code Terminal | Run `/terminal-setup` first for full shortcut support; some shortcuts conflict with VS Code keybindings |

---

## Multi-Line Input

Copilot CLI supports multi-line input for composing complex prompts. The
mechanism for entering newlines depends on your terminal and configuration.

### Newline Entry Methods

| Method | Terminal Support | Notes |
|--------|-----------------|-------|
| `Shift+Enter` | Kitty protocol terminals | Enabled by default since v0.0.342 |
| `Shift+Enter` | VS Code integrated terminal | Requires `/terminal-setup` first |
| `Ctrl+Enter` | VS Code integrated terminal | Alternative to `Shift+Enter` after setup |
| `Ctrl+G` / `Ctrl+X Ctrl+E` | All terminals | Opens `$EDITOR` for unrestricted multi-line editing |

### Input Box Behavior

- The input box is **scrollable** and limited to approximately **10 visible lines**
- You can type or paste content longer than 10 lines — the box scrolls to
  accommodate, but only ~10 lines are visible at any time
- Line wrapping within the input box follows your terminal width

### Paste Handling

Large pastes receive special treatment to keep the UI manageable:

| Paste Size | Behavior |
|------------|----------|
| ≤ 10 lines | Displayed inline in the input box as-is |
| > 10 lines | Compacted to a summary: `[Paste #1 - 15 lines]` |
| > 30 KB | Auto-saved to a workspace file; referenced by path |

> 💡 **Tip:** When pasting large code blocks for Copilot to analyze, the
> compacted display (`[Paste #1 - 15 lines]`) still sends the full content to
> the model. The compaction is purely visual — no data is lost.

> ⚠️ **Warning:** Content exceeding 30 KB is saved to a file in your workspace
> directory. Be aware that this creates files on disk. Clean up workspace files
> periodically if you frequently paste large content.

### Multi-Line Input Example

Composing a detailed prompt across multiple lines:

```
Shift+Enter to start a new line:

  Refactor the authentication middleware to:
  1. Extract token validation into a separate function
  2. Add rate limiting with a configurable window
  3. Log failed attempts with the client IP
  4. Return proper 401/429 status codes
```

The CLI renders this as a scrollable multi-line input block before sending it
to the model as a single prompt.

---

## History Navigation

Copilot CLI maintains a persistent command history across sessions, similar to
your shell's history. History is saved automatically and restored when you
start a new session.

### Basic History

| Action | Shortcut | Behavior |
|--------|----------|----------|
| Previous command | `↑` | Cycles backward through history |
| Next command | `↓` | Cycles forward through history |
| Search history | `Ctrl+R` | Reverse incremental search (since v0.0.422) |

### Reverse Incremental Search (`Ctrl+R`)

The reverse search works identically to Bash's `Ctrl+R`:

1. Press `Ctrl+R` — the prompt changes to a search indicator
2. Start typing — the most recent matching entry appears
3. Press `Ctrl+R` again to cycle to the next older match
4. Press `Ctrl+J` or `Enter` to **accept** the shown entry
5. Press `Ctrl+G` to **cancel** and return to the original prompt

```
(reverse-i-search)`refac': Refactor the user service to use dependency injection
```

> 💡 **Tip:** Reverse search is invaluable when you remember part of a
> previous prompt but not the whole thing. Type a distinctive keyword and
> `Ctrl+R` will find it across your entire history.

### Shell Mode History Filtering

When using the `!` prefix for shell commands, history navigation gains
**prefix filtering**:

```
Type:  !git
Press: ↑

Cycles through only previous commands starting with "git":
  !git status
  !git diff --staged
  !git log --oneline -10
```

This filtering only applies in shell mode (`!` prefix). At the normal Copilot
prompt, `↑` and `↓` cycle through all history entries regardless of content.

---

## @ File Mentions

The `@` symbol is Copilot CLI's mechanism for explicitly including file
contents in your prompt's context. This is one of the most powerful input
features — it lets you precisely control what the model sees.

### How It Works

1. Type `@` at the prompt
2. Start typing a filename or path fragment
3. An autocomplete picker appears with matching files
4. Use `↑` / `↓` arrows to navigate the picker
5. Press `Tab` or `Enter` to select a file
6. The file's contents are included in the context sent to the model

### Autocomplete Behavior

| Feature | Details |
|---------|---------|
| Search scope | Current working directory and subdirectories |
| Directory support | Directories appear in autocomplete; selecting one shows its contents |
| Real-time state | Always reflects the current filesystem state (including newly created files) |
| CLI-created files | Files created by Copilot CLI during the session are immediately available |
| Image support | Image files are supported; the model receives the image content |
| Multiple mentions | You can `@`-mention multiple files in a single prompt |

### Usage Examples

```
@src/routes/events.ts What validation is missing from the POST endpoint?
```

```
@package.json @tsconfig.json Are there any version conflicts in my config?
```

```
@src/models/event.ts @src/services/eventService.ts
Refactor the service to match the updated model interface
```

> 💡 **Tip:** Mentioning specific files with `@` is almost always better than
> hoping the model will find the right context automatically. When you know
> which files are relevant, mention them explicitly. This reduces hallucination
> and improves response accuracy.

> ⚠️ **Warning:** Each `@`-mentioned file consumes tokens from the model's
> context window. Mentioning very large files (or many files) can exhaust the
> available context, causing the model to truncate or ignore some content.
> Be selective about what you include.

---

## # GitHub Reference Picker

Since v0.0.420, typing `#` opens an interactive picker for GitHub references.
This lets you pull issue descriptions, PR details, and discussion threads
directly into your prompt context without leaving the CLI.

### Supported Reference Types

| Type | Syntax | What Gets Included |
|------|--------|--------------------|
| Issues | `#123` | Issue title, body, labels, and recent comments |
| Pull Requests | `#456` | PR title, description, changed files summary |
| Discussions | `#789` | Discussion title and body |

### Picker Interaction

1. Type `#` — the picker opens showing recent issues and PRs
2. Type a number or search term to filter
3. Use `↑` / `↓` to navigate results
4. Press `Enter` to select and insert the reference

> 💡 **Tip:** Combine `#` references with `@` file mentions for maximum
> context: `@src/auth.ts Fix the bug described in #142` gives the model both
> the code and the bug report.

> 📋 API errors from the GitHub reference picker are now handled gracefully
> (since v0.0.420) — you'll see a clean error message instead of raw HTTP
> response bodies.

---

## Paste & Image Input

Copilot CLI handles pasted content and images intelligently, adapting its
behavior based on the size and type of content.

### Text Paste Behavior

| Scenario | Behavior | Since |
|----------|----------|-------|
| Small paste (≤ 10 lines) | Displayed inline in input box | — |
| Large paste (> 10 lines) | Compacted: `[Paste #1 - N lines]` | — |
| Very large paste (> 30 KB) | Auto-saved to workspace file | — |
| Multi-line paste correctness | Large pastes handled without truncation | v0.0.401 |
| Windows right-click paste | Works correctly | v0.0.421 |

### Image Input

Copilot CLI supports multiple methods for providing image input to vision-
capable models:

| Method | Description | Since |
|--------|-------------|-------|
| Clipboard paste | Paste an image from your clipboard | v0.0.362 |
| Drag and drop | Drag an image file onto the terminal | v0.0.359 |
| `@` file mention | Mention an image file with `@path/to/image.png` | — |

When processing image files, the CLI prioritizes **file contents** over icon
representations (since v0.0.363), ensuring the model receives the actual image
data rather than a filesystem icon.

### Image Input Example

```
@screenshot.png What UI component is shown in this screenshot?
Suggest improvements to the layout.
```

> 💡 **Tip:** Image input is particularly useful for debugging visual issues —
> paste a screenshot of a broken UI and ask Copilot to identify the problem.
> The model can analyze CSS layout issues, visual regressions, and design
> inconsistencies from images.

> ⚠️ **Warning:** Image input requires a vision-capable model. If your
> currently selected model does not support vision, the image data will be
> ignored. Check your model selection with `/model` if image analysis is not
> producing results.

---

## Slash Command Input

Slash commands provide structured operations within Copilot CLI. The input
system includes several features to make discovering and using slash commands
efficient.

### Autocomplete Behavior

| Feature | Details |
|---------|---------|
| Ghost text | Typing `/` shows ghost-text completion suggestions |
| Tab completion | `Tab` cycles through commands matching your typed prefix |
| Substring matching | Autocomplete matches anywhere in the command name, not just the prefix |
| Argument hints | After selecting a command, hints for expected arguments appear in the input box |
| Newline handling | Slash commands work correctly when immediately followed by a newline |

### Slash Command Discovery

```
Type: /
Shows: autocomplete menu with all available commands

Type: /mo
Shows: /model (ghost text completion)

Press: Tab
Completes: /model
Shows: argument hint for model selection
```

### Combining Slash Commands with Messages

You can queue slash commands alongside natural language messages using
`Ctrl+D`:

```
/compact Summarize the current session
```

### Session Search in /resume

When using the `/resume` command to resume a previous session, you can press
`/` within the session picker to switch to search mode. This lets you filter
past sessions by keyword rather than scrolling through a chronological list.

> 💡 **Tip:** If you can't remember the exact slash command name, type `/` and
> a few letters from anywhere in the command name. Substring matching will find
> it — you don't need to remember the exact prefix.

---

## Undo / Rewind

One of Copilot CLI's most valuable safety features is the ability to undo file
changes and rewind to any previous snapshot. This is especially important in
Autopilot mode where the CLI makes changes autonomously.

### How Undo Works

| Feature | Details | Since |
|---------|---------|-------|
| Trigger | `Esc Esc` (double-tap Escape) | v0.0.393 |
| Input clearing | First `Esc` clears input if text present; hint shown after first press | v1.0.7 |
| Scope | Reverts file changes to any previous snapshot | — |
| File count | Shows accurate count of affected files | — |
| Confirmation | Requires explicit confirmation before reverting | v0.0.416 |
| Non-git warning | Displays clear warning when used outside a git repository | — |

### Undo Workflow

1. Copilot CLI makes changes to your files (via edit, create, or shell commands)
2. You notice something is wrong or want to revert
3. Press `Esc Esc` (double-tap Escape quickly)
4. The CLI shows which files would be affected and how many
5. Confirm to revert, or cancel to keep the current state

```
⟲ Rewind: 3 files would be reverted to their previous state
  - src/routes/events.ts
  - src/services/eventService.ts
  - src/middleware/auth.ts

Confirm revert? (y/n)
```

> 💡 **Tip:** The undo system uses **snapshots**, not git. Every time a file is
> modified during a session, the CLI saves the previous state. You can rewind
> through multiple snapshots by pressing `Esc Esc` repeatedly after each
> confirmation.

> ⚠️ **Warning:** In non-git repositories, undo is your **only** safety net.
> The CLI will display a prominent warning reminding you that there is no git
> history to fall back on. Consider initializing a git repository before
> starting significant work, even if you don't plan to push it.

### Undo vs. Git Reset

| Feature | `Esc Esc` Undo | `git checkout` / `git restore` |
|---------|----------------|-------------------------------|
| Scope | Files changed in current CLI session | Any tracked file in the repository |
| Granularity | Per-snapshot (each CLI operation) | Per-commit or working tree |
| Availability | Always (with or without git) | Requires git repository |
| History depth | All snapshots from current session | Full git history |
| New files | Can revert file creation | Untracked files not affected by checkout |

> 📋 For more on how undo interacts with different execution modes, see
> [Chapter 4: Modes of Operation](./04-modes-of-operation.md).

---

## Shortcut Quick Reference Card

For fast lookup, here is every shortcut organized by category in a single
condensed table:

### Navigation & Control

| Shortcut | Action |
|----------|--------|
| `↑` / `↓` | History navigation |
| `Ctrl+R` | Reverse history search |
| `Ctrl+O` | Expand recent timeline |
| `Ctrl+E` | Expand all timeline (empty input) |
| `Ctrl+L` | Clear screen |
| `Ctrl+Z` | Suspend / resume (Unix) |
| `Esc` | Cancel operation |
| `Esc Esc` | Undo / rewind |
| `Ctrl+C` | Cancel / clear / exit |
| `Ctrl+D` | Shutdown / queue commands |
| `?` | Quick help |

### Mode & Display

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Cycle mode forward |
| `Tab` | Cycle mode backward |
| `Ctrl+T` | Toggle reasoning display |
| `Ctrl+S` | Run preserving input |

### Text Editing

| Shortcut | Action |
|----------|--------|
| `Ctrl+A` | Beginning of line |
| `Ctrl+E` | End of line (with input) |
| `Ctrl+B` / `Ctrl+F` | Back / forward one character |
| `Meta+←` / `Meta+→` | Back / forward one word |
| `Ctrl+N` / `Ctrl+P` | Down / up line |
| `Ctrl+H` | Delete previous character |
| `Ctrl+W` | Delete previous word |
| `Ctrl+U` | Delete to line start |
| `Ctrl+K` | Delete to line end |
| `Ctrl+G` | External editor / dismiss |
| `Ctrl+X Ctrl+E` | Terminal editor |
| `Ctrl+Y` | Edit plan in editor |
| `Home` / `End` | Visual line boundaries |
| `Ctrl+Home` / `Ctrl+End` | Text boundaries |
| `Page Up` / `Page Down` | Scroll alt-screen |

### Context Input

| Shortcut | Action |
|----------|--------|
| `@` | File mention picker |
| `#` | GitHub reference picker |
| `!` | Shell command passthrough |
| `/` | Slash command autocomplete |

---

## Troubleshooting Shortcuts

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| `Shift+Enter` doesn't insert newline | Terminal doesn't support Kitty keyboard protocol | Use `Ctrl+G` to open `$EDITOR` instead |
| `Meta+←` / `Meta+→` not working | Terminal sends `Alt` as escape prefix | Enable "Use Option as Meta key" (macOS) or check terminal settings |
| `Ctrl+Z` does nothing | Running on Windows | `Ctrl+Z` suspend/resume is Unix only (since v0.0.410) |
| `Ctrl+S` freezes terminal | Terminal interprets as XOFF flow control | Disable flow control: `stty -ixon` in your shell profile |
| `#` picker shows errors | GitHub authentication issue | Run `gh auth status` to verify your GitHub CLI authentication |
| Shortcuts conflict in VS Code | VS Code intercepts keystrokes | Run `/terminal-setup` to configure VS Code key passthrough |

> 💡 **Tip:** If you're unsure whether a shortcut is working, press `?` at an
> empty prompt to bring up the quick help overlay. This shows all currently
> active shortcuts for your context and terminal.

---

## Building Muscle Memory

Learning all shortcuts at once is overwhelming. Here is a recommended
progression for building muscle memory over time:

### Week 1 — Essential Navigation

Focus on these five shortcuts only:

| Shortcut | Why It Matters |
|----------|---------------|
| `@` | Precise context control is the #1 quality lever |
| `Shift+Tab` | Mode switching without slash commands |
| `↑` | Recall and iterate on previous prompts |
| `Esc` | Cancel when output goes in the wrong direction |
| `Ctrl+C` | Clean exit without confusion |

### Week 2 — Editing Efficiency

Add text manipulation shortcuts:

| Shortcut | Why It Matters |
|----------|---------------|
| `Ctrl+A` / `Ctrl+E` | Jump to line boundaries instantly |
| `Ctrl+W` | Delete a mistyped word without backspacing |
| `Ctrl+U` | Clear the entire line to start over |
| `Ctrl+K` | Remove everything after the cursor |

### Week 3 — Power Features

Layer in advanced capabilities:

| Shortcut | Why It Matters |
|----------|---------------|
| `Ctrl+R` | Find any previous prompt by keyword |
| `#` | Pull GitHub context without switching tools |
| `Esc Esc` | Safety net for autonomous operations |
| `Ctrl+T` | Understand model reasoning when debugging |
| `Ctrl+G` | Full editor for complex multi-line prompts |

---

Next: [Chapter 4: Modes of Operation](./04-modes-of-operation.md)
