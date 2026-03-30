# Level 9: Extend — Build Your Own Copilot Experience

> ⚠️ **Risk Level: 🔴 High** — This level involves creating extensions, configuring hooks, and working with the full extensibility ecosystem. You'll be writing code that integrates directly with Copilot CLI.

## Learning Objectives

After completing this level, you will be able to:

1. Browse, enable, and disable CLI extensions
2. Create a custom tool extension using the Copilot SDK
3. Conduct deep research investigations with `/research`
4. Execute complete PR workflows with `/pr`
5. Configure lifecycle hooks (preCompact, subagentStart)
6. Create and manage personal skills
7. Control reasoning effort for different task types
8. Customize your terminal theme and appearance
9. Set up cross-tool instruction files (CLAUDE.md, GEMINI.md)
10. Configure advanced MCP with sampling support
11. Chain research → plan → implement → PR workflows
12. Orchestrate the full extensibility ecosystem

---

## Prerequisites

- [ ] Completed **Levels 1–8** (all skills are assumed)
- [ ] Copilot CLI **v1.0.13+** installed
- [ ] Familiarity with **JavaScript/ES modules** (for extension exercises)
- [ ] Understanding of **custom instructions** (from Level 7)
- [ ] Understanding of **permissions and sessions** (from Level 8)
- [ ] A GitHub repository where you can push branches and create pull requests (Exercises 4, 11, 12 use `/pr`)
  - Option A: Fork this workshop repository to your own account
  - Option B: Create a new personal repository and copy the sample app into it

---

## About the Sample App

Level 9 uses a **Project Scaffolder** — a Python CLI that creates project templates. It also includes a custom Copilot extension, cross-tool instruction files, and MCP configuration for hands-on practice.

> Unlike previous levels that focused on using Copilot, this level focuses on **extending** Copilot — building tools, hooks, skills, and instruction systems that shape how Copilot works for you and your team.

```
sample-app/
├── scaffolder/
│   ├── __init__.py          — Package init
│   ├── cli.py               — CLI entry point (argparse)
│   ├── templates.py         — Template definitions and rendering
│   ├── config.py            — Configuration constants
│   └── hooks.py             — Hook demonstration utilities
├── extensions/
│   └── scaffolder-ext/
│       ├── extension.mjs    — Custom Copilot CLI extension
│       └── package.json     — Extension manifest
├── hooks/
│   ├── preCompact.mjs       — Context summary before compaction
│   └── subagentStart.mjs    — Inject project context into subagents
├── tests/
│   └── test_scaffolder.py   — Unit tests
├── skills/
│   └── scaffold-helper/
│       └── SKILL.md         — Example skill definition
├── .mcp.json                — MCP configuration (project root)
├── CLAUDE.md                — Cross-tool instructions (Claude)
├── GEMINI.md                — Cross-tool instructions (Gemini)
├── Makefile                 — Common commands
└── requirements.txt         — No external dependencies
```

Navigate to the sample app:

```bash
cd workshop/level-9/sample-app
```

---

## Workshop Structure

This level contains **12 exercises**. Estimated time: **150–180 minutes**.

| Exercise | Topic | Time |
|----------|-------|------|
| 1 | The Extensions System | 8 min |
| 2 | Building Your First Extension | 20 min |
| 3 | Deep Research with /research | 10 min |
| 4 | The /pr Workflow Deep Dive | 25 min |
| 5 | The Hooks System | 15 min |
| 6 | Personal Skills Directory | 7 min |
| 7 | Reasoning Effort Control | 7 min |
| 8 | Adaptive Themes & Personalization | 5 min |
| 9 | Cross-Tool Instructions | 8 min |
| 10 | MCP Sampling & Advanced MCP | 8 min |
| 11 | Advanced PR Workflows | 30 min |
| 12 | Mastery Capstone | 45 min |

---

## Exercise 1: The Extensions System

### Goal
Browse, enable, and disable CLI extensions to understand how Copilot's capabilities are extended.

### Steps

**1.0** Set up the extension for loading:

```bash
mkdir -p .github/extensions
cp -r extensions/scaffolder-ext .github/extensions/scaffolder-ext
```

> This copies the sample extension to the location where Copilot CLI discovers project extensions.

> 💡 **Extension discovery:** Copilot CLI loads extensions from `.github/extensions/` (project-level) and `~/.copilot/extensions/` (user-level). The sample app's `extensions/scaffolder-ext/` directory is a reference implementation. To actually load it, copy it: `cp -r extensions/scaffolder-ext .github/extensions/scaffolder-ext`

**1.1** Start Copilot and list installed extensions:

```bash
copilot
```

```
/extensions
```

> Expected: A list of extensions — built-in and any project-local or user-global extensions. Each entry shows the extension name, status (enabled/disabled), and source location.

**1.2** Explore what extensions can provide:

```
What can Copilot CLI extensions do?
List the different capabilities an extension can register:
- Custom tools
- Lifecycle hooks
- Slash commands
What's the difference between an extension and an MCP server?
```

> Expected: Copilot explains that extensions use the `@github/copilot-sdk` and run in-process, while MCP servers are external processes communicating via JSON-RPC. Extensions can hook into the agent lifecycle; MCP servers provide tools only.

