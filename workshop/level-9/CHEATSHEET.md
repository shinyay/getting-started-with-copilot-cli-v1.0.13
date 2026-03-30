# Level 9 Cheat Sheet — Build Your Own Copilot Experience

## Extensions

| Command / Pattern | Purpose | Example |
|-------------------|---------|---------|
| `/extensions` | List, enable, disable extensions | View all loaded extensions |
| `.github/extensions/<name>/extension.mjs` | Project extension location | ES module format required |
| `~/.copilot/extensions/<name>/extension.mjs` | User extension location | Available across all projects |
| `import { joinSession } from "@github/copilot-sdk/extension"` | Extension SDK entry point | Register tools, hooks, slash commands |
| `/extensions reload` | Reload extensions after changes | Apply updates without restart |

## Research & PR Workflow

| Command / Pattern | Purpose | Example |
|-------------------|---------|---------|
| `/research <topic>` | Deep research with GitHub search + web | Produces exportable reports |
| `/pr` | Create PR from current changes | AI-generated description |
| `/pr view [local\|web]` | View PR status and checks | Monitor CI/CD |
| `/pr fix` | Fix CI failures in PR | Analyze logs + apply fixes |
| `/research` → `/plan` → implement → `/pr` | Full research-to-PR chain | Complete workflow |

## Hooks System

| Hook Type | When It Fires | Use Case |
|-----------|---------------|----------|
| `preCompact` | Before context compaction | Save summary, archive context |
| `subagentStart` | When subagent launches | Inject project context |
| `agentStop` | When agent completes | Cleanup, notifications |
| `preToolUse` | Before tool execution | Validation, safety checks |

## Skills & Personal Directory

| Location | Scope | Discovery |
|----------|-------|-----------|
| `.github/skills/` | Project-level | Auto-discovered for this repo |
| `~/.agents/skills/` | User-level (v1.0.11) | Shared between CLI and VS Code |
| `~/.copilot/skills/` | User-level | Copilot CLI specific |

## Cross-Tool Instructions

| File | Compatible With | Location |
|------|-----------------|----------|
| `.github/copilot-instructions.md` | Copilot CLI | Repo-wide |
| `CLAUDE.md` | Copilot CLI + Claude Code (v1.0.13) | Repo root |
| `GEMINI.md` | Copilot CLI + Gemini CLI (v1.0.13) | Repo root |
| `AGENTS.md` | Copilot CLI Coding Agent | Repo root / .github/ |
| `.claude/settings.json` | Copilot CLI + Claude Code (v1.0.12) | Repo root |
| `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` | Copilot CLI (v1.0.13) | Environment variable |

## Reasoning & Models

| Flag / Command | Purpose | Values |
|----------------|---------|--------|
| `--reasoning-effort` | Control AI thinking depth (v1.0.4) | `low`, `medium`, `high`, `xhigh` |
| `Ctrl+T` | Toggle reasoning display | Show/hide thinking process |
| `/model` | Switch AI model | `gpt-5.4-mini` for speed, `claude-opus-4.6` for depth |

## MCP Advanced

| Feature | Description | Since |
|---------|-------------|-------|
| `.mcp.json` at git root | Simplified MCP configuration | v1.0.12 |
| MCP sampling | Servers request LLM inference | v1.0.13 |
| Org policy enforcement | Enterprise MCP restrictions | v1.0.11 |
| `{{project_dir}}` | Template variable in config | v1.0.12 |

## Themes & Personalization

| Command | Purpose |
|---------|---------|
| `/theme` | Interactive theme picker |
| `GitHub Dark` / `GitHub Light` / `Auto` | Theme options |
| OSC 8 hyperlinks | Clickable URLs in VS Code terminal (v1.0.12) |

## Level 9 Sample App Quick Reference

| File | Purpose |
|------|---------|
| `scaffolder/cli.py` | Main CLI entry point |
| `scaffolder/templates.py` | Template engine |
| `extensions/scaffolder-ext/extension.mjs` | Custom Copilot extension |
| `.mcp.json` | MCP configuration |
| `CLAUDE.md` | Cross-tool instructions (Claude) |
| `GEMINI.md` | Cross-tool instructions (Gemini) |
| `skills/scaffold-skill/SKILL.md` | Example skill definition |
