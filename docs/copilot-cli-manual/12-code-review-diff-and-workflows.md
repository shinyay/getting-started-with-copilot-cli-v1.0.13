# Chapter 12: Code Review, Diff & Development Workflows

Copilot CLI is not just a code generator — it is a complete development
environment with built-in tools for reviewing changes, analyzing diffs,
integrating with git workflows, delegating tasks, and orchestrating complex
multi-step development processes. This chapter covers the full suite of review
and workflow capabilities, from the `/diff` viewer to the `/delegate` pipeline
that hands work off to Copilot coding agent in the cloud.

> 📋 This chapter reflects CLI features through **v1.0.x**. Run `/changelog` to
> verify which features are available in your installed version.

---

## `/diff` — Reviewing Changes

The `/diff` command displays all file changes made during the current Copilot CLI
session. Unlike raw `git diff`, this is a purpose-built visual diff viewer
designed for reviewing AI-assisted edits in context.

```
> /diff
```

When invoked, `/diff` opens a full-screen diff viewer that shows every file
Copilot has created or modified since the session began.

> 💡 Since v0.0.389, `/diff` tracks changes from the **session start**, not just
> the last commit. This means you see everything Copilot has touched, even if
> you have not staged or committed yet.

### Version History

| Version | Enhancement |
|---------|-------------|
| v0.0.335 | File diffs shown by default in timeline |
| v0.0.364 | Syntax highlighting for diffs |
| v0.0.370 | Respects your configured git pager (delta, diff-so-fancy) |
| v0.0.389 | Reviews all changes since session start |
| v0.0.392 | Diffs shown in timeline when expanded |
| v0.0.396 | Shows changes from entire repo when run from subdirectory |
| v0.0.399 | Enhanced visual indicators and scroll acceleration |
| v0.0.400 | Carousel navigation — up to 5 files at a time |
| v0.0.401 | Dual column layout with accurate line numbers |
| v0.0.407 | No longer flickers when navigating between files |
| v0.0.409 | Full-screen in alt-screen mode |
| v0.0.422 | Long lines no longer overflow; mouse scroll support; `color.diff=always` fix |
| v0.0.423 | CRLF line endings display cleanly on Windows |
| v1.0.12 | Intra-line diff highlighting — individual changed characters within lines are highlighted |

### Visual Features

The diff viewer provides a rich visual experience built for readability:

**Full-screen alt-screen mode** (since v0.0.409): The diff viewer takes over the
entire terminal using the alternate screen buffer. When you exit, your previous
terminal content is restored cleanly — no scrollback pollution.

**Dual-column layout** (since v0.0.401): Additions and deletions are displayed
side by side with accurate line numbers on both columns. This makes it easy to
trace how code moved or changed:

```
  old.py (lines 10-15)            │  new.py (lines 10-16)
  ────────────────────────────────│────────────────────────────────
  10  def calculate(x, y):        │ 10  def calculate(x, y):
  11      return x + y            │ 11      if y == 0:
                                  │ 12          raise ValueError(...)
                                  │ 13      return x + y
  12                              │ 14
  13  def main():                 │ 15  def main():
```

**Carousel navigation** (since v0.0.400): When your diff spans many files,
the viewer groups them into pages of up to 5 files. Navigate between pages with
arrow keys or `j`/`k` bindings:

| Key | Action |
|-----|--------|
| `↑` / `k` | Previous file |
| `↓` / `j` | Next file |
| `←` / `h` | Previous page of files |
| `→` / `l` | Next page of files |
| `q` / `Esc` | Exit diff viewer |
| Mouse scroll | Scroll within file (since v0.0.422) |

**Syntax highlighting** (since v0.0.364): Diffs are syntax-highlighted according
to the file's language, not just colored as raw additions/deletions. This means
keywords, strings, and comments are visually distinct within the diff context.

**Git pager integration** (since v0.0.370): If you have configured a custom git
pager such as `delta` or `diff-so-fancy`, Copilot CLI respects that configuration:

```bash
# Your git config is automatically detected
git config --global core.pager delta
git config --global interactive.diffFilter "delta --color-only"
```