**1.3** Check if the sample app's extension is detected:

```
Is there an extension in the extensions/ directory of this project?
What does it provide?
```

> Expected: Copilot identifies `extensions/scaffolder-ext/extension.mjs` and describes its registered tools and hooks.

**1.4** Disable and re-enable an extension:

```
/extensions
```

> Select the scaffolder extension and toggle its status. Use the interactive menu or follow the prompts.

**1.5** Verify the effect of disabling:

```
Try to use the scaffolder tool that the extension provides.
What happens when the extension is disabled?
```

> Expected: The tool is unavailable when the extension is disabled. Re-enable it and confirm the tool works again.

### Key Concept: Extensions Architecture

Extensions are **ES modules** (`.mjs` files) that live in `.github/extensions/` (project-level) or `~/.copilot/extensions/` (user-level). They communicate with the CLI via the `@github/copilot-sdk/extension` API, registering tools, hooks, and slash commands at session startup. Unlike MCP servers, extensions run in-process and have access to the full agent lifecycle — they can intercept events like context compaction and subagent creation.

### ✅ Checkpoint
You can list, enable, disable, and understand the role of CLI extensions.

---

## Exercise 2: Building Your First Extension

### Goal
Create a custom tool extension that adds a new capability to Copilot CLI.

### Steps

**2.1** Read the existing extension:

```
@ extensions/scaffolder-ext/extension.mjs

Explain this extension line by line:
- What does joinSession() do?
- What tools does it register?
- How does the tool handler work?
```

> Expected: Copilot walks through the `joinSession()` call, the tool definition (name, description, parameters schema), and the handler function.

**2.2** Understand the extension manifest:

```
@ extensions/scaffolder-ext/package.json

What fields are required in an extension's package.json?
How does Copilot discover this extension?
```

> Expected: Copilot explains the `main` field pointing to the `.mjs` entry, the `copilot-extension` metadata, and the discovery mechanism.

**2.3** Add a new tool to the extension:

```
Add a new tool called "list-templates" to the scaffolder extension.
It should:
- Read the TEMPLATE_REGISTRY from scaffolder/templates.py
- Return a formatted list of available templates with descriptions
- Accept an optional "category" parameter to filter templates
```

> Expected: Copilot modifies `extension.mjs` to add a second tool registration within the `joinSession()` call.

> ⚠️ Review the change carefully before approving — verify the tool name, parameter schema, and handler logic.

> 💡 **Bridging JavaScript and Python:** Your extension runs in Node.js but the template registry is in Python. The simplest approach is to call the Python CLI from your tool using `child_process`:
> ```javascript
> import { execSync } from "node:child_process";
> // In your tool's execute function:
> const output = execSync("python3 -m scaffolder.cli list", { encoding: "utf-8" });
> ```
> Alternatively, you can hardcode the template data directly in JavaScript (as the `list_templates` tool already does).

**2.4** Reload the extension:

```
/extensions
```

> Select "reload" for the scaffolder extension, or restart the session.

**2.5** Test your new tool:

```
List all available project templates.
```

> Expected: Copilot uses the `list-templates` tool you just created to read the registry and display the results.

**2.6** Verify the tool works with parameters:

```
List only the Python project templates.
```

> Expected: The `category` parameter filters the output correctly.

### Key Concept: Extension SDK

The `joinSession()` function from `@github/copilot-sdk/extension` is the entry point for every extension. It receives a session object and registers tools (with JSON Schema parameters), lifecycle hooks, and slash commands. Extensions must be **ES modules** (`.mjs` only — CommonJS is not supported). Each tool handler receives the parsed parameters and returns a result string or object that Copilot incorporates into its response.

### ✅ Checkpoint
You can build a custom extension that registers tools and integrates with Copilot CLI.

---

## Exercise 3: Deep Research with /research

### Goal
Conduct a deep research investigation using `/research` and understand how it differs from regular questions.

### Steps

**3.1** Ask a regular question first (baseline):

```
How should I structure a project scaffolder that supports multiple 
languages and template registries?
```

> Expected: Copilot answers using its training data and conversation context — no external sources.

**3.2** Now run the same question through `/research`:

```
/research How should I structure a project scaffolder that supports multiple languages and template registries? Include current best practices from popular tools like cookiecutter, yeoman, and create-*-app.
```

> Expected: Copilot launches a research investigation — searching GitHub repositories, reading documentation, and synthesizing findings into a structured report with citations. This takes longer but produces more comprehensive, source-backed results.

**3.3** Compare the outputs:

```
Compare the answer you gave me before /research with the research 
report. What new information did the research uncover that you 
didn't know from your training data alone?
```

> Expected: Copilot highlights specific differences — newer patterns, real-world examples from repositories, recent community consensus that wasn't in its training data.

**3.4** Research the scaffolder's architecture:

```
/research Analyze the architecture of this project's scaffolder/cli.py 
and compare it to best practices from popular template generators. 
What improvements would bring it in line with modern standards?
```

> Expected: A detailed report covering the scaffolder's current design, comparisons with established tools, and specific actionable recommendations.

