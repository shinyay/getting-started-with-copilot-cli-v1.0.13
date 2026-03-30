# Chapter 7: Custom Instructions & Configuration

Copilot CLI becomes dramatically more effective when it understands your project's
conventions, architecture, and constraints. This chapter covers the full instruction
system — from personal preferences to path-scoped rules — plus every configuration
option and environment variable available.

---

## Why Custom Instructions Matter

Without custom instructions, Copilot operates on general knowledge. It will produce
valid code, but it will **guess** at your conventions. With instructions, Copilot
**follows** your patterns consistently.

| Without Instructions | With Instructions |
|----------------------|-------------------|
| Guesses naming conventions | Follows your `camelCase` / `snake_case` rules |
| Uses generic error handling | Throws your custom `AppError` class |
| Picks arbitrary test frameworks | Uses your project's Jest + `describe`/`it` style |
| Ignores architecture boundaries | Routes → Services → Models layering respected |
| Generic log calls (`console.log`) | Structured `logger.info('msg', { context })` |
| Invents response formats | Wraps everything in `ApiResponse<T>` |

> 💡 Think of instructions as a **persistent system prompt** — they are silently
> included in every interaction within their scope, so Copilot never "forgets"
> your rules.

### What Instructions Encode

Instructions work best when they capture knowledge that **cannot be inferred**
from the code alone:

- **Coding standards** — naming, formatting, import style
- **Architecture decisions** — layer boundaries, dependency direction
- **Tech stack choices** — which libraries, which versions, why
- **Testing conventions** — framework, structure, coverage expectations
- **Error handling patterns** — custom error classes, response formats
- **Security rules** — input validation, auth requirements
- **Domain-specific rules** — business logic constraints, terminology

> ⚠️ Don't duplicate what linters and CI already enforce. Instructions should
> cover the **intent** behind your rules, not mechanical formatting checks.

---

## Instruction File Hierarchy

Copilot CLI recognizes instruction files at five distinct levels. All applicable
files are **combined** (not overridden) into the context for every interaction.

### Hierarchy Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     INSTRUCTION AGGREGATION                     │
│                                                                 │
│  All matching files are COMBINED into the context window.       │
│  There is NO priority-based fallback — every layer contributes. │
│  Identical files are deduplicated to save tokens.               │
└─────────────────────────────────────────────────────────────────┘

     ┌──────────────────────────────────────┐
     │  1. User-Level Instructions          │
     │     ~/.copilot/copilot-instructions  │
     │     ~/.copilot/instructions/*.md     │
     └──────────────┬───────────────────────┘
                    │ combined with
     ┌──────────────▼───────────────────────┐
     │  2. Repository-Wide Instructions     │
     │     .github/copilot-instructions.md  │
     └──────────────┬───────────────────────┘
                    │ combined with
     ┌──────────────▼───────────────────────┐
     │  3. Path-Specific Instructions       │
     │     .github/instructions/**/*.md     │
     │     (filtered by applyTo globs)      │
     └──────────────┬───────────────────────┘
                    │ combined with
     ┌──────────────▼───────────────────────┐
     │  4. Agent/Tool-Specific Files        │
     │     AGENTS.md / CLAUDE.md / etc.     │
     │     (in git root and cwd)            │
     └──────────────┬───────────────────────┘
                    │ combined with
     ┌──────────────▼───────────────────────┐
     │  5. Environment Variable Override    │
     │     COPILOT_CUSTOM_INSTRUCTIONS_DIRS │
     └──────────────────────────────────────┘