> ⚠️ If `git config color.diff` is set to `always`, earlier versions could
> produce garbled output. This was fixed in v0.0.422.

### Interactive Features

Beyond passive viewing, `/diff` supports interactive annotation:

**Line-specific commenting** (since v0.0.395): While viewing a diff, you can
select a specific line and add a comment. This creates a feedback point that
Copilot can act on — for example, "this null check is wrong" or "add error
handling here":

```
> /diff
# Navigate to the line, then press 'c' to comment
# Type your feedback and press Enter
# Copilot receives the comment as context for follow-up prompts
```

> 💡 Line comments in `/diff` feed directly into the conversation context. After
> commenting, you can ask Copilot to "address all my diff comments" and it will
> have full awareness of each annotation and its location.

### Subdirectory Behavior

Since v0.0.396, running `/diff` from a subdirectory still shows changes across
the **entire repository**, not just the current directory. This prevents the
common mistake of missing changes in other parts of the project.

```
# Even from a subdirectory, all repo changes appear
~/project/src/utils $ copilot
> /diff
# Shows changes in src/, tests/, docs/, etc.
```

---

## `/review` — AI-Powered Code Review

The `/review` command launches a specialized code review agent that analyzes your
changes with an extremely high signal-to-noise ratio. It only surfaces issues
that genuinely matter.

```
> /review
```

Since v0.0.388, `/review` runs a built-in Code-review agent powered by the
Sonnet model. This agent reads every changed file, understands the surrounding
context, and produces review comments that focus exclusively on correctness and
safety.

### What `/review` Looks For

| Category | What It Detects | Example |
|----------|----------------|---------|
| **Bugs** | Off-by-one errors, null/undefined dereferences, race conditions | `array[length]` instead of `array[length - 1]` |
| **Security** | SQL injection, XSS, hardcoded secrets, path traversal | `query("SELECT * FROM users WHERE id = " + input)` |
| **Logic errors** | Wrong conditions, missing edge cases, inverted checks | `if (x > 0)` when it should be `if (x >= 0)` |
| **Performance** | N+1 queries, unnecessary allocations, unbounded loops | Querying the database inside a loop |
| **Data integrity** | Missing validation, unchecked type coercion | Parsing user input without error handling |
| **Resource leaks** | Unclosed file handles, database connections, sockets | `open(file)` without `with` block or `finally` |

### What `/review` Deliberately Ignores

The review agent is opinionated about staying **high-signal**. It will never
comment on:

| Ignored Category | Rationale |
|-----------------|-----------|
| Code style and formatting | Use a linter/formatter instead |
| Naming conventions | Subjective and project-specific |
| Comment quality or quantity | Not a correctness issue |
| Minor refactoring suggestions | Noise that obscures real problems |
| Import ordering | Handled by tooling (isort, ESLint) |
| Whitespace and indentation | Handled by formatters (Black, Prettier) |

> 💡 This philosophy means that if `/review` flags something, it is almost
> certainly worth your attention. Treat every review comment as actionable.

### Handling Large Changesets

Since v0.0.400, `/review` intelligently handles large diffs:

- **File limit**: Reviews up to 100 changed files per invocation
- **Artifact exclusion**: Automatically skips build artifacts, compiled output,
  lock files, and generated code
- **Priority ordering**: Reviews the most critical files first (source code
  before configuration, application code before tests)

```
> /review
Reviewing 47 changed files...
Skipping 12 generated/build files...

Found 3 issues:

1. [BUG] src/auth.ts:42
   Missing null check on user object before accessing .role property.
   If the database returns null, this will throw a TypeError.

2. [SECURITY] src/api/routes.ts:118
   User input is interpolated directly into SQL query string.
   Use parameterized queries to prevent SQL injection.

3. [LOGIC] src/utils/validator.ts:67
   Boundary condition: isEmpty() returns true for whitespace-only strings,
   but the caller expects it to return false for " ".
```

### Review in a Workflow Context

The most effective pattern is to run `/review` **after** making changes but
**before** committing:

```
> Implement the user authentication middleware

# Copilot makes changes...

> /diff
# Visual inspection of changes

> /review
# AI analysis of changes

> Address the security issue from the review

# Copilot fixes the flagged issue

> /review
# Confirm all issues resolved
```