**3.5** Export the research report:

```
Save that research report to docs/scaffolder-architecture-review.md
```

> Expected: A structured markdown file with sections, citations, and recommendations — ready for team review.

> 💡 **Research reports** are designed to be shared. They include source citations, making them useful as team reference documents, not just ephemeral chat output.

### Key Concept: Research vs Questions

`/research` uses GitHub search, web sources, and deep analysis to produce exportable reports with citations. Regular questions use only the model's training data and conversation context. Use `/research` when you need current information, authoritative sources, or a comprehensive analysis you'll share with others. Use regular questions for quick answers where speed matters more than depth.

### ✅ Checkpoint
You can conduct research investigations and understand when to use `/research` vs regular questions.

---

## Exercise 4: The /pr Workflow Deep Dive

### Goal
Execute a complete PR workflow entirely from the terminal using `/pr`.

### Steps

> ⚠️ **Setup required:** Exercises 4, 11, and 12 use `/pr` to create pull requests. Make sure you have push access to a GitHub repository. If you haven't set this up, fork this workshop repo or create a personal repo now.

**4.1** Create a feature branch:

```bash
git checkout -b feat/template-validation
```

**4.2** Make a change to the scaffolder:

```
Add input validation to scaffolder/cli.py:
- Validate that the template name exists in TEMPLATE_REGISTRY (in scaffolder/templates.py) before scaffolding
- Return a helpful error message listing available templates if invalid
- Add a --dry-run flag that shows what would be created without writing files
```

> Expected: Copilot modifies `scaffolder/cli.py` with the validation logic. Review and approve the changes.

**4.3** Commit and use `/pr` to create a PR:

```bash
git add -A && git commit -m "feat: add template validation and dry-run support"
```

```
/pr
```

> Expected: Copilot creates a pull request on GitHub with a title, description, and summary of changes — all generated from the diff and commit messages.

**4.4** Check PR status:

```
/pr
```

> Expected: With an open PR on the current branch, `/pr` shows status: CI checks, review status, merge readiness.

**4.5** Demonstrate CI failure handling:

```
If CI fails on my PR, how would I use /pr to diagnose and fix it?
Walk me through the workflow.
```

> Expected: Copilot explains the `/pr` workflow for CI failures — it reads the failure logs, suggests fixes, and can push corrective commits directly.

**4.6** Demonstrate conflict resolution:

```
If my PR has merge conflicts, how does /pr help resolve them?
Compare this to resolving conflicts manually with git.
```

> Expected: Copilot explains how `/pr` can detect merge conflicts, show the conflicting files, and help resolve them interactively.

> 💡 **`/pr` is bidirectional** — it creates PRs from your work AND manages existing PRs. Think of it as `gh pr` on steroids, with AI understanding the code changes.

### Key Concept: Terminal-Native PR Workflow

`/pr` brings the entire GitHub pull request lifecycle into the terminal — creating PRs, viewing status, fixing CI failures, addressing review comments, and resolving merge conflicts. Combined with the programmatic mode from Level 8, you can build fully automated PR pipelines. The key advantage is that Copilot understands the code context, so it can write meaningful PR descriptions, diagnose test failures from logs, and suggest conflict resolutions that make semantic sense.

### ✅ Checkpoint
You can create, manage, and troubleshoot PRs entirely from the terminal with `/pr`.

---

## Exercise 5: The Hooks System

### Goal
Configure lifecycle hooks that customize Copilot's behavior at key events.

### Steps

**5.1** Understand the available hook types:

```
What lifecycle hooks does Copilot CLI support?
For each hook, explain:
- When does it fire?
- What data does it receive?
- What can it return to affect behavior?
```

> Expected: Copilot lists hooks including `preCompact`, `subagentStart`, `agentStop`, and others — with their trigger conditions and capabilities.

**5.2** Read the existing preCompact hook:

```
@ extensions/scaffolder-ext/extension.mjs

Explain the preCompact hook registered in this extension:
- When does preCompact fire?
- What context does it receive?
- How does it influence what gets preserved during compaction?
```

> Expected: Copilot explains that `preCompact` fires before the context window is compressed, receives the current conversation summary, and can inject critical information to preserve across compaction.

> 💡 **Where hooks live:** Copilot CLI loads hooks through extensions — they're registered in the `hooks` property of `joinSession()` in `extension.mjs`. The standalone files in `hooks/` are reference implementations. When modifying hooks, edit `extensions/scaffolder-ext/extension.mjs` (or `.github/extensions/scaffolder-ext/extension.mjs` if you copied it in Exercise 1).

**5.3** Read the subagentStart hook:

```
@ extensions/scaffolder-ext/extension.mjs

Explain the subagentStart hook registered in this extension:
- When does subagentStart fire?
- How does it inject context into subagents?
- Why is this important for project-specific knowledge?
```

> Expected: Copilot explains that `subagentStart` fires when a new subagent (explore, task, etc.) is spawned, and it can inject project conventions, architectural decisions, or other context the subagent needs.

**5.4** Modify the preCompact hook:

```
Update the preCompact hook in extensions/scaffolder-ext/extension.mjs to:
- Summarize all file paths that have been edited in this session
- Include the current git branch and last commit message
- Format this as a "Session Context" block that survives compaction
```

> Expected: Copilot modifies the preCompact hook in `extension.mjs` with the enhanced logic.

**5.5** Modify the subagentStart hook:

```
Update the subagentStart hook in the extension to inject:
- The project's template naming conventions
- The directory structure for new templates
- A reminder to check TEMPLATE_REGISTRY in scaffolder/templates.py when adding templates
```

> Expected: Copilot modifies the subagentStart hook in `extension.mjs` to inject scaffolder-specific context.

**5.6** Test the hooks by triggering compaction:

```
Let's have a long conversation to fill the context window. 
Then we'll verify that the preCompact hook preserved our session context.

Start by explaining the entire architecture of this sample app in detail.
```

> After enough conversation, compaction will trigger. Verify the preserved context matches what the hook should produce.

> 💡 **Hooks run automatically** — you don't invoke them. They fire at specific lifecycle events. This makes them powerful for enforcing team conventions without requiring developer action.

### Key Concept: Hooks

Hooks are event-driven customization points in the agent lifecycle, defined as ES modules. `preCompact` runs before context compression — use it to preserve critical information across long sessions. `subagentStart` fires when subagents are spawned — use it to inject project-specific context that subagents wouldn't otherwise have. Hooks are registered via extensions or placed in well-known directories, making them composable with other extensibility features.

### ✅ Checkpoint
You can configure lifecycle hooks that customize Copilot's behavior at key agent events.

---

## Exercise 6: Personal Skills Directory

### Goal
Create a personal skill that is available across all your projects.

### Steps

**6.1** Examine the project-level skill:

```
@ skills/scaffold-helper/SKILL.md

Explain this skill:
- What does the SKILL.md define?
- How does Copilot discover it?
- When would Copilot invoke this skill?
```

> Expected: Copilot explains the SKILL.md format — name, description, trigger patterns, and the instructions it provides when invoked.

**6.2** Create a personal skill directory:

```bash
mkdir -p ~/.agents/skills/my-code-reviewer
```

**6.3** Create the skill definition:

```
Create a SKILL.md file at ~/.agents/skills/my-code-reviewer/SKILL.md 
that defines a personal code review skill.

It should:
- Trigger when asked to review code
- Enforce my personal standards: meaningful variable names, 
  no magic numbers, tests for public functions
- Include a checklist format for the review output
```

> Expected: Copilot creates a SKILL.md with appropriate frontmatter (name, description, triggers) and detailed instructions.

**6.4** Verify auto-discovery:

```
What skills are available in this session?
Is my personal code reviewer skill detected?
```

> Expected: Copilot lists both the project-level `scaffold-helper` skill and your personal `my-code-reviewer` skill.

**6.5** Invoke the personal skill:

```
Review the scaffolder/cli.py file using my code review standards.
```

> Expected: Copilot uses the personal skill's checklist format and your defined standards to produce a structured review.

**6.6** Compare project vs personal skills:

```
What's the difference between a project skill (in ./skills/) and 
a personal skill (in ~/.agents/skills/)?

When should I use each type?
```

> Expected: Copilot explains that project skills are shared with the team via version control, while personal skills reflect individual preferences and are available across all projects.

> 💡 **Skills in `~/.agents/skills/` work in both Copilot CLI and VS Code** — one definition, two tools. This is the most efficient way to encode your personal conventions.

### Key Concept: Skill Discovery

Skills placed in `~/.agents/skills/` are automatically discovered and available across ALL projects in both Copilot CLI and VS Code's Copilot extension. Project-level skills (in the repository) are shared with the team and version-controlled. Personal skills encode your individual preferences and follow you everywhere. The SKILL.md format defines the skill's name, description, trigger conditions, and the instructions Copilot follows when the skill is invoked.

### ✅ Checkpoint
You can create personal skills that are available across all your projects and tools.

---

## Exercise 7: Reasoning Effort Control

### Goal
Control AI reasoning depth for different task types and understand the quality/speed tradeoff.

### Steps

**7.1** Start with low reasoning effort:

```bash
copilot --reasoning-effort low
```

```
What files are in the templates/ directory?
```

> Expected: A fast, concise answer — directory listing with minimal explanation. Low effort is ideal for simple factual lookups.

**7.2** Try the same question with high effort:

```bash
copilot --reasoning-effort xhigh
```

```
What files are in the templates/ directory?
```

> Expected: A more thorough answer — possibly including file sizes, purposes, relationships between templates, and suggestions. Notice it takes longer but provides more context.

**7.3** Use high reasoning for complex analysis:

```bash
copilot --reasoning-effort xhigh
```

```
Analyze the scaffolder's template registry system. Consider:
- Scalability: what happens with 100+ templates?
- Extensibility: how hard is it to add a new template type?
- Security: can a malicious template compromise the system?
- Performance: are there any bottlenecks?
Provide a detailed architectural review.
```

> Expected: Deep, multi-faceted analysis with specific code references, potential attack vectors, and performance projections. This is where `xhigh` shines — complex analysis that benefits from extended thinking.

