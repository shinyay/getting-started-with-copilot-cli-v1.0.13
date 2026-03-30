# Chapter 10: Plugins & Skills

Copilot CLI's extensibility model revolves around two complementary concepts:
**plugins** and **skills**. Plugins are installable packages that bundle multiple
extension types into a single distributable unit. Skills are discrete, callable
capabilities — often packaged inside plugins but also definable standalone in your
repository or user configuration. Together, they let you tailor Copilot CLI to any
workflow, toolchain, or domain.

> 📋 This chapter builds on concepts from [Chapter 9: MCP Servers](./09-mcp-servers.md).
> MCP servers are one of several extension types a plugin can bundle.

---

## Plugin System Overview

The plugin system (introduced in **v0.0.392**, January 2026) provides a unified
mechanism for extending Copilot CLI. A single plugin can contain any combination
of the following extension types:

| Extension Type | Purpose | Available Since |
|----------------|---------|-----------------|
| Custom Agents | Specialized agent definitions (`.agent.md` files) | v0.0.396 |
| Skills | Callable capabilities with instructions and tool access | v0.0.395 |
| MCP Servers | Model Context Protocol server configurations | v0.0.389 |
| Hooks | Session lifecycle event handlers | v0.0.402 |
| LSP Servers | Language Server Protocol configurations | v0.0.405 |
| Commands | Slash-command definitions (translated to skills) | v0.0.406 |

Plugins are stored locally in `~/.copilot/plugins/` and are sourced from GitHub
repositories, local directories, or plugin marketplaces.

> 💡 Plugins installed from GitHub repos are cloned locally, so they work offline
> after the initial install. Updates require network access.

---

## Plugin Structure

A well-formed plugin follows this directory layout:

```
my-plugin/
├── plugin.json           # Manifest — name, description, version, extension paths
├── agents/
│   └── my-agent.agent.md # Custom agent definitions
├── skills/
│   └── deploy/
│       └── SKILL.md      # Skill definition with instructions
├── mcp-servers/
│   └── server-config.json # MCP server configurations
├── hooks/
│   └── pre-tool.js       # Lifecycle hook handlers
├── commands/
│   └── lint.md           # Command files (auto-translated to skills)
└── README.md             # Plugin documentation
```

### The `plugin.json` Manifest

Every plugin requires a `plugin.json` at the root. This manifest tells Copilot CLI
what the plugin provides and where to find each extension.

