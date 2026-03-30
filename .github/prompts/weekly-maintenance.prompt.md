---
mode: "agent"
description: "All-in-one weekly maintenance routine: check updates, triage, fix, and validate across the entire repository"
---

# Weekly Maintenance

Execute a comprehensive maintenance routine for the workshop repository.
This prompt orchestrates multiple audit and update workflows into a single
session, ensuring nothing falls through the cracks.

## When to Use

Run this prompt:
- Weekly (or bi-weekly) as a proactive maintenance routine
- After a known major Copilot CLI release
- Before a planned workshop delivery
- After merging a batch of content changes

## Phase 1: Discovery — What Changed?

### 1.1 Check Copilot CLI Updates

Perform the `check-cli-updates` workflow:

1. Use **web_search** to find the latest Copilot CLI release notes and changelog
2. Use **fetch_copilot_cli_documentation** to get the current `/help` output
3. Use **web_fetch** on the official docs:
   - `https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli`
   - `https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli`
   - `https://docs.github.com/copilot/concepts/agents/about-copilot-cli`
   - `https://docs.github.com/en/copilot/reference/cli-command-reference`

Capture:
- Current CLI version (stable + prerelease)
- Any new or changed slash commands
- Any new or changed keyboard shortcuts
- Any new or changed CLI flags
- Any new or changed execution modes
- Any model changes
- Any instruction file path changes

### 1.2 Check Repository State

```bash
# Last commit date
git --no-pager log -1 --format="%ai %s"

# Recent changes (last 2 weeks)
git --no-pager log --oneline --since="2 weeks ago"

# Any uncommitted changes?
git --no-pager status --short
```

## Phase 2: Triage — What Needs Attention?

Categorize all findings from Phase 1:

### Priority Matrix

| Priority | Criteria | Action |
|----------|----------|--------|
| 🔴 **Critical** | Factual errors — commands that no longer exist or work differently | Fix immediately |
| 🟠 **Important** | Missing coverage — significant new features not in any exercise | Plan update |
| 🟡 **Moderate** | Outdated wording — descriptions that diverge from upstream but aren't wrong | Schedule update |
| 🟢 **Low** | Cosmetic — minor wording improvements, new blog post links | Batch later |

Present triage results:

```markdown
### Triage Results

| # | Finding | Priority | Affected Files | Action |
|---|---------|----------|---------------|--------|
| 1 | Description | 🔴/🟠/🟡/🟢 | file1.md, file2.md | Fix/Plan/Schedule/Batch |
```

## Phase 3: Apply Fixes

Apply fixes in priority order. For each fix type, use the appropriate workflow:

### 3.1 Guide-Level Fixes (README.md, workshop/README.md)

For 🔴 Critical and 🟠 Important findings affecting the main guides:

1. Read the affected section in README.md
2. Compare against the latest upstream documentation
3. Update the section with accurate information
4. Preserve reference link style and educational tone

### 3.2 Workshop-Level Fixes (Level exercises and cheat sheets)

For findings affecting workshop content:

1. Grep all 9 levels for the affected feature
2. Update each occurrence consistently
3. Verify exercise step numbering is intact
4. Check that cheat sheet tables are formatted correctly

### 3.3 Sample App Checks

If dependency updates are available:

1. Check Level 7 TypeScript dependencies with `npm outdated`
2. Verify Level 1–6 Python 3.8+ compatibility
3. Apply safe updates (minor/patch) if appropriate
4. **Do NOT fix intentional bugs** — verify they're intact after any changes

## Phase 4: Validate — Is Everything Consistent?

After applying fixes, run validation checks:

### 4.1 Cross-Reference Validation

Check all links and references:

```bash
# Internal links — check if targets exist
grep -rohn '\[.*\](\.\.*/[^)]*)\|(\.\./[^)]*)' workshop/ --include="*.md" | head -20

# Reference link definitions in README
grep -n '^\[' README.md | tail -20
```

### 4.2 Exercise Table Sync

Verify main README exercise tables match level content:

```bash
# Count exercises per level
for level in 1 2 3 4 5 6 7 8 9; do
  count=$(grep -c '^## Exercise' "workshop/level-$level/README.md" 2>/dev/null || echo 0)
  echo "Level $level: $count exercises"
done
```