> 📋 See [Workflow 4: Code Review Before PR](#workflow-4-code-review-before-pr)
> later in this chapter for the complete end-to-end pattern.

---

## File Editing Workflow

When Copilot creates or modifies files during a session, it uses a structured
edit tool that tracks every change with full undo support.

### How Edits Work

1. Copilot identifies the file and the specific lines to change
2. The edit is applied and recorded as a **session snapshot**
3. The diff appears in the conversation timeline (since v0.0.335)
4. You can expand the timeline entry to see the full diff (since v0.0.392)
5. Multiple pending edits can be approved simultaneously (since v0.0.375)

### Timeline Integration

Every file operation appears in the session timeline with a visual diff. Since
v0.0.392, expanding a timeline entry shows the exact changes:

```
 [12:34:05] Created src/middleware/auth.ts (+45 lines)
 [12:34:12] Modified src/routes/api.ts (3 hunks, +12 -4)
 [12:34:18] Modified src/app.ts (+2 -0)
```

> 💡 File operations no longer time out waiting for permission confirmation
> (fixed in v0.0.360). If you have file write permissions enabled, edits apply
> immediately.

---

## Undo / Rewind with Double-Esc

One of the most powerful safety features in Copilot CLI is the ability to
**rewind file changes** to any previous snapshot in the session.

### How It Works

Press `Esc` twice quickly (`Double-Esc`) to open the rewind interface. This
presents a list of session snapshots, each representing the state of your files
at a specific point in the conversation:

```
Rewind to a previous state:

  [3] After "Add error handling" (4 files affected)
  [2] After "Create auth middleware" (2 files affected)
  [1] After "Set up project structure" (5 files affected)
  [0] Session start (clean state)

Select snapshot [0-3]:
```

| Version | Enhancement |
|---------|-------------|
| v0.0.393 | Double-Esc undo introduced |
| v0.0.395 | Clear warning in non-git repos or repos without any commits |
| v0.0.396 | Shows accurate count of affected files per snapshot |
| v0.0.416 | Confirmation prompt required before rewind executes |

> ⚠️ Rewinding is **destructive** to file contents — it restores files to the
> selected snapshot state. Since v0.0.416, a confirmation prompt prevents
> accidental rewinds. However, conversation history is preserved, so you can
> re-apply changes by asking Copilot to repeat earlier steps.

### Safety in Non-Git Repos

Since v0.0.395, running rewind in a directory that is not a git repository (or a
git repo with no commits) produces a clear warning:

```
⚠️  This directory is not a git repository. Rewind will modify files
    with no way to recover the original state via git. Proceed? [y/N]
```

> 💡 Even in a git repo, rewind only affects **uncommitted** Copilot changes.
> Your committed history remains untouched.

### The `/rewind` Slash Command

Since **v1.0.13**, the `/rewind` command provides a lightweight alternative to
`Double-Esc`. It undoes the last conversation turn and reverts all associated
file changes in a single action — no snapshot picker required. This is
especially useful during iterative code changes where you want to quickly undo
the agent's last edit and try a different approach.

```
> /rewind
```

> 💡 Use `/rewind` for quick single-turn undo during active coding. Use
> `Double-Esc` when you need to jump back to an arbitrary earlier snapshot.

---

## Git Integration

Copilot CLI integrates deeply with your local git repository, providing
awareness of branch state, change tracking, and commit authorship.

### Automatic Co-authored-by Trailer

Since v0.0.410, when you create a git commit during a Copilot CLI session,
the commit message automatically includes a co-authorship trailer:

```
feat: add user authentication middleware

Implement JWT-based auth middleware with role checking
and token refresh support.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

This trailer ensures that Copilot's contribution is properly attributed in the
git history and shows up in GitHub's contributor graphs.

**Disabling the trailer** (since v0.0.411): If you prefer not to include the
co-author trailer, set the `include_coauthor` config to `false`:

```bash
copilot config set include_coauthor false
```

### Status Bar Integration

The Copilot CLI status bar displays git-related information:

| Element | Description | Since |
|---------|-------------|-------|
| Branch name | Current checked-out branch | — |
| Change indicator | Number of staged/unstaged changes | — |
| PR reference | Clickable link to associated PR | v0.0.421 |

> 💡 Git status updates are triggered **on-demand** (since v0.0.394), not by
> polling. This means Copilot reads git state when it needs to, avoiding
> unnecessary filesystem operations in large repositories.

---

## `/delegate` — Async Task Delegation

The `/delegate` command hands off work to the **Copilot coding agent** running
on GitHub's infrastructure. This is the bridge between local Copilot CLI work
and cloud-powered autonomous coding.

```
> /delegate Add comprehensive test coverage for the auth module
```

### How Delegation Works

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Local Session   │───▶│  GitHub Branch    │───▶│  Coding Agent   │
│                  │    │  + PR Created     │    │  (Cloud)        │
│  - Your changes  │    │  - Auto-committed │    │  - Reads PR     │
│  - Your context  │    │  - Description    │    │  - Makes changes│
│  - Your prompt   │    │  - Co-author tag  │    │  - Pushes commits│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

1. **Prepare**: Any unstaged local changes are committed to a new branch
2. **Push**: The branch is pushed to the remote repository
3. **Open PR**: A pull request is created with a description derived from
   your conversation context and optional prompt
4. **Handoff**: The Copilot coding agent picks up the PR and works on it
   asynchronously in the cloud
5. **Resume**: You can continue working locally or resume the session later

### Usage Patterns

**Basic delegation** — delegate with conversation context:
```
> I've set up the basic route structure for the events API.
> The models are defined but services aren't implemented yet.
> /delegate Implement the event services with full CRUD operations
```

**Shortcut with `&` prefix** (since v0.0.384):
```
> & Add input validation to all API endpoints
```

**Delegation with no local changes** (since v0.0.354): You can delegate even
when you have made no local changes. Copilot creates the branch from the current
HEAD:

```
> /delegate Refactor the database layer to use connection pooling
```

### Multi-Remote Repositories

Since v0.0.422, if your repository has multiple remotes configured, `/delegate`
prompts you to select which remote to push to:

```
> /delegate Add caching layer

Multiple remotes detected:
  [1] origin  → github.com/yourorg/project.git
  [2] upstream → github.com/upstream/project.git

Push to remote [1-2]: 1
```

### Enterprise Support

Since v0.0.394, `/delegate` works with **GitHub Enterprise Cloud** (GHE Cloud)
instances. The CLI automatically detects your enterprise endpoint from git remote
configuration.

> ⚠️ `/delegate` requires that Copilot coding agent is enabled for your
> repository or organization. If it is not enabled, the command will display
> an error with instructions for your administrator.

### Version History

| Version | Enhancement |
|---------|-------------|
| v0.0.353 | Initial `/delegate` command |
| v0.0.354 | Works when no local changes exist |
| v0.0.384 | `&` prefix shortcut |
| v0.0.394 | Accepts optional prompt; uses conversation context; GHE Cloud support |
| v0.0.422 | Prompts for target remote in multi-remote repos |

---

## `/research` — Deep Research Investigation

The `/research` command (since v0.0.417) launches a deep research agent that
investigates topics using GitHub search, web sources, and repository context.

```
> /research What are the best practices for rate limiting in Express.js?
```

The research agent produces a structured, exportable report that includes
sources, code examples, and recommendations. After research completes, you can
share the results using `/share`.

> 📋 See [Chapter 5: Complete Slash Commands Reference](./05-slash-commands-reference.md)
> for the full command syntax and options.

---

## IDE Integration with `/ide`

Since v0.0.409, the `/ide` command connects your Copilot CLI session to a
VS Code workspace, enabling bidirectional communication between the terminal
and your editor.

```
> /ide
Connected to VS Code workspace: ~/project
```

### Features

| Feature | Description | Since |
|---------|-------------|-------|
| File selection sync | Status bar shows currently selected file in VS Code | v0.0.410 |
| Shift+Enter | Send selected code from VS Code to Copilot CLI | v0.0.421 |
| Ctrl+Enter | Execute Copilot suggestion in VS Code terminal | v0.0.421 |
| WSL/Devcontainer support | Opens plan files correctly in remote VS Code | v0.0.396 |

> 💡 IDE integration is especially powerful when combined with `/diff` — you can
> review changes in Copilot CLI's diff viewer while simultaneously seeing the
> files open in VS Code with full IntelliSense.

---

## LSP Integration — Language Server Protocol

Copilot CLI uses Language Server Protocol (LSP) to provide code intelligence —
go-to-definition, find-references, hover information, and diagnostics. This
makes the explore agent significantly more accurate when navigating codebases.

> ⚠️ Since v0.0.400, LSP servers are **not bundled** with Copilot CLI. You must
> install language servers separately and configure them in your LSP config file.

### Configuration Hierarchy

LSP configuration follows a layered hierarchy, where more specific configurations
override broader ones:

| Level | File | Scope |
|-------|------|-------|
| User-global | `~/.copilot/lsp-config.json` | All projects for this user |
| Repository | `.github/lsp.json` | This repository only |
| Plugin-bundled | Included in plugin package | Plugin-specific defaults |

### Example: TypeScript LSP Configuration

```json
{
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "fileExtensions": {
        ".ts": "typescript",
        ".tsx": "typescriptreact",
        ".js": "javascript",
        ".jsx": "javascriptreact"
      }
    }
  }
}
```

### Example: Python LSP Configuration

```json
{
  "lspServers": {
    "python": {
      "command": "pylsp",
      "args": [],
      "fileExtensions": {
        ".py": "python"
      }
    }
  }
}
```

### Timeout Configuration

| Version | Default Timeout | Notes |
|---------|----------------|-------|
| < v0.0.412 | 30 seconds | Fixed, not configurable |
| v0.0.412 | 30 seconds | Now configurable via LSP config |
| v0.0.413+ | 90 seconds | Default increased for large projects |

> 💡 The explore agent automatically uses LSP when available, providing far more
> accurate responses for questions like "find all callers of this function" or
> "what type does this variable have?"

---

## Built-in Search Tools

Copilot CLI bundles fast search tools that work without any external
dependencies. These are used internally by the explore agent and are also
available as standalone tools.

### `grep` — Content Search (ripgrep)

Bundled since v0.0.355, the `grep` tool is built on
[ripgrep](https://github.com/BurntSushi/ripgrep) and provides extremely fast
content search:

```
# Copilot uses grep internally when you ask:
> Find all files that import the auth middleware
```

Key characteristics:

| Feature | Detail |
|---------|--------|
| Engine | ripgrep (rg) |
| Speed | Searches large repos in milliseconds |
| Hidden files | Finds dotfiles and hidden directories (since v0.0.389) |
| Regex | Full PCRE2 regex support |
| Binary | Skips binary files by default |
| Gitignore | Respects `.gitignore` patterns |

### `glob` — File Pattern Matching

Also bundled since v0.0.355, the `glob` tool finds files by name patterns:

```
# Copilot uses glob internally when you ask:
> List all TypeScript test files in the project
```

Common patterns:

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files |
| `src/**/*.test.ts` | Test files under src/ |
| `*.{js,ts}` | JavaScript and TypeScript in current dir |
| `**/README.md` | All README files at any depth |

> 💡 Since v0.0.413, code search performance has been significantly improved for
> large repositories with 10,000+ files.

---

## Development Workflow Examples

The following workflows demonstrate how to combine Copilot CLI features into
complete development processes. Each workflow shows the commands and
interactions from start to finish.

### Workflow 1: Fix a Bug

A complete bug-fix workflow from investigation to verified fix.

```
# 1. Start Copilot CLI in the project
$ copilot

