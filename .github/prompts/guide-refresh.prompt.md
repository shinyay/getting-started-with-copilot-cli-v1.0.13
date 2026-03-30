---
mode: "agent"
description: "Update README.md and workshop/README.md after discovering Copilot CLI changes"
---

# Guide Refresh

Update the main `README.md` and `workshop/README.md` to reflect the latest
Copilot CLI state. Use this prompt **after** running `check-cli-updates` or
`upstream-diff-analysis` to apply the discovered changes.

## Scope

This prompt updates **guide-level documentation** — the README's description,
installation, features, and reference sections. It does NOT update:

- Exercise tables (use `sync-readme`)
- Exercise content within levels (use `workshop-refresh`)
- Sample app code or dependencies (use `sample-app-upgrade`)

## Input

Before starting, check if findings from a previous `check-cli-updates` or
`upstream-diff-analysis` session exist. If not, run a quick check:

1. Use **web_fetch** on the official docs and **fetch_copilot_cli_documentation**
   to get the current CLI state
2. Compare against the current README content

## Sections to Update (in order)

Work through each section of `README.md` sequentially. For each section,
read the current content, compare against the latest CLI state, and update
if needed.

### 1. Description & Key Characteristics

**Location:** Top of README.md (after the title and note)

Check and update:
- Public Preview status — is it still preview, or has it gone GA?
- Feature description — does it accurately reflect current capabilities?
- Key Characteristics list — platforms, execution modes, integrations
- Mode names — verify "Interactive / Plan / Programmatic" (or if Autopilot
  has graduated from experimental)

### 2. Requirements

**Location:** `## Requirement` section

Check and update:
- Copilot subscription types listed
- Node.js version requirement (currently "22+")
- PowerShell version requirement (Windows)
- Any new requirements added upstream

### 3. Installation

**Location:** `## Installation` section

Check and update:
- npm package name and install command
- WinGet package identifier
- Homebrew formula name
- Install script URL and options
- GitHub CLI extension installation
- Any new installation methods

### 4. Quick Start

**Location:** `## Quick Start` section

Check and update:
- Launch command
- Trust prompt behavior and options
- Authentication flow (`/login`, PAT instructions)
- First prompt example

### 5. Key Commands Cheat Sheet

**Location:** `### 🏆 Summary: Key Commands Cheat Sheet` section

Check and update:
- All slash commands listed — add new ones, remove deprecated ones
- CLI flags listed — verify syntax and descriptions
- Command categories — ensure logical grouping
- Cross-reference to per-level cheat sheets

### 6. Features (Detailed Reference)

**Location:** `## Features (Detailed Reference)` section

Update each subsection:

- **Execution Modes** — Mode names, descriptions, how to switch
- **Safety Model** — Approval options, permission flags, `--yolo`/`--allow-all`
- **Context & Session Management** — Session commands, token management
- **Custom Instructions** — File paths, scope, this-repo examples table
- **Custom Agents** — Agent profile format
- **Agent Skills (Reusable Prompts)** — Prompt table (update after creating
  new prompts; see `update-readme-table` todo)
- **Agent Skills (Auto-Loaded)** — Skills table
- **MCP Integration** — Config location, flags
- **Model Selection** — Default model, available models, premium vs non-premium
- **ACP** — Protocol details, flags
- **SDK** — Version, installation, auth methods

### 7. Best Practices

**Location:** `## Best Practices` section

Verify each practice still references valid commands and reflects current
recommended workflow.

### 8. Reference Links

**Location:** `## References` section and `[1]`–`[12]` definitions at bottom

For each reference link:
1. Verify the URL still resolves (use web_fetch with a HEAD-like check)
2. Verify the link description matches the page content
3. Add new reference links if new upstream docs exist
4. Remove links to pages that no longer exist

### 9. Workshop README

**Location:** `workshop/README.md`

Check and update:
- Skill Progression table — tool names, command references
- Quick Navigation — time estimates (if dramatically changed by new features)
- Level descriptions — verify CLI feature references are current

## Update Rules

- **Preserve existing structure** — Do not reorganize sections unless required
  by upstream changes
- **Maintain reference link style** — Use `[text][N]` format with definitions
  at the bottom of the file
- **Keep educational tone** — This is a learning guide, not a changelog
- **Note version context** — If the README has a `Note:` block mentioning
  Public Preview, verify it's still accurate
- **Link new blog posts** — If major CLI updates have corresponding blog posts,
  add them to the References section
- **Preserve the Note about Legacy Package** — The `@githubnext/github-copilot-cli`
  warning should remain until that package is fully removed from npm

## Output

After making updates, provide:

```markdown
## Guide Refresh Summary

**Sections Updated:** N of 9
**Sections Unchanged:** N of 9

| # | Section | Status | Changes Made |
|---|---------|--------|-------------|
| 1 | Description | ✅ Updated / ➖ No change | Brief description |
| 2 | Requirements | ✅ Updated / ➖ No change | Brief description |
...

### Reference Links Status
| Ref | URL | Status |
|-----|-----|--------|
| [1] | https://... | ✅ Valid / ❌ Broken / 🔄 Updated |
...

### Next Steps
- [ ] Run `sync-readme` if exercise tables need updating
- [ ] Run `workshop-refresh` if exercises reference changed features
- [ ] Run `cross-reference-validate` to verify all links
```
