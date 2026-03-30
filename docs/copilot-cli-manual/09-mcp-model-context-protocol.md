# Chapter 9: MCP (Model Context Protocol)

MCP is one of the most powerful extensibility features in GitHub Copilot CLI. It
transforms Copilot from a standalone AI assistant into a **connected platform**
that can interact with databases, APIs, file systems, and virtually any external
service — all through a single, standardized protocol.

This chapter covers everything you need to know about MCP: what it is, how to
configure it, the built-in GitHub MCP server, and how to add your own servers.

---

## 9.1 What is MCP?

**Model Context Protocol (MCP)** is an open standard that defines how AI models
communicate with external tools and data sources. Originally developed by
Anthropic and now adopted across the AI ecosystem, MCP provides a uniform
interface for tool invocation, context retrieval, and structured interaction.

### The "USB for AI" Analogy

Think of MCP as **USB for AI assistants**:

| USB | MCP |
|-----|-----|
| Standardized connector for peripherals | Standardized protocol for AI tools |
| Plug in a keyboard, mouse, or printer | Plug in a database, API, or file system |
| Device drivers handle the translation | MCP servers handle the translation |
| Works across different computers | Works across different AI models |

Before MCP, every AI tool integration required custom code. With MCP, any
compliant server can be connected to any compliant client — including
GitHub Copilot CLI.

### How MCP Works in Copilot CLI

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Copilot CLI  │────▶│   MCP Client     │────▶│   MCP Server     │
│  (user prompt)│     │   (built into    │     │   (stdio process  │
│               │◀────│    Copilot CLI)  │◀────│    or HTTP)       │
│  (AI response)│     │                  │     │                   │
└──────────────┘     └──────────────────┘     └──────────────────┘
                                                      │
                                                      ▼
                                               ┌──────────────┐
                                               │  External     │
                                               │  Service      │
                                               │  (DB, API,    │
                                               │   filesystem) │
                                               └──────────────┘