# 2. Investigate the bug
> Users report that the search endpoint returns 500 when the query
  contains special characters. Investigate the issue.

# Copilot uses grep/LSP to find the search handler,
# traces the input flow, identifies missing sanitization

# 3. Review the plan
> /plan

# 4. Apply the fix
> Fix the search input sanitization issue

# 5. Verify the fix
> Run the existing tests for the search module

# 6. Review what changed
> /diff

# 7. AI code review
> /review

# 8. Commit
> Commit these changes with a descriptive message
```

> 💡 Notice how the workflow naturally flows through investigation → planning →
> implementation → verification → review → commit. Each step builds on the
> context from previous steps.

### Workflow 2: Add a Feature with Plan Mode

Using plan mode for a larger feature that requires deliberate design.

```
# 1. Enter plan mode with Ctrl+P or use the flag
$ copilot -p

# 2. Describe the feature
> Add rate limiting to the API with per-user quotas.
  Support 100 requests per minute for free users and
  1000 per minute for premium users.

# Copilot creates a structured plan without making changes

# 3. Review and iterate on the plan
> Add Redis caching for the rate limit counters

# 4. Switch to implementation (Ctrl+P to toggle)
# Copilot executes the plan step by step

# 5. Review the full implementation
> /diff

# 6. Run the test suite
> Run all tests to make sure nothing is broken

