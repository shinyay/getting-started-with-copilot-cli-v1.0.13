# Chapter 2: Core Interface & Terminal UI

GitHub Copilot CLI presents a rich, purpose-built terminal user interface that
goes far beyond a simple read-eval-print loop. Every element — from the branded
header to the responsive status bar — is designed to keep you oriented while an
autonomous agent reads, writes, and executes code on your behalf. This chapter
dissects every visual component, interaction mode, and display feature so you
can navigate the interface with confidence and customize it to your workflow.

> 📋 This chapter covers the **visual interface and display behavior**. For
> keyboard shortcuts and text-input mechanics, see
> [Chapter 3: Keyboard Shortcuts & Input](./03-keyboard-shortcuts-and-input.md).

---

## Anatomy of the CLI Interface

The Copilot CLI interface is divided into four distinct regions, stacked
vertically in your terminal window:

```
┌──────────────────────────────────────────────────────────┐
│  ◐  GitHub Copilot                        (Header)       │
│  Welcome! Type your prompt or use ? for help.            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  > User message                           (Timeline)     │
│  ● bash  echo "hello"                                    │
│  Agent response with markdown...                         │
│  ● edit  src/app.ts  (+3 -1)                             │
│  ...                                                     │
│                                                          │
├──────────────────────────────────────────────────────────┤
│  ~/project (main) · claude-sonnet-4 · MCP: 2  (Status)  │
├──────────────────────────────────────────────────────────┤
│  >  _                                     (Prompt)       │
└──────────────────────────────────────────────────────────┘
```

| Region | Position | Purpose |
|--------|----------|---------|
| **Header** | Top | Branded mascot, welcome message, session greeting |
| **Timeline** | Center (scrollable) | Chronological record of all interactions |
| **Status Bar** | Below timeline | CWD, git branch, model, MCP connections, PR link |
| **Prompt Area** | Bottom | Text input, shows current model and working directory |

### Header

The header displays the GitHub Copilot mascot (the `◐` or Copilot logo glyph)
alongside a welcome message. In **v0.0.388** the header was redesigned: the
previous multi-line ASCII banner was replaced with a compact, single-line
branded header that wastes less vertical space while remaining instantly
recognizable. The welcome message now reads as a concise prompt hint rather
than a paragraph of instructions.

### Prompt Area

The prompt area lives at the very bottom of the screen. It is where you type
messages, slash commands, and `@`-mentions. The prompt itself shows:

- A `>` caret indicating you are in input mode.
- The **current working directory** (abbreviated if the terminal is narrow).
- The **active model name** when you start typing.

Multi-line input is supported: press `Shift+Enter` (or `Ctrl+J`) to insert a
newline without submitting. The prompt area expands upward to accommodate
multiple lines, pushing the timeline content up.

### Status Bar

