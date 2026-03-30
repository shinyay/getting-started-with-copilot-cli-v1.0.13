# GitHub Copilot CLI — Complete Manual

> **Version:** 1.0.5 (General Availability) — March 2026
> **Total:** 15 chapters · 9,400+ lines · Covers every feature, command, and configuration option

---

## About This Manual

This is a comprehensive reference manual for **GitHub Copilot CLI**, the
terminal-native AI coding agent by GitHub. It covers everything from
installation to advanced automation, organized into self-contained chapters
that can be read sequentially or used as standalone references.

**Who is this for?**
- Developers learning Copilot CLI from scratch (start at Chapter 1)
- Experienced users looking up specific features (jump to any chapter)
- Team leads setting up Copilot CLI for their organization (Chapters 7, 8, 14)
- DevOps engineers integrating Copilot into CI/CD (Chapter 15)

---

## Table of Contents

### Getting Started

| # | Chapter | Lines | Description |
|---|---------|-------|-------------|
| 1 | [Introduction & Installation](./01-introduction-and-installation.md) | 369 | What Copilot CLI is, 5 installation methods, authentication, updating |
| 2 | [Core Interface & Terminal UI](./02-core-interface-and-terminal-ui.md) | 711 | Timeline, alt-screen, themes, mouse support, accessibility |
| 3 | [Keyboard Shortcuts & Input](./03-keyboard-shortcuts-and-input.md) | 589 | Every shortcut, multi-line input, history, @mentions, #references |

### Core Concepts

| # | Chapter | Lines | Description |
|---|---------|-------|-------------|
| 4 | [Modes of Operation](./04-modes-of-operation.md) | 912 | Interactive, Plan, Autopilot, Shell — deep dive with examples |
| 5 | [Slash Commands Reference](./05-slash-commands-reference.md) | 600 | All 35+ slash commands organized by category |
| 6 | [Context Management & Prompt Engineering](./06-context-management-and-prompt-engineering.md) | 649 | Token limits, compaction, images, steering, prompt patterns |

### Customization & Extensibility

| # | Chapter | Lines | Description |
|---|---------|-------|-------------|
| 7 | [Custom Instructions & Configuration](./07-custom-instructions-and-configuration.md) | 692 | Instruction hierarchy, /init, config files, environment variables |
| 8 | [Custom Agents](./08-custom-agents.md) | 468 | Built-in agents, agent files, fleet mode, /delegate |
| 9 | [MCP (Model Context Protocol)](./09-mcp-model-context-protocol.md) | 819 | GitHub MCP, adding servers, OAuth, Elicitations, troubleshooting |
| 10 | [Plugins & Skills](./10-plugins-and-skills.md) | 833 | Plugin system, marketplaces, skills, hooks, creating plugins |

### Workflows & Tools

| # | Chapter | Lines | Description |
|---|---------|-------|-------------|
| 11 | [Session Management & Memory](./11-session-management-and-memory.md) | 497 | Sessions, resume, compaction, cross-session memory, sharing |
| 12 | [Code Review, Diff & Workflows](./12-code-review-diff-and-workflows.md) | 791 | /diff, /review, undo, /delegate, /research, IDE, LSP |
| 13 | [AI Models & Reasoning](./13-ai-models-and-reasoning.md) | 372 | All models, selection strategies, extended thinking, PRU |

### Administration & Advanced

| # | Chapter | Lines | Description |
|---|---------|-------|-------------|
| 14 | [Security, Permissions & Enterprise](./14-security-permissions-and-enterprise.md) | 422 | Permission model, enterprise policies, proxy, GHE Cloud |
| 15 | [CLI Flags, Scripting & Automation](./15-cli-flags-scripting-and-automation.md) | 733 | All flags, prompt mode, hooks, CI/CD, ACP server |

---

## Reading Guides

### 🟢 New to Copilot CLI?

Read in order: **1 → 2 → 3 → 4 → 5 → 6**. This gives you a solid foundation
to use Copilot CLI productively. Then explore the remaining chapters based on
your needs.

### 🟡 Setting up for your team?

Focus on: **1** (installation) → **7** (instructions) → **8** (agents) →
**14** (security) → **9** (MCP). These chapters cover everything needed to
configure Copilot CLI for team use.

### 🔴 Advanced automation?

Jump to: **15** (scripting & flags) → **8** (agents & fleet) → **10**
(plugins) → **9** (MCP). These chapters cover programmatic usage, CI/CD
integration, and extensibility.

---

## Conventions Used in This Manual

| Convention | Meaning |
|------------|---------|
| `> 💡` | Helpful tip or best practice |
| `> ⚠️` | Warning — pay attention to avoid issues |
| `> 📋` | Cross-reference to another chapter or resource |
| `(since v0.0.NNN)` | Version when the feature was introduced |
| `` `code` `` | Commands, file paths, or configuration values |
| **Bold** | Key terms or emphasis |

---

## Quick Links

- [Official Documentation](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)
- [GitHub Copilot CLI Repository](https://github.com/github/copilot-cli)
- [Changelog](https://github.com/github/copilot-cli/blob/main/changelog.md)
- [Release History](../../../RELEASE-HISTORY.md)
- [Copilot Plans](https://github.com/features/copilot/plans)

---

*This manual is based on GitHub Copilot CLI v1.0.5 (March 2026). Features
marked as "experimental" may change in future releases. Run `/changelog` in
the CLI to see the latest updates.*
