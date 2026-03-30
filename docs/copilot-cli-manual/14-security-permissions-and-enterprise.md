# Chapter 14: Security, Permissions & Enterprise

GitHub Copilot CLI is designed around a single, non-negotiable principle:
**nothing happens without your explicit approval**. Every file write, shell
command, and network request passes through a permission system that gives you
full visibility and control. This chapter covers the entire permission model,
enterprise deployment considerations, authentication security, and hardening
best practices for individuals and organizations alike.

---

## 14.1 Permission Model Overview

Copilot CLI uses a **three-tiered approval model** for every tool invocation.
When the agent wants to run a shell command, edit a file, or call an MCP tool,
you are prompted to approve the action before it executes.

| Tier | Scope | How to Select | Persistence |
|------|-------|---------------|-------------|
| **Per use** | This single invocation only | Press `y` or select "Allow once" | None — next call re-prompts |
| **Per session** | All invocations of this tool for the current session | Select "Allow for this session" | Until you exit the CLI |
| **Per location** | This tool at this workspace permanently | Select "Always allow at this location" | Persisted to disk (since v0.0.407) |

### Approval Behavior Details

- **Parallel auto-approval**: When you approve a tool for the session, any
  pending parallel requests of the same type are automatically approved as well.
  This prevents a flood of duplicate prompts when the agent launches several
  similar operations at once (since v0.0.384).

- **Rejection feedback**: If you reject a permission prompt, Copilot CLI
  captures inline feedback about why you declined. The agent uses this context
  to adjust its approach rather than blindly retrying (since v0.0.380).

- **Escape key abort**: Pressing `Esc` in any permission dialog consistently
  aborts the pending action without side effects (since v0.0.403).

> 💡 Start with per-use approval when exploring unfamiliar repositories. Once
> you trust the agent's behavior for a specific tool, promote to session or
> location-level approval to reduce friction.

> ⚠️ Location-level ("always allow") permissions persist across sessions. Review
> them periodically with `/reset-allowed-tools` to avoid stale approvals.

---

## 14.2 Tool Permissions

### /allow-all (alias: /yolo)

The `/allow-all` slash command enables all tool permissions for the current
session. It executes immediately with no confirmation prompt (since v0.0.404).

```
/allow-all
```

Since **v1.0.12**, `/allow-all` supports subcommands for explicit state management:

| Subcommand | Behavior | Since |
|------------|----------|-------|
| `/allow-all on` | Enable all permissions (same as bare `/allow-all`) | v1.0.12 |
| `/allow-all off` | Revoke blanket approval, return to per-use prompting | v1.0.12 |
| `/allow-all show` | Display current permission state | v1.0.12 |

Since **v1.0.12**, `/yolo` permission decisions persist after `/clear`. You no
longer need to re-enable `/allow-all` after resetting your conversation context.

Equivalent CLI flags when launching:

```bash
# Both flags are identical in behavior
copilot --allow-all
copilot --yolo
```

These flags have been available since v0.0.381 and apply for the entire session.

> ⚠️ `/allow-all` grants blanket approval for **every** tool — shell commands,
> file edits, MCP calls, and network requests. Use it only in trusted,
> disposable environments (CI runners, containers, personal scratch projects).

### --allow-tool and --deny-tool

For fine-grained control, use `--allow-tool` and `--deny-tool` with glob
patterns to pre-approve or block specific tools:

```bash
# Allow any npm test variant without prompting
copilot --allow-tool "shell(npm run test:*)"

# Allow file reads but deny writes
copilot --allow-tool "read_file(*)" --deny-tool "edit_file(*)"

# Allow a specific MCP tool
copilot --allow-tool "mcp__github__search_code"
```

Glob matching (since v0.0.329) supports `*` for any characters and `?` for a
single character inside the parenthesized argument.

| Flag | Purpose | Since |
|------|---------|-------|
| `--allow-tool PATTERN` | Pre-approve matching tools | v0.0.329 |
| `--deny-tool PATTERN` | Block matching tools | v0.0.329 |
| `--available-tools LIST` | Whitelist — only these tools are available | v0.0.370 |
| `--excluded-tools LIST` | Blacklist — these tools are hidden from the agent | v0.0.370 |