```

1. **You ask Copilot** a question or give it a task
2. **Copilot recognizes** it needs external data or capabilities
3. **Copilot calls an MCP tool** exposed by a configured server
4. **The MCP server** executes the operation and returns results
5. **Copilot incorporates** the results into its response

> 💡 Copilot CLI ships with the GitHub MCP server enabled by default — you get
> GitHub integration out of the box with zero configuration.

---

## 9.2 Built-in GitHub MCP Server

The GitHub MCP server is bundled with Copilot CLI and provides direct access to
GitHub's API. Since **v0.0.350**, it ships with a curated default tool set
designed to conserve context window tokens while covering the most common
workflows.

### Default Tools (Read-Only)

The default tool set is intentionally conservative — read-only operations that
help you explore code, issues, and pull requests without risk of modification.

| Category | Tool | Description |
|----------|------|-------------|
| **Code & Repo** | `get_file_contents` | Read file or directory contents from a repo |
| | `search_code` | Search code across repositories |
| | `search_repositories` | Find repositories by name, topic, or metadata |
| | `list_branches` | List branches in a repository |
| | `list_commits` | List commits on a branch |
| | `get_commit` | Get details and diff for a specific commit |
| **Issues** | `get_issue` | Get details of a specific issue |
| | `list_issues` | List issues in a repository |
| | `get_issue_comments` | Get comments on an issue |
| | `search_issues` | Search issues across repositories |
| **Pull Requests** | `pull_request_read` | Get PR details, diff, files, reviews, checks |
| | `list_pull_requests` | List PRs in a repository |
| | `search_pull_requests` | Search PRs across repositories |
| **Actions** | `list_workflows` | List workflows in a repository |
| | `list_workflow_runs` | List runs for a workflow |
| | `get_workflow_run` | Get details of a specific run |
| | `get_job_logs` | Get logs for a workflow job |
| | `get_workflow_run_logs` | Get logs URL for a workflow run |
| **Other** | `user_search` | Search for GitHub users |
| | `list_copilot_spaces` | List accessible Copilot Spaces *(since v0.0.373)* |
| | `get_copilot_space` | Get details of a specific Copilot Space |

> 💡 The default set is curated to conserve context. Each tool's schema
> consumes tokens, so fewer tools means more room for your actual conversation.

### Enabling Full Tool Access

To unlock **read-write tools** (create issues, merge PRs, push commits, manage
labels, and more), use the `--enable-all-github-mcp-tools` flag:

```bash
# Start Copilot with full GitHub API access
copilot --enable-all-github-mcp-tools
```

This flag was introduced in **v0.0.388** and enables operations such as:

| Operation | Tool |
|-----------|------|
| Create/update issues | `create_issue`, `update_issue` |
| Manage pull requests | `create_pull_request`, `merge_pull_request` |
| Add comments | `add_issue_comment` |
| Manage labels | `add_label`, `remove_label` |
| Create branches | `create_branch` |
| Push file changes | `create_or_update_file` |

> ⚠️ With full tool access enabled, Copilot can **modify your repositories**.
> Always review tool calls before approving them, especially for destructive
> operations like merging PRs or deleting branches.

---

## 9.3 MCP Configuration Locations

Copilot CLI looks for MCP configuration in multiple locations, applied in a
specific priority order. Later sources override earlier ones.

| Priority | Location | File | Scope | Since |
|----------|----------|------|-------|-------|
| 1 (lowest) | Built-in | Bundled with CLI | Always active | — |
| 2 | Plugin | Plugin package | Per plugin | — |
| 3 | User | `~/.copilot/mcp-config.json` | All projects | — |
| 4 | Workspace | `.vscode/mcp.json` | Current project | v0.0.407 |
| 5 | Git root | `.mcp.json` | Current project | v1.0.12 |
| 6 | Windows Registry | On-Device Registry | System-wide | v0.0.411 |
| 7 (highest) | CLI Flag | `--additional-mcp-config` | Per session | v0.0.343 |

### When to Use Each Location

```
User config (~/.copilot/mcp-config.json)
  └── Tools you want everywhere: databases, note-taking, personal APIs

Workspace config (.vscode/mcp.json)
  └── Project-specific tools: project database, staging API, local services

CLI Flag (--additional-mcp-config)
  └── Temporary or experimental servers, CI/CD environments, overrides
