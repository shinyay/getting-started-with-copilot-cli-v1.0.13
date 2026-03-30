---
mode: "agent"
description: "Validate all internal links, reference links, external URLs, and cross-references across the repository"
---

# Cross-Reference Validate

Comprehensively verify that every link, reference, and cross-reference in the
repository resolves correctly. This goes far beyond `sync-readme` (which only
checks exercise table alignment) to cover all link types across all files.

## Link Types to Validate

| Type | Syntax | Example | Where Found |
|------|--------|---------|------------|
| Inline links | `[text](path)` | `[Level 1](workshop/level-1/)` | All .md files |
| Reference links | `[text][N]` + `[N]: URL` | `([Docs][2])` | README.md |
| Anchor links | `[text](#anchor)` | `[Installation](#installation)` | README.md |
| Relative paths | `../level-N/` | `../level-2/README.md` | Workshop .md files |
| External URLs | `https://...` | Official docs, GitHub repos | README.md, exercises |
| Image links | `![alt](url)` | Screenshots, diagrams | Any .md file |
| Code references | paths in text | `.github/copilot-instructions.md` | Exercises, instructions |

## Step 1: Scan All Markdown Files

Build a complete inventory of links:

```bash
# Find all markdown files
find . -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*"
```

For each markdown file, extract:
1. All inline links `[text](target)`
2. All reference link usages `[text][ref]`
3. All reference link definitions `[ref]: URL`
4. All anchor links `[text](#anchor)`
5. All bare URLs `https://...`
6. All file path references in text (e.g., "See `.github/copilot-instructions.md`")

## Step 2: Validate Internal Links

### 2.1 File Links

For every `[text](path)` where path is a relative file/directory:

```bash
# Check if the target exists
# Account for the source file's directory when resolving relative paths
```

Report:
| Source File | Link Text | Target Path | Resolved Path | Exists? |
|------------|-----------|-------------|---------------|---------|
| README.md | Level 1 | workshop/level-1/ | workshop/level-1/ | ✅/❌ |

### 2.2 Anchor Links

For every `[text](#anchor-name)`:
- Verify the anchor exists in the same file (or target file if cross-file)
- Markdown anchors are generated from headings: lowercase, spaces→hyphens,
  special chars removed

### 2.3 Reference Link Definitions

For `README.md` specifically (which uses reference-style links):
- Every `[N]` usage must have a matching `[N]: URL` definition
- Every `[N]: URL` definition should be used at least once
- No duplicate definitions

## Step 3: Validate External URLs

For every external URL (https://...):

Use **web_fetch** to check each unique URL:
- HTTP 200 = ✅ Valid
- HTTP 301/302 = ⚠️ Redirect (update to final URL)
- HTTP 404 = ❌ Broken
- HTTP 403/timeout = ⚠️ May be valid but restricted (note it)

**Priority URLs to check:**

| Priority | URLs | Why |
|----------|------|-----|
| 🔴 High | README.md reference links `[1]`–`[12]` | Most visible; learners click these |
| 🔴 High | Official GitHub docs links | May restructure without redirects |
| 🟠 Medium | Blog post links | Generally stable but may move |
| 🟡 Lower | npm package links | Very stable |

> ⚠️ Rate limiting: Space out web_fetch calls. Check unique URLs only
> (deduplicate first).

## Step 4: Validate Cross-Level References

### 4.1 Level-to-Level References

Check that references between levels are accurate:

```bash
# Find cross-level references
grep -rn 'level-[0-9]' workshop/ --include="*.md" | grep -v '/sample-app/'
```

For each reference:
- Does the target level exist?
- Does the referenced section/exercise exist in that level?
- Is the level number correct in context?

### 4.2 "What's Next" Sections

Each level README should have a "What's Next" section pointing to the next level:
- Level N should reference Level N+1
- Level 9 should have a capstone/conclusion (no next level)

### 4.3 "Unlike Level N-1" Paragraphs

Each level (2–9) should have a comparison paragraph referencing the previous level:
- Verify the level number is correct
- Verify the comparison is accurate

## Step 5: Validate Configuration File References

Check that references to configuration files in exercises are accurate:

```bash
# Find references to .github/ files
grep -rn '\.github/' workshop/ --include="*.md"

# Find references to instruction files
grep -rn 'copilot-instructions\|AGENTS\.md\|instructions/' workshop/ --include="*.md"
```

For each reference:
- Does the file/path exist?
- Is the description of what the file does accurate?

## Step 6: Validate Prompt and Skill References

Check that references to prompts and skills are accurate:

```bash
# Find prompt references
grep -rn 'prompt' . --include="*.md" -l | grep -v node_modules | grep -v '.git'

# Find skill references
grep -rn 'skill' . --include="*.md" -l | grep -v node_modules | grep -v '.git'
```

- Verify prompt files referenced in README.md exist in `.github/prompts/`
- Verify skill directories referenced exist in `.github/skills/`
- Verify descriptions match actual prompt/skill content

## Output

```markdown
## Cross-Reference Validation Report

**Date:** YYYY-MM-DD
**Files scanned:** N markdown files
**Total links checked:** N

---

### ❌ Broken Links

| # | Source File | Line | Link Text | Target | Issue |
|---|-----------|------|-----------|--------|-------|
| 1 | README.md | NN | "text" | URL/path | 404 / file not found |

### ⚠️ Redirects (Should Update)

| # | Source File | Line | Current URL | Redirects To |
|---|-----------|------|-------------|-------------|
| 1 | README.md | NN | old URL | new URL |

### ⚠️ Orphaned Definitions

| # | File | Definition | Issue |
|---|------|-----------|-------|
| 1 | README.md | [N]: URL | Defined but never used |

### ⚠️ Missing Definitions

| # | File | Line | Reference | Issue |
|---|------|------|-----------|-------|
| 1 | README.md | NN | [N] | Used but not defined |

### ✅ Validation Summary

| Category | Total | ✅ Valid | ❌ Broken | ⚠️ Warning |
|----------|-------|---------|---------|------------|
| Internal file links | N | N | N | N |
| Anchor links | N | N | N | N |
| Reference links | N | N | N | N |
| External URLs | N | N | N | N |
| Cross-level refs | N | N | N | N |
| Config file refs | N | N | N | N |
| Prompt/skill refs | N | N | N | N |

### 📋 Recommended Fixes

1. **[Critical]** Fix broken link in...
2. **[Important]** Update redirect in...
3. **[Minor]** Remove orphaned definition...
```