All levels must have exactly 12 exercises.

### 4.3 Bug Preservation

Quick-verify intentional bugs are intact:

```bash
# Level 5: Check that divide still doesn't raise ValueError
grep -A5 'def divide' workshop/level-5/sample-app/mathlib/calculator.py 2>/dev/null

# Level 6: Check that test_validator.py is still missing
ls workshop/level-6/sample-app/tests/test_validator.py 2>/dev/null && echo "EXISTS (unexpected)" || echo "Missing (expected)"
```

### 4.4 Self-Assessment Alignment

```bash
# Count self-assessment items per level
for level in 1 2 3 4 5 6 7 8 9; do
  count=$(grep -c '^\s*[0-9]\+\.' "workshop/level-$level/README.md" 2>/dev/null | tail -1)
  echo "Level $level: self-assessment items in file"
done
```

### 4.5 Extension Verification (Level 9)

If Level 9 content exists, verify extension-related teaching points:

```bash
# Check Level 9 extension scaffold is intact
ls workshop/level-9/sample-app/.mcp.json 2>/dev/null && echo "MCP config present" || echo "Missing (check if expected)"
ls workshop/level-9/sample-app/CLAUDE.md 2>/dev/null && echo "CLAUDE.md present" || echo "Missing (check if expected)"

# Verify placeholder tool is still a TODO (not accidentally completed)
grep -l 'TODO' workshop/level-9/sample-app/ -r 2>/dev/null
```

## Phase 5: Report

Produce a comprehensive summary:

```markdown
## Weekly Maintenance Report

**Date:** YYYY-MM-DD
**CLI Version:** vX.Y.Z (stable) / vX.Y.Z (prerelease)
**Repository Last Commit:** SHA — "message" (date)

---

### 📡 Phase 1: Discovery

| Category | Status | Details |
|----------|--------|---------|
| CLI version | ✅ Current / ⚠️ New release | vX.Y.Z |
| Slash commands | ✅ No changes / ⚠️ N changes | List changes |
| Keyboard shortcuts | ✅ No changes / ⚠️ N changes | List changes |
| CLI flags | ✅ No changes / ⚠️ N changes | List changes |
| Models | ✅ No changes / ⚠️ N changes | List changes |

### 🔍 Phase 2: Triage

| Priority | Count | Items |
|----------|-------|-------|
| 🔴 Critical | N | Brief list |
| 🟠 Important | N | Brief list |
| 🟡 Moderate | N | Brief list |
| 🟢 Low | N | Brief list |

### 🔧 Phase 3: Fixes Applied

| # | Fix | Files Changed | Type |
|---|-----|--------------|------|
| 1 | Description | file.md | Guide/Workshop/Sample |

### ✅ Phase 4: Validation

| Check | Status | Notes |
|-------|--------|-------|
| Cross-references | ✅ All valid / ❌ N broken | Details |
| Exercise count | ✅ 108 total (12 × 9) | — |
| Exercise table sync | ✅ In sync / ❌ N mismatches | Details |
| Intentional bugs | ✅ All intact / ❌ N missing | Details |
| Self-assessment | ✅ All aligned / ❌ N misaligned | Details |

### 📋 Deferred Items

Items not addressed this session (🟡 Moderate and 🟢 Low priority):

| # | Item | Priority | Suggested Prompt |
|---|------|----------|-----------------|
| 1 | Description | 🟡 | `workshop-refresh` |

---

### 🏁 Overall Status: ✅ Healthy / ⚠️ Needs Attention / ❌ Issues Found
```

## Notes

- This prompt is designed for a **single comprehensive session**. For focused
  work on specific areas, use the individual prompts instead:
  - `check-cli-updates` — CLI update discovery only
  - `upstream-diff-analysis` — Deep doc comparison only
  - `guide-refresh` — README updates only
  - `workshop-refresh` — Exercise updates only
  - `sample-app-upgrade` — Dependency updates only
  - `cross-reference-validate` — Link validation only
  - `verify-bugs` — Bug preservation only
  - `sync-readme` — Exercise table sync only
  - `review-level` — Single level quality audit
- If Phase 1 reveals no changes, skip Phases 2–3 and go straight to Phase 4
  (validation is always valuable)
- Keep the report as a reference for the next maintenance session