**7.4** Toggle reasoning display with Ctrl+T:

While Copilot is thinking on an `xhigh` query, press `Ctrl+T` to toggle the reasoning trace display:

> Expected: You see (or hide) the model's internal reasoning process — the "thinking" that happens before the response. This is useful for understanding how the model approaches complex problems.

**7.5** Compare timing:

```
Time yourself on these two tasks:
1. With --reasoning-effort low: "List all Python files in this project"
2. With --reasoning-effort xhigh: "List all Python files in this project"

Notice the speed difference. The low-effort response should be 
noticeably faster for this simple task.
```

**7.6** Choose effort levels for common tasks:

| Task Type | Recommended Effort | Why |
|-----------|-------------------|-----|
| File lookups, simple questions | `low` | Speed matters, depth doesn't |
| Code explanations, summaries | `medium` (default) | Balanced quality and speed |
| Architecture reviews, security audits | `high` | Depth matters more than speed |
| Complex multi-step analysis | `xhigh` | Extended thinking for hard problems |

> ⚠️ **`xhigh` consumes premium requests** — use it deliberately for tasks that genuinely need deep reasoning, not for every query.

### Key Concept: Reasoning Effort

`--reasoning-effort` controls how deeply the model reasons before responding: `low` is fast and cheap for simple tasks, `medium` (default) balances quality and speed, `high` enables deeper analysis, and `xhigh` activates extended thinking for complex problems. Higher effort produces better results on hard tasks but costs more (premium request consumption) and takes longer. The key skill is matching effort to task complexity — most daily work is fine at `medium`, reserving `high`/`xhigh` for architecture decisions, security reviews, and complex debugging.

### ✅ Checkpoint
You can control reasoning effort and match it to task complexity for optimal results.

---

## Exercise 8: Adaptive Themes & Personalization

### Goal
Customize Copilot CLI's appearance to match your terminal environment.

### Steps

**8.1** Open the theme picker:

```
/theme
```

> Expected: An interactive theme picker showing available themes — GitHub Dark, GitHub Light, GitHub Auto, and others. Each preview shows how text, code blocks, and status indicators will appear.

**8.2** Try different themes:

> Select a few themes and observe how they change:
> - Prompt colors and styling
> - Code block backgrounds
> - Status indicators (success, error, warning)
> - Heading and emphasis formatting

**8.3** Set the auto theme:

```
/theme
```

> Choose "GitHub Auto" — this adapts to your terminal's light/dark setting automatically.

**8.4** Check contrast improvements:

```
Show me a code block with syntax highlighting, a warning message, 
and an error message so I can verify contrast is readable in my 
terminal.
```

> Expected: Output that is clearly readable in your terminal. The enhanced contrast improvements (v1.0.7) ensure that all text meets accessibility standards regardless of your terminal's background color.

**8.5** Verify hyperlink support:

> 💡 If you're in a terminal that supports OSC 8 hyperlinks (VS Code terminal, iTerm2, Windows Terminal), file paths and URLs in Copilot's output should be clickable. Try clicking a file path in the output.

```
Show me the path to scaffolder/cli.py and a link to the GitHub docs 
for Copilot CLI.
```

> Expected: In supported terminals, file paths and URLs are rendered as clickable hyperlinks.

### Key Concept: Adaptive Themes

Copilot CLI themes adapt to your terminal's color scheme automatically when set to "Auto". Enhanced contrast (v1.0.7) improves readability across diverse terminal configurations — from high-contrast accessibility themes to transparent backgrounds. OSC 8 hyperlink support makes file paths and URLs clickable in supported terminals (VS Code, iTerm2, Windows Terminal). These personalization features may seem minor, but they significantly reduce visual friction during long coding sessions.

### ✅ Checkpoint
You can customize Copilot CLI's theme and understand the adaptive display features.

---

## Exercise 9: Cross-Tool Instructions

### Goal
Set up instruction files that work across multiple AI coding tools.

### Steps

**9.1** Read the CLAUDE.md file:

```
@ CLAUDE.md

Explain what this file does:
- What tool originally uses CLAUDE.md?
- How does Copilot CLI interpret it?
- What instructions does it contain?
```

