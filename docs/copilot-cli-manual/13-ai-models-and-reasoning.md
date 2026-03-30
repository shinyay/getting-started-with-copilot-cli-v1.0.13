# Chapter 13: AI Models & Reasoning

Copilot CLI is model-agnostic — it routes prompts through a growing roster of
LLMs from multiple providers and gives you fine-grained control over which
model runs at any moment. Choosing the right model for a task is one of the
highest-leverage skills you can develop. This chapter covers the default model,
selection methods, the full catalog, premium request accounting, and the
reasoning and streaming features that let you peek inside the model's thought
process.

> 📋 For context-window mechanics and compaction, see
> [Chapter 6: Context Management & Prompt Engineering](./06-context-management-and-prompt-engineering.md).

---

## Default Model

As of **v1.0.5 (March 2026)**, the default model is **Claude Sonnet 4.5**.

| Period | Default | Notes |
|--------|---------|-------|
| v0.0.329 (Sep 2025) | Claude Sonnet 4.5 | Briefly set, then reverted |
| v0.0.330 (Sep 2025) | Claude Sonnet 4 | 4.5 not fully rolled out |
| Late 2025 onwards | Claude Sonnet 4.5 | Re-established after rollout |
| v1.0.2 (Mar 2026) | Claude Sonnet 4.5 | Confirmed default at GA |
| v1.0.5 (Mar 2026) | Claude Sonnet 4.5 | Current stable release |

Since **v0.0.413**, the CLI auto-migrates deprecated model preferences on
startup. If your config references `gpt-5` (deprecated v0.0.412), you'll see:

```
⚠ Model "gpt-5" is deprecated. Switched to claude-sonnet-4.5.
```

> 💡 Auto-migration only fires on startup. Passing a deprecated model via
> `--model` produces a hard error instead of a silent fallback.

---

## Selecting a Model

Three methods, in precedence order (highest wins):

| Method | Scope | Precedence |
|--------|-------|------------|
| `--model` CLI flag | Single invocation | **Highest** |
| `model` in `~/.copilot/config.json` | All sessions | Medium |
| Built-in default | Fallback | Lowest |

### /model Command

**Interactive picker (since v0.0.400)** — fuzzy-searchable list of accessible models:

```
/model
```

**Direct selection (since v0.0.329):**

```
/model claude-opus-4.6
```

Key improvements over time:

| Version | Enhancement |
|---------|------------|
| v0.0.329 | `/model <name>` sets model directly |
| v0.0.331 | Shows only accessible models based on plan/region |
| v0.0.370 | Two-column layout with aligned multipliers |
| v0.0.372 | Enable disabled models directly when selecting |
| v0.0.374 | Clearer message with settings link when unavailable |
| v0.0.400 | Interactive picker with fuzzy search |
| v1.0.7 | All entitled models visible in picker for Pro and trial users |

### --model Flag

For non-interactive (prompt) mode:

```bash
copilot --model claude-opus-4.6 -p "Explain this Dockerfile"
```

Since **v0.0.421**, passing an unavailable model is a hard error:

```bash
$ copilot --model nonexistent -p "hello"
Error: Model "nonexistent" is not available. Run `copilot /model` to see options.
```

### Config File

Set a persistent default in `~/.copilot/config.json`:

```json
{
  "model": "claude-sonnet-4.6"
}
```

> 💡 Run `copilot help config` to see all configurable fields including `model`.

---

## Available Models (March 2026, v1.0.5)

### Anthropic Models

| Model | ID | Tier | Best For |
|-------|----|------|----------|
| Claude Opus 4.6 | `claude-opus-4.6` | Premium | Complex reasoning, large codebases |
| Claude Opus 4.6 (1M) | `claude-opus-4.6-1m` | Premium | Very large context tasks, monorepos |
| Claude Opus 4.6 Fast | `claude-opus-4.6-fast` | Premium | Fast premium reasoning |
| Claude Opus 4.5 | `claude-opus-4.5` | Premium | Complex tasks, deep analysis |
| Claude Sonnet 4.6 | `claude-sonnet-4.6` | Standard | Good balance of speed and quality |
| Claude Sonnet 4.5 | `claude-sonnet-4.5` | Standard | **Default** — reliable all-rounder |
| Claude Sonnet 4 | `claude-sonnet-4` | Standard | Previous generation, still capable |
| Claude Haiku 4.5 | `claude-haiku-4.5` | Fast/Cheap | Quick tasks, sub-agents, exploration |

### OpenAI Models

