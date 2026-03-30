# Level 4 Cheat Sheet — Write Operations & Verification

## Approval Flow

| Choice | Scope | Use When |
|--------|-------|----------|
| **Allow** | This one call | First write to any file |
| **Deny** | This one call | Wrong tool, wrong file, wrong content |
| **Allow for session** | All calls of this tool type | Trusted tool, many edits ahead |
| **Allow permanently for this location** | All future sessions at this directory | Fully trusted tool in a known project (v0.0.407) |
| **One-time path approval** | Single task only | Approve path access without adding to permanent allowed list (v1.0.4) |

## Tool Risk Levels

| Tool | Risk | Notes |
|------|------|-------|
| `view`, `grep`, `glob` | 🟢 Safe | Read-only tools |
| `create` | 🟡 Low | Creates new files only |
| `edit` | 🟡 Low | Modifies existing files |
| `bash` | 🔴 Variable | Read the command! Could do anything |

## Write Commands

```
Create a file called X with content Y          → triggers "create" tool
Fix the bug in search.py                        → triggers "edit" tool
Add a docstring to function Z                   → triggers "edit" tool
Run the tests                                   → triggers "bash" tool
```

## Verification Commands

| Purpose | Command | What It Shows |
|---------|---------|---------------|
| See all changes | `/diff` | Copilot-formatted diff with syntax highlighting for 17 languages (v1.0.5) |
| AI review | `/review` | Quality assessment |
| Raw git diff | `!git diff` | Standard unified diff |
| Changed files | `!git status` | File-level change summary |
| Specific file diff | `!git diff search.py` | Changes in one file |

## Revert Commands

| Scope | Command |
|-------|---------|
| `/rewind` | Undo last turn + revert files | Most convenient for recent mistakes (v1.0.13) |
| Undo/rewind file changes | `Esc Esc` (double-Esc) — rewind to any previous file snapshot (v0.0.393); undo now requires confirmation (v0.0.416) |
| One file | `!git checkout -- search.py` |
| All tracked files | `!git checkout -- .` |
| Remove untracked files | `!git clean -fd` |
| Unstage a file | `!git reset HEAD file.py` |
| Reset entire sample app | `!git checkout -- workshop/level-4/sample-app/` |

## The 7-Step Cycle

```
/plan [task]              ← 1. Plan
Review plan               ← 2. Evaluate
Approve → implement       ← 3. Let Copilot write
/diff                     ← 4. See what changed
/review                   ← 5. AI quality check
!test manually            ← 6. Verify behavior
!git diff                 ← 7. Cross-check
```

## Bug Fix Targets in Sample App

| # | File | Bug | Fix Hint |
|---|------|-----|----------|
| 1 | `search.py` | Case-sensitive search | `.lower()` comparison |
| 2 | `models.py` | Tags not normalized | `.strip().lower()` in `__post_init__` |
| 3 | `export.py` | XSS — raw HTML | `html.escape()` all user content |
| 4 | `export.py` | No `<br>` for newlines | `.replace('\n', '<br>')` |
| 5 | `notes.py` | Pinned notes not sorted first | Sort by `pinned` descending |
| 6 | `notes.py` | Edit bypasses validation | Add validation before save |
| 7 | `storage.py` | No JSON error handling | `try/except json.JSONDecodeError` |
| 8 | `storage.py` | No thread safety | File locking or atomic writes |

## Common Prompts

```
# Understand before fixing
@ search.py  Explain the case-sensitivity bug.

# Plan a fix
/plan Fix the case-sensitive search in search.py.

# Ask for targeted review
/review Are all user inputs properly HTML-escaped?

# Test after fix
!python notes.py add "Test" --tags python
!python notes.py search "PYTHON"
```

## Tips

- **First time editing a file?** Choose **Allow**, not **Allow for session**
- **Run `/diff` after EVERY set of changes** — catches unintended modifications
- **Test manually** even if `/review` says everything looks good
- **Incremental > monolithic** — small changes with `/diff` between each
- **When in doubt, revert** — `git checkout -- .` is always available
