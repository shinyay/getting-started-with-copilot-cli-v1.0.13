---
layout: workshop
---

# Getting Started with GitHub Copilot CLI — Workshop

A progressive **9-level, 108-exercise** curriculum for mastering GitHub Copilot CLI. Starting from read-only exploration and building up to custom extensions, each level introduces a unique sample app and incrementally higher autonomy so you learn safe, effective AI-assisted development in the terminal.

> **Verified against Copilot CLI v1.0.13** (2026-03-28).
> If you are using a newer version, some details may differ — check `/changelog` inside Copilot CLI for what has changed.

## Curriculum

| Level | Title | Exercises | Sample App | Time |
|-------|-------|:---------:|------------|------|
| [Setup](/setup/) | Installation & Quick Start | — | — | 15 min |
| [1](/steps/1/) | Observe — Read-Only Exploration | 12 | Python Task Manager CLI | 45–60 min |
| [2](/steps/2/) | Understand — Ask Questions | 12 | Python Bookmark Manager API | 60–80 min |
| [3](/steps/3/) | Plan — Think Before Acting | 12 | Python Quick Notes CLI (with bugs) | 60–80 min |
| [4](/steps/4/) | Create — Make Your First Changes | 12 | Quick Notes CLI (writable copy) | 60–90 min |
| [5](/steps/5/) | Execute — Run Commands | 12 | Python Math Utilities (pytest) | 75–100 min |
| [6](/steps/6/) | Workflow — Full SDLC Cycle | 12 | Python URL Shortener CLI | 90–120 min |
| [7](/steps/7/) | Customize — Configuration | 12 | TypeScript Event API (Express) | 75–100 min |
| [8](/steps/8/) | Advanced — Permissions & Delegation | 12 | Multi-service DevOps Toolkit | 90–120 min |
| [9](/steps/9/) | Extend — Build Your Own Experience | 12 | Python Scaffolder + Extension | 90–120 min |

## Skill Progression

```
Risk Level:  🟢 None ──────────────────────────── 🔴 High awareness
Autonomy:    Human reads ───────── Human + AI ───── AI proposes
Scope:       One file ─── Multi-file ── Project ── Multi-service ── CI/CD
```

> [!TIP]
> Levels 1–3 are **read-only** — there is zero risk of breaking anything. Great for first-timers.

## Quick Start

```bash
# 1. Install Copilot CLI
npm install -g @github/copilot

# 2. Clone this workshop
git clone https://github.com/shinyay/getting-started-with-copilot-cli-v1.0.13.git
cd getting-started-with-copilot-cli-v1.0.13

# 3. Start Level 1
cd workshop/level-1/sample-app
copilot
```

## How to Use

Pick the format that fits your schedule:

| Format | Levels | Duration |
|--------|--------|----------|
| Quick intro | Levels 1–2 | 2 hours |
| Core skills | Levels 1–5 | 4–5 hours |
| Full training | Levels 1–9 | 10–15 hours |
| Advanced only | Levels 6–9 | 4–6 hours |

> [!TIP]
> For self-paced learning, aim for 1–2 levels per session and take the self-assessment at the end of each level before moving on.

## Safety Net

Every level's sample app can be restored to its original state:

```bash
# Reset any level's sample app to original state
git checkout -- workshop/level-N/sample-app/
```