> 💡 Tool filtering flags propagate to subagents automatically (since v0.0.396).
> A `--deny-tool "shell(rm *)"` on the parent session also blocks subagents
> from running destructive `rm` commands.

### /reset-allowed-tools

Reset all previously approved tools back to their default state:

```
/reset-allowed-tools
```

This command can be executed while the agent is mid-task (since v0.0.412). It
does not cancel in-flight operations but ensures future invocations re-prompt.

---

## 14.3 Path Permissions

### Trusted Directories

The first time you launch Copilot CLI in a new directory, a trust dialog
appears with three options:

```
? Do you trust the files in this folder?
  1. Yes, proceed             — trust for this session only
  2. Yes, and remember        — persistent trust for this location
  3. No, exit                 — cancel and exit
```

You can manage trusted directories at any time:

| Command | Purpose |
|---------|---------|
| `/add-dir /path/to/project` | Manually add a trusted directory |
| `/list-dirs` | Show all persistently trusted directories |
| `--allow-all-paths` | Approve all paths for this session (since v0.0.340) |

> 💡 Temporary directories (e.g., `/tmp`, `%TEMP%`) are automatically trusted
> since v0.0.349 — no prompt needed for scratch work.

### Path Detection Heuristics

Copilot CLI analyzes shell commands to determine whether they reference paths
outside trusted directories. Over time, the heuristics have been refined to
reduce unnecessary prompts (since v0.0.351):

| Pattern Recognized | Example | Prompted? |
|--------------------|---------|-----------|
| Read-only bash commands | `cat README.md`, `ls src/` | No |
| npm test arguments | `npm test -- --coverage` | No |
| Shell redirections | `echo ok > /dev/null`, `cmd 2>&1` | No |
| `gh api` arguments | `gh api /repos/{owner}/{repo}` | No |
| Environment variable expansion | `$HOME/.config/file` | Expanded first (since v0.0.349) |
| Windows switch flags | `/D`, `/S` | Not treated as paths (since v0.0.407) |
| Paths with spaces/quotes | `"C:\My Projects\app"` | Correctly parsed (since v0.0.400) |

---

## 14.4 URL Permissions

Shell commands that access the web are subject to URL permission controls
(since v0.0.372). When the agent runs a `curl`, `wget`, or similar command
targeting an external URL, you are prompted to approve the destination.

> ⚠️ The `web-fetch` tool explicitly rejects `file://` URLs to prevent local
> file exfiltration through URL handlers (since v0.0.380).

---

## 14.5 Security Guardrails

### Shell Command Safety

Copilot CLI includes hardened shell analysis that detects and blocks dangerous
command patterns before they reach execution:

| Blocked Pattern | Reason | Since |
|-----------------|--------|-------|
| `${var@P}` parameter transformation | Obfuscates malicious commands | v0.0.423 |
| Chained variable assignments building substitutions | Progressive command injection | v0.0.423 |
| `${!var}` / `eval`-like dynamic construction | Arbitrary code execution | v0.0.423 |
| `pkill`, `killall`, name-based process killing | Risk of killing unrelated processes | — |
| Dangerous expansion/substitution in arguments | Shell injection via user input | v0.0.423 |
| Heredoc content outside command context | Unexpected code execution | v0.0.354 |

The agent is also protected from killing its own process (since v0.0.418).
If a command would terminate the Copilot CLI process, it is blocked.

```bash
# ❌ Blocked — name-based process killing
pkill -f copilot

# ❌ Blocked — dangerous parameter transformation
echo ${MALICIOUS@P}

# ✅ Allowed — specific PID targeting
kill 12345
```

### Module Integrity

| Protection | Description | Since |
|------------|-------------|-------|
| Application bundle check | Prevents loading modules from outside the CLI bundle | v0.0.403 |
| Authenticode signing | Windows native prebuilds are code-signed | v0.0.412 |
| SHA256 checksums | Published for every release artifact | v0.0.370 |

> 💡 Verify release integrity by comparing the downloaded binary's SHA256 hash
> against the published checksum before deploying to shared environments.

