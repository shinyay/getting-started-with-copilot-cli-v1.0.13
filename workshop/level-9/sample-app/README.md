# Project Scaffolder — Level 9 Sample Application

A project scaffold generator that demonstrates Copilot CLI extensibility features: custom extensions, cross-tool instructions, MCP configuration, skills, and hooks.

## Purpose

This app is designed for practicing:
- Building and loading Copilot CLI extensions
- Configuring cross-tool instruction files (CLAUDE.md, GEMINI.md)
- Setting up MCP servers at the project root
- Creating personal skills
- Configuring lifecycle hooks

## Usage

```bash
python -m scaffolder.cli create --template python --name my-project
python -m scaffolder.cli list
python -m scaffolder.cli info python
```

## File Structure

```
scaffolder/
├── __init__.py          — Package init
├── cli.py               — CLI entry point (argparse)
├── templates.py         — Template definitions and rendering
├── config.py            — Configuration constants
└── hooks.py             — Hook demonstration utilities
extensions/
└── scaffolder-ext/
    └── extension.mjs    — Custom Copilot CLI extension
.mcp.json                — MCP configuration (project root)
CLAUDE.md                — Cross-tool instructions (Claude)
GEMINI.md                — Cross-tool instructions (Gemini)
skills/
└── scaffold-skill/
    └── SKILL.md         — Example skill definition
Makefile                 — Common commands
requirements.txt         — No external dependencies (stdlib only)
```

## Teaching Points

- The extension has a placeholder tool for students to complete (Exercise 2)
- CLAUDE.md is intentionally minimal — students expand it (Exercise 9)
- `.mcp.json` references configuration students modify (Exercise 10)
- The skill has an incomplete description — students refine it (Exercise 6)