# 7. AI review before committing
> /review

# 8. Commit with context
> Commit with message "feat: add per-user rate limiting with Redis"
```

### Workflow 3: Refactor with Parallel Subagents

For large refactoring tasks that span many files, use autopilot fleet mode
to parallelize the work across multiple subagents.

```
# 1. Start in autopilot mode
$ copilot --autopilot

# 2. Describe the refactoring
> Refactor all API route handlers to use the new AppError class
  instead of throwing raw Error objects. Update the corresponding
  tests to verify AppError properties.

# Copilot spawns parallel subagents:
#   Agent 1: routes/events.ts + tests/events.test.ts
#   Agent 2: routes/users.ts + tests/users.test.ts
#   Agent 3: routes/auth.ts + tests/auth.test.ts

# 3. Review all changes
> /diff

# 4. Run the full test suite
> Run all tests

# 5. Final review
> /review
```

> ⚠️ Fleet mode makes many changes in parallel. Always run `/review` and your
> test suite before committing to catch any inconsistencies between the parallel
> changes.

### Workflow 4: Code Review Before PR

The gold-standard workflow for submitting high-quality pull requests.

```
# 1. Make your changes (interactive or autopilot)
> Implement the event notification system with email and webhook support

# 2. Self-review with /diff
> /diff
# Navigate through all changes, add line comments on anything
# that looks off

