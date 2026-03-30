---
mode: "agent"
description: "Batch-update exercises and cheat sheets across all 9 levels for specific Copilot CLI changes"
---

# Workshop Refresh

Apply a specific Copilot CLI change across all 9 workshop levels, updating
exercises and cheat sheets consistently. Use this prompt **after** running
`check-cli-updates` or `upstream-diff-analysis` to propagate discovered
changes into the workshop content.

## Input: What Changed?

Describe the CLI change to propagate. Examples:

- "The `/plan` command was renamed to `/blueprint`"
- "A new slash command `/fleet` was added for parallel subagent execution"
- "Autopilot mode graduated from experimental to stable"
- "The `--yolo` flag was deprecated in favor of `--allow-all`"
- "Default model changed from Claude Sonnet 4.5 to Claude Sonnet 4.6"

If you have output from `check-cli-updates`, reference the specific findings.

**CLI change:** {{change_description}}

## Step 1: Find All Affected Content

Search for all references to the changed feature across the workshop:

```bash
# Search all workshop markdown files
grep -rn "SEARCH_TERM" workshop/ --include="*.md"

# Also search the main README for exercise table references
grep -n "SEARCH_TERM" README.md
```

Organize findings by level:

| Level | File | Line | Current Content | Needs Update? |
|-------|------|------|----------------|---------------|
| 1 | README.md | NN | "text" | Yes/No |
| 1 | CHEATSHEET.md | NN | "text" | Yes/No |
| 2 | README.md | NN | "text" | Yes/No |
...

## Step 2: Assess Impact per Level

For each affected level, determine:

1. **Exercise impact** — Does the change affect exercise steps that learners
   follow? These are high priority.
2. **Cheat sheet impact** — Does the change affect command/shortcut tables?
   These are high priority.
3. **Contextual mention** — Is the feature mentioned in explanatory text but
   not in actionable steps? Lower priority.
4. **Progression impact** — Does the change affect which level introduces this
   feature? This may require reordering.

### Level-Specific Considerations

| Level | Sensitivity | Why |
|-------|------------|-----|
| **1** | 🔴 High | First exposure — wrong commands here create confusion for all subsequent levels |
| **2** | 🟠 Medium | Understanding-focused; mostly explanatory references |
| **3** | 🟠 Medium | `/plan` is central to this level |
| **4** | 🟠 Medium | `/diff`, `/review`, approval flow are core |
| **5** | 🟡 Lower | Focused on `bash` tool execution, less command variety |
| **6** | 🟠 Medium | Full SDLC cycle references many commands |
| **7** | 🔴 High | Configuration-focused — instruction file paths, MCP, session management |
| **8** | 🔴 High | Permission flags, programmatic mode, advanced features |

## Step 3: Apply Updates

For each affected file, make the update. Follow these rules:

### Exercise Updates
- Update the specific step text (`**N.M**` description and prompt)
- Update the `> Expected:` text if the expected output changed
- Update the `### Key Concept` if the concept explanation references the change
- Update the `### ✅ Checkpoint` if it mentions the changed feature
- **Do NOT change exercise numbering or structure**

### Cheat Sheet Updates
- Update command/shortcut table entries
- Add new entries for new commands/features
- Remove entries for deprecated/removed features
- Maintain table formatting consistency

### Cross-Level Consistency
- If a feature is first introduced in Level N, verify the introduction is
  accurate before updating references in Levels N+1 through 9
- If the change affects the learning progression (e.g., a feature moved from
  experimental to stable), consider whether it should be introduced earlier

## Step 4: Preserve Intentional Bugs

**CRITICAL:** After making updates, verify that no intentional bugs were
accidentally fixed. Read `.github/copilot-instructions.md` for the bug catalog.

Quick verification checklist:
- [ ] Level 3/4: All 8 Quick Notes CLI bugs still present
- [ ] Level 5: All 6 test failures + lint issues still present
- [ ] Level 6: All 5 URL Shortener issues still present

If an update inadvertently touched a buggy file, verify the bug is intact.

## Step 5: Verify Progression Coherence

After all updates, verify the learning progression still makes sense:

1. **Read Level 1 CHEATSHEET.md** — Does it only reference features taught
   at Level 1? (No forward references to advanced features)
2. **Scan each level** — Are features introduced in the right order?
3. **Check self-assessment items** — Do they still align with exercises?

## Output

```markdown
## Workshop Refresh Report

**CLI Change Applied:** {{change_description}}
**Levels Affected:** N of 9
**Files Modified:** N

### Changes by Level

#### Level 1
| File | Line | Before | After |
|------|------|--------|-------|
| README.md | NN | "old text" | "new text" |
| CHEATSHEET.md | NN | "old text" | "new text" |

#### Level 2
...

### Bug Preservation Check
| Level | Bugs Expected | Bugs Verified | Status |
|-------|--------------|---------------|--------|
| 3/4 | 8 | 8 | ✅ All intact |
| 5 | 6+lint | 6+lint | ✅ All intact |
| 6 | 5 | 5 | ✅ All intact |

### Progression Check
- [ ] No forward references to features not yet introduced
- [ ] Feature introduction order is logical
- [ ] Self-assessment items align with exercises

### Next Steps
- [ ] Run `sync-readme` to update main README exercise tables if titles changed
- [ ] Run `cross-reference-validate` to verify all links still work
- [ ] Run `review-level` on the most heavily modified levels
```