> Expected: Copilot explains that `CLAUDE.md` is the instruction file for Claude Code (Anthropic's CLI tool), and Copilot CLI also reads it as a context source. The instructions inside apply to both tools.

**9.2** Read the GEMINI.md file:

```
@ GEMINI.md

How does this compare to CLAUDE.md?
Does Copilot CLI read GEMINI.md as well?
```

> Expected: Copilot explains that `GEMINI.md` is for Google's Gemini CLI, and Copilot CLI reads it too. This enables "write once, use everywhere" instruction files.

**9.3** Verify all instruction sources:

```
/instructions
```

> Expected: A list of all instruction sources Copilot is currently loading — including `copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and any others.

**9.4** Expand the existing CLAUDE.md with detailed conventions:

> 💡 The sample app already includes a minimal CLAUDE.md — your task is to enhance it with detailed conventions.

```
Expand the existing CLAUDE.md with additional instructions 
useful for ANY AI coding tool working on this project:
- Template naming conventions
- Test requirements for new templates
- Directory structure rules
- Code style preferences

Make sure the instructions are tool-agnostic — they should work 
equally well in Copilot CLI, Claude Code, and Gemini CLI.
```

> Expected: Copilot expands the existing `CLAUDE.md` with project-specific instructions written in a tool-neutral way.

**9.5** Use the `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` environment variable:

```bash
export COPILOT_CUSTOM_INSTRUCTIONS_DIRS="$HOME/.copilot/instructions"
mkdir -p "$HOME/.copilot/instructions"
```

```
Create a file at ~/.copilot/instructions/copilot-instructions.md 
that contains my personal coding preferences:
- Always use descriptive variable names
- Prefer early returns over nested if-else
- Include error handling for all external calls
```

> Expected: Copilot creates the personal instruction file. These instructions apply globally to all projects.

**9.6** Verify instructions affect output:

```
Write a function to read a template from the registry.
```

> Expected: The output should reflect your personal instructions (descriptive names, early returns, error handling) AND the project instructions (template conventions, directory structure). Both instruction layers should be active.

> 📋 **Instruction precedence:** Project-level instructions override personal ones. See **Level 7** for the full instruction layering model.

### Key Concept: Cross-Tool Compatibility

`CLAUDE.md` works with both Claude Code and Copilot CLI. `GEMINI.md` works with both Gemini CLI and Copilot CLI. `copilot-instructions.md` and `AGENTS.md` are Copilot-native. By placing shared project conventions in `CLAUDE.md` (or any cross-tool file), you ensure consistent AI behavior regardless of which tool your team members use. The `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` environment variable lets you add personal instruction directories that apply across all projects.

### ✅ Checkpoint
You can set up instruction files that work across Copilot CLI, Claude Code, and Gemini CLI.

---

## Exercise 10: MCP Sampling & Advanced MCP

### Goal
Understand advanced MCP features including sampling, where MCP servers can request LLM inference.

### Steps

**10.1** Read the MCP configuration:

```
@ .mcp.json

Explain this MCP configuration:
- What servers are configured?
- What transport does each use?
- Are there any sampling-enabled servers?
```

> Expected: Copilot explains the JSON structure — server names, command/args for stdio transport or URL for HTTP transport, and any `sampling` configuration.

**10.2** Understand MCP sampling:

```
Explain MCP sampling:
- What is it?
- Why would an MCP server need to call the LLM?
- What does the approval flow look like?
- What are the security implications?
```

> Expected: Copilot explains that sampling allows MCP servers to delegate reasoning tasks back to the user's LLM. Each sampling request requires user approval, preventing runaway inference. This enables sophisticated multi-step tool workflows where the tool itself needs to "think."

**10.3** Understand org policy enforcement:

```
How do organization policies affect MCP configuration?
- Can an org restrict which MCP servers are allowed?
- How does this interact with personal MCP configs?
- What happens if an org policy blocks a server?
```

> Expected: Copilot explains the policy enforcement hierarchy — organization policies can restrict MCP servers, override personal configurations, and enforce security boundaries.

**10.4** Configure an MCP server:

```
Help me add a new MCP server to .mcp.json:
- Name: "template-validator"
- Command: "node"
- Args: ["./mcp-servers/validator.js"]
- Enable sampling so it can ask the LLM to analyze template quality
```

> Expected: Copilot modifies `.mcp.json` to add the new server configuration with sampling enabled.

> ⚠️ **Sampling requests cost tokens** — each sampling request from an MCP server triggers an LLM inference call. Monitor usage when enabling sampling for production MCP servers.

> 💡 **Workshop note:** The `.mcp.json` contains a disabled placeholder server for demonstration purposes. In this exercise, focus on **understanding the configuration format and MCP sampling concepts** rather than running a live server. To see MCP in action with a real server, try: `/mcp add` and follow the prompts to configure the built-in GitHub MCP server or another available server.

**10.5** Verify MCP configuration:

```
List all MCP servers currently configured and their status.
Which ones have sampling enabled?
```

> Expected: A summary of configured MCP servers showing connection status and sampling capability.

### Key Concept: MCP Sampling

MCP sampling is a protocol extension that allows MCP servers to request LLM inference from the user's model. This enables sophisticated tool workflows — for example, a code analysis server that uses the LLM to interpret its findings, or a documentation server that generates summaries. Each sampling request requires explicit user approval, providing a security boundary. Combined with organization policy enforcement, teams can control which servers have sampling access and which models they can use.

### ✅ Checkpoint
You understand MCP sampling, security implications, and advanced MCP configuration.

---

## Exercise 11: Advanced PR Workflows

### Goal
Chain multiple Copilot features into a realistic end-to-end development workflow.

### Steps

**11.1** Start with research — investigate an improvement:

```
/research What are the best practices for template validation in 
project scaffolding tools? Look at how cookiecutter, yeoman, and 
degit handle template integrity checks and user input validation.
```

> Expected: A research report with findings from real repositories and documentation.

**11.2** Use the research findings to create a plan:

```
Based on that research, create a plan to add template validation 
to our scaffolder:
1. Schema validation for TEMPLATE_REGISTRY entries in scaffolder/templates.py
2. Template directory structure validation
3. Variable placeholder syntax checking
4. User input sanitization

/plan
```

> Expected: Copilot enters plan mode with a structured implementation plan informed by the research findings.

**11.3** Implement the first change:

```
Implement the schema validation for TEMPLATE_REGISTRY entries in scaffolder/templates.py.
Add a validate_registry() function to scaffolder/templates.py that checks:
- Required fields (name, description, path) exist
- Template paths actually exist on disk
- No duplicate template names
```

> Expected: Copilot implements the validation function with proper error handling.

**11.4** Run the tests:

```bash
python -m pytest tests/ -v
```

```
If any tests fail, diagnose and fix them.
Add new tests for the validate_registry() function.
```

> Expected: Tests pass, and new test cases cover the validation logic.

**11.5** Create the PR with full context:

```
/pr
```

> Expected: Copilot creates a PR with a description that references the research findings, explains the implementation approach, and lists the test coverage.

**11.6** Review the end-to-end workflow:

```
Walk me through what we just did:
1. /research — gathered best practices
2. /plan — structured the implementation
3. Implementation — wrote the code
4. Tests — verified correctness
5. /pr — delivered the change

How does each step feed into the next?
What would we do differently for a larger feature?
```

> Expected: Copilot synthesizes the workflow, explaining how research informed the plan, the plan guided implementation, tests verified the code, and `/pr` packaged everything for review.

### Key Concept: Feature Chaining

The real power of Copilot CLI comes from combining `/research` → `/plan` → implementation → `/pr` into seamless workflows. Research provides evidence-based design decisions. Planning structures the implementation. Code and tests validate the approach. And `/pr` delivers it with full context. Each step feeds artifacts and context to the next, creating a development workflow where every decision is traceable back to its rationale.

### ✅ Checkpoint
You can chain research, planning, implementation, and PR creation into a complete workflow.

---

## Exercise 12: Mastery Capstone

### Goal
Orchestrate the full v1.0.13 extensibility ecosystem in a single realistic scenario.

### Steps

> 💡 **Capstone flexibility:** This exercise combines skills from the entire level. If you skipped or couldn't complete a previous exercise, that's OK — each step below includes a fallback approach so you can still demonstrate mastery of the overall ecosystem.

**12.1** Set the scene — you're adding a new template type:

```
I want to add a "Rust" project template to the scaffolder.
Before I start, let me use every extensibility feature we've learned:
- Research best practices for Rust project templates
- Use my extension's list-templates tool to see what exists
- Check my personal code review skill is active
- Verify my hooks are configured
```

> Expected: Copilot runs the research, uses the custom tool, confirms skills and hooks are active.

> 💡 **Fallback:** If your extension isn't loaded, use the built-in tools to explore the `scaffolder/templates.py` file directly. If you didn't create a personal skill, reference the sample skill in `skills/scaffold-helper/`.

**12.2** Research with `/research`:

```
/research What should a minimal but production-ready Rust project 
template include? Look at cargo-generate templates and popular 
Rust project starters on GitHub.
```

> Expected: Research report with Cargo.toml structure, recommended directories, CI configuration, and community conventions.

**12.3** Plan with the research context:

```
Based on the research, plan the Rust template addition:
1. Create templates/rust/ directory with template files
2. Add the Rust entry to TEMPLATE_REGISTRY in scaffolder/templates.py
3. Test with the scaffolder
4. Verify with the extension's list-templates tool

/plan
```

> Expected: A structured plan incorporating research findings and referencing the tools available from extensions.

**12.4** Implement — create the template files:

```
Implement the plan. Create the Rust template with:
- Cargo.toml with placeholder variables
- src/main.rs with a hello world
- README.md template
- .gitignore for Rust
- GitHub Actions CI workflow
```

> Expected: Copilot creates the template files following the project's conventions (from cross-tool instructions) and the research findings.

**12.5** Verify — use the extension tool:

```
List all templates to verify the Rust template appears correctly.
Then run the scaffolder to generate a test project from the Rust template.
```

> Expected: The extension's `list-templates` tool shows the new Rust entry. The scaffolder generates the project correctly.

> 💡 **Fallback:** If your extension isn't loaded, use the built-in tools to read `scaffolder/templates.py` and verify the Rust entry was added correctly.

**12.6** Review — invoke the personal skill:

```
Review the changes I just made using my code review standards.
```

> Expected: The personal code review skill produces a structured checklist review of all changes.

> 💡 **Fallback:** If you didn't create a personal skill, reference the sample skill in `skills/scaffold-helper/` or simply ask Copilot to review the changes using its built-in analysis.

**12.7** Deliver — create the PR:

```
/pr
```

> Expected: A PR with a comprehensive description that includes the research context, implementation details, and test results.

> 💡 **Fallback:** If GitHub isn't configured, use `/diff` and `/review` instead of `/pr` to review your changes locally.

**12.8** Reflect on the ecosystem:

```
Summarize every extensibility feature we used in this exercise:
1. Extension (custom tool)
2. /research (investigation)
3. Personal skill (code review)
4. Hooks (context preservation and subagent injection)
5. Cross-tool instructions (project conventions)
6. MCP (server configuration)
7. /pr (delivery)
8. Reasoning effort (matching depth to task)

How do these features compose together?
What would you add to this ecosystem for a real team?
```

> Expected: A comprehensive synthesis showing how all extensibility features form an integrated developer platform.

### Key Concept: Ecosystem Orchestration

Extensions, MCP servers, skills, hooks, instructions, `/pr`, and `/research` are not isolated features — they form a composable ecosystem. Extensions provide custom tools, hooks inject context automatically, skills encode conventions, instructions guide behavior, `/research` gathers evidence, and `/pr` delivers results. The mastery skill is knowing when to use each feature and how they compound — a well-configured ecosystem makes every Copilot interaction more effective because context, conventions, and tooling are always present.

### ✅ Checkpoint
You can orchestrate the full Copilot CLI extensibility ecosystem for real-world development workflows.

---

## 🏆 Level 9 Self-Assessment

Rate yourself on each skill (1 = need review, 2 = mostly comfortable, 3 = confident):

| # | Skill | 1 | 2 | 3 |
|---|-------|---|---|---|
| 1 | Browse, enable, and disable CLI extensions | ☐ | ☐ | ☐ |
| 2 | Build a custom tool extension with the SDK | ☐ | ☐ | ☐ |
| 3 | Conduct deep research with `/research` | ☐ | ☐ | ☐ |
| 4 | Execute full PR workflows with `/pr` | ☐ | ☐ | ☐ |
| 5 | Configure lifecycle hooks (preCompact, subagentStart) | ☐ | ☐ | ☐ |
| 6 | Create and manage personal skills | ☐ | ☐ | ☐ |
| 7 | Control reasoning effort for different tasks | ☐ | ☐ | ☐ |
| 8 | Customize terminal themes and appearance | ☐ | ☐ | ☐ |
| 9 | Set up cross-tool instruction files | ☐ | ☐ | ☐ |
| 10 | Configure advanced MCP with sampling | ☐ | ☐ | ☐ |
| 11 | Chain research → plan → implement → PR workflows | ☐ | ☐ | ☐ |
| 12 | Orchestrate the full extensibility ecosystem | ☐ | ☐ | ☐ |

**Scoring:**
- **30–36:** 🎉 Extensibility Master — you can build and customize Copilot for any team
- **22–29:** Re-practice exercises 2 (extensions), 5 (hooks), and 10 (MCP sampling)
- **Below 22:** Revisit Levels 7–8 before attempting Level 9 again

---

## Key Takeaways

1. **Extensions are the ultimate customization** — when built-in tools aren't enough, build your own with `@github/copilot-sdk`
2. **`/research` produces shareable artifacts** — use it for evidence-based decisions, not just quick answers
3. **`/pr` owns the full lifecycle** — creation, CI diagnosis, conflict resolution, all from the terminal
4. **Hooks automate context** — `preCompact` preserves critical state, `subagentStart` injects project knowledge
5. **Skills follow you everywhere** — personal skills in `~/.agents/skills/` work across all projects and tools
6. **Reasoning effort is a resource** — match `low`/`medium`/`high`/`xhigh` to task complexity
7. **Cross-tool instructions reduce duplication** — `CLAUDE.md` and `GEMINI.md` work in Copilot CLI too
8. **MCP sampling enables sophisticated workflows** — tools that think, with user-approved boundaries
9. **Feature chaining multiplies value** — `/research` + `/plan` + implement + `/pr` > sum of parts
10. **The ecosystem is composable** — extensions + hooks + skills + instructions + MCP form an integrated platform

---

## What's Next

Congratulations! You've completed the entire Copilot CLI workshop — from your first read-only exploration in Level 1 to orchestrating the full extensibility ecosystem in Level 9.

> 📋 **Review your journey:** Look back at your self-assessments across all 9 levels. Any scores below 2? Revisit those exercises.

> 📋 **Stay current:** Use `/changelog` inside Copilot CLI to track what's new. The CLI evolves rapidly — new features appear in almost every release.

> 📋 **Build your ecosystem:** Start creating project-specific instructions, personal skills, and custom extensions for your real projects. The patterns you practiced here apply directly to production work.

---

## 🎓 The Complete Learning Path

```
Level 1: Observe     — Read code safely
Level 2: Understand  — Ask questions, get explanations
Level 3: Plan        — Think before acting
Level 4: Create      — Make changes with verification
Level 5: Execute     — Run commands and interpret results
Level 6: Workflow    — Complete development cycles
Level 7: Customize   — Configure for your project
Level 8: Advanced    — Permissions, automation, delegation
Level 9: Extend      — Build your own Copilot experience
```

You now have the skills to not just use Copilot CLI, but to **extend and customize it** — building tools, hooks, skills, and instruction systems that make Copilot work exactly the way you and your team need it to.

**Your next steps:**
- Build a custom extension for your team's most repetitive workflow
- Create a `CLAUDE.md` or `AGENTS.md` for your main project
- Set up personal skills for your coding conventions
- Share this workshop with your team — teaching deepens mastery