The status bar is a dense, information-rich strip that provides at-a-glance
context. Its full anatomy is covered in the [Status Bar Details](#status-bar-details)
section below.

### Timeline

The timeline is the heart of the interface — a scrollable, chronological log of
everything that happens during your session. It is covered in depth in the next
section.

---

## Timeline

The timeline displays every interaction between you, the agent, and the tools
it invokes. Each entry is visually distinct so you can scan a long session
without losing track of what happened.

### What Appears in the Timeline

| Entry Type | Visual Indicator | Content |
|------------|-----------------|---------|
| **User message** | `>` prefix, distinct foreground color | Your typed prompt, verbatim |
| **Agent response** | Rendered markdown (bold, lists, code) | The model's textual answer |
| **Tool call** | Icon prefix + tool name | Tool name, arguments summary, and result |
| **File edit** | `edit` tool label, `(+N -M)` diff stat | File path; expandable inline diff |
| **Shell output** | `bash` tool label | Command executed; stdout/stderr when expanded |
| **Subagent entry** | **BOLD CAPS** name | Agent type, description, and nested timeline |
| **Compaction entry** | Simplified summary line | Indicates conversation was compacted |

### Tool Call Icons

Tool calls use circle icons to communicate status at a glance:

| Icon | Meaning |
|------|---------|
| `●` (filled circle) | Tool call **completed successfully** |
| `○` (empty circle) | Tool call **in progress** (still running) |
| `●` (red/error color) | Tool call **failed** (error occurred) |

When a tool call finishes, the empty circle fills in and the result appears
beneath it. For long-running commands like builds or test suites, watching the
circle transition from empty to filled gives you a clear heartbeat of progress.

### Expanding and Collapsing Entries

By default, completed tool calls are collapsed to a single summary line to
keep the timeline compact. You can expand them to see full details:

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Expand the **most recent** collapsed tool call or response |
| `Ctrl+E` | Expand **all** collapsed entries in the timeline |

> 💡 Use `Ctrl+O` repeatedly to progressively reveal recent tool calls one at
> a time — useful when you only care about the last few operations.

When expanded:

- **`edit` tool** entries show a full inline diff with added lines (`+`) and
  removed lines (`-`), colored green and red respectively. Since **v1.0.12**,
  individual changed characters within a line are highlighted (intra-line diff
  highlighting), making it easy to spot exactly what changed in long lines.
  This lets you review every change the agent made without leaving the CLI.
- **`bash` tool** entries show the full command, stdout, and stderr.
- **`read_agent`** and other agent-coordination tools show the content returned
  by the subagent, including any structured output.

### Subagent Entries

When Copilot CLI delegates work to a subagent (e.g., an `explore` agent or a
`task` agent), the timeline shows a distinct subagent block:

```
  ■ EXPLORE — Investigating authentication flow
    ● grep  "authMiddleware" src/**/*.ts
    ● view  src/middleware/auth.ts
    Result: The auth middleware validates JWT tokens...
```

Subagent names appear in **BOLD CAPITALIZED** text, followed by the agent type
and a brief description of the delegated task. The subagent's own tool calls
are nested and indented beneath the header, so you can trace exactly what it
did without confusing its actions with the main agent's work.

### Compaction Entries

When the conversation history grows long enough to approach the model's context
window limit, Copilot CLI automatically compacts older messages into a summary.
The timeline shows a simplified compaction entry — a single line indicating that
earlier conversation was summarized. This replaced the previously verbose
compaction blocks to reduce visual noise.

> ⚠️ Compaction is lossy. If you need to refer back to exact earlier prompts
> or outputs, scroll up before compaction occurs, or use `Ctrl+E` to expand
> any remaining collapsed entries.

---

## Alt-Screen Mode

Alt-screen mode transforms Copilot CLI from a conventional terminal program
into a full-screen terminal user interface (TUI) with dedicated viewport
management, mouse support, and optimized rendering.

### History and Availability

| Version | Milestone |
|---------|-----------|
| **v0.0.407** | Alt-screen mode introduced as an experimental feature |
| **v0.0.408** | Mouse text selection added within alt-screen |
| **v0.0.413** | Enabled by default when using the `--experimental` flag |

### Enabling and Disabling

```bash
# Explicitly enable alt-screen
copilot-cli --alt-screen on

# Explicitly disable alt-screen
copilot-cli --alt-screen off

# Enabled automatically with --experimental (since v0.0.413)
copilot-cli --experimental
```

The `--alt-screen` flag accepts `on` or `off` as values. When enabled, Copilot
CLI switches the terminal into its **alternate screen buffer** — the same
mechanism used by editors like `vim` and pagers like `less`. This means:

- The CLI gets a **full-screen canvas** independent of your scrollback history.
- When you exit, your previous terminal content is **restored cleanly** — no
  session replay floods your scrollback.
- The terminal's native scrollback buffer is not consumed.

### Benefits

| Benefit | Description |
|---------|-------------|
| **Full-screen TUI** | Dedicated viewport; no interference with shell scrollback |
| **Mouse support** | Click, drag-select, scroll wheel — all work natively |
| **Better scrolling** | Page Up / Page Down move through the timeline by pages |
| **Clean exit** | Exiting does not replay the full session into scrollback |
| **Memory optimization** | Long sessions use less memory via viewport-based rendering |

### Keyboard Scrolling

In alt-screen mode, the terminal's native scroll does not apply. Instead, use
dedicated keys:

| Key | Action |
|-----|--------|
| `Page Up` | Scroll the timeline up by one page |
| `Page Down` | Scroll the timeline down by one page |
| `Home` | Jump to the top of the timeline |
| `End` | Jump to the bottom of the timeline |

### Mouse Text Selection

Since **v0.0.408**, alt-screen mode supports rich mouse text selection:

| Action | Result |
|--------|--------|
| **Click and drag** | Select a range of text |
| **Double-click** | Select the word under the cursor |
| **Triple-click** | Select the entire line |
| **Drag to viewport edge** | Auto-scrolls the viewport while extending selection |

To copy selected text:

| Method | How |
|--------|-----|
| `Ctrl+Insert` | Copy selection to system clipboard |
| `copy_on_select` config | Automatically copies to clipboard on selection |

On Linux, selected text is also placed in the **primary selection buffer**,
enabling middle-click paste in other applications — matching standard X11/Wayland
behavior.

> 💡 If you use a terminal multiplexer (tmux, screen), you may need to hold
> `Shift` while clicking to let mouse events pass through to Copilot CLI
> rather than being intercepted by the multiplexer.

### Permission Prompts in Alt-Screen

When the agent requests permission to run a tool (e.g., execute a shell
command), the permission prompt is displayed within the alt-screen viewport.
For prompts that include long command strings or multiple items, the prompt
itself becomes **scrollable** so you can review the full request before
approving or denying.

### Memory Optimizations

Alt-screen mode uses **viewport-based rendering**: only the visible portion of
the timeline is rendered to the terminal at any given time. In long sessions
with hundreds of tool calls, this dramatically reduces memory usage and
improves rendering performance compared to classic scrollback mode, which must
maintain the entire rendered history in the terminal's buffer.

### Exit Behavior

When you exit Copilot CLI in alt-screen mode, the alternate screen buffer is
discarded and your original terminal content is restored. The full session
history is **not replayed** into your scrollback. This keeps your terminal
clean but means you cannot scroll up in your shell to review the session after
exiting.

> 📋 To preserve session history, use `/history` before exiting, or rely on
> the `--continue` flag to resume a previous session.

---

## Classic Scrollback Mode

Classic scrollback mode is the **default** rendering mode when alt-screen is
not enabled (i.e., when running without `--experimental` or with
`--alt-screen off`).

### How It Works

In classic mode, Copilot CLI writes directly to the terminal's standard output
stream, and all content accumulates in the terminal emulator's native
**scrollback buffer**. This means:

- You scroll using your **terminal's own scroll mechanism** (scroll wheel,
  `Shift+Page Up`, or terminal-specific shortcuts).