```json
{
  "name": "my-deploy-plugin",
  "description": "Production deployment workflows for cloud-native applications",
  "version": "1.2.0",
  "author": "your-org",
  "license": "MIT",
  "agents": [
    "agents/deploy-agent.agent.md",
    "agents/rollback-agent.agent.md"
  ],
  "skills": [
    "skills/deploy",
    "skills/rollback",
    "skills/health-check"
  ],
  "mcpServers": {
    "cloud-api": {
      "command": "node",
      "args": ["mcp-servers/cloud-api/index.js"],
      "env": {
        "CLOUD_REGION": "us-east-1"
      }
    }
  },
  "hooks": {
    "preToolUse": "hooks/pre-tool.js",
    "agentStop": "hooks/on-stop.js"
  },
  "lspServers": {
    "terraform": {
      "command": "terraform-ls",
      "args": ["serve"],
      "languages": ["terraform", "hcl"]
    }
  },
  "minimumCopilotVersion": "0.0.392"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique plugin identifier (kebab-case recommended) |
| `description` | string | Yes | Brief description shown in `/plugin list` |
| `version` | string | No | Semantic version (informational, not enforced) |
| `author` | string | No | Plugin author or organization |
| `license` | string | No | SPDX license identifier |
| `agents` | string[] | No | Paths to `.agent.md` files relative to plugin root |
| `skills` | string[] | No | Paths to skill directories containing `SKILL.md` |
| `mcpServers` | object | No | MCP server configurations (same format as `mcp.json`) |
| `hooks` | object | No | Hook type → handler file path mappings |
| `lspServers` | object | No | LSP server configurations keyed by language ID |
| `minimumCopilotVersion` | string | No | Minimum Copilot CLI version required |

> ⚠️ Agent file paths specified in `plugin.json` must be relative to the plugin
> root directory. Absolute paths are rejected. This was fixed in **v0.0.418** —
> earlier versions silently failed to load agents with incorrectly specified paths.

### Template Variable Support

Since v1.0.12, hook and plugin configuration values support **template variables**
that are expanded at runtime:

| Variable | Expands To | Since |
|----------|-----------|-------|
| `{{project_dir}}` | Absolute path to the current project root | v1.0.12 |
| `{{plugin_data_dir}}` | Plugin-specific data directory | v1.0.12 |

```json
{
  "hooks": {
    "preToolUse": "{{project_dir}}/hooks/guard.js"
  },
  "mcpServers": {
    "local-db": {
      "command": "node",
      "args": ["{{plugin_data_dir}}/server.js"]
    }
  }
}
```

> 💡 Template variables eliminate hardcoded absolute paths, making plugin
> configurations portable across developer machines and operating systems.

---

## Installing Plugins

### The `/plugin install` Command

Install plugins from multiple sources using the `/plugin install` slash command:

```
/plugin install owner/repo
/plugin install https://github.com/owner/repo
/plugin install /local/path/to/plugin
/plugin install ssh://git@github.com/owner/repo
```

| Source Type | Syntax | Available Since |
|-------------|--------|-----------------|
| GitHub shorthand | `owner/repo` | v0.0.392 |
| HTTPS URL | `https://github.com/owner/repo` | v0.0.392 |
| Local directory | `/path/to/plugin` | v0.0.396 |
| Local path (with spaces) | `"/path/with spaces/plugin"` | v0.0.415 |
| SSH URL | `ssh://git@github.com/owner/repo` | v0.0.422 |
| Local dir flag | `--plugin-dir /path` | v0.0.421 |

**Installation examples:**

```bash
# Install from GitHub shorthand
/plugin install acme-corp/copilot-deploy

# Install from a specific tag
/plugin install acme-corp/copilot-deploy@v2.1.0

# Install from local development directory
/plugin install --plugin-dir ./my-local-plugin

# Install from SSH (useful behind corporate firewalls)
/plugin install ssh://git@github.com/acme-corp/copilot-deploy
```

> 💡 When installing from a local path, Copilot CLI creates a symlink rather than
> a copy. Changes you make to the local plugin are reflected immediately — ideal
> for plugin development.

### Plugin Management Commands

| Command | Description | Since |
|---------|-------------|-------|
| `/plugin install [source]` | Install a plugin from repo, URL, or path | v0.0.392 |
| `/plugin update [name]` | Update one or all installed plugins | v0.0.396 |
| `/plugin list` | List all installed plugins with status | v0.0.392 |
| `/plugin uninstall [name]` | Remove a plugin and clean up resources | v0.0.392 |
| `/plugin marketplace add [url]` | Register a custom plugin marketplace | v0.0.409 |
| `copilot plugin` | Non-interactive plugin management from shell | v0.0.400 |

**Non-interactive management** (since v0.0.400) lets you manage plugins from
shell scripts and CI pipelines without entering interactive mode:

```bash
# List plugins in JSON format
copilot plugin list --json

# Install a plugin non-interactively
copilot plugin install acme-corp/deploy-tools

# Update all plugins
copilot plugin update --all

# Uninstall by name
copilot plugin uninstall deploy-tools
```

---

## Plugin Marketplaces

Marketplaces are curated directories of plugins. Copilot CLI ships with two
default marketplaces and supports custom registries.

### Default Marketplaces

| Marketplace | Description | Since |
|-------------|-------------|-------|
| `copilot-plugins` | Official curated plugins from GitHub | v0.0.409 |
| `awesome-copilot` | Community-maintained plugin directory | v0.0.409 |

### Adding Custom Marketplaces