---

## 14.6 Enterprise & Organization Policies

### Copilot MCP Policy

Organization administrators can control MCP server access:

| Policy Control | Effect | Since |
|----------------|--------|-------|
| Block third-party MCP servers | Only approved servers can connect | v0.0.416 |
| Organization MCP policy enforcement | Enterprise-level control over which third-party MCP servers are allowed | v1.0.11 |
| Subagent model fallback | Falls back to session model when default is blocked | v0.0.407 |
| Improved denial messaging | Clear error when access denied by policy | v0.0.411 |
| Organization-level error handling | Descriptive "blocked by org policy" errors | v0.0.328 |

### EMU (Enterprise Managed Users) Restrictions

Enterprise Managed Users operate under tighter controls:

- **`/share gist` is blocked** for EMU accounts (since v0.0.423) — gist
  creation is disabled to prevent data leakage outside the enterprise boundary.
- **GHE Cloud data residency** policies restrict where data can be stored and
  processed. Copilot CLI respects these boundaries.

> 📋 For EMU configuration details, see your GitHub Enterprise administrator or
> the [GitHub Enterprise documentation](https://docs.github.com/enterprise-cloud@latest/admin/identity-and-access-management/using-enterprise-managed-users-for-iam).

### Organization Settings

Administrators control Copilot CLI availability through the organization
settings dashboard:

```
Organization Settings → Copilot → Policies
├── Enable/disable Copilot CLI for org members
├── Model availability (restrict to specific models)
├── Tool and agent policies (allow/block specific tools)
└── MCP server allowlist
```

> ⚠️ Model availability may vary depending on your GitHub plan (Individual,
> Business, Enterprise). Not all models are available on all plans.

---

## 14.7 GitHub Enterprise (GHE) Cloud

### Configuration

Connect Copilot CLI to a GHE Cloud instance by setting the `GH_HOST`
environment variable:

```bash
# Standard GHE Cloud hostname
export GH_HOST=github.example.com

# *.ghe.com domain support (since v0.0.393)
export GH_HOST=mycompany.ghe.com
```

Non-interactive logins are supported via `GH_HOST` since v0.0.342, which is
essential for CI/CD pipelines and automated environments.

### GHE Feature Support

| Feature | GHE Support | Since |
|---------|------------|-------|
| `/delegate` command | ✅ Fully supported | v0.0.394 |
| Remote custom agents (org `.github` repo) | ✅ Fully supported | — |
| `/share gist` | ⚠️ May be restricted by data residency | — |
| GitHub MCP server URL resolution | ✅ Resolves correctly for GHE | v0.0.373 |

> 💡 Custom agents stored in your organization's `.github` repository are
> automatically available to all org members using Copilot CLI with GHE Cloud.

---

## 14.8 Authentication Security

### Token Precedence

When multiple authentication tokens are available, Copilot CLI uses the
following precedence order:

| Priority | Variable | Typical Use Case | Since |
|----------|----------|------------------|-------|
| 1 (highest) | `COPILOT_GITHUB_TOKEN` | Explicit Copilot-specific token | v0.0.354 |
| 2 | `GH_TOKEN` | Standard GitHub CLI authentication | — |
| 3 | `GITHUB_TOKEN` | CI/CD environments (Actions, Codespaces) | — |
| 4 | `GITHUB_ASKPASS` | External auth helper program | v0.0.363 |

> ⚠️ If you set `COPILOT_GITHUB_TOKEN`, it overrides **all** other tokens. Make
> sure it has the required `Copilot Requests` fine-grained permission scope.

### OAuth Device Code Flow

Copilot CLI authenticates through GitHub's OAuth device code flow:

1. CLI generates a device code and displays a URL + user code.
2. You open the URL in a browser and enter the code.
3. CLI polls for authorization (begins immediately since v0.0.337).
4. Proper `slow_down` interval is respected to avoid rate limits (since v0.0.384).

```
! Please visit https://github.com/login/device
  and enter code: ABCD-1234

Waiting for authentication...
✓ Authentication successful
```

### PAT (Personal Access Token) Requirements

When using a PAT instead of OAuth, ensure it includes:

- **Fine-grained permission**: `Copilot Requests` (required)
- **Repository access**: As needed for your workflows

### GITHUB_TOKEN in Shell Sessions

The `GITHUB_TOKEN` environment variable is accessible within agent shell
sessions (since v0.0.404). Additionally, `COPILOT_CLI=1` is set in all
subprocess environments so scripts can detect they are running inside the
Copilot CLI agent (since v0.0.421).

---

## 14.9 Network & Proxy

### Proxy Support

Copilot CLI respects standard proxy environment variables:

```bash
export HTTPS_PROXY=https://proxy.corp.example.com:8443
export HTTP_PROXY=http://proxy.corp.example.com:8080

# Proxy URLs without scheme are also supported (since v0.0.384)
export HTTPS_PROXY=proxy.corp.example.com:8443
```

Proxy support works regardless of the installed Node.js version (since
v0.0.336), removing a previous dependency on Node's built-in proxy handling.

### CA Certificates

Custom CA certificates are loaded from both the system trust store and
environment variables (since v0.0.370):

```bash
# Point to your corporate CA bundle
export NODE_EXTRA_CA_CERTS=/etc/ssl/certs/corporate-ca.pem
```

### Per-Subscription API Endpoints

Since v0.0.332, Copilot CLI routes API calls through per-subscription
endpoints. This ensures compliance with enterprise network access policies
and data residency requirements.

---

## 14.10 Audit & Monitoring

| Tool | Purpose | Details |
|------|---------|---------|
| `/usage` | Session metrics | Token counts, tool invocations, model usage |
| `events.jsonl` | Persistent event log | All session events written to disk (since v0.0.422) |
| `copilot help permissions` | Permission reference | Complete list of permission types and controls |
| `copilot help logging` | Logging configuration | Log levels, output destinations, debug mode |

> 💡 The `events.jsonl` log file is useful for compliance auditing. Each entry
> records the timestamp, tool name, approval status, and execution result.

---

## 14.11 Security Best Practices

### For Individual Developers

| Practice | Why | How |
|----------|-----|-----|
| Start with per-use approval | Build trust incrementally | Default behavior — no action needed |
| Use `--allow-tool` with specific patterns | Avoid over-permissioning | `--allow-tool "shell(npm test)"` |
| Verify release checksums | Detect tampered binaries | Compare SHA256 before first run |
| Review `/usage` after sessions | Understand what the agent did | Run `/usage` before exiting |
| Avoid `--yolo` in shared environments | Prevents unreviewed actions on shared resources | Use specific `--allow-tool` patterns |
| Set `COPILOT_GITHUB_TOKEN` explicitly | Prevent token confusion | Export in your shell profile |
| Keep CLI updated | Security patches in every release | `npm update -g @github/copilot` |

### For Organizations

| Practice | Why | How |
|----------|-----|-----|
| Enable MCP server allowlists | Prevent unauthorized integrations | Org settings → Copilot → MCP policy |
| Restrict model availability | Compliance and cost control | Org settings → Copilot → Model policy |
| Use EMU for sensitive repos | Full identity control | GitHub Enterprise Managed Users |
| Configure proxy and CA certs | Network compliance | Set `HTTPS_PROXY` and `NODE_EXTRA_CA_CERTS` |
| Audit `events.jsonl` centrally | Track agent behavior at scale | Collect logs from developer machines |
| Pin CLI version in CI/CD | Reproducible builds | `npm install -g @github/copilot@0.0.423` |
| Block dangerous tools in policy | Prevent destructive operations | `--deny-tool` or org-level tool policy |

> ⚠️ Organizations handling regulated data (HIPAA, SOC 2, PCI-DSS) should
> consult their compliance team before enabling Copilot CLI for production
> repositories. Use MCP server restrictions, model policies, and audit logging
> to maintain compliance boundaries.

> 📋 For a complete reference of all CLI flags related to permissions, see
> [Chapter 15: CLI Flags, Scripting & Automation](./15-cli-flags-scripting-and-automation.md).

---

Next: [Chapter 15: CLI Flags, Scripting & Automation](./15-cli-flags-scripting-and-automation.md)
