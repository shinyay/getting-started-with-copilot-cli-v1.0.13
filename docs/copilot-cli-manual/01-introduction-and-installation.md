# Chapter 1: Introduction & Installation

This chapter covers everything you need to go from zero to a fully
authenticated, working Copilot CLI installation.

---

## What Is GitHub Copilot CLI?

GitHub Copilot CLI is a **terminal-native agentic AI coding assistant** built by
GitHub. It brings the full power of Copilot directly into your command line,
enabling you to build, edit, debug, and refactor code through natural language —
without ever leaving your terminal.

Unlike traditional code-completion tools, Copilot CLI functions as an **agentic
system**: it reasons about your codebase, formulates multi-step plans, executes
shell commands, reads and writes files, and orchestrates complex workflows —
all while keeping you in full control. Every file edit, command execution, and
tool call is presented for your review before it runs.

| Characteristic | Description |
|----------------|-------------|
| **Agentic architecture** | Same agentic harness as Copilot coding agent — plan, execute, verify loops with tool use |
| **Terminal-native** | Renders rich Markdown, diffs, and interactive UI elements directly in your terminal |
| **GitHub integration** | Out-of-the-box access to issues, PRs, repos, commits via built-in MCP servers |
| **Extensible via MCP** | Connect any Model Context Protocol server for databases, APIs, docs, and custom tooling |
| **Multi-model support** | Switch between available foundation models with the `/model` slash command |
| **Full transparency** | Preview every action before execution |

### Timeline

| Date | Milestone |
|------|-----------|
| September 2025 | **Public Preview** launch |
| February 25, 2026 | **General Availability (GA)** — v1.0 |
| June 2026 | Current stable release: **v1.0.13** |

---

## Supported Platforms

| Platform | Minimum Version | Notes |
|----------|----------------|-------|
| **Linux** | glibc 2.17+ | x64 and arm64 architectures |
| **macOS** | macOS 12 (Monterey)+ | Intel and Apple Silicon (universal binary) |
| **Windows** | Windows 10 1809+ | Requires **PowerShell v6+** |