```
/plugin marketplace add https://my-org.example.com/marketplace.json
```

### The `marketplace.json` Format

Since **v0.0.413**, marketplaces support remote plugin source definitions:

```json
{
  "name": "Acme Corp Plugins",
  "description": "Internal plugins for Acme Corp engineering",
  "plugins": [
    {
      "name": "acme-deploy",
      "description": "Deploy to Acme Cloud infrastructure",
      "source": "https://github.com/acme-corp/copilot-deploy",
      "tags": ["deploy", "cloud", "infrastructure"],
      "verified": true
    },
    {
      "name": "acme-db-tools",
      "description": "Database migration and query tools",
      "source": "https://github.com/acme-corp/copilot-db-tools",
      "tags": ["database", "migration"],
      "verified": true
    }
  ]
}
```

### Extra Known Marketplaces

Since **v0.0.421**, you can also register marketplaces in your settings file:

```json
// ~/.copilot/settings.json
{
  "extraKnownMarketplaces": [
    "https://internal.example.com/marketplace.json",
    "https://community.example.com/plugins.json"
  ]
}
```

> 💡 Enterprise teams can maintain a private marketplace to distribute approved
> internal plugins. This keeps tooling consistent without requiring manual
> install commands for each developer.

---

## Auto-Install with `enabledPlugins`

Since **v0.0.422**, you can configure plugins to install automatically when
Copilot CLI starts. Add an `enabledPlugins` array to your config file:

```json
// ~/.copilot/config.json
{
  "enabledPlugins": [
    "acme-corp/deploy-tools",
    "acme-corp/db-migration",
    "community/test-helpers"
  ]
}
```

On startup, Copilot CLI checks each entry:
1. If the plugin is not installed, it clones and installs it
2. If the plugin is already installed, it checks for updates
3. Failed installs are logged but do not block startup

> ⚠️ The `enabledPlugins` config triggers network requests on every Copilot CLI
> startup. In air-gapped environments or behind strict proxies, pre-install
> plugins manually and omit this config to avoid startup delays.

---

## Plugin Features in Detail

### Plugin Agents

Plugins can provide custom agent definitions that specialize Copilot CLI's
behavior for specific domains.

| Capability | Details | Since |
|------------|---------|-------|
| Custom agent bundling | Agents defined in plugin `agents/` directory | v0.0.396 |
| Hot-reload on install | Available immediately without restart | v0.0.417 |
| File path resolution | Agent paths in `plugin.json` resolve correctly | v0.0.418 |

A plugin agent file follows the same format as repository-level agents:

```markdown
<!-- agents/deploy-agent.agent.md -->
---
name: deploy-specialist
description: Expert in cloud deployment and infrastructure management
tools:
  - shell
  - read
  - edit
---

# Deploy Specialist Agent

You are a deployment expert. When asked to deploy, follow these steps...
```

### Plugin Skills

Skills bundled in plugins are discoverable and invocable just like repository
or user-level skills.

| Capability | Details | Since |
|------------|---------|-------|
| Basic skill loading | Skills from plugin `skills/` directory | v0.0.395 |
| Prompt mode support | Skills work in non-interactive prompt mode | v0.0.403 |
| Hot-reload on install | Available immediately without restart | v0.0.417 |
| Custom path loading | Skill paths specified in `plugin.json` | v0.0.417 |

### Plugin MCP Servers

MCP servers bundled in plugins are managed automatically by Copilot CLI:

| Capability | Details | Since |
|------------|---------|-------|
| Auto-load on install | Bundled servers start automatically | v0.0.389 |
| Visibility in `/mcp show` | Listed under a dedicated "Plugins" section | v0.0.389 |
| Stop before update | Servers gracefully stopped before plugin update | v0.0.403 |
| Stop on uninstall | Servers stopped and cleaned up on removal | v0.0.402 |

> 💡 Use `/mcp show` to verify that plugin MCP servers loaded correctly. They
> appear in a separate "Plugins" section distinct from project and user servers.