```

---

### 1. User-Level Instructions

User-level instructions apply to **every repository** you work in. They live in
your home directory and encode personal preferences.

| File | Purpose | Since |
|------|---------|-------|
| `~/.copilot/copilot-instructions.md` | Personal instructions for all repos | — |
| `~/.copilot/instructions/*.instructions.md` | Cross-repo instruction modules | v0.0.412 |

**Best for:**
- Personal coding style preferences
- Always-on rules (e.g., "never use `var` in JavaScript")
- Preferred libraries or patterns you use across all projects

**Example — `~/.copilot/copilot-instructions.md`:**

```markdown
# Personal Coding Preferences

- Prefer functional programming patterns over imperative loops
- Use early returns to reduce nesting
- Always add JSDoc comments to exported functions
- When writing tests, include edge cases for null/undefined inputs
- Prefer named exports over default exports
```

> 💡 Keep user-level instructions **short and universal**. Project-specific
> rules belong in repository-level files.

---

### 2. Repository-Wide Instructions

Repository-wide instructions are the most common and most impactful layer. They
define your project's conventions and are automatically included in every Copilot
interaction within the repo.

| File | Purpose |
|------|---------|
| `.github/copilot-instructions.md` | Project-wide rules, standards, and context |

**Best for:**
- Coding standards and architecture
- Tech stack and dependency rules
- Testing conventions
- Error handling patterns
- Domain-specific terminology

> 📋 See [Writing Effective Instructions](#writing-effective-instructions) below
> for detailed guidance on crafting high-quality repository instructions.

---

### 3. Path-Specific Instructions

Path-specific instructions let you apply different rules to different parts of
your codebase. They use YAML frontmatter with `applyTo` globs to target files.

| File | Purpose |
|------|---------|
| `.github/instructions/**/*.instructions.md` | Rules scoped to file patterns |

**How `applyTo` works:**

The `applyTo` field in the YAML frontmatter accepts glob patterns. The
instruction file is only included when the user is working with files that match
the pattern.

```yaml
---
applyTo: "src/frontend/**/*.{ts,tsx}"
---
```

| Glob Pattern | Matches |
|--------------|---------|
| `**/*.py` | All Python files in the repo |
| `src/api/**/*.ts` | TypeScript files under `src/api/` |
| `**/*.test.{ts,js}` | All test files (TS and JS) |
| `workshop/level-7/**/*.{ts,js,json}` | Level 7 sample app files |
| `*.md` | Markdown files in the root only |
| `**/*.md` | All markdown files in the repo |

**Best for:**
- Language-specific rules (Python vs TypeScript)
- Module-specific conventions (API vs frontend vs tests)
- Different standards for different team areas

> 💡 Path-specific instructions **add** to repository-wide instructions — they
> don't replace them. A TypeScript file will receive both the repo-wide rules
> and any matching path-specific rules.

---

### 4. Agent/Tool-Specific Files

These files provide instructions specifically for AI coding agents and tools.
Copilot CLI reads them from both the **git root** and the **current working
directory**.

| File | Purpose | Since |
|------|---------|-------|
| `AGENTS.md` | Agent-specific instructions | — |
| `CLAUDE.md` | Claude Code compatible instructions | v1.0.13 |
| `GEMINI.md` | Gemini CLI compatible instructions | v1.0.13 |

> 💡 File name matching is **case-insensitive** since v0.0.411 — `agents.md`,
> `AGENTS.md`, and `Agents.md` are all recognized.

Agent files are especially useful when you want to give instructions to Copilot's
autonomous coding agent mode (see [Chapter 8: Custom Agents](./08-custom-agents.md))
without affecting interactive chat behavior.

---

### 5. Environment Variable Override

Since v1.0.13, you can point Copilot at additional instruction directories using
the `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` environment variable:

```bash
export COPILOT_CUSTOM_INSTRUCTIONS_DIRS="/path/to/shared-instructions:/path/to/team-rules"
```

This is useful for:
- **Shared team standards** stored outside the repo
- **Organization-wide rules** distributed via a central location
- **Monorepo setups** where instructions live in a common directory

---

### Aggregation Behavior

Understanding how instruction files are combined is critical:

| Behavior | Details | Since |
|----------|---------|-------|
| **Combination** | All applicable files are merged into context | v0.0.385 |
| **Deduplication** | Identical files are included only once | v0.0.394 |
| **Case-insensitive** | File names matched regardless of casing | v0.0.411 |
| **No override** | Higher-level instructions are NOT replaced by lower-level ones |  — |

> ⚠️ Because all layers are **combined**, contradictions between layers will
> confuse Copilot. If your user-level file says "use tabs" and your repo file
> says "use spaces," Copilot receives both rules and may produce inconsistent
> output. Keep your layers complementary, not contradictory.

---

## Instruction Management Commands

### `/instructions` — View and Toggle Instructions

The `/instructions` slash command lets you see which instruction files are
currently active and toggle them on or off.

```
/instructions
```

| Feature | Details | Since |
|---------|---------|-------|
| View active instruction files | Lists all files contributing to context | v0.0.407 |
| Toggle files on/off | Temporarily disable specific instruction files | v0.0.407 |
| Full-screen alt-screen view | Renders in a dedicated full-screen panel | v0.0.412 |
| Skills picker | Also opens as full-screen view | v0.0.412 |
| Toggle individual files | Enable/disable specific instruction files independently | v1.0.13 |

> 💡 Use `/instructions` to **debug unexpected behavior**. If Copilot is
> following rules you don't expect, check which instruction files are active.

---

### `/init` — Generate Instructions for a Repository

The `/init` command uses AI to analyze your codebase and generate a
`.github/copilot-instructions.md` file tailored to your project.

```
/init
```

| Feature | Details | Since |
|---------|---------|-------|
| AI-assisted generation | Analyzes codebase structure and conventions | v0.0.396 |
| Suppress suggestions | `/init suppress` prevents future init prompts | v0.0.410 |

**How it works:**

1. Copilot scans your repository structure, languages, and patterns
2. It generates a draft instruction file based on what it finds
3. You review, edit, and commit the result

> 💡 `/init` is a great **starting point**, but always review and customize the
> generated instructions. The AI may miss domain-specific conventions or include
> rules you disagree with.

> ⚠️ If you already have a `.github/copilot-instructions.md`, running `/init`
> will offer to update it. Back up your existing file first if you have extensive
> custom rules.

---

## Writing Effective Instructions

The quality of your instructions directly impacts Copilot's output. Here's how
to write instructions that make a real difference.

### Do's

| Practice | Example |
|----------|---------|
| Be specific and concise | "Use `AppError.notFound()` for missing resources" |
| Focus on what code can't show | "Routes must never access the database directly" |
| Include concrete examples | "Logging format: `logger.info('Event created', { eventId })`" |
| Specify naming conventions | "`camelCase` for variables, `PascalCase` for types" |
| Reference specific files | "Error classes are defined in `src/utils/errors.ts`" |
| State the WHY | "We use Zod for validation because it provides type inference" |
| Keep it scannable | Use tables, bullet points, short paragraphs |

### Don'ts

| Anti-Pattern | Why It's Bad |
|--------------|-------------|
| "Write good code" | Too vague — Copilot can't act on this |
| "Follow best practices" | Which practices? Be explicit |
| Duplicate linter rules | Wastes context tokens on what CI already enforces |
| Write a novel | Context window limits — instructions compete with your code |
| Contradict between layers | User + repo instructions saying opposite things confuse Copilot |
| Include sensitive data | Instructions are plaintext in your repo — no secrets |

> ⚠️ **Context window budget**: Every instruction token reduces the space
> available for code context. Aim for **200–500 lines** of instructions total
> across all layers. If you exceed this, prioritize the rules Copilot violates
> most often.

---

### Example: A Complete Repository Instruction File

This is a realistic `.github/copilot-instructions.md` for a TypeScript API
project:

```markdown
# Project: Event Management API

## Language & Runtime
- TypeScript 5.x with `strict: true`
- Node.js 20+, Express 4.x
- Target: ES2020, CommonJS output

## Code Style
- Named imports only: `import { Router } from 'express'`
- `const` by default, `let` only when reassignment is necessary
- Arrow functions for callbacks, regular functions for named exports
- `camelCase` for variables/functions, `PascalCase` for types/interfaces
- Single quotes, semicolons required, 100-char line limit

## Architecture
- Routes → Services → Models (never skip layers)
- Routes: HTTP concerns only (params, response formatting)
- Services: business logic, validation orchestration
- Middleware: cross-cutting concerns (auth, logging, errors)

## Error Handling
- Always use `AppError` from `src/utils/errors.ts`
- Factory methods: `.notFound()`, `.badRequest()`, `.unauthorized()`
- Every error needs a machine-readable `code` and HTTP `statusCode`
- Never throw raw `Error` objects

## API Responses
- Wrap all responses in `ApiResponse<T>` from `src/utils/response.ts`
- `respondSuccess(data)` for single items
- `respondPaginated(data, page, pageSize, total)` for lists
- Error format: `{ success: false, error: { code, message } }`

## Logging
- Use `logger` from `src/utils/logger.ts` (never console.log)
- Include context: `logger.info('Event created', { eventId, userId })`
- Levels: error > warn > info > debug

## Testing
- Jest with `describe`/`it` blocks (never `test()`)
- `beforeEach` to reset state
- Test both success and error paths
- Use `toThrow(AppError)` for error testing
```

---

### Example: Path-Specific Instructions

This file applies rules only to frontend components:

**`.github/instructions/frontend.instructions.md`:**

```yaml
---
applyTo: "src/frontend/**/*.{ts,tsx}"
---
```

```markdown
# Frontend Component Rules