```

> 💡 Workspace configuration in `.vscode/mcp.json` is shared with VS Code's
> Copilot extension, so the same MCP servers work in both the editor and CLI.

---

## 9.4 `/mcp` Commands

Copilot CLI provides a complete set of slash commands for managing MCP servers
interactively.

### `/mcp add` — Add a New Server

The `/mcp add` command opens an interactive form where you configure a new MCP
server:

```
/mcp add
```

**Form fields:**

| Field | Description | Required |
|-------|-------------|----------|
| Name | Unique identifier for the server | Yes |
| Type | `stdio` (local process) | Yes |
| Command | Executable to run | Yes |
| Arguments | Command-line arguments | No |
| Working Directory | `cwd` for the server process | No |
| Environment Variables | Key-value pairs | No |
| Scope | User or Workspace | Yes |

**Navigation:**

| Key | Action |
|-----|--------|
| `Tab` | Move to next field |
| `Shift+Tab` | Move to previous field |
| `Ctrl+S` | Save and start the server |
| `Escape` | Cancel without saving |

> 💡 Since **v0.0.339**, the command field accepts the full command string
> (no comma-separated arguments). Since **v0.0.407**, editing an existing
> server pre-fills the form with its current values.

### `/mcp show` — View Configured Servers

```
/mcp show
```

Displays all configured MCP servers grouped by source:

- **Built-in** — Servers bundled with Copilot CLI (e.g., GitHub)
- **User** — Servers from `~/.copilot/mcp-config.json`
- **Workspace** — Servers from `.vscode/mcp.json`
- **Plugins** — Servers provided by installed plugins

Since **v0.0.415**, all groups are displayed with clear headings and navigation.

To view details and the full tool list for a specific server:

```
/mcp show github
```

```
/mcp show my-database
```

> 💡 Since **v0.0.406**, `/mcp show` displays enabled/disabled status for
> individual tools within each server.

### `/mcp enable` / `/mcp disable` — Toggle Servers

```
/mcp enable my-database
```

```
/mcp disable my-database
```

Toggle an MCP server on or off without removing its configuration. This is
useful for temporarily disabling a server that is slow or consuming too many
context tokens.

Since **v0.0.419**, this also works for built-in servers that were
auto-disabled. Since **v0.0.407**, attempting to enable/disable a non-existent
server produces a clear error message.

### `/mcp reload` — Reload Configuration

```
/mcp reload
```

Re-reads all MCP configuration files and restarts servers as needed, without
restarting Copilot CLI itself. Added in **v0.0.412**.

> 💡 Use `/mcp reload` after editing your `mcp-config.json` or `.vscode/mcp.json`
> file — no need to quit and restart the CLI.

---

## 9.5 Server Configuration Format

### Local (stdio) Server

The most common server type runs as a local subprocess communicating over
standard input/output (stdio):

```json
{
  "mcpServers": {
    "my-database": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "cwd": "/path/to/project",
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### Configuration Fields Reference

| Field | Type | Required | Description | Since |
|-------|------|----------|-------------|-------|
| `type` | `string` | Yes | Transport type: `"stdio"` or `"Local"` (synonymous) | v0.0.370 |
| `command` | `string` | Yes | Executable to run (e.g., `"npx"`, `"python"`, `"node"`) | — |
| `args` | `string[]` | No | Command-line arguments passed to the executable | — |
| `cwd` | `string` | No | Working directory for the server process (supports `~` expansion) | v0.0.410 |
| `env` | `object` | No | Environment variables as key-value string pairs | — |
| `tools` | `string[]` | No | Allowed tool names (defaults to all if omitted) | v0.0.404 |

> 💡 The `tools` field is powerful for restricting a server to only the tools
> you need. This conserves context tokens and reduces noise in tool selection.

### Environment Variables in Configuration

Environment variables use the `${VAR_NAME}` syntax:

```json
{
  "mcpServers": {
    "my-api": {
      "type": "stdio",
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_KEY": "${MY_API_KEY}",
        "API_URL": "https://api.example.com",
        "DEBUG": "true"
      }
    }
  }
}
```

| Syntax | Meaning |
|--------|---------|
| `"${VAR_NAME}"` | Replaced with the value of environment variable `VAR_NAME` |
| `"literal-value"` | Used as-is (no substitution) |

> ⚠️ The variable reference syntax changed in **v0.0.340**. Ensure you use
> `${VAR_NAME}` (with curly braces), not `$VAR_NAME`.

Since **v0.0.419**, environment variables referenced in `command`, `args`, or
`cwd` fields are automatically included in the server's environment — you do
not need to duplicate them in the `env` block.

### Plugin Environment Variables

Since v1.0.12, the following environment variables are automatically available to
hooks, plugins, and MCP server processes:

| Variable | Value | Since |
|----------|-------|-------|
| `CLAUDE_PROJECT_DIR` | Absolute path to the current project root | v1.0.12 |
| `CLAUDE_PLUGIN_DATA` | Plugin-specific data directory path | v1.0.12 |

> 💡 These variables use Claude-compatible naming for cross-tool portability.
> They are available alongside the existing `COPILOT_CLI` detection variable.

### Claude-Compatible Format

Since **v0.0.401**, Copilot CLI also supports a simplified format without the
`mcpServers` wrapper, compatible with Claude's `.mcp.json` convention:

```json
{
  "my-database": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres"]
  }
}
```

> 💡 Both formats are valid. The wrapped `{ "mcpServers": { ... } }` format is
> recommended for clarity and forward compatibility.

---

## 9.6 `--additional-mcp-config` Flag

For per-session or ephemeral MCP configurations, use the
`--additional-mcp-config` flag (added in **v0.0.343**):

### Inline JSON

```bash
copilot --additional-mcp-config '{"mcpServers": {"my-tool": {"type": "stdio", "command": "my-server"}}}'
```

### From a File

```bash
copilot --additional-mcp-config @/path/to/config.json
```

### Multiple Configurations

```bash
copilot --additional-mcp-config @base.json --additional-mcp-config @overrides.json
```

When multiple configurations are provided, **later values override earlier ones**
for servers with the same name. This makes it easy to compose configurations:

```bash
# Base config defines the server; overrides changes the database URL
copilot \
  --additional-mcp-config @mcp-base.json \
  --additional-mcp-config '{"mcpServers": {"db": {"env": {"DATABASE_URL": "postgres://staging:5432/mydb"}}}}'
```

> 💡 The `@` prefix for file paths follows the same convention as `curl` and
> other CLI tools. Without `@`, the value is treated as inline JSON.

---

## 9.7 OAuth 2.0 Authentication

MCP servers can authenticate using **OAuth 2.0** for secure access to external
services. This feature was introduced in **v0.0.389**.

### How It Works

1. The MCP server declares that it requires OAuth authentication
2. Copilot CLI opens a browser window for the OAuth authorization flow
3. After authorization, tokens are stored and refreshed automatically
4. Subsequent tool calls use the stored token transparently

### Supported Providers

| Provider | Auto-Configuration | Since |
|----------|--------------------|-------|
| Microsoft / Entra ID | Yes — automatic setup | v0.0.407 |
| Generic OAuth 2.0 | Manual configuration | v0.0.389 |

Since **v0.0.423**, MCP servers can request URL visits for OAuth flows or API
key entry, with Copilot presenting the URL to the user inline.

> ⚠️ OAuth tokens are stored in your local system's credential store. Never
> commit MCP configuration files that contain hardcoded tokens or secrets.

---

## 9.8 MCP Server Instructions

Since **v0.0.400**, MCP servers can provide **instructions** — text that
augments Copilot's system prompt when the server is active. This allows servers
to teach Copilot how to use their tools effectively.

For example, a database MCP server might include instructions like:

```
Always use parameterized queries. Never construct SQL by string concatenation.
Prefer SELECT with explicit columns over SELECT *.
```

These instructions are injected automatically when the server is loaded and
apply for the duration of the session.

> 💡 Server instructions are a powerful way to improve Copilot's behavior
> with specialized tools. If you are building your own MCP server, include
> clear instructions that describe best practices for your tools.

### Organization MCP Policy Enforcement

Since v1.0.11, GitHub organizations can enforce **MCP server policies** that control
which third-party MCP servers are allowed, blocked, or require approval. This gives
enterprise administrators centralized governance over MCP extensibility.

| Policy Action | Effect | Since |
|---------------|--------|-------|
| Allow | Server loads normally | v1.0.11 |
| Block | Server is prevented from loading; user sees a policy message | v1.0.11 |
| Require approval | Server requires admin approval before first use | v1.0.11 |

> ⚠️ Policy enforcement applies to third-party servers only. The built-in GitHub
> MCP server is always available regardless of organization policy settings.

---

## 9.9 MCP Elicitations (Experimental)

**MCP Elicitations** allow servers to request structured input from the user
via interactive forms, rather than free-text prompts. This feature is
experimental, introduced in **v0.0.421**.

### Capabilities

| Feature | Description | Since |
|---------|-------------|-------|
| Structured forms | Servers define fields with types, labels, and validation | v0.0.421 |
| Multi-line text | Taller text input areas for longer content | v0.0.421 |
| Simplified single-field | Single-field forms hide the tab bar for cleaner UX | v0.0.421 |
| Enter to confirm | Press Enter to confirm selection (✓ indicator shown) | v0.0.423 |

### Example Flow

```
1. MCP server needs a database connection string
2. Server sends an elicitation request with form fields:
   - Host (text, required)
   - Port (number, default: 5432)
   - Database name (text, required)
   - SSL mode (dropdown: disable, require, verify-full)
3. Copilot CLI renders the form in the terminal
4. User fills in values and confirms
5. Server receives structured input and proceeds
```

> ⚠️ Elicitations are an **experimental feature** and the API may change in
> future releases. Use them in personal workflows but avoid depending on them
> in shared team configurations until the feature stabilizes.

### MCP Sampling

Since v1.0.13, MCP servers can request **LLM inference** from the client through
the MCP sampling capability. This allows a server to ask the model a question and
receive a response — enabling server-side reasoning, summarization, or
classification without the server needing its own model access.

| Aspect | Details | Since |
|--------|---------|-------|
| Server-initiated LLM requests | Servers can request inference with user approval | v1.0.13 |
| User confirmation | Each sampling request requires explicit user consent | v1.0.13 |
| Context isolation | Sampling requests use a separate context from the main conversation | v1.0.13 |

> ⚠️ MCP sampling adds a new trust boundary — a server can influence model
> behavior through crafted inference requests. Always review sampling prompts
> before approving them.

---

## 9.10 MCP Tool Results

MCP tools can return rich, structured results beyond plain text.

### Result Types

| Type | Description | Since |
|------|-------------|-------|
| Plain text | Simple string responses | — |
| Structured content | Images, resources, formatted data | v0.0.406 |
| Progress messages | Real-time status updates in the timeline | v0.0.389 |
| Tool notifications | Asynchronous updates from long-running tools | v0.0.354 |

### Large Result Handling

Since **v0.0.376**, large tool outputs are automatically written to disk to
avoid memory issues. This is transparent to the user — Copilot reads the
results from disk and incorporates them normally.

```
Tool output size   → Handling
─────────────────────────────────
< 100 KB           → In-memory (normal)
100 KB – 10 MB     → Written to temp file, read back
> 10 MB            → Written to temp file, summarized
```

> 💡 If an MCP tool returns very large results frequently, consider using the
> `tools` field in your server config to limit which tools are available, or
> ask the server author to implement pagination.

---

## 9.11 MCP in Special Contexts

MCP servers integrate with various Copilot CLI execution modes and contexts:

| Context | Support | Since |
|---------|---------|-------|
| Interactive mode | Full support | — |
| Prompt mode (`-p`) | MCP tools available in one-shot prompts | v0.0.363 |
| ACP mode | MCP servers apply to agent-controlled processes | v0.0.402 |
| Custom agents | Servers start correctly for custom agent contexts | v0.0.384 |

### Performance Optimizations

Several improvements ensure MCP servers work efficiently in all contexts:

| Optimization | Description | Since |
|--------------|-------------|-------|
| No unnecessary restarts | Custom agents with MCP reuse running servers | v0.0.390 |
| Concurrent shutdown | Multiple servers shut down in parallel | v0.0.404 |
| Pre-update stop | Servers stop before plugin updates to avoid conflicts | v0.0.403 |
| Delete requests | Cleanup requests sent on shutdown | v0.0.400 |

> 📋 For custom agents, see [Chapter 12](./12-custom-agents.md). For prompt
> mode, see [Chapter 5: Execution Modes](./05-execution-modes.md).

---

## 9.12 MCP Server Names

MCP server names support a wide range of characters to accommodate package
naming conventions from various ecosystems:

| Format | Example | Since |
|--------|---------|-------|
| Simple | `my-database` | — |
| Dotted | `io.github.server` | v0.0.419 |
| Scoped (npm-style) | `@modelcontextprotocol/server` | v0.0.419 |
| Slashed | `github/copilot-mcp` | v0.0.419 |

Name validation was added in **v0.0.337** to prevent invalid characters from
causing configuration errors.

> ⚠️ While special characters in names are supported, avoid spaces and
> shell-special characters (`$`, `` ` ``, `!`) to prevent quoting issues
> when using `/mcp` commands.

---

## 9.13 Troubleshooting

### Common Issues and Solutions

| Issue | Cause | Solution | Fixed In |
|-------|-------|----------|----------|
| Python MCP server times out on startup | stdout buffering prevents handshake | Use `python -u` (unbuffered) or set `PYTHONUNBUFFERED=1` in env | v0.0.421 |
| Server fails intermittently | Race condition during loading | Retry or run `/mcp reload` | v0.0.417 |
| One invalid tool schema breaks all tools | Strict validation rejected entire server | Invalid tools are now skipped individually | v0.0.412 |
| Third-party MCP servers blocked | Organization Copilot MCP policy | Contact your GitHub org admin to review MCP policy | v0.0.416 |
| Server not loading at all | Configuration format error | Run `/mcp show` to check status, verify JSON syntax | — |
| Server loads but no tools appear | Tool names filtered or server error | Check `tools` field in config; check server logs | — |
| Environment variable not resolved | Wrong syntax or var not set | Verify `${VAR_NAME}` syntax and that the variable is exported | v0.0.340 |

### Diagnostic Steps

**Step 1: Check server status**

```
/mcp show
```

Look for your server in the output. Check if it shows as enabled or disabled.

**Step 2: Check specific server details**

```
/mcp show my-server-name
```

Review the tool list and look for error messages.

**Step 3: Reload configuration**

```
/mcp reload
```

This re-reads config files and restarts servers.

**Step 4: Verify configuration file syntax**

```bash
# Validate JSON syntax
cat ~/.copilot/mcp-config.json | python3 -m json.tool
```

**Step 5: Check server process manually**

```bash
# Test if the server command runs
npx -y @modelcontextprotocol/server-postgres
```

> 💡 Most MCP issues fall into two categories: **configuration errors** (wrong
> JSON syntax, missing env vars) or **server startup failures** (missing
> dependencies, wrong command path). The diagnostic steps above cover both.

---

## 9.14 Example: Adding a PostgreSQL Database Server

This walkthrough demonstrates adding an MCP server that connects Copilot to a
PostgreSQL database, allowing you to query schemas, run SQL, and explore data.

### Prerequisites

- Node.js 18+ installed
- A running PostgreSQL instance
- Database connection URL

### Step 1: Set Your Database URL

```bash
export DATABASE_URL="postgres://user:password@localhost:5432/mydb"
```

### Step 2: Add the Server via CLI

```
/mcp add
```

Fill in the form:

| Field | Value |
|-------|-------|
| Name | `my-database` |
| Type | `stdio` |
| Command | `npx` |
| Arguments | `-y @modelcontextprotocol/server-postgres` |
| Environment | `DATABASE_URL` = `${DATABASE_URL}` |
| Scope | User |

Press `Ctrl+S` to save.

### Step 3: Verify the Server

```
/mcp show my-database
```

You should see the server listed with its available tools.

### Step 4: Use It

Now you can ask Copilot questions about your database:

```
What tables are in my database?
```

```
Show me the schema for the users table
```

```
Write a query to find all orders placed in the last 7 days
```

### Equivalent Manual Configuration

If you prefer to edit the config file directly:

```json
{
  "mcpServers": {
    "my-database": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

Save this to `~/.copilot/mcp-config.json` for global access, or
`.vscode/mcp.json` for project-specific access.

> ⚠️ Never hardcode database credentials in configuration files that are
> committed to version control. Always use environment variable references.

---

## 9.15 Example: Adding a File System Server

This walkthrough demonstrates adding an MCP server that gives Copilot
read-only access to a directory, useful for exploring documentation, logs,
or configuration files outside the current working directory.

### Step 1: Add the Server

```
/mcp add
```

| Field | Value |
|-------|-------|
| Name | `project-docs` |
| Type | `stdio` |
| Command | `npx` |
| Arguments | `-y @modelcontextprotocol/server-filesystem /path/to/docs` |
| Scope | Workspace |

### Step 2: Restrict Tools (Optional)

To limit the server to read-only operations, specify allowed tools in your
configuration:

```json
{
  "mcpServers": {
    "project-docs": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/docs"],
      "tools": ["read_file", "list_directory", "search_files"]
    }
  }
}
```

### Step 3: Use It

```
List all markdown files in my project docs
```

```
Summarize the architecture document
```

```
Find all references to "authentication" in the docs folder
```

> 💡 The `tools` field restricts which MCP tools Copilot can call. This is
> especially useful for file system servers where you want to prevent
> accidental writes to important directories.

---

## 9.16 Quick Reference

### MCP Slash Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/mcp add` | Add a new MCP server interactively | `/mcp add` |
| `/mcp show` | List all configured servers | `/mcp show` |
| `/mcp show <name>` | Show details for one server | `/mcp show github` |
| `/mcp enable <name>` | Enable a disabled server | `/mcp enable my-db` |
| `/mcp disable <name>` | Disable a server | `/mcp disable my-db` |
| `/mcp reload` | Reload all MCP configuration | `/mcp reload` |

### CLI Flags

| Flag | Purpose | Since |
|------|---------|-------|
| `--additional-mcp-config` | Add per-session MCP config (inline JSON or `@file`) | v0.0.343 |
| `--enable-all-github-mcp-tools` | Enable read-write GitHub MCP tools | v0.0.388 |

### Configuration Files

| File | Location | Scope |
|------|----------|-------|
| `~/.copilot/mcp-config.json` | Home directory | Global (all projects) |
| `.vscode/mcp.json` | Project root | Workspace (current project) |
| `.mcp.json` | Git root | Current project *(v1.0.12)* |

### Version History Highlights

| Version | Feature |
|---------|---------|
| v0.0.337 | Server name validation |
| v0.0.339 | Full command input in `/mcp add` form |
| v0.0.340 | `${VAR_NAME}` env var syntax |
| v0.0.343 | `--additional-mcp-config` flag |
| v0.0.350 | Curated default GitHub MCP tools |
| v0.0.354 | Tool notifications |
| v0.0.363 | MCP in prompt mode (`-p`) |
| v0.0.370 | `"Local"` as alias for `"stdio"` type |
| v0.0.376 | Large outputs written to disk |
| v0.0.384 | Correct server start for custom agents |
| v0.0.388 | `--enable-all-github-mcp-tools` |
| v0.0.389 | OAuth 2.0, progress messages |
| v0.0.400 | Server instructions, delete on shutdown |
| v0.0.401 | Claude-compatible `.mcp.json` format |
| v0.0.404 | `tools` field, concurrent shutdown |
| v0.0.406 | Structured content, tool enabled/disabled status |
| v0.0.407 | Workspace config, edit pre-fill, Microsoft OAuth |
| v0.0.410 | `~` expansion in `cwd` |
| v0.0.412 | `/mcp reload`, resilient tool schema handling |
| v0.0.415 | Grouped server display |
| v0.0.416 | MCP policy support |
| v0.0.417 | Improved server loading reliability |
| v0.0.419 | Extended name characters, env var auto-include, built-in toggle |
| v0.0.421 | MCP Elicitations, Python stdout fix |
| v0.0.423 | URL visit requests, enter-to-confirm |
| v1.0.5 | `preCompact` hook |
| v1.0.7 | `subagentStart` hook, Session SDK APIs |
| v1.0.11 | Organization MCP policy enforcement, `~/.agents/skills/` |
| v1.0.12 | `.mcp.json` at git root, plugin env vars, template variables |
| v1.0.13 | MCP sampling |

---

Next: [Chapter 10: Plugins & Skills](./10-plugins-and-skills.md)