- When you exit, the full session remains visible in your scrollback history.
- Mouse support is limited to what your terminal natively provides.

### Timeline Expansion

The same expansion shortcuts work in classic mode:

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Expand the most recent collapsed entry |
| `Ctrl+E` | Expand all collapsed entries |

> 💡 Classic mode is a good choice if you prefer to review session history
> after exiting, or if your terminal does not support the alternate screen
> buffer well.

---

## Status Bar Details

The status bar is a single-line (or two-line on narrow terminals) information
strip displayed between the timeline and the prompt. It packs a surprising
amount of context into a small space.

### Status Bar Elements

| Element | Position | Description | Since |
|---------|----------|-------------|-------|
| **CWD** | Left | Current working directory, middle-truncated on narrow terminals | Launch |
| **Git branch** | After CWD | Active branch name (e.g., `main`, `feature/auth`) | Launch |
| **Model name** | Center-right | Currently active model (e.g., `claude-sonnet-4`) | Launch |
| **PR link** | After model | Clickable pull request reference (e.g., `PR #42`) | v0.0.421 |
| **MCP indicator** | Right | Count of connected MCP servers (e.g., `MCP: 2`) | Launch |
| **IDE indicator** | Right | Shows connected IDE file selection | When connected |

### CWD with Middle-Truncation

When the terminal is too narrow to display the full working directory path,
the status bar uses **middle-truncation** rather than right-truncation:

```
Full:       /home/user/projects/my-awesome-app/src/components
Truncated:  /home/user/…/src/components
```

This preserves both the root context and the immediate directory, which are
typically more informative than the middle segments.

### Clickable PR Reference

Since **v0.0.421**, when you create a pull request using Copilot CLI (e.g., via
`/pr` or the `gh` tool), the status bar displays a clickable PR reference. In
terminals that support OSC 8 hyperlinks, clicking the reference opens the PR
directly in your browser.

### MCP Server Connection Count

The MCP indicator shows how many Model Context Protocol servers are currently
connected. This is essential when you've configured custom MCP servers for
database access, API integration, or other external tools:

```
MCP: 0    No MCP servers connected
MCP: 2    Two MCP servers active and available
```

### IDE File Selection Indicator

When Copilot CLI is connected to a VS Code instance (via the Copilot CLI
extension), the status bar shows an indicator reflecting the currently selected
file in the editor. This helps the agent understand which file you're focused
on without requiring you to specify it explicitly.

### Two-Line Layout

Since **v0.0.416**, when the terminal width is too narrow to fit all status bar
elements on a single line, the status bar automatically switches to a
**two-line layout**:

```
Line 1:  ~/project (main)
Line 2:  claude-sonnet-4 · MCP: 2 · PR #42
```

This ensures no information is lost, even in narrow terminal panes or split
views.

---

## Themes

Copilot CLI includes a built-in theming system that controls syntax
highlighting, diff colors, markdown rendering, and general UI chrome.

### The `/theme` Command

Introduced in **v0.0.400**, the `/theme` command opens an interactive theme
picker. Since **v1.0.4**, the picker supports adaptive themes with GitHub
Dark, GitHub Light, and AUTO modes that respond to your terminal's color
scheme:

```
/theme
```

The picker displays a **live preview** showing how each theme renders diffs,
markdown with bold and italic text, code blocks, and table borders. Navigate
the list with arrow keys and press `Enter` to apply.

### Built-In Themes

| Theme | Description | Best For |
|-------|-------------|----------|
| **GitHub Dark** | Dark background with GitHub's signature color palette | Dark terminal backgrounds |
| **GitHub Light** | Light background variant | Light terminal backgrounds |
| **AUTO** | Reads the terminal's ANSI color palette directly | Matching your existing terminal theme |
| **Colorblind** | Optimized contrast for deuteranopia/protanopia | Red-green color vision deficiency |
| **Tritanopia** | Optimized contrast for tritanopia | Blue-yellow color vision deficiency |

> 💡 The **AUTO** theme (added in **v0.0.421**) is particularly powerful: it
> reads your terminal emulator's configured ANSI colors and maps them to
> Copilot CLI's UI elements. If you've already customized your terminal's
> color scheme, AUTO makes Copilot CLI feel native.

### Accessibility Themes

The **Colorblind** and **Tritanopia** variants (added in **v0.0.407**) replace
red/green diff indicators with colors that remain distinguishable for users
with color vision deficiency. They also use additional visual cues (bold,
underline) to convey information that would otherwise rely solely on color.

### Enhanced Color Contrast (v1.0.7)

Starting in **v1.0.7**, the rendering engine improved overall readability with
enhanced color contrast. User messages now display with a subtle background
differentiation from agent responses, making it easier to scan long
conversations and identify who said what at a glance.

### Theme Persistence

Your selected theme is saved to Copilot CLI's configuration and **persists
across sessions**. You do not need to re-select your theme each time you
launch the CLI.

---

## Streamer Mode

Streamer mode is designed for situations where your screen is visible to an
audience — live streams, conference presentations, screen recordings, or
pair programming sessions.

### Activation

```
/streamer-mode
```

This command was added in **v0.0.408** and acts as a toggle: run it once to
enable, run it again to disable.

### What Streamer Mode Hides

| Hidden Element | Why |
|----------------|-----|
| **Preview model names** | Prevents leaking unreleased or internal model identifiers |
| **Quota details** | Hides usage limits, remaining requests, and plan information |

> ⚠️ Streamer mode does **not** hide file contents, environment variables, or
> secrets that may appear in tool call output. Ensure your environment is
> sanitized before streaming.

---

## Screen Reader Mode

Copilot CLI includes a dedicated screen reader mode for users who rely on
assistive technology.

### Activation

```bash
copilot-cli --screen-reader
```

On first use, the CLI prompts you to **save this as a persistent preference**
so you do not need to pass the flag on every invocation.

### Adaptations

| Standard Mode | Screen Reader Mode |
|---------------|-------------------|
| `●` / `○` circle icons | Text labels: `[done]`, `[running]`, `[failed]` |
| Animated spinner | Static text: `Thinking...` |
| Tab icons in quick help | Descriptive tab labels (e.g., `Shortcuts Tab`, `Commands Tab`) |
| Visual scrollbar in pickers | Accessible scrollbar with position announcements |
| Color-coded diff markers | Prefixed text: `[added]`, `[removed]` |