## Component Structure
- One component per file
- File name matches component name: `EventCard.tsx` → `EventCard`
- Props interface named `<Component>Props`: `EventCardProps`

## State Management
- Use React hooks for local state
- Use context for shared state (no Redux)
- Custom hooks in `src/frontend/hooks/`

## Styling
- CSS Modules only — no inline styles, no global CSS
- File: `<Component>.module.css` next to the component

## Testing
- Co-locate tests: `EventCard.test.tsx` next to `EventCard.tsx`
- Use React Testing Library (never Enzyme)
- Test user interactions, not implementation details
```

---

### Example: Path-Specific Instructions for Tests

**`.github/instructions/testing.instructions.md`:**

```yaml
---
applyTo: "**/*.test.{ts,tsx,js}"
---
```

```markdown
# Test File Rules

- Use `describe` blocks grouped by function or component
- Use `it` with descriptive names: `it('returns 404 when event not found')`
- Arrange-Act-Assert pattern in every test
- Mock external dependencies, never real network calls
- Include edge cases: empty input, null, boundary values
- Minimum 3 test cases per function: happy path, error path, edge case
```

---

## Configuration Files

Copilot CLI uses two configuration files — one per-user and one per-repository.

### User Configuration — `~/.copilot/config.json`

This file stores your personal Copilot CLI preferences. It applies to all
repositories.

| Option | Type | Description | Since |
|--------|------|-------------|-------|
| `model` | `string` | Default model for interactions | — |
| `log_level` | `string` | Logging verbosity | — |
| `theme` | `string` | Terminal color theme | — |
| `include_coauthor` | `boolean` | Add `Co-authored-by` trailer to git commits | v0.0.411 |
| `copy_on_select` | `boolean` | Auto-copy selected text to clipboard | v0.0.422 |
| `companyAnnouncements` | `boolean` | Show startup announcements | v0.0.422 |
| `enabledPlugins` | `string[]` | Plugins to auto-install at startup | v0.0.422 |
| `mouse` | `object` | Mouse interaction mode configuration | — |
| `banner` | `boolean` | Show/hide the startup banner | — |

**`log_level` values:**

| Value | What It Captures |
|-------|------------------|
| `"none"` | No logging |
| `"error"` | Errors only |
| `"warning"` | Errors and warnings |
| `"info"` | Errors, warnings, and info messages |
| `"debug"` | Everything including debug output |
| `"all"` | Maximum verbosity |
| `"default"` | Platform-appropriate default level |

**Example — `~/.copilot/config.json`:**

```json
{
  "model": "claude-sonnet-4-20250514",
  "log_level": "info",
  "theme": "dark",
  "include_coauthor": true,
  "copy_on_select": false,
  "banner": true,
  "companyAnnouncements": true,
  "enabledPlugins": []
}
```

> 💡 The `include_coauthor` option controls whether Copilot adds a
> `Co-authored-by: Copilot <...>` trailer when it creates git commits. This is
> useful for tracking AI-assisted contributions.

> ⚠️ The `companyAnnouncements` option was renamed from `launch_messages` in
> v0.0.422. If you have the old key in your config, update it.

---

### Repository Configuration — `.github/copilot/settings.json`

This file stores project-level Copilot settings shared across the team.

| Option | Type | Description | Since |
|--------|------|-------------|-------|
| Marketplaces | `object` | MCP marketplace configuration | — |
| Tool validation | `object` | Tool permission settings | v0.0.410 |

> ⚠️ This file was renamed from `.github/copilot/config.json` to
> `.github/copilot/settings.json` in v0.0.422. Update your repository if you're
> using the old path.

**Example — `.github/copilot/settings.json`:**

```json
{
  "tools": {
    "allowed": ["bash", "glob", "grep", "view", "edit", "create"],
    "blocked": []
  }
}
```

---

### Claude-Compatible Configuration — `.claude/settings.json`

Since v1.0.12, Copilot CLI reads **`.claude/settings.json`** at the project root
as an additional configuration source, along with the `.claude/settings.local.json`
variant for local overrides. This provides compatibility with Claude Code project
settings.

| File | Scope | Since |
|------|-------|-------|
| `.claude/settings.json` | Project-level (committed to repo) | v1.0.12 |
| `.claude/settings.local.json` | Local overrides (add to `.gitignore`) | v1.0.12 |

> 💡 If you work across both Copilot CLI and Claude Code, shared settings in
> `.claude/settings.json` ensure consistent behavior without maintaining
> separate configurations.

---

### Template Variables in Configuration

Since v1.0.12, hook and plugin configurations support **template variables** that
are expanded at runtime:

| Variable | Expands To | Since |
|----------|-----------|-------|
| `{{project_dir}}` | Absolute path to the current project root | v1.0.12 |
| `{{plugin_data_dir}}` | Plugin-specific data directory | v1.0.12 |

```json
{
  "hooks": {
    "preToolUse": "{{project_dir}}/hooks/guard.js"
  }
}
```

> 💡 Template variables eliminate the need for absolute paths in shared
> configuration files, making them portable across developer machines.

---

### Getting Help with Configuration

Run the built-in help command for the complete, up-to-date configuration
reference:

```bash
copilot help config
```

This displays all available options, their types, defaults, and descriptions
directly from the CLI.

---

## Environment Variables — Complete Reference

Copilot CLI reads and sets a number of environment variables. These control
authentication, configuration paths, proxy settings, and subprocess behavior.

### Authentication

| Variable | Purpose | Precedence |
|----------|---------|------------|
| `COPILOT_GITHUB_TOKEN` | Copilot-specific auth token | Highest |
| `GH_TOKEN` | GitHub CLI auth token | Medium |
| `GITHUB_TOKEN` | General GitHub auth token | Lower |
| `GITHUB_ASKPASS` | Auth helper program | Fallback |

> 💡 If multiple auth tokens are set, Copilot uses the **highest precedence**
> token. Set `COPILOT_GITHUB_TOKEN` to use a dedicated token that won't conflict
> with other GitHub tools.

> ⚠️ Never hardcode tokens in instruction files or configuration. Use
> environment variables or credential managers.

### Host & Network

| Variable | Purpose | Notes |
|----------|---------|-------|
| `GH_HOST` | GitHub Enterprise hostname | For GHE Server connections |
| `HTTPS_PROXY` | HTTPS proxy URL | Standard proxy configuration |
| `HTTP_PROXY` | HTTP proxy URL | Fallback if HTTPS_PROXY not set |

### Configuration Paths

| Variable | Purpose | Default |
|----------|---------|---------|
| `XDG_CONFIG_HOME` | Override config directory location | `~/.config` |
| `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Additional instruction directories | Not set |

