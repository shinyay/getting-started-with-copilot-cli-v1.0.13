---
mode: "agent"
description: "Audit repository content against the latest Copilot CLI features and identify outdated references"
---

# Check Copilot CLI Updates

Audit all repository content against the current state of GitHub Copilot CLI
to identify outdated, missing, or inaccurate references. This prompt is for
focused update-and-refresh sessions.

## Step 1: Gather Current CLI State

Use **web search** and **web_fetch** to collect the latest Copilot CLI information
from these authoritative sources:

1. **Official documentation**:
   `https://docs.github.com/copilot/concepts/agents/about-copilot-cli`
2. **CLI repository and changelog**:
   Search for the latest GitHub Copilot CLI release notes and changelog
3. **npm package registry**:
   Check `@github/copilot` for the latest stable and prerelease versions
4. **CLI help output** (from this agent's own documentation):
   Use `fetch_copilot_cli_documentation` to get the current `/help` output

Capture the current state for each category:

| Category | What to Capture |
|----------|----------------|
| **Version** | Latest stable and prerelease version numbers |
| **Slash commands** | Complete list from `/help` (grouped by section) |
| **Keyboard shortcuts** | All shortcuts — global, editing, navigation |
| **CLI flags** | All command-line flags (`--allow-tool`, `-p`, `-s`, `--continue`, `--experimental`, etc.) |
| **Execution modes** | Available modes and how to switch between them |
| **Models** | Default model and all available alternatives |
| **Instruction file paths** | All supported custom instruction file locations |
| **Installation methods** | npm, Homebrew, WinGet, install script, gh extension |
| **Agent tools** | Available tools (view, edit, bash, grep, glob, etc.) |
| **MCP support** | Configuration format, file paths, capabilities |
| **Authentication** | Login methods, PAT support, environment variables |
| **Session management** | Session commands, resume, continue, share |

## Step 2: Inventory Repository References

Scan these repository files for CLI-specific references using grep:

### Primary Documents

| File | What to Check |
|------|--------------|
| `README.md` | Installation methods, quick start steps, execution modes, learning path exercise tables |
| `workshop/README.md` | Skill progression table, navigation, tools listed per level |

### Per-Level Content (repeat for each level 1–9)

| File | What to Check |
|------|--------------|
| `workshop/level-N/README.md` | Exercises referencing slash commands, shortcuts, flags, modes, tools |
| `workshop/level-N/CHEATSHEET.md` | Command tables, shortcut tables, mode descriptions, permission flags |

### Configuration Files

| File | What to Check |
|------|--------------|
| `.github/copilot-instructions.md` | Any CLI feature references, instruction file paths |
| `.github/AGENTS.md` | CLI feature references, tool names |
| `.github/prompts/*.prompt.md` | CLI commands used in prompt workflows |
| `.github/skills/*/SKILL.md` | CLI commands referenced in skill definitions |

### Search Patterns

Use these grep patterns to find CLI references efficiently:

```
# Slash commands
grep -rn '/[a-z]\+' --include="*.md" workshop/ README.md

# CLI flags
grep -rn '\-\-[a-z]' --include="*.md" workshop/ README.md

# Keyboard shortcuts
grep -rn 'Ctrl+\|Shift+\|ctrl+\|shift+' --include="*.md" workshop/ README.md

# Execution modes
grep -rni 'interactive\|plan mode\|autopilot\|programmatic' --include="*.md" workshop/ README.md

# Model references
grep -rni 'claude\|gpt\|sonnet\|opus\|haiku' --include="*.md" workshop/ README.md

# Instruction file references
grep -rn 'copilot-instructions\|AGENTS\.md\|CLAUDE\.md\|GEMINI\.md\|\.copilotignore' --include="*.md" workshop/ README.md
```

## Step 3: Cross-Reference and Identify Gaps

For each category captured in Step 1, compare against what the repository documents.
Classify findings into:

- **❌ Outdated** — Commands, shortcuts, or flags that changed, were renamed, or removed
- **⚠️ Missing** — New CLI capabilities not covered in any exercise or cheat sheet
  that are significant enough to warrant coverage
- **🔄 Inaccurate** — Behaviors described differently from current reality
- **🧪 Experimental drift** — Features that moved from experimental to stable
  (or vice versa) but aren't labeled correctly
- **✅ Accurate** — Content verified as current

## Step 4: Report Findings

Present results in this structured format:

```markdown
## Copilot CLI Update Audit Report

**Date:** YYYY-MM-DD
**CLI Version Checked:** vX.Y.Z (stable) / vX.Y.Z (prerelease)
**Repository State:** (last relevant commit SHA and date)

---

### ❌ Outdated Content (Must Fix)

| # | File | Section/Line | Current Content | Should Be | Category |
|---|------|-------------|-----------------|-----------|----------|
| 1 | README.md | Line NN | "text as written" | "corrected text" | Category |

### ⚠️ Missing Coverage (Should Add)

| # | New Feature | Category | Suggested Location | Priority |
|---|-------------|----------|-------------------|----------|
| 1 | Feature name | Category | file.md section | High/Med/Low |

### 🔄 Inaccurate Descriptions

| # | File | Section | Issue | Correction |
|---|------|---------|-------|------------|
| 1 | file.md | Section | What's wrong | What it should say |

### 🧪 Experimental Status Changes

| # | Feature | Was | Now | Affected Files |
|---|---------|-----|-----|---------------|
| 1 | Feature | Experimental | Stable | file1.md, file2.md |

### ✅ Verified Accurate

| Category | Files Checked | Status |
|----------|--------------|--------|
| Slash commands | Level 1-9 cheat sheets | All current |
| Installation | README.md | All current |

---

### 📋 Recommended Actions (Priority Order)

1. **[High]** Description of critical fix...
2. **[Medium]** Description of important update...
3. **[Low]** Description of nice-to-have improvement...

### 📊 Summary

| Status | Count |
|--------|-------|
| ❌ Outdated | N |
| ⚠️ Missing | N |
| 🔄 Inaccurate | N |
| 🧪 Experimental drift | N |
| ✅ Verified | N |
```

## Important Notes

- Focus on **factual CLI accuracy** — do not rewrite exercises for style or pedagogy
- Some content references experimental features intentionally (Level 8 covers
  `--experimental`); verify these are correctly labeled, not removed
- The main README's reference links (`[1]`, `[2]`, etc.) point to official docs;
  verify these URLs still resolve correctly
- The **baseline CLI version** for this repository's content is **v1.0.13**. When
  auditing, compare the latest CLI against this version to identify what changed
  since the last content update
- If uncertain whether something changed, note it as "⚠️ Needs verification"
  rather than making assumptions
- After completing the audit, suggest using the `sync-readme.prompt.md` prompt
  if cross-reference updates are needed