### Plugin LSP Servers

Since **v0.0.405**, plugins can bundle Language Server Protocol configurations
for enhanced code intelligence:

```json
// In plugin.json
{
  "lspServers": {
    "custom-lang": {
      "command": "custom-lang-server",
      "args": ["--stdio"],
      "languages": ["custom-lang"],
      "initializationOptions": {
        "diagnostics": true
      }
    }
  }
}
```

| Capability | Details | Since |
|------------|---------|-------|
| LSP bundling | Plugins can define LSP server configs | v0.0.405 |
| Full lifecycle | Auto-loaded, started, visible in `/lsp show` | v0.0.422 |

### Plugin Hooks

Hooks let plugins intercept and modify Copilot CLI's behavior at key lifecycle
points. Introduced in **v0.0.402**.

| Hook | Trigger | Use Cases |
|------|---------|-----------|
| `preToolUse` | Before any tool executes | Deny dangerous commands, modify parameters, add logging |
| `agentStop` | When the main agent completes | Clean up resources, send notifications, validate output |
| `subagentStop` | When a sub-agent completes | Aggregate results, chain follow-up actions |

**Example hook — blocking dangerous commands:**

```javascript
// hooks/pre-tool.js
module.exports = {
  name: 'safety-guard',
  async preToolUse({ tool, input }) {
    // Block destructive database commands
    if (tool === 'shell' && /DROP\s+TABLE/i.test(input.command)) {
      return {
        decision: 'deny',
        reason: 'Destructive SQL blocked by safety-guard plugin'
      };
    }

    // Allow everything else
    return { decision: 'allow' };
  }
};
```

**Example hook — notification on completion:**

```javascript
// hooks/on-stop.js
module.exports = {
  name: 'notify-on-complete',
  async agentStop({ result, sessionId }) {
    // Send a notification when a long task finishes
    if (result.turnCount > 10) {
      await fetch('https://hooks.slack.com/...', {
        method: 'POST',
        body: JSON.stringify({
          text: `Copilot session ${sessionId} completed (${result.turnCount} turns)`
        })
      });
    }
  }
};
```

> ⚠️ Hooks execute in the Copilot CLI process. A poorly written hook that throws
> an unhandled exception or blocks indefinitely can degrade the entire session.
> Always wrap hook logic in try/catch and set timeouts for async operations.

### Plugin & Hook Environment Variables

Since v1.0.12, the following environment variables are automatically set for all
hook and plugin processes:

| Variable | Value | Since |
|----------|-------|-------|
| `CLAUDE_PROJECT_DIR` | Absolute path to the current project root | v1.0.12 |
| `CLAUDE_PLUGIN_DATA` | Plugin-specific data directory path | v1.0.12 |

These variables use Claude-compatible naming for cross-tool portability. Access
them in hook handlers:

```javascript
// hooks/my-hook.js
const projectDir = process.env.CLAUDE_PROJECT_DIR;
const pluginData = process.env.CLAUDE_PLUGIN_DATA;
```

---

## Plugin Cache & Updates

Copilot CLI maintains a local cache of installed plugins in `~/.copilot/plugins/`.
Several robustness improvements have been made to the caching mechanism:

| Behavior | Details | Since |
|----------|---------|-------|
| Corrupted clone recovery | Auto-detects and re-clones broken plugin repos | v0.0.422 |
| Force-push handling | Correctly updates after upstream force-pushes | v0.0.420 |
| Tag-based installs | Pinned versions via `owner/repo@tag` work correctly | v0.0.396 |
| Windows file lock handling | Retries operations when files are locked by other processes | v0.0.420 |

**Updating plugins:**

```
# Update a specific plugin
/plugin update acme-deploy

# Update all installed plugins
/plugin update
```

> 💡 Pin production-critical plugins to a specific tag (`owner/repo@v1.0.0`)
> to avoid unexpected behavior changes from upstream updates. Use untagged
> installs only during development.

---

## Commands from Plugins