| Model | ID | Tier | Best For |
|-------|----|------|----------|
| GPT-5.4 | `gpt-5.4` | Standard | Latest OpenAI, general purpose |
| GPT-5.4 mini | `gpt-5.4-mini` | Fast/Cheap | Lightweight speed-focused tasks |
| GPT-5.3-Codex | `gpt-5.3-codex` | Standard | Code generation |
| GPT-5.2-Codex | `gpt-5.2-codex` | Standard | Code generation |
| GPT-5.2 | `gpt-5.2` | Standard | General-purpose reasoning |
| GPT-5.1-Codex-Max | `gpt-5.1-codex-max` | Standard | Maximum code quality |
| GPT-5.1-Codex | `gpt-5.1-codex` | Standard | Code generation |
| GPT-5.1 | `gpt-5.1` | Standard | General purpose |
| GPT-5.1-Codex-Mini | `gpt-5.1-codex-mini` | Fast/Cheap | Quick code tasks |
| GPT-5-Mini | `gpt-5-mini` | Fast/Cheap | Fast, lightweight operations |
| GPT-4.1 | `gpt-4.1` | Fast/Cheap | Budget option |

### Google Models

No Google models are currently available. Gemini 3 Pro (Preview) was removed in
v1.0.13.

### Deprecated Models

| Model | Deprecated In | Date | Replacement |
|-------|--------------|------|-------------|
| GPT-5 | v0.0.412 | Feb 2026 | GPT-5.2 or newer |
| Gemini 3 Pro (Preview) | v1.0.13 | — | — |

> ⚠️ Deprecated models are removed from the picker and cannot be selected.
> Auto-migration handles stale config references on startup.

---

## Model Availability Timeline

| Date | Version | Model | Event |
|------|---------|-------|-------|
| 2025-09-29 | 0.0.329 | Claude Sonnet 4.5 | Added |
| 2025-10-16 | 0.0.343 | Claude Haiku 4.5 | Added |
| 2025-11-13 | 0.0.356 | GPT-5.1, GPT-5.1-Codex, GPT-5.1-Codex-Mini | Added |
| 2025-11-24 | 0.0.363 | Claude Opus 4.5, GPT-4.1, GPT-5-Mini | Added |
| 2025-12-04 | 0.0.367 | GPT-5.1-Codex-Max | Added |
| 2025-12-11 | 0.0.369 | GPT-5.2 | Added |
| 2026-01-14 | 0.0.382 | GPT-5.2-Codex | Added |
| 2026-02-05 | 0.0.404 | Claude Opus 4.6 | Added |
| 2026-02-07 | 0.0.406 | Claude Opus 4.6 Fast (Preview) | Added |
| 2026-02-17 | 0.0.411 | Claude Sonnet 4.6 | Added |
| 2026-02-19 | 0.0.412 | GPT-5 | **Deprecated** |
| 2026-03-05 | 0.0.422 | GPT-5.4, GPT-5.3-Codex | Added |
| — | 1.0.7 | GPT-5.4 mini | Added |
| — | 1.0.13 | Gemini 3 Pro (Preview) | **Removed** |

---

## Premium Request Usage (PRU)

Every prompt consumes one **premium request** from your monthly Copilot quota.

**Check usage:** `/usage` (added v0.0.333) — shows consumed/remaining PRU,
session duration, and code change stats.

**Multipliers:** The `/model` picker displays a multiplier column. As of
v1.0.5 (March 2026), all models show **1×** per prompt. This may change with new tiers.

| Version | PRU Fix |
|---------|---------|
| v0.0.345 | Fixed overcounting bug |
| v0.0.346 | Model config accounted for in estimation |
| v0.0.347 | Display stats corrected |
| v0.0.368 | PRU correctly displayed for all tiers |
| v0.0.399 | Sub-agent usage included in totals |

> ⚠️ Before v0.0.399, sub-agent usage was invisible and could cause
> surprising quota depletion. Update to get accurate accounting.

---

## Extended Thinking (Anthropic)

Since **v0.0.384**, Claude models support **extended thinking** — step-by-step
internal reasoning before producing a response.

When active, a "Thinking…" shimmer appears, followed by a collapsible block:

```
▸ Thinking (12 steps, 3.2s)
  The user wants to refactor auth middleware for both JWT and API key…

Here's my recommendation for the refactored middleware:
…
```

**Ctrl+T** toggles reasoning visibility (persists across sessions).

| Version | Enhancement |
|---------|------------|
| v0.0.375 | Fixed duplicate messages from reasoning |
| v0.0.384 | Extended thinking introduced |
| v0.0.390 | Reasoning preserved after compaction |

> 💡 Extended thinking works best with Opus models on complex tasks. For
> simple questions, the overhead may slow responses without quality gains.

---

## Reasoning for GPT Models

GPT models have their own reasoning capabilities, distinct from Anthropic's
extended thinking but serving a similar purpose.

| Version | Feature |
|---------|---------|
| v0.0.384 | Configurable reasoning effort (`low`/`medium`/`high`) |
| v1.0.4 | `--reasoning-effort` CLI flag (`low`/`medium`/`high`/`xhigh`) |
| v0.0.403 | Reasoning summaries enabled by default |
| v0.0.413 | Heading content from reasoning displayed |
| v0.0.421 | ACP clients configure reasoning via session config |
| v1.0.12 | Active reasoning effort level displayed next to model name in header |

Configure in `~/.copilot/config.json`:

```json
{
  "reasoningEffort": "high"
}
```