**Using `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`:**

```bash
# Single additional directory
export COPILOT_CUSTOM_INSTRUCTIONS_DIRS="/path/to/shared-instructions"

# Multiple directories (colon-separated)
export COPILOT_CUSTOM_INSTRUCTIONS_DIRS="/team/standards:/org/policies"
```

### Subprocess & Runtime

| Variable | Purpose | Notes |
|----------|---------|-------|
| `COPILOT_CLI` | Set to `1` inside Copilot subprocesses | Detect if running under Copilot |
| `COPILOT_KITTY` | Enable Kitty graphics protocol (legacy) | For Kitty terminal emulator |
| `USE_BUILTIN_RIPGREP` | Use ripgrep from `$PATH` instead of bundled | Override bundled binary |
| `BASH_ENV` | Source file in shell sessions | Requires `--bash-env` flag |
| `NODE_ENV` | Node.js environment | **Excluded** from shell tool sessions |
| `GITHUB_WORKSPACE` | MCP server working directory | Used in GitHub Actions |

> 💡 Check `COPILOT_CLI` in your scripts to detect when they're being run by
> Copilot's shell tool:
>
> ```bash
> if [ "${COPILOT_CLI:-0}" = "1" ]; then
>   echo "Running inside Copilot CLI"
> fi
> ```