Since **v0.0.406**, plugins can include **command files** — simple markdown files
that are automatically translated into skills. This is the easiest way to add
new slash commands without writing a full `SKILL.md`.

```markdown
<!-- commands/lint.md -->
Run the project linter and report results.

## Steps
1. Detect the project type (Node.js, Python, Go, etc.)
2. Run the appropriate linter command
3. Summarize warnings and errors
4. Suggest fixes for the most critical issues
```

| Behavior | Details | Since |
|----------|---------|-------|
| Command → skill translation | Command files auto-convert to invocable skills | v0.0.406 |
| YAML frontmatter optional | Plain markdown with auto-derived name and description | v0.0.412 |
| Name derivation | Filename becomes the command name (`lint.md` → `/lint`) | v0.0.412 |

> 💡 Command files are the simplest plugin extension. If you only need a new
> slash command — no agents, hooks, or MCP servers — a single `.md` file in a
> `commands/` directory is all you need.

---

## Skills

### What Are Skills?

Skills are **discrete, callable capabilities** that enhance what Copilot CLI can
do. Think of them as specialized instruction sets that Copilot can invoke — either
when you explicitly request them via a slash command, or automatically when the
model determines a skill is relevant to your task.

Key characteristics:

- **Self-contained** — each skill includes its own instructions, tool permissions,
  and optional resources
- **Composable** — skills can reference other skills and chain together
- **Discoverable** — `/skills` lists all available skills with descriptions
- **Multi-source** — skills can come from your user config, repository, or plugins

### Skill File Format (`SKILL.md`)

A skill is defined by a `SKILL.md` file inside a named directory. The file
contains optional YAML frontmatter followed by markdown instructions:

```markdown
---
name: deploy
description: Deploy the application to the staging or production environment
allowed-tools:
  - shell
  - read
  - edit
  - mcp__cloud-api__deploy
disable-model-invocation: false
---

# Deploy Skill

You are a deployment specialist. Follow these steps precisely.

## Pre-flight Checks
1. Verify all tests pass: `npm test`
2. Check for uncommitted changes: `git status`
3. Confirm the target environment variable is set

## Deployment Steps
1. Build the production bundle: `npm run build`
2. Run database migrations if pending
3. Deploy using the cloud API MCP tool
4. Verify health endpoint responds with 200

## Rollback Plan
If deployment fails:
1. Revert to the previous version tag
2. Notify the team channel
3. Document the failure reason

> ⚠️ Never deploy on Fridays without explicit approval.
```

### YAML Frontmatter Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | No | Directory name | Skill identifier used as slash command |
| `description` | string | No | First paragraph | Brief description shown in `/skills` list |
| `allowed-tools` | string[] | No | All tools | Tools this skill can access (since v0.0.413: supports YAML array syntax; earlier: comma-separated only) |
| `disable-model-invocation` | boolean | No | `false` | When `true`, prevents Copilot from auto-invoking this skill |

> 💡 Omitting `name` and `description` is fine — Copilot derives them from the
> directory name and first paragraph of content. This keeps simple skills concise.

> ⚠️ The `allowed-tools` field restricts which tools the skill can use. If you
> reference an MCP tool (e.g., `mcp__server__tool`), ensure the corresponding
> MCP server is configured and running.

### Skill Locations

Skills are loaded from multiple locations, searched in the following priority order:

| Priority | Location | Path | Description |
|----------|----------|------|-------------|
| 1 | Repository (`.agents/`) | `.agents/skills/<name>/SKILL.md` | Project-specific skills (since v0.0.401) |
| 2 | Repository (`.claude/`) | `.claude/commands/<name>.md` | Claude-compatible single-file commands (since v0.0.399) |
| 3 | User | `~/.copilot/skills/<name>/SKILL.md` | Personal skills available across all projects |
| 4 | User (shared) | `~/.agents/skills/<name>/SKILL.md` | Personal skills shared with VS Code *(v1.0.11)* |
| 5 | Plugin | `<plugin>/skills/<name>/SKILL.md` | Skills bundled with installed plugins |