Since **v1.0.4**, you can also set reasoning effort per-invocation via flag:

```bash
copilot -p "Analyze this complex algorithm" --reasoning-effort xhigh
```

| Value | Use Case |
|-------|----------|
| `low` | Quick tasks, simple questions |
| `medium` | Default — balanced depth and speed |
| `high` | Complex debugging, architecture decisions |
| `xhigh` | Maximum reasoning depth for the hardest problems |

---

## Streaming

Token-by-token streaming has been enabled by default since **v0.0.348**.
Disable it for scripting with `--stream off`.

| Version | Improvement |
|---------|------------|
| v0.0.348 | Streaming introduced |
| v0.0.407 | Auto-retry on server errors during streaming |
| v0.0.416 | Response size counter updates continuously |
| v0.0.421 | No more truncation in alt-screen mode |

> ⚠️ If you see truncated output in alt-screen, upgrade to **v0.0.421+**.

---

## Model Selection Strategies

### When to Use Opus (Premium)

| Task | Why Opus |
|------|----------|
| Complex architecture decisions | Deep reasoning about trade-offs |
| Security-sensitive code review | Catches subtle vulnerabilities |
| Large-scale refactoring | Consistency across many files |
| Difficult debugging | Better at holding complex state |

### When to Use Sonnet (Standard)

| Task | Why Sonnet |
|------|------------|
| Day-to-day coding | Good speed/quality balance |
| Bug fixes and features | Reliable code generation |
| Documentation | Clear, structured output |
| General questions | Fast turnaround |

### When to Use Haiku / Mini (Fast/Cheap)

| Task | Why Fast/Cheap |
|------|----------------|
| Quick questions | Sub-second responses |
| File exploration | Default for Explore agent |
| Running tests/builds | Low orchestration overhead |
| Batch operations | Maximize throughput per PRU |

### When to Use Codex Models

| Task | Why Codex |
|------|-----------|
| Heavy code generation | Trained for code completion |
| Applying patches | `apply_patch` toolchain (v0.0.366) |
| Batch transformations | Efficient at repetitive changes |
| Grep workflows | `grep` tool available (v0.0.368) |

> 💡 Codex models use **specialized truncation logic** (v0.0.370) that
> preserves code structure at logical boundaries instead of raw token count.

---

## Sub-Agent Model Selection

Built-in sub-agents each use an optimized default model:

| Agent | Default Model | Rationale |
|-------|---------------|-----------|
| Explore | Claude Haiku 4.5 | Speed — many fast queries |
| Code Review | Claude Sonnet | Quality — careful analysis |
| Task | Claude Haiku 4.5 | Speed — build/test orchestration |
| General-Purpose | Claude Sonnet | Balance — full capability |

Since **v0.0.415**, custom agents can specify a `model` field:

```yaml
---
name: security-reviewer
model: claude-opus-4.6
tools: [grep, view, bash]
---
You are a security-focused code reviewer...
```

The agent knows which model powers it when asked (since v0.0.415).

Since **v0.0.407**, if a sub-agent's default model is blocked by policy, it
falls back to the session's active model instead of failing.

> ⚠️ If your organization blocks Haiku, Explore falls back to Sonnet —
> functional but slower. Check with your admin if exploration feels sluggish.

---

## Model-Related Configuration

| Field | Location | Purpose |
|-------|----------|---------|
| `model` | `~/.copilot/config.json` | Persistent default model |
| `reasoningEffort` | `~/.copilot/config.json` | GPT reasoning depth |
| `--reasoning-effort` | CLI flag | Per-invocation reasoning depth (since v1.0.4) |
| `stream` | `~/.copilot/config.json` | Enable/disable streaming |

**Chat history on model switch:** Since v0.0.401, switching between model
families (Anthropic ↔ OpenAI) handles conversation format correctly.

**Codex-specific tools:** `apply_patch` (v0.0.366) and `grep` (v0.0.368) are
auto-available when a Codex model is active — no configuration needed.

---

## Quick Reference

```
┌─────────────────────────────────────────────────────────┐
│                 MODEL SELECTION GUIDE                    │
├──────────────┬──────────────────────────────────────────┤
│ Complex task │ → claude-opus-4.6 or claude-opus-4.6-1m  │
│ Daily coding │ → claude-sonnet-4.5 (default) or 4.6     │
│ Quick query  │ → claude-haiku-4.5 or gpt-5.4-mini          │
│ Code gen     │ → gpt-5.3-codex or gpt-5.2-codex         │
│ Budget max   │ → gpt-4.1                                │
├──────────────┴──────────────────────────────────────────┤
│ Switch: /model <id>  │  Flag: --model <id>              │
│ Check usage: /usage  │  Config: ~/.copilot/config.json  │
└─────────────────────────────────────────────────────────┘
```

> 📋 For more configuration beyond model selection, see
> [Chapter 7: Custom Instructions & Configuration](./07-custom-instructions-and-configuration.md).

---

Next: [Chapter 14: Security, Permissions & Enterprise](./14-security-permissions-and-enterprise.md)