> 💡 Screen reader mode can be combined with any theme. The accessibility
> themes (Colorblind, Tritanopia) complement screen reader mode by providing
> high-contrast visuals for users with partial vision.

---

## Mouse Support

Mouse support is available in alt-screen mode and provides a range of
interactions beyond basic text selection.

### Configuration

Since **v0.0.419**, mouse support can be explicitly controlled:

```bash
# Enable mouse support
copilot-cli --mouse

# Disable mouse support
copilot-cli --no-mouse
```

You can also set this in your configuration file:

```json
{
  "mouse": true
}
```

### Mouse Interactions

| Action | Result | Notes |
|--------|--------|-------|
| **Click and drag** | Select text range | Works across multiple lines |
| **Double-click** | Select word under cursor | Respects word boundaries |
| **Triple-click** | Select entire line | Includes leading whitespace |
| **Scroll wheel** | Scroll timeline up/down | Alt-screen and `/diff` views |
| **Click in prompt** | Reposition text cursor | Move insertion point within your message |
| **Click a link** | Open in browser | OSC 8 hyperlinks (since v0.0.421); enhanced in v1.0.12 for VS Code terminals |
| **Drag to edge** | Auto-scroll viewport | Extends selection while scrolling (alt-screen) |

### Clipboard Behavior

| Platform | Copy Method | Paste Method |
|----------|-------------|--------------|
| **macOS** | `Cmd+C` or `Ctrl+Insert` | `Cmd+V` |
| **Linux (X11)** | Auto-copied to primary selection | Middle-click paste |
| **Linux (Wayland)** | `Ctrl+Insert` | `Ctrl+Shift+V` |
| **Windows** | `Ctrl+Insert` | `Ctrl+Shift+V` or right-click |

The `copy_on_select` configuration option, when enabled, automatically copies
any selected text to the system clipboard the moment you release the mouse
button — no explicit copy shortcut needed.

> ⚠️ Some terminal emulators intercept mouse events for their own selection
> mechanism. If mouse interactions aren't working, check your terminal's
> settings for a "mouse reporting" or "application mouse mode" option.

---

## Quick Help Overlay

Pressing `?` at an empty prompt opens the **quick help overlay** — a
categorized reference of all available keyboard shortcuts and slash commands.

### Navigation

| Key | Action |
|-----|--------|
| `←` / `→` or `Tab` | Switch between help tabs |
| `↑` / `↓` | Scroll within the current tab |
| `Ctrl+C` or `Esc` | Dismiss the overlay |

The overlay groups information into tabs:

| Tab | Contents |
|-----|----------|
| **Shortcuts** | Keyboard shortcuts for navigation, editing, and control |
| **Commands** | All available `/slash` commands with descriptions |
| **Tools** | Available tools and their brief descriptions |

> 💡 In screen reader mode, the tabs are labeled with descriptive names
> (e.g., `Shortcuts Tab`, `Commands Tab`) instead of icons, making them
> navigable with assistive technology.

---

## Terminal Title

Copilot CLI dynamically updates your terminal's title bar to reflect the
current state of the session.

### Title States

| State | Title Content | Since |
|-------|---------------|-------|
| **Idle** | Session name (e.g., `Copilot: my-feature`) | v0.0.407 |
| **Working** | Current intent (e.g., `Copilot: Fixing auth bug`) | v0.0.407 |
| **Thinking** | Progress indicator (e.g., `Copilot ◐ Thinking...`) | v0.0.400 |

The terminal title is updated using standard **OSC escape sequences**, which
are supported by virtually all modern terminal emulators. When the agent is
actively working, the title shows the current intent — the same text visible in
the status area — so you can monitor progress even when Copilot CLI's window is
minimized or in another tab.

> 💡 If you use tmux, the session name appears in your tmux window list,
> making it easy to identify which Copilot session is running in which pane.

---

## Markdown Rendering

Copilot CLI renders the agent's markdown responses directly in the terminal
with high fidelity. Since **v0.0.421**, the rendering engine received
significant improvements.

### Rendering Capabilities

