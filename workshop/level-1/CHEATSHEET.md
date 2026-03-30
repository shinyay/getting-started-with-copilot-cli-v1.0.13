# Level 1 — Quick Reference Card

## Syntax

| Syntax | Purpose | Token Cost |
|--------|---------|------------|
| `!command` | Run shell command directly (no AI) | **Free** |
| `@ filename` | Inject file contents into context | Adds input tokens |
| `@ ~/...`, `@ ../...`, `@ /abs/path` | Inject file from outside project (v1.0.5+) | Adds input tokens |
| `text + Enter` | Send prompt to AI model | Input + output tokens |
| `/slash-command` | Run local CLI command | **Free** |

## Essential Slash Commands

| Command | What It Does |
|---------|-------------|
| `/help` | Show all commands and shortcuts |
| `/model` | View/switch AI model |
| `/usage` | View premium request and token stats |
| `/context` | Visualize context window consumption |
| `/compact` | Compress conversation history |
| `/version` | Display version and check for updates |
| `/restart` | Hot restart preserving session |
| `/extensions` | View/enable/disable CLI extensions |
| `/pr` | PR workflow (create, view, fix CI, review feedback) |
| `/experimental on\|off` | Toggle experimental features |
| `/rewind` | Undo last turn and revert file changes | `(v1.0.13)` |
| `/new` | Start fresh conversation, keep settings | `(v1.0.13)` |
| `/session` | View session info and management | `(v1.0.13)` |
| `/exit` | Exit Copilot CLI |
| `/quit` | Exit Copilot CLI | `(v1.0.13)` |
| `quit` | Exit the CLI (alias for `/exit`) |

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel operation / clear input / exit |
| `Ctrl+L` | Clear screen |
| `Ctrl+D` | Shutdown |
| `Esc` | Cancel current operation |
| `Double-Esc` | First clears input, second triggers undo | `(v1.0.7)` |
| `↑` / `↓` | Navigate command history |
| `Ctrl+A` | Move to beginning of line |
| `Ctrl+E` | Move to end of line |
| `Ctrl+W` | Delete previous word |
| `Ctrl+U` | Delete to beginning of line |
| `Ctrl+K` | Delete to end of line |
| `Ctrl+R` | Reverse incremental history search |
| `Ctrl+G` | Edit prompt in external editor |
| `Ctrl+Z` | Suspend/resume on Unix |
| `Ctrl+O` | Expand recent timeline entries (no input) |
| `Ctrl+E` | Expand all timeline (no input) |
| `Ctrl+T` | Toggle model reasoning display |
| `?` | Quick help overlay (grouped shortcuts) |
| `#` | Reference GitHub issues, PRs, discussions |

## Tool Approval Options

| Option | Meaning |
|--------|---------|
| **Allow** | Approve this one call only |
| **Deny** | Block this call |
| **Allow for session** | Auto-approve this tool for the session |

## Cost-Awareness Rules

```
Free:           !command, /help, /model, /usage, /context, /compact, /version
Costs tokens:   Every natural-language prompt
Costs 1+ req:   Every prompt sent to the model
```

## Effective Question Patterns

| Pattern | Example |
|---------|---------|
| Structure | "What files are in this project and what does each one do?" |
| Data flow | "Trace the execution path when I run `python main.py add ...`" |
| Edge cases | "What happens if the JSON file is corrupted?" |
| Comparison | "How does `format_table` differ from `format_csv`?" |
| Dependencies | "Which files import from `config.py`?" |
| Deep dive | "Explain the `format_table` function line by line" |