When skills share the same name, higher-priority locations take precedence.
Repository skills override user skills, which override plugin skills.

**Example repository skill structure:**

```
.agents/
└── skills/
    ├── deploy/
    │   └── SKILL.md
    ├── test-e2e/
    │   └── SKILL.md
    └── db-migrate/
        └── SKILL.md
```

### Managing Skills with `/skills`

| Command | Description | Since |
|---------|-------------|-------|
| `/skills` | List all available skills with source and description | v0.0.389 |
| `/skills add [path]` | Register an additional skill directory | v0.0.389 |

Behavioral notes:

| Behavior | Since |
|----------|-------|
| Skill changes take effect immediately (no restart needed) | v0.0.407 |
| Correct skill count when directory path has trailing slash | v0.0.396 |

### Invoking Skills

There are two ways skills get invoked:

**1. Explicit invocation** — type the skill name as a slash command:

```
/deploy staging
```

```
/test-e2e --browser chrome
```

**2. Model-initiated invocation** — Copilot automatically selects a relevant
skill based on your request. For example, asking "deploy this to staging"
may trigger the `deploy` skill without you typing `/deploy`.

> 💡 Set `disable-model-invocation: true` in the frontmatter of skills that
> should only run when explicitly requested — such as destructive operations
> like database wipes or production deployments.

### Skill Compatibility & Edge Cases

The skill system has matured through several releases. Here is a summary of
compatibility improvements:

| Behavior | Details | Since |
|----------|---------|-------|
| Slash command invocation | Skills invocable as `/skill-name` | v0.0.389 |
| Windows path loading | Skills load correctly on Windows file systems | v0.0.399 |
| Post-compaction persistence | Skills remain effective after context compaction | v0.0.399 |
| Uppercase names | Skill names with uppercase characters resolve correctly | v0.0.396 |
| Underscores in names | `my_skill` works as `/my_skill` | v0.0.396 |
| Dots in names | `my.skill` works as `/my.skill` | v0.0.410 |
| Spaces in names | Skill names with spaces are supported | v0.0.410 |
| UTF-8 BOM files | `SKILL.md` files with UTF-8 BOM load correctly | v0.0.415 |
| Unknown frontmatter fields | Warns instead of skipping the entire skill | v0.0.403 |
| YAML array syntax | `allowed-tools` supports standard YAML arrays | v0.0.413 |

---

## Creating a Plugin from Scratch

Follow this step-by-step guide to create, test, and share your own plugin.

### Step 1: Scaffold the Plugin

```bash
mkdir my-copilot-plugin && cd my-copilot-plugin
mkdir -p skills/greet agents hooks commands
```

### Step 2: Create the Manifest

Create `plugin.json`:

```json
{
  "name": "my-copilot-plugin",
  "description": "A sample plugin demonstrating skills, agents, and hooks",
  "version": "0.1.0",
  "skills": ["skills/greet"],
  "agents": ["agents/helper.agent.md"],
  "hooks": {
    "preToolUse": "hooks/guard.js"
  }
}
```

### Step 3: Define a Skill

Create `skills/greet/SKILL.md`:

```markdown
---
name: greet
description: Generate a friendly greeting message
allowed-tools:
  - shell
---

# Greet Skill

Generate a personalized greeting for the user. Ask for their name if not
provided, then print a creative, friendly greeting to the terminal.
```

### Step 4: Define an Agent

Create `agents/helper.agent.md`:

```markdown
---
name: helper
description: A helpful assistant for common development tasks
tools:
  - read
  - edit
  - shell
---

# Helper Agent

You assist with routine development tasks such as creating boilerplate files,
running common commands, and organizing project structure.
```

### Step 5: Add a Hook

Create `hooks/guard.js`:

```javascript
module.exports = {
  name: 'basic-guard',
  async preToolUse({ tool, input }) {
    // Log all tool invocations for audit purposes
    console.error(`[guard] Tool: ${tool}, Input length: ${JSON.stringify(input).length}`);
    return { decision: 'allow' };
  }
};
```

