# Chapter 8: Custom Agents

Custom agents let you create **specialized AI assistants** — each with its own
expertise, tool access, and behavioral instructions — that operate alongside
your main Copilot session. Think of them as hiring specialists: a security
reviewer, a documentation writer, a Kubernetes expert, each purpose-built
for a class of tasks.

> 📋 Custom agents were introduced in **v0.0.353** (October 2025) and have
> received enhancements in every subsequent release through v0.0.422.

---

## 8.1 What Are Custom Agents?

Custom agents are **markdown files with YAML frontmatter** that define a
persona, tool permissions, and instructions. When invoked, the agent runs in
its own context with its own system prompt.

| Scenario | Approach | Why |
|----------|----------|-----|
| One-off code question | Direct prompt | No setup overhead |
| Recurring security reviews | Custom agent | Consistent methodology, reusable |
| Team-wide coding standards | Custom agent | Shared via repo, version-controlled |
| Complex multi-step refactor | General-purpose subagent | Full tools, separate context |

> 💡 If you repeatedly write the same preamble ("You are a security expert,
> check for XSS…"), that's a strong signal to create a custom agent.

---

## 8.2 Built-In Agents

| Agent | Default Model | Tools | Best For |
|-------|---------------|-------|----------|
| **Explore** | Haiku | grep, glob, view, bash | Finding files, understanding architecture |
| **Task** | Haiku | All CLI tools | Running tests, builds, linting |
| **General-purpose** | Sonnet | All CLI tools | Complex multi-step tasks, large refactors |
| **Code-review** | Sonnet | All (read-only) | Bugs, security issues, logic errors (NOT style) |

The model **automatically delegates** to subagents when it judges delegation
more effective. Key evolution:

| Capability | Since |
|-----------|-------|
| Abort signals propagate to sub-agents | v0.0.380 |
| Subagents receive correct tools across models | v0.0.389 |
| Subagents receive environment context | v0.0.402 |
| Subagents return complete responses | v0.0.409 |

> ⚠️ The code-review agent analyzes diffs — it is not designed for full-codebase
> audits. Use a custom security agent for that.

---

## 8.3 Agent File Format

Files use `.md` or `.agent.md` extension (the latter adds VS Code compatibility).

### YAML Frontmatter Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | — | Display name in agent picker |
| `description` | string | — | Brief description of expertise |
| `tools` | list | All | Allowed tools (restricts capabilities) |
| `mcp-servers` | list | None | MCP servers available to this agent |
| `model` | string | Session default | Specific model to use (since v0.0.415) |
| `user-invocable` | boolean | `true` | Whether user can directly invoke |
| `disable-model-invocation` | boolean | `false` | Prevent auto-invocation (since v0.0.411) |

### Available Tools

| Tool | Capability | Risk |
|------|-----------|------|
| `read` | Read file contents | 🟢 None |
| `grep` | Search file contents with regex | 🟢 None |
| `glob` | Find files by name pattern | 🟢 None |
| `edit` | Modify file contents | 🟡 Medium |
| `create` | Create new files | 🟡 Medium |
| `shell` | Execute shell commands | 🔴 High |
| `web_fetch` | Fetch URLs from the internet | 🟡 Medium |

Tools can be a YAML list or comma-separated (since v0.0.403):

```yaml
# List format
tools:
  - read
  - grep
  - glob

# Comma-separated (since v0.0.403)
tools: read, grep, glob
```

### Example Agent File

```markdown
---
name: Security Reviewer
description: Expert in finding security vulnerabilities in code
tools:
  - read
  - grep
  - glob
  - shell
model: claude-opus-4.6
user-invocable: true
---

# Instructions

You are a security expert who reviews code for vulnerabilities.

## Focus Areas
- SQL injection, XSS, CSRF
- Authentication and authorization flaws
- Hardcoded secrets or credentials
- Input validation gaps

## Output Format
For each finding:
1. Severity: Critical / High / Medium / Low
2. File and line number
3. Description of the vulnerability
4. Recommended fix with code example
```

---

## 8.4 Agent Locations and Precedence

| Level | Location | Scope |
|-------|----------|-------|
| User | `~/.copilot/agents/` | All your projects |
| Repository | `.github/agents/` | Current project only |
| Organization | `.github-private/agents/` | All org repositories |
| Plugin | Bundled in plugins | Per plugin |

**Precedence:** System-level > Repository-level > Organization-level

- Agents follow symbolic links (since v0.0.384)
- Unknown fields load with warnings instead of errors (since v0.0.402)

> 💡 Symlink agents from a central location into each repo's `.github/agents/`
> to share without duplication.

### Personal Skills Directory

Since v1.0.11, the **`~/.agents/skills/`** directory serves as a personal skills
directory shared between Copilot CLI and the VS Code Copilot extension. Skills
placed here are available across all projects in both environments.

| Path | Scope | Since |
|------|-------|-------|
| `~/.agents/skills/<name>/SKILL.md` | All projects, CLI + VS Code | v1.0.11 |

---

## 8.5 Invoking Agents

### Interactive Picker

```
/agent
```

### Natural Language

```
Use the security-reviewer agent to check src/ for vulnerabilities
```

### CLI Flag (since v0.0.380)

```bash
copilot --agent=security-reviewer --prompt "Review auth module"
```

| Method | Best For | Requires Exact Name |
|--------|----------|---------------------|
| `/agent` picker | Browsing, discovery | No |
| Natural language | Conversational use | Approximate |
| `--agent` flag | Scripts, CI/CD, automation | Yes |

---

## 8.6 Agent Creation Wizard

Since v0.0.396, an interactive wizard streamlines agent creation:

```bash
copilot --create-agent
```

Since v0.0.399, the **"Copilot option"** generates name, description, and
instructions from a brief description:

```
? Describe your agent: Reviews Python code for PEP 8 compliance

✓ Generated agent: pep8-reviewer
✓ Created: .github/agents/pep8-reviewer.md
```

> 💡 Copilot-generated instructions are a starting point — always review and
> refine them.

---

## 8.7 Fleet Mode

Fleet mode enables **parallel subagent execution** for decomposable tasks
(since v0.0.411).

```
/fleet
```

| Scenario | Fleet Mode? | Reason |
|----------|-------------|--------|
| Refactor 20 files with same pattern | ✅ Yes | Highly parallelizable |
| Add tests for 8 modules | ✅ Yes | Independent tasks |
| Fix a cross-cutting bug | ❌ No | Sequential dependencies |
| Update docs across levels | ✅ Yes | Independent files |

Key behaviors:
- Orchestrator **validates** each subagent's work (since v0.0.412)
- Dispatches more subagents in parallel for speed (since v0.0.412)

> ⚠️ Fleet mode works best when tasks are truly independent. If subagent
> results depend on each other, use sequential execution.

---

## 8.8 The `/delegate` Command

Hands a task to the **Copilot coding agent** which works asynchronously —
creating a branch, making changes, and opening a pull request.

```
/delegate Add input validation to all API endpoints
```

Or use the `&` prefix shortcut (since v0.0.384):

```
& Add input validation to all API endpoints
```

| Feature | Since |
|---------|-------|
| Basic delegation | v0.0.353 |
| Works with no local changes | v0.0.354 |
| `&` prefix shortcut | v0.0.384 |
| Uses conversation context | v0.0.394 |
| GHE Cloud support | v0.0.394 |
| Multi-remote prompt | v0.0.422 |

---

## 8.9 Background Agents and `/tasks`

Background agents execute long-running tasks while you keep working
(since v0.0.404).

```
/tasks
```

```
┌──────────────────────────────────────────────┐
│  Background Tasks                            │
│                                              │
│  ● Running   Integration tests    2m 14s     │
│  ✓ Complete  Lint check           passed      │
│  ✗ Failed    Build (arm64)        see logs    │
└──────────────────────────────────────────────┘
```

| Feature | Since |
|---------|-------|
| Background agents enabled | v0.0.404 |
| `/tasks` command | v0.0.404 |
| Recent Activity display | v0.0.407 |
| Consistent icons and typography | v0.0.410 |
| Automatic completion notifications | v0.0.422 |

### Multi-Turn Background Agent Conversations

Since v1.0.5, the **`write_agent`** tool enables multi-turn conversations with
background agents. Instead of launching a new agent for each follow-up, you can
send additional messages to a running or idle background agent — the agent retains
its full conversation context across turns.

| Feature | Since |
|---------|-------|
| `write_agent` for follow-up messages | v1.0.5 |
| Background agents stay alive after responding | v1.0.5 |
| Idle agents accept `write_agent` immediately | v1.0.5 |

> 💡 Prefer `write_agent` for iterative refinement over launching new agents —
> the agent retains its full conversation context.

---

## 8.10 Agent Hooks

Hooks intercept and control agent behavior at lifecycle points.

| Hook | Trigger | Since | Use Case |
|------|---------|-------|----------|
| `preToolUse` | Before a tool executes | v0.0.396 | Deny dangerous commands, modify args |
| `subagentStart` | Subagent is about to launch | v1.0.7 | Inject context into subagent prompts |
| `agentStop` | Main agent finishes | v0.0.401 | Post-processing, cleanup |
| `subagentStop` | Subagent finishes | v0.0.401 | Validate output, aggregation |

Example `preToolUse` hook denying dangerous shell commands:

```yaml
hooks:
  preToolUse:
    shell:
      deny:
        - pattern: "rm -rf"
          message: "Recursive deletion is not allowed"
        - pattern: "DROP TABLE"
          message: "Destructive DB operations are blocked"
```

### Session SDK APIs (Experimental)

Since v1.0.7, the CLI exposes **experimental Session SDK APIs** for programmatic
management of agent capabilities — registering/unregistering skills, starting/stopping
MCP servers, and querying plugin state within a running session.

| API Area | Capability | Since |
|----------|-----------|-------|
| Skills management | Register/unregister skills programmatically | v1.0.7 |
| MCP management | Start/stop MCP servers within a session | v1.0.7 |
| Plugin management | Query and control plugin state | v1.0.7 |

> ⚠️ Session SDK APIs are **experimental** — the interface may change in future
> releases. Use them for prototyping and internal tooling, not in shared plugins
> distributed to external users.

---

## 8.11 Practical Agent Examples

### Example 1: Documentation Writer

```markdown
---
name: Documentation Writer
description: Generates and updates project documentation
tools:
  - read
  - grep
  - glob
  - edit
  - create
model: claude-sonnet-4.6
---

# Instructions

You are a technical documentation expert.

## Standards
- Active voice, present tense
- Code examples for every public API
- Tables for comparisons and structured data

## For Each Function
1. One-line summary
2. Parameters table (name, type, required, description)
3. Return value description
4. Usage example
5. Error cases
```

### Example 2: Test Generator

```markdown
---
name: Test Generator
description: Creates comprehensive test suites with edge cases
tools:
  - read
  - grep
  - glob
  - edit
  - create
  - shell
---

# Instructions

You write thorough, maintainable test suites.

## Rules
- One behavior per test
- Arrange-Act-Assert pattern
- Test names describe scenarios: `it('returns 404 when not found')`
- Always test: null inputs, boundary values, error paths

## Workflow
1. Read source to understand all code paths
2. Identify existing test gaps
3. Generate happy-path tests first
4. Add edge cases and error scenarios
5. Run suite to verify
```

### Example 3: Refactoring Specialist

```markdown
---
name: Refactoring Specialist
description: Safe, incremental code refactoring with verification
tools:
  - read
  - grep
  - glob
  - edit
  - shell
model: claude-sonnet-4.6
---

# Instructions

You improve code structure without changing behavior.

## Process
1. Read the code and all callers before changing anything
2. Run existing tests to confirm baseline
3. Make one small change at a time
4. Run tests after every modification
5. If tests break, revert and try a smaller step

## Rules
- NEVER change behavior — structure only
- NEVER refactor without passing tests first
- If no tests exist, write them BEFORE refactoring
```

### Example 4: DevOps / CI Agent

```markdown
---
name: DevOps Engineer
description: CI/CD pipelines, Docker, and deployment automation
tools:
  - read
  - grep
  - glob
  - edit
  - create
  - shell
  - web_fetch
---

# Instructions

You specialize in CI/CD, containerization, and deployment.

## GitHub Actions Standards
- Pin actions to major versions: `actions/checkout@v4`
- Explicit `permissions:` blocks (least privilege)
- Cache dependencies aggressively

## Security
- NEVER hardcode secrets or credentials
- Use environment variables or secret managers
- Scan images for vulnerabilities before deploying
```

---

## 8.12 Best Practices

### Tool Selection Templates

```
Read-only (reviewer):    tools: [read, grep, glob]
Code modification:       tools: [read, grep, glob, edit, create]
Full-capability:         tools: [read, grep, glob, edit, create, shell, web_fetch]
```

### Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Vague instructions | Inconsistent output | Add specific rules and examples |
| Too many tools | Risky actions | Restrict to minimum needed |
| No output format | Responses vary wildly | Define exact structure |
| Duplicate names | Wrong agent invoked | Use unique, descriptive names |

> ⚠️ An agent with `shell` access and vague instructions is essentially
> unrestricted AI with command-line access. Pair broad tools with tight
> behavioral constraints.

> 📋 See [Chapter 7: Customization](./07-customization.md) for instruction
> file layering and how agent instructions interact with repository-level
> Copilot instructions.

---

Next: [Chapter 9: MCP (Model Context Protocol)](./09-mcp-model-context-protocol.md)