# 3. Address your own comments
> Fix the issues I commented on in the diff

# 4. AI review
> /review
# Read each finding carefully

# 5. Address review findings
> Address the security issue flagged in the review

# 6. Re-review to confirm
> /review
# Should return clean (no issues found)

# 7. Run tests one final time
> Run the complete test suite

# 8. Delegate to open the PR
> /delegate Open PR with a detailed description of the notification system
```

This workflow ensures that by the time a PR is opened, it has been:
- Visually inspected (via `/diff`)
- Self-reviewed with inline comments
- AI-reviewed for bugs and security issues
- Verified by the test suite
- Properly described in the PR body

---

## Quick Reference: Review & Workflow Commands

| Command | Purpose | Since |
|---------|---------|-------|
| `/diff` | Open full-screen diff viewer for session changes | v0.0.389 |
| `/review` | Run AI code review agent on changes | v0.0.388 |
| `/delegate` | Hand off work to Copilot coding agent (cloud) | v0.0.353 |
| `/research` | Launch deep research investigation | v0.0.417 |
| `/ide` | Connect to VS Code workspace | v0.0.409 |
| `/lsp` | Manage Language Server Protocol configuration | v0.0.400 |
| `/share` | Share conversation or research results | — |
| `Double-Esc` | Rewind file changes to a previous snapshot | v0.0.393 |
| `/rewind` | Undo last turn and revert associated file changes | v1.0.13 |
| `&` (prefix) | Shortcut for `/delegate` | v0.0.384 |

---

> 📋 The review and workflow tools covered in this chapter form the backbone of
> productive Copilot CLI usage. Mastering the `/diff` → `/review` → `/delegate`
> pipeline will dramatically improve both the quality and speed of your
> development workflow.

Next: [Chapter 13: AI Models & Reasoning](./13-ai-models-and-reasoning.md)