| Element | Rendering | Notes |
|---------|-----------|-------|
| **Headings** | Bold, scaled text (no `#` prefixes shown) | H1–H3 visually distinct |
| **Bold / Italic** | Terminal bold and italic attributes | Requires terminal support |
| **Code blocks** | Syntax-highlighted, bordered box | Language-specific highlighting |
| **Inline code** | Distinct background color | Colons inside inline code render correctly in tables |
| **Tables** | Unicode box-drawing borders, word-wrap | Column widths auto-calculated |
| **Ordered lists** | Rendered with numbers (1. 2. 3.) | Not converted to dashes |
| **Unordered lists** | Bullet characters (•) | Nested indentation preserved |
| **Links** | Clickable in supporting terminals | OSC 8 hyperlinks; v1.0.12 added reliable support in VS Code integrated terminals |
| **Blockquotes** | Indented with vertical bar | Color-coded by type |

### Table Rendering (v0.0.421 Improvements)

Tables are rendered with **Unicode box-drawing characters** for clean borders:

```
┌──────────┬─────────┬────────────────────────────────────┐
│ Command  │ Shortcut│ Description                        │
├──────────┼─────────┼────────────────────────────────────┤
│ /help    │ ?       │ Show the quick help overlay         │
│ /theme   │ —       │ Open the theme picker               │
│ /compact │ —       │ Compact conversation history        │
└──────────┴─────────┴────────────────────────────────────┘
```

Key improvements:

- **Bold headers**: The first row of a table is rendered in bold.
- **Word wrap**: Long cell content wraps within the cell rather than breaking
  the table layout.
- **Proper column widths**: Columns are sized based on content, not fixed widths.
- **Inline code in tables**: Backtick-delimited code within table cells renders
  correctly, including content with colons (e.g., `key: value`).

### Formatted Text Wrapping

When the terminal is too narrow for a line of formatted text (bold, italic,
links), the rendering engine wraps at word boundaries while preserving the
formatting attributes across the wrap point. Previously, formatting could be
lost at line boundaries.

---

## Responsive Layout

Copilot CLI is designed to work in terminals as narrow as **40 columns**,
though the optimal experience is at 80 columns or wider.

### Adaptive Behaviors

| Terminal Width | Adaptation |
|----------------|-----------|
| **< 60 columns** | Status bar switches to two-line layout |
| **< 80 columns** | CWD in header uses middle-truncation |
| **< 80 columns** | Diff file list uses carousel (5 files at a time) |
| **≥ 80 columns** | Full single-line status bar, complete paths |
| **≥ 120 columns** | Tables and diffs render with generous column widths |

### Diff Mode File Carousel

When viewing diffs (via `/diff` or within expanded edit tool calls), the file
list at the top of the diff view is displayed as a **carousel** that shows
5 files at a time. Navigate with arrow keys to scroll through the list. This
prevents the file list from consuming the entire viewport when a change spans
many files.

### Middle-Truncation Examples

Copilot CLI uses middle-truncation throughout the interface to preserve the
most informative parts of long paths:

```
Path:       /home/user/projects/copilot-workshop/workshop/level-7/sample-app
Truncated:  /home/user/…/level-7/sample-app

Branch:     feature/TICKET-1234-add-authentication-middleware
Truncated:  feature/TICK…middleware
```

> 💡 Middle-truncation keeps both the root (for orientation) and the leaf
> (for specificity), sacrificing only the less informative middle segments.

---

## Summary

The Copilot CLI interface is a carefully layered system: the **header** orients
you, the **timeline** shows the full history of agent work, the **status bar**
provides persistent context, and the **prompt** is where you drive the
conversation. Alt-screen mode and themes let you customize the experience,
while screen reader mode and accessibility themes ensure the interface works
for everyone.

| Feature | Key Takeaway |
|---------|-------------|
| **Timeline** | `Ctrl+O` to expand recent, `Ctrl+E` to expand all |
| **Alt-Screen** | Full TUI with mouse support; `--alt-screen on` to enable |
| **Themes** | `/theme` to pick; AUTO reads your terminal's colors |
| **Streamer Mode** | `/streamer-mode` hides model names and quota |
| **Screen Reader** | `--screen-reader` replaces icons with labels |
| **Mouse** | Click, drag, scroll; `--mouse` / `--no-mouse` to control |
| **Responsive** | Works down to 40 columns with adaptive layout |

---

Next: [Chapter 3: Keyboard Shortcuts & Input](./03-keyboard-shortcuts-and-input.md)