### Step 6: Add a README

Create `README.md`:

```markdown
# My Copilot Plugin

A sample plugin that demonstrates skills, agents, and hooks.

## Installation

\`\`\`
/plugin install /path/to/my-copilot-plugin
\`\`\`

## Features

- `/greet` — Generate a personalized greeting
- `helper` agent — Assist with routine dev tasks
- `basic-guard` hook — Audit all tool invocations
```

### Step 7: Test Locally

```bash
# Install from local directory
/plugin install --plugin-dir /path/to/my-copilot-plugin

# Verify it loaded
/plugin list

# Verify the skill is available
/skills

# Test the skill
/greet
```

### Step 8: Publish

Push the plugin to a GitHub repository, then anyone can install it:

```bash
git init && git add -A && git commit -m "Initial plugin release"
gh repo create my-copilot-plugin --public --push --source=.
```

Others install with:

```
/plugin install your-username/my-copilot-plugin
```

> 💡 Add your plugin to a marketplace by submitting a pull request to the
> marketplace repository's `marketplace.json` file with your plugin's metadata.

---

## Quick Reference: Plugins vs. Skills vs. Commands

| Aspect | Plugin | Skill | Command |
|--------|--------|-------|---------|
| **Scope** | Multi-extension package | Single capability | Single slash command |
| **File** | `plugin.json` + directories | `SKILL.md` in named directory | Single `.md` file |
| **Install** | `/plugin install` | Place in skills directory | Place in commands directory |
| **Contains** | Agents, skills, MCP, hooks, LSP | Instructions + tool permissions | Markdown instructions |
| **Distribution** | GitHub repo or marketplace | Part of repo or plugin | Part of repo or plugin |
| **Complexity** | High (most flexible) | Medium | Low (simplest) |

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Plugin installs but skills don't appear | Paths in `plugin.json` don't match actual file locations | Verify paths are relative to plugin root |
| `/plugin list` shows plugin but agent is missing | Agent file path in manifest is absolute | Use relative paths in the `agents` array |
| MCP server from plugin won't start | Missing runtime dependency (Node.js, Python) | Install the required runtime on your system |
| Hook crashes Copilot CLI session | Unhandled exception in hook code | Wrap all hook logic in try/catch |
| Plugin won't update | Upstream force-push with divergent history | Uninstall and reinstall, or update to v0.0.420+ |
| Skills with special characters in name fail | Running older CLI version | Update to v0.0.410+ for full character support |
| Marketplace plugins fail to install behind proxy | Corporate firewall blocking GitHub | Use SSH URLs or pre-clone locally |

> ⚠️ If a plugin fails to load after a Copilot CLI update, check the
> `minimumCopilotVersion` field in `plugin.json`. The plugin author may need
> to update their manifest for newer CLI versions.

---

## Summary

Plugins and skills transform Copilot CLI from a general-purpose assistant into a
domain-specific powerhouse. Start with simple skills for your most common workflows,
graduate to full plugins when you need agents, hooks, or MCP servers, and share
your creations through marketplaces to benefit your team and the community.

| What You Learned | Key Takeaway |
|------------------|--------------|
| Plugin structure | `plugin.json` manifest + organized extension directories |
| Installation sources | GitHub repos, local paths, SSH URLs, marketplaces |
| Plugin features | Agents, skills, MCP servers, hooks, LSP servers |
| Skill definitions | `SKILL.md` with optional YAML frontmatter |
| Skill locations | Repository (`.agents/`, `.claude/`), user, plugin |
| Skill invocation | Explicit (`/skill-name`) or model-initiated |
| Plugin lifecycle | Install → use → update → uninstall, with auto-install option |
| Creating plugins | Scaffold → manifest → extensions → test → publish |

---

Next: [Chapter 11: Session Management & Memory](./11-session-management-and-memory.md)
