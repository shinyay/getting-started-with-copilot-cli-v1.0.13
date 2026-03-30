# Copilot Instructions — Getting Started with Copilot CLI

## Repository Identity

This is an **educational workshop repository** that teaches developers how to use
GitHub Copilot CLI through 96 hands-on exercises across 8 progressive levels.
It is NOT a regular application — it is a learning curriculum where the code itself
is instructional material.

## 🔄 Copilot CLI Version Awareness

GitHub Copilot CLI reached **General Availability (GA)** on February 25, 2026, with frequent releases that
add, change, or deprecate features. Since this entire repository teaches
Copilot CLI, **content accuracy depends on staying current with the CLI itself.**

When creating or refining content that references CLI capabilities:

- **Verify before writing** — Confirm that referenced slash commands, keyboard
  shortcuts, CLI flags, execution modes, and tool behaviors still exist and
  work as described in the current CLI version
- **Consult authoritative sources** — Use web search to check the
  [official documentation][1], the CLI's `/help` and `/changelog` output,
  and the [CLI repository](https://github.com/github/copilot-cli) release notes
- **Update holistically** — A single CLI change can affect the main README,
  level exercises, cheat sheets, and configuration files simultaneously;
  trace all references before considering an update complete

Content areas most sensitive to CLI evolution:

| Category | Examples | Where Referenced |
|----------|----------|------------------|
| Slash commands | `/plan`, `/diff`, `/review`, `/compact`, `/model`, `/pr`, `/extensions`, `/version`, `/restart` | Exercises, cheat sheets, main README |
| Keyboard shortcuts | `Ctrl+S`, `Shift+Tab`, `@`, `!`, `Ctrl+T` | Cheat sheets, Level 1–2 exercises |
| CLI flags | `--allow-tool`, `-p`, `-s`, `--continue`, `--reasoning-effort` | Level 7–8 exercises, cheat sheets |
| Execution modes | Interactive, Plan, Autopilot | Multiple levels, main README |
| Instruction file paths | `copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md` | Level 7 exercises |
| Model availability | Default model, available alternatives | Level 1 exercises, main README |
| Installation methods | npm, Homebrew, WinGet, install script | Main README |
| Extensions system | `/extensions`, `@github/copilot-sdk`, `extension.mjs`, `joinSession()` | Level 9 exercises, main README |
| Cross-tool instructions | `CLAUDE.md`, `GEMINI.md`, `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Level 7, Level 9 exercises |

## Repository Structure

```
README.md                    # Main learning guide and entry point
workshop/
  README.md                  # Curriculum overview with progression map
  level-1/ through level-8/  # Each level contains:
    README.md                #   12 exercises (Goal → Steps → Key Concept → Checkpoint)
    CHEATSHEET.md            #   Quick-reference card with categorized tables
    sample-app/              #   Unique hands-on application per level
.github/
  copilot-instructions.md    # This file — repo-wide Copilot instructions
  AGENTS.md                  # Coding Agent configuration
  instructions/              # Path-specific Copilot instructions
  workflows/                 # CI/CD (workshop branch creation)
  ISSUE_TEMPLATE/            # Issue forms for workshop management
```

## The 8-Level Learning Path

| Level | Theme | Risk | Sample App | Language |
|-------|-------|------|------------|----------|
| 1 | Observe — Read-Only Exploration | 🟢 None | Task Manager CLI | Python |
| 2 | Understand — Ask Questions | 🟢 None | Bookmark Manager API | Python |
| 3 | Plan — Think Before Acting | 🟡 Low | Quick Notes CLI (8 bugs) | Python |
| 4 | Create — First Changes | 🟡 Medium | Quick Notes CLI (copy) | Python |
| 5 | Execute — Run Commands | 🟠 Medium | Math Utilities Library | Python |
| 6 | Workflow — Full SDLC Cycle | 🟠 High | URL Shortener CLI | Python |
| 7 | Customize — Configuration | 🔵 Variable | Event API | TypeScript |
| 8 | Advanced — Delegation | 🔴 High | DevOps Toolkit | JS + Python |
| 9 | Extend — Build Your Own Experience | 🔴 High | Project Scaffolder | Python + JS |

## 🚫 Critical: Never Auto-Fix Intentional Bugs

Sample apps contain **deliberately planted bugs** for teaching exercises.
These must NEVER be silently fixed. The full catalog:

**Level 3/4 — Quick Notes CLI (8 bugs):**
- Off-by-one in display numbering
- Missing `strip()` on search input
- No duplicate-ID check on add
- Broken export encoding (UTF-8 BOM)
- Delete removes wrong note (index vs ID confusion)
- Priority filter logic inverted
- Empty-title acceptance (no validation)
- Stats double-count on edit

**Level 5 — Math Utilities Library (6 test failures + lint issues):**
- `divide()` returns None instead of raising ValueError for zero
- Negative exponent returns 0 instead of 0.5
- `median()` off-by-one for even-length lists
- `mode()` returns first element instead of most frequent
- `is_positive(0)` returns True (should be False)
- `is_integer(str)` crashes instead of returning False
- Lint: unused imports (math, os), long docstring line, missing docstring on `absolute()`

**Level 6 — URL Shortener CLI (5 issues):**
- Multi-file bug: `store.py` delete doesn't decrement `stats.json` total counter
- `test_validator.py` entirely missing (zero test coverage for validator module)
- Feature gap: no URL expiration support
- Code duplication across store operations
- Incomplete test assertions in existing test files

**Level 9 — Project Scaffolder (teaching points, not bugs):**
- Extension has TODO placeholder tool (students complete it in Exercise 2)
- CLAUDE.md is intentionally minimal (students expand in Exercise 9)
- `.mcp.json` has disabled placeholder server (students configure real one in Exercise 10)
- Skill has incomplete description (students refine in Exercise 6)

When modifying sample apps, preserve these bugs unless the change explicitly
adds, modifies, or documents an intentional bug for teaching purposes.

## Content Conventions

- Every level has exactly **12 exercises**
- Self-assessment: **1–3 scale × 12 items = 36 max** (Ready for next level ≥ 30)
- Exercise structure: `## Exercise N: Title` → `### Goal` → `### Steps` → `### Key Concept` → `### ✅ Checkpoint`
- Copilot prompts: fenced code blocks with no language tag
- Tips: `> 💡`, Warnings: `> ⚠️`, References: `> 📋`
- Use tables for comparisons, options, and structured information

## Writing Style

- Direct, practical, action-oriented
- Effectiveness over simplicity — depth is valued over brevity
- Second-person voice ("you will", "ask Copilot to")
- Include expected output or behavior after each step
- Always explain WHY, not just HOW

## Language Conventions

| Scope | Language | Version | Dependencies |
|-------|----------|---------|-------------|
| Levels 1–6 | Python | 3.8+ | stdlib only (zero external deps) |
| Level 7 | TypeScript | 5.x strict, ES2020 | Express 4.x, Jest |
| Level 8 scripts | Bash | POSIX + bash | `set -euo pipefail` |
| Level 8 services | Node.js + Python | Mixed | Minimal deps |
| All documentation | Markdown | GFM | ATX headers, fenced code blocks |
