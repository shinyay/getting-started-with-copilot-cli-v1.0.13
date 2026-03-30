---
mode: "agent"
description: "Deep section-by-section comparison of repository content against official Copilot CLI documentation"
---

# Upstream Diff Analysis

Perform a forensic, section-by-section comparison of this repository's content
against the official GitHub Copilot CLI documentation. Unlike `check-cli-updates`
(which discovers what changed in the CLI), this prompt compares **exactly what
we say** against **exactly what the official docs say**.

## Step 1: Fetch Official Documentation

Use **web_fetch** to retrieve each of these official documentation pages.
Read the full content of each page:

| # | Source | URL | Repo Sections It Maps To |
|---|--------|-----|--------------------------|
| 1 | Installing Copilot CLI | `https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli` | README.md → Installation, Requirement |
| 2 | Using Copilot CLI | `https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli` | README.md → Quick Start, Safety Model, Custom Instructions |
| 3 | About Copilot CLI | `https://docs.github.com/copilot/concepts/agents/about-copilot-cli` | README.md → Description, Key Characteristics |
| 4 | CLI Command Reference | `https://docs.github.com/en/copilot/reference/cli-command-reference` | README.md → Features, Cheat Sheet; all CHEATSHEETs |
| 5 | Advanced CLI Usage | `https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli` | README.md → Context & Session, Model Selection |
| 6 | Copilot CLI Features | `https://github.com/features/copilot/cli` | README.md → Key Characteristics |

Also use **fetch_copilot_cli_documentation** to get the current `/help` output
as a baseline for slash commands and keyboard shortcuts.

## Step 2: Map Repository Content to Upstream

Create a mapping between repository sections and upstream documentation:

### README.md Mappings

| Repo Section | Lines (approx.) | Upstream Source | Comparison Focus |
|-------------|-----------------|----------------|-----------------|
| Description & Key Characteristics | Top | Source #3 | Feature claims, mode count, platform support |
| Requirement | Early | Source #1 | Node.js version, prerequisites |
| Installation | Early | Source #1 | Install methods, package names, commands |
| Quick Start | After Install | Source #2 | Trust flow, auth steps, first prompt |
| Three Execution Modes | Features | Source #4 | Mode names, descriptions, how to switch |
| Safety Model | Features | Source #2 | Approval options, permission flags |
| Context & Session Mgmt | Features | Source #5 | Session commands, token management |
| Custom Instructions & MCP | Features | Source #2 | File paths, scope descriptions |
| Model Selection | Features | Source #5 | Default model, available models |
| ACP | Features | Source #2 | Protocol details, flags |
| Best Practices | End | All sources | Accuracy of referenced commands |

### Workshop Content Mappings

For each level's CHEATSHEET.md, compare command/shortcut tables against
Source #4 (CLI Command Reference) and the `/help` output.

### Key Comparison Areas

For each mapping, compare:

1. **Factual accuracy** — Do we state the same facts as upstream?
2. **Completeness** — Does upstream document features we don't mention?
3. **Wording divergence** — Do we describe things differently (which could
   confuse learners who also read official docs)?
4. **Version specificity** — Do we reference version-specific behavior that
   may have changed?
5. **URL validity** — Do our reference links `[1]`–`[12]` still point to
   the correct upstream pages?

## Step 3: Perform Section-by-Section Diff

For each mapped section:

1. **Read our content** — Extract the exact text from the repository file
2. **Read upstream content** — Extract the corresponding section from the
   fetched official docs
3. **Compare** — Identify differences in:
   - Feature names or descriptions
   - Command syntax or flags
   - Default values (models, settings)
   - Supported platforms or versions
   - Behavioral descriptions (what happens when you do X)

## Step 4: Report Findings

```markdown
## Upstream Diff Analysis Report

**Date:** YYYY-MM-DD
**Upstream docs fetched:** (list URLs and fetch status)

---

### Section-by-Section Comparison

#### 1. Installation
| Aspect | Our Content | Upstream Says | Match? | Action |
|--------|-------------|---------------|--------|--------|
| npm command | `npm install -g @github/copilot` | (upstream text) | ✅/❌ | None/Update |
| Node.js version | 22+ | (upstream text) | ✅/❌ | None/Update |
| Homebrew formula | `copilot-cli` | (upstream text) | ✅/❌ | None/Update |
...

#### 2. Quick Start
(same format)

...continue for each section...

#### N. Reference Links
| Ref | URL | Resolves? | Content Match? |
|-----|-----|-----------|---------------|
| [1] | https://docs.github.com/... | ✅/❌ | ✅/❌ |
...

---

### 📊 Summary

| Section | Total Checks | ✅ Match | ❌ Differ | ⚠️ Partial |
|---------|-------------|---------|---------|------------|
| Installation | N | N | N | N |
| Quick Start | N | N | N | N |
...

### 📋 Prioritized Actions

1. **[Critical]** Factual errors...
2. **[Important]** Missing features...
3. **[Minor]** Wording improvements...
```

## Notes

- This prompt is **read-only analysis** — it produces a report but does not
  make changes. Use `guide-refresh` or `workshop-refresh` to apply fixes.
- Some intentional divergence is acceptable — we may simplify concepts for
  teaching purposes. Flag these as "intentional divergence" rather than errors.
- If a URL fails to fetch, note it and try alternative URLs or web search.
- The reference links section (`[1]`–`[12]`) at the bottom of README.md is
  critical — broken links undermine credibility.