### Getting the Full Reference

For the complete, up-to-date environment variable reference:

```bash
copilot help environment
```

---

## Putting It All Together — A Real-World Setup

Here's how instruction files, configuration, and environment variables work
together in a typical TypeScript project:

```
my-project/
├── .github/
│   ├── copilot-instructions.md          # Repo-wide: architecture, standards
│   ├── copilot/
│   │   └── settings.json                # Repo config: tool permissions
│   └── instructions/
│       ├── backend.instructions.md      # applyTo: "src/api/**/*.ts"
│       ├── frontend.instructions.md     # applyTo: "src/frontend/**/*.tsx"
│       └── testing.instructions.md      # applyTo: "**/*.test.ts"
├── AGENTS.md                            # Agent-specific instructions
├── src/
│   ├── api/          ← gets: user + repo + backend rules
│   ├── frontend/     ← gets: user + repo + frontend rules
│   └── shared/       ← gets: user + repo rules only
└── tests/            ← gets: user + repo + testing rules
```

**What Copilot sees when editing `src/api/routes/events.ts`:**

1. `~/.copilot/copilot-instructions.md` (user preferences)
2. `.github/copilot-instructions.md` (repo architecture + standards)
3. `.github/instructions/backend.instructions.md` (API-specific rules)
4. `AGENTS.md` (if running in agent mode)