> ⚠️ On Windows, the legacy Windows PowerShell 5.1 (bundled with Windows) is
> **not supported**. Install [PowerShell 7+](https://github.com/PowerShell/PowerShell).

### Terminal Compatibility

Works in any terminal supporting ANSI escape codes (80+ columns recommended):

| Terminal | Platform | Status |
|----------|----------|--------|
| VS Code integrated terminal | All | ✅ Fully supported |
| Windows Terminal | Windows | ✅ Fully supported |
| iTerm2 / Terminal.app | macOS | ✅ Fully supported |
| GNOME Terminal / Konsole | Linux | ✅ Fully supported |
| Ghostty | macOS, Linux | ✅ Fully supported |
| kitty / Alacritty | All | ✅ Fully supported |
| tmux | macOS, Linux | ✅ Supported (ensure 256-color mode) |

> 💡 For the best experience, use a terminal with true-color (24-bit) support
> and a modern font with Unicode glyphs.

---

## Prerequisites

### 1. Active GitHub Copilot Subscription

| Plan | Audience | CLI Access |
|------|----------|------------|
| **Copilot Individual** | Personal accounts | ✅ Included |
| **Copilot Business** | Organizations | ✅ Included (admin must enable) |
| **Copilot Enterprise** | Enterprises | ✅ Included (admin must enable) |
| **Copilot Free** | All GitHub users | ⚠️ Limited interactions/month |

> 📋 Manage your subscription at
> [github.com/settings/copilot](https://github.com/settings/copilot).
> For plan details, see the [Copilot plans page](https://github.com/features/copilot/plans).

### 2. Organization / Enterprise Policy (Business & Enterprise)

Admins must enable Copilot CLI: **Organization Settings → Copilot → Policies →
Copilot CLI → Enabled**. Even with a valid seat, authentication fails if the
policy disables CLI access.

### 3. Node.js (npm Installation Only)

Only required for the npm method. Other methods bundle their own runtime.

---

## Installation Methods

### 1. Install Script (macOS / Linux) — Recommended

```bash
curl -fsSL https://gh.io/copilot-install | bash
```

Installs to `~/.local/bin` by default. Customize with environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PREFIX` | `~/.local` | Installation prefix; binary goes to `$PREFIX/bin/` |
| `VERSION` | Latest stable | Specific version to install (e.g., `1.0.5`) |

**System-wide install:**

```bash
curl -fsSL https://gh.io/copilot-install | sudo PREFIX=/usr/local bash
```

**Using `wget`:**

```bash
wget -qO- https://gh.io/copilot-install | bash
```

> ⚠️ Ensure `~/.local/bin` is on your `PATH`. Add it with:
> ```bash
> echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
> ```

### 2. Homebrew (macOS / Linux)

```bash
brew install copilot-cli            # Stable
brew install copilot-cli@prerelease  # Pre-release channel
brew upgrade copilot-cli             # Update
```

### 3. WinGet (Windows)

```bash
winget install GitHub.Copilot            # Stable
winget install GitHub.Copilot.Prerelease  # Pre-release
winget upgrade GitHub.Copilot             # Update
```

### 4. npm (Cross-Platform)

```bash
npm install -g @github/copilot            # Stable
npm install -g @github/copilot@prerelease  # Pre-release
npm update -g @github/copilot              # Update
```

> ⚠️ Avoid `sudo npm install -g`. Configure a user-writable prefix instead:
> ```bash
> npm config set prefix ~/.npm-global
> export PATH="$HOME/.npm-global/bin:$PATH"
> ```

### 5. MSI Installer (Windows)

Available from the [GitHub releases page](https://github.com/github/copilot-cli/releases).
Added in **v0.0.389 (January 2026)**. Supports silent install:

```bash
msiexec /i copilot-cli-x64.msi /quiet /norestart
```

### Installation Method Comparison

| Method | Platform | Auto-Update | Node.js Required | Pre-release | Best For |
|--------|----------|-------------|------------------|-------------|----------|
| **Install Script** | macOS, Linux | Via `/update` | No | No | Quick setup, servers |
| **Homebrew** | macOS, Linux | `brew upgrade` | No | Yes | macOS developers |
| **WinGet** | Windows | `winget upgrade` | No | Yes | Windows developers |
| **npm** | All | `npm update -g` | Yes (18+) | Yes | CI/CD, Node.js users |
| **MSI** | Windows | Manual | No | Via releases | Enterprise deployment |

---

## First Launch Experience

```bash
copilot
```

### Welcome Banner

On first launch, an animated welcome banner displays version info. It appears
once and is suppressed afterward. To redisplay: `copilot --banner`.

### Trust Dialog

Before operating in a directory, Copilot CLI presents a trust dialog:

| Option | Behavior |
|--------|----------|
| **Yes, proceed** | Trust this directory for the current session only |
| **Yes, and remember** | Trust permanently (saved to `~/.copilot/config.json`) |
| **No, exit** | Abort without taking any action |

> 💡 Trusting a parent directory (e.g., `~/projects`) automatically trusts
> all subdirectories beneath it.

> ⚠️ Only trust directories containing code you control. Copilot CLI can read,
> execute, and modify files within trusted directories.

---

## Authentication

Copilot CLI checks for credentials in a specific precedence order:

| Priority | Method | Details |
|----------|--------|---------|
| 1 (highest) | `COPILOT_GITHUB_TOKEN` env var | Dedicated Copilot variable (added v0.0.354) |
| 2 | `GH_TOKEN` env var | Standard GitHub CLI token variable |
| 3 | `GITHUB_TOKEN` env var | Common CI/CD token variable |
| 4 | OAuth device flow | Interactive browser-based login |
| 5 | GitHub CLI (`gh`) token | Reuses existing `gh auth` session |
| 6 | `GITHUB_ASKPASS` | External credential helper |

### OAuth Device Flow

The default interactive login method. Triggered automatically on first run or
manually via the `/login` slash command.

1. Copilot CLI generates a one-time **device code** and displays it
2. Opens `https://github.com/login/device` in your browser
3. You enter the code and authorize the application
4. Copilot CLI polls until authorization confirms
5. The OAuth token is stored in your system keychain

> 💡 The device code expires after 15 minutes. Run `/login` again to regenerate.

### Personal Access Token (PAT)

For non-interactive environments (CI/CD, containers, remote servers):

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens?type=beta)
2. Create a fine-grained PAT with **"Copilot Requests"** permission
3. Set the token as an environment variable:

```bash
export COPILOT_GITHUB_TOKEN="github_pat_xxxxxxxxxxxx"  # Recommended
export GH_TOKEN="github_pat_xxxxxxxxxxxx"               # Alternative
export GITHUB_TOKEN="github_pat_xxxxxxxxxxxx"            # Alternative
```

> ⚠️ Never commit tokens to source control. Use your OS secret management
> or a `.env` file excluded via `.gitignore`.

### GitHub CLI (`gh`) Authentication

If `gh auth login` is already configured, Copilot CLI reuses that token
automatically — no additional login required.

> 📋 Check status with: `gh auth status`

### Enterprise / GHE Cloud

Set `GH_HOST` for GitHub Enterprise Cloud (`*.ghe.com`) environments:

```bash
export GH_HOST="your-enterprise.ghe.com"
```

Requirements: enterprise Copilot enabled, CLI policy set to Enabled, and a
valid Copilot seat assigned to your account.

> ⚠️ GitHub Enterprise Server (self-hosted) is **not currently supported**.
> Only GitHub.com and GHE Cloud (*.ghe.com) hosts are compatible.

---

## Updating

### In-Session Update

```
/update
```

The `/update` slash command (added **v0.0.412**) updates without leaving your session.

### Shell Update

```bash
copilot update
```

### Auto-Update

Since **v0.0.420**, Copilot CLI auto-updates on launch — both the JS package
and native binary. Auto-update is disabled by default when `CI=true` is detected.
Previous versions are cleaned up automatically after successful updates.

| Package Manager | Manual Update Command |
|-----------------|-----------------------|
| Install Script | Re-run the install script |
| Homebrew | `brew upgrade copilot-cli` |
| WinGet | `winget upgrade GitHub.Copilot` |
| npm | `npm update -g @github/copilot` |
| MSI | Download latest from releases page |

> 💡 Disable auto-update explicitly: `export COPILOT_AGENT_AUTO_UPDATE=0`

---

## Verifying Installation

```bash
copilot --version    # Expected: copilot version 1.0.13
copilot help         # Display available subcommands and flags
```

### Binary Integrity Verification

SHA256 checksums have been published since **v0.0.370**:

```bash
curl -fsSL https://github.com/github/copilot-cli/releases/download/v1.0.13/checksums.txt -o checksums.txt
sha256sum --check --ignore-missing checksums.txt
```

> 💡 Checksum verification is recommended for enterprise deployments and
> security-sensitive environments.

---

## Uninstalling

| Install Method | Uninstall Command |
|----------------|-------------------|
| Install Script | `rm $(which copilot)` |
| Homebrew | `brew uninstall copilot-cli` |
| WinGet | `winget uninstall GitHub.Copilot` |
| npm | `npm uninstall -g @github/copilot` |
| MSI | Windows **Apps & Features** settings |

Remove all configuration data:

```bash
rm -rf ~/.copilot/
```

> ⚠️ This deletes stored preferences, trusted directories, and cached tokens.
> You will need to re-authenticate after reinstalling.

---

## Version History Highlights

| Version | Date | Milestone |
|---------|------|-----------|
| v0.0.1 | Sep 2025 | **Public Preview** — core chat, file editing, command execution |
| v0.0.354 | Nov 2025 | `COPILOT_GITHUB_TOKEN` env var for dedicated authentication |
| v0.0.370 | Dec 2025 | SHA256 checksums for all release artifacts |
| v0.0.389 | Jan 2026 | MSI installer for Windows enterprise deployment |
| v0.0.412 | Jan 2026 | `/update` slash command for in-session updates |
| v0.0.420 | Feb 2026 | Auto-update: JS package + binary, CI auto-disable |
| v1.0.0 | Feb 25, 2026 | **General Availability** — stable API, production-ready |
| v1.0.2 | Mar 2026 | Bug fixes and performance improvements |
| v1.0.5 | Mar 2026 | Extensions, /pr, /version, /diff syntax highlighting, --reasoning-effort |
| v1.0.6 | Apr 2026 | Improved `/compact` summarization, `--model` startup flag |
| v1.0.7 | Apr 2026 | Double-Esc input clearing, enhanced color contrast, "Customize" mode |
| v1.0.8 | Apr 2026 | MCP server health checks, `/fleet` reliability improvements |
| v1.0.9 | May 2026 | Context window usage optimizations, `/research` report export |
| v1.0.10 | May 2026 | Plugin marketplace search improvements, `/delegate` multi-remote |
| v1.0.11 | May 2026 | Session restore reliability, `--continue` flag for CI pipelines |
| v1.0.12 | Jun 2026 | OSC 8 hyperlinks in VS Code, intra-line diff highlighting, `/allow-all` subcommands, Ctrl+Y for research reports |
| v1.0.13 | Jun 2026 | `/rewind`, `/new`, `/quit`, `/session` subcommands, improved `/instructions` toggle |

> 📋 For the full changelog, run `/changelog` in a session or visit the
> [releases page](https://github.com/github/copilot-cli/releases).

---

Next: [Chapter 2: Core Interface & Terminal UI](./02-core-interface-and-terminal-ui.md)
