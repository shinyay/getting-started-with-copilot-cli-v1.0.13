---
layout: step
title: "Installation & Quick Start"
step_number: 0
permalink: /setup/
---

## 1. Requirements

Before starting the workshop, make sure you have the following:

- **Valid GitHub Copilot subscription** (Individual, Business, or Enterprise)
- **Node.js 22+** (if installing via npm)
- **Python 3.8+** (Levels 1–6, 9)
- **Node.js 18+** (Level 7)
- **Git** installed and configured
- A **terminal** (macOS Terminal, iTerm2, Windows Terminal, or Linux)

---

## 2. Install Copilot CLI

Choose one of the six installation methods below.

### npm (All Platforms)

```bash
npm install -g @github/copilot
```

### macOS / Linux (Homebrew)

```bash
brew install copilot-cli
```

### Windows (WinGet)

```powershell
winget install GitHub.Copilot
```

### macOS / Linux (Install Script)

```bash
curl -fsSL https://gh.io/copilot-install | bash
```

### Via GitHub CLI

```bash
gh extension install github/gh-copilot
gh copilot
```

> [!WARNING]
> The `gh copilot` extension is a **different tool** from the standalone `copilot` CLI. For the full agent experience used in this workshop, use one of the other installation methods.

### Direct Download

Download from the [releases page](https://github.com/github/copilot-cli/releases/).

---

## 3. Verify Installation

Run the following command to confirm Copilot CLI is installed correctly:

```bash
copilot --version
```

You should see the version number printed to your terminal (e.g. `1.0.13`).

---

## 4. Quick Start (Your First Session)

1. **Navigate** to the Level 1 sample app:

   ```bash
   cd workshop/level-1/sample-app
   ```

2. **Launch** Copilot CLI:

   ```bash
   copilot
   ```

3. **Trust the folder** — Copilot will ask whether to trust the current directory since it may read, modify, and execute files within it. You have three options:
   - **Yes, proceed** — trust for this session only
   - **Yes, and remember this folder** — trust for this and future sessions
   - **No, exit (Esc)** — end the session

4. **Authenticate** — if not already logged in, run `/login` inside the Copilot session. Alternatively, set a fine-grained PAT with the "Copilot requests" permission via `GH_TOKEN` or `GITHUB_TOKEN`.

5. **Try your first prompt:**

   ```
   What does this project contain?
   ```

---

## 5. Dev Container (Alternative)

This repository includes a `.devcontainer/` configuration for VS Code and GitHub Codespaces. Opening the repo in a dev container automatically sets up **Python** and **Node.js** with the correct versions so you can skip manual installation.

---

> [!TIP]
> You're ready to start! Head to **[Level 1: Observe →](/steps/1/)** for your first 12 exercises.