All four files are **combined** into the context — giving Copilot a comprehensive
understanding of both your personal style and the project's specific conventions
for backend API code.

> 💡 Start with a repo-wide instruction file. Add path-specific files only when
> different parts of your codebase genuinely need different rules. Over-splitting
> wastes context tokens on boilerplate.

---

## Troubleshooting Instructions

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| Copilot ignores your rules | Run `/instructions` to check active files | Ensure file is in the correct path and format |
| Contradictory behavior | Check for conflicting rules across layers | Remove duplicates, align user + repo instructions |
| Too much context used | Instructions consuming too many tokens | Trim verbose instructions, remove linter-level rules |
| Path-specific not activating | `applyTo` glob not matching | Test glob patterns, check YAML frontmatter syntax |
| `/init` keeps suggesting | Already have instructions but still prompted | Run `/init suppress` to disable suggestions |
| Old config key warnings | Renamed options in recent versions | Update `launch_messages` → `companyAnnouncements`, `config.json` → `settings.json` |

---

## Quick Reference Card

| What You Want | Where to Put It |
|---------------|-----------------|
| Personal coding style | `~/.copilot/copilot-instructions.md` |
| Project architecture | `.github/copilot-instructions.md` |
| Frontend-specific rules | `.github/instructions/frontend.instructions.md` |
| Agent behavior | `AGENTS.md` in repo root |
| Claude Code compatibility | `CLAUDE.md` in repo root *(v1.0.13)* |
| Gemini CLI compatibility | `GEMINI.md` in repo root *(v1.0.13)* |
| Claude Code project settings | `.claude/settings.json` *(v1.0.12)* |
| Default model | `~/.copilot/config.json` → `"model"` |
| Team tool permissions | `.github/copilot/settings.json` |
| Extra instruction dirs | `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` env var *(v1.0.13)* |
| Auth token | `COPILOT_GITHUB_TOKEN` env var |
| Proxy settings | `HTTPS_PROXY` / `HTTP_PROXY` env var |

---

> 📋 **See also:**
> - [Chapter 6: Tool Use & Shell Integration](./06-tool-use-and-shell-integration.md) — how Copilot executes commands
> - [Chapter 8: Custom Agents](./08-custom-agents.md) — building autonomous agents with `AGENTS.md`

---

*Next: [Chapter 8: Custom Agents](./08-custom-agents.md)*
