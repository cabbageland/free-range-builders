# Claude for Financial Services

- Repo: `anthropics/financial-services`
- URL: https://github.com/anthropics/financial-services
- Date: 2026-05-08
- Repo snapshot studied: `main@57772c3f1607229fba0270f94abf3c976bbd852f`
- Why picked today: It is one of the hottest repos on GitHub right now, clearly AI-related, and unusually worth dissecting because it is not another thin agent shell. It is a real packaging system for domain-specific agents, skills, connector bundles, and managed-agent deployment manifests.

## Executive summary
This repo is a distribution system for financial-workflow agents.

The core idea is simple and strong: define each workflow once, then ship it through two surfaces, a Claude Cowork plugin and a Claude Managed Agent template. The same agent prompt, the same bundled skills, and mostly the same capability boundaries get reused across both. That is the repo's best design decision.

Structurally, this is less an “AI app” than a prompt-and-manifest monorepo. The heavy lifting lives in markdown prompts, skill folders, connector manifests, and a few deployment and validation scripts such as [`scripts/deploy-managed-agent.sh`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/deploy-managed-agent.sh), [`scripts/check.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/check.py), [`scripts/sync-agent-skills.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/sync-agent-skills.py), and [`scripts/orchestrate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/orchestrate.py).

The smart part is not “finance agents exist”. The smart part is the repo's source-of-truth discipline: vertical plugins author shared skills once, agent plugins vendor the exact skill copies they need, managed-agent cookbooks point back to those canonical plugin assets, and lint scripts enforce reference integrity and drift detection.

## What they built
They built a reference library of finance-oriented agent products for workflows like pitch-book creation, market research, earnings review, GL reconciliation, KYC screening, and valuation review.

The main deliverables are:

- named workflow agents under [`plugins/agent-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins)
- reusable vertical/domain bundles under [`plugins/vertical-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins)
- partner-specific connector or workflow packages under [`plugins/partner-built/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/partner-built)
- managed-agent deployment templates under [`managed-agent-cookbooks/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks)
- a Microsoft 365 add-in provisioning package under [`claude-for-msft-365-install/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/claude-for-msft-365-install)
- a small validation and deployment harness under [`scripts/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/scripts)

A representative agent like [`plugins/agent-plugins/market-researcher/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/market-researcher) contains the canonical system prompt in [`agents/market-researcher.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/market-researcher/agents/market-researcher.md), a plugin manifest in [`.claude-plugin/plugin.json`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/market-researcher/.claude-plugin/plugin.json), and a vendored `skills/` bundle for the exact research methods it uses.

## Why it matters
Most agent repos are either demos or wrappers. This one is trying to solve a more enterprise-shaped problem: how do you package domain-specific agent workflows so they can run in chat, in add-ins, or as headless managed agents without rewriting the workflow definition every time?

That matters because the true scaling problem for business agents is not model access. It is packaging, boundaries, repeatability, connector definition, and deployability into real enterprise surfaces.

This repo gets that. It treats agent behavior as shippable operational content.

## Repo shape at a glance
Top-level structure:

- [`README.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/README.md) is the product map and architecture overview.
- [`plugins/agent-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins) holds self-contained named agents like pitch-agent, market-researcher, and gl-reconciler.
- [`plugins/vertical-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins) holds shared skill sources, slash commands, and connector manifests by finance vertical.
- [`plugins/partner-built/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/partner-built) holds partner-authored packages like LSEG and S&P Global.
- [`managed-agent-cookbooks/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks) wraps the agent plugins into API-deployable managed-agent manifests.
- [`claude-for-msft-365-install/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/claude-for-msft-365-install) is a separate admin plugin for provisioning the Microsoft 365 add-in into a tenant.
- [`scripts/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/scripts) is the glue that checks references, syncs vendored skill copies, deploys managed agents, and demonstrates cross-agent handoff orchestration.
- [`.github/workflows/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/.github/workflows) carries CI for keeping the packaging coherent.

This is a file-first monorepo. There is almost no classic application code. The architecture is in repo layout and manifest relationships.

## Layered architecture dissection
### High-level system shape
The repo has a clean five-layer shape:

1. product-facing agent/plugin packages
2. shared domain skill and command sources
3. connector definitions for external finance data systems
4. managed-agent wrappers for headless deployment
5. validation and orchestration scripts that keep the whole thing from drifting apart

The nice part is that these layers are explicit in the directory tree instead of being buried in docs.

### Main layers
**1. Named-agent product layer**

[`plugins/agent-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins) is the user-facing product layer. Each subdirectory is a workflow product, not just a skill.

Examples:

- [`plugins/agent-plugins/pitch-agent/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/pitch-agent)
- [`plugins/agent-plugins/market-researcher/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/market-researcher)
- [`plugins/agent-plugins/model-builder/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/model-builder)
- [`plugins/agent-plugins/gl-reconciler/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/gl-reconciler)

Each agent carries:

- a canonical system prompt under `agents/`, for example [`plugins/agent-plugins/market-researcher/agents/market-researcher.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/market-researcher/agents/market-researcher.md)
- plugin packaging metadata under [`.claude-plugin/plugin.json`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/market-researcher/.claude-plugin/plugin.json)
- a vendored copy of the exact `skills/` it depends on

That means the repo favors self-contained deployability over perfect deduplication.

**2. Vertical skill-source layer**

[`plugins/vertical-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins) is the real authoring layer for shared expertise.

Examples include:

- [`plugins/vertical-plugins/financial-analysis/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis)
- [`plugins/vertical-plugins/equity-research/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/equity-research)
- [`plugins/vertical-plugins/investment-banking/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/investment-banking)
- [`plugins/vertical-plugins/private-equity/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/private-equity)

These directories contain the source-of-truth skill folders, slash commands, and sometimes hooks. The repo's own maintenance guidance in [`CLAUDE.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/CLAUDE.md) explicitly says to edit skills here first, then propagate them into agent bundles.

This is a pragmatic architecture choice. Shared expertise lives centrally, but shipping agents still get local copies so they remain installable as standalone units.

**3. Connector and tool-binding layer**

The most concrete connector hub is [`plugins/vertical-plugins/financial-analysis/.mcp.json`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis/.mcp.json), which declares MCP endpoints for Daloopa, Morningstar, S&P Global, FactSet, Moody's, MT Newswires, Aiera, LSEG, PitchBook, Chronograph, and Egnyte.

This is important because it reveals the real philosophy of the repo: the prompts are valuable, but the product assumes enterprise data access is the thing that makes the agent useful.

**4. Managed-agent deployment layer**

[`managed-agent-cookbooks/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks) packages the same workflows for Claude Managed Agents.

A cookbook like [`managed-agent-cookbooks/market-researcher/agent.yaml`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks/market-researcher/agent.yaml) references the same system prompt file from the plugin, enables a restricted toolset, wires in MCP servers via environment variables, and declares depth-1 worker agents through [`managed-agent-cookbooks/market-researcher/subagents/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks/market-researcher/subagents).

This is one of the strongest parts of the repo. The managed-agent wrapper is visibly a wrapper, not a fork.

**5. Repo integrity and orchestration layer**

This layer is the difference between a neat content repo and an operational one.

- [`scripts/check.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/check.py) validates JSON/YAML parsing, prompt frontmatter, manifest references, marketplace sources, and skill-bundle drift.
- [`scripts/sync-agent-skills.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/sync-agent-skills.py) re-vendors shared skills into agent plugin bundles.
- [`scripts/deploy-managed-agent.sh`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/deploy-managed-agent.sh) expands manifest conveniences like `system.file`, `skills.from_plugin`, and `callable_agents.manifest` into real API payloads.
- [`scripts/validate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/validate.py) adds schema validation for structured worker outputs.
- [`scripts/orchestrate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/orchestrate.py) demonstrates how cross-agent handoffs should be constrained by allowlists and JSON schema checks.

This repo knows that once agents start delegating, repo hygiene becomes a security boundary.

### Request / data / control flow
A typical path looks like this:

1. a user installs or invokes an agent plugin, for example [`plugins/agent-plugins/market-researcher/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/market-researcher)
2. the system prompt in [`agents/market-researcher.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/market-researcher/agents/market-researcher.md) scopes the task, required artifacts, guardrails, and skills
3. the agent relies on bundled copies of skills that were sourced from a vertical plugin and propagated by [`scripts/sync-agent-skills.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/sync-agent-skills.py)
4. data access comes through MCP connector definitions like [`plugins/vertical-plugins/financial-analysis/.mcp.json`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis/.mcp.json)
5. if the same workflow is deployed headlessly, a cookbook like [`managed-agent-cookbooks/market-researcher/agent.yaml`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks/market-researcher/agent.yaml) points back to the same prompt and skill assets
6. worker outputs can be schema-checked with [`scripts/validate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/validate.py)
7. cross-agent handoffs are mediated by a separate orchestrator process like [`scripts/orchestrate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/orchestrate.py), not by letting every agent call every other agent freely

That last point is especially good. They are at least trying to keep orchestration explicit instead of magical.

## Key directories and files
- [`README.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/README.md): the clearest single map of the repo's packaging model.
- [`CLAUDE.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/CLAUDE.md): contributor guidance for how skills, manifests, and bundling are supposed to stay coherent.
- [`plugins/agent-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins): the self-contained workflow products.
- [`plugins/agent-plugins/market-researcher/agents/market-researcher.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/market-researcher/agents/market-researcher.md): representative agent prompt showing task decomposition, sourcing rules, and review stops.
- [`plugins/vertical-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins): shared skill, command, and connector authoring layer.
- [`plugins/vertical-plugins/equity-research/commands/earnings.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/equity-research/commands/earnings.md): representative slash-command workflow entry point.
- [`plugins/vertical-plugins/financial-analysis/.mcp.json`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis/.mcp.json): the connector spine.
- [`managed-agent-cookbooks/README.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks/README.md): the best explanation of how the managed-agent layer maps back to plugins.
- [`managed-agent-cookbooks/market-researcher/agent.yaml`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks/market-researcher/agent.yaml): the most concrete example of the one-source, two-surfaces idea.
- [`scripts/deploy-managed-agent.sh`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/deploy-managed-agent.sh): manifest resolution and deployment logic.
- [`scripts/check.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/check.py): repo hygiene enforcement.
- [`scripts/orchestrate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/orchestrate.py): delegation-security reference loop.
- [`claude-for-msft-365-install/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/claude-for-msft-365-install): separate but strategically important enterprise adoption layer.

## Important components
**The agent prompt directories are the canonical workflow definitions**

Files like [`plugins/agent-plugins/market-researcher/agents/market-researcher.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/market-researcher/agents/market-researcher.md) are not decoration. They are the actual workflow engine in human-readable form.

**The vertical-plugin skill trees are the true source-of-truth layer**

The repo's design assumes shared know-how should be authored once in [`plugins/vertical-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins), then copied into agents for standalone distribution. That is a very practical compromise.

**The deployment script is doing a lot of hidden architecture work**

[`scripts/deploy-managed-agent.sh`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/deploy-managed-agent.sh) effectively behaves like a tiny compiler from friendly repo manifests to concrete API payloads. It expands file references, uploads skills, resolves subagent manifests, and inlines system prompts.

**The linting script is a real quality boundary**

[`scripts/check.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/check.py) is one of the most important files in the repo because this entire architecture becomes brittle if any reference path, bundle copy, or manifest shape drifts.

**The orchestration script shows they are thinking about prompt-injection risk**

[`scripts/orchestrate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/orchestrate.py) explicitly warns that handoff requests can surface in downstream text from untrusted documents and therefore validates targets and payload schemas before steering. That is one of the most serious parts of the repo.

## Important knobs / configs / extension points
- [`plugins/vertical-plugins/financial-analysis/.mcp.json`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis/.mcp.json): central place to swap finance data providers.
- [`managed-agent-cookbooks/*/agent.yaml`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks): per-agent control surface for model choice, tool enablement, MCP bindings, and callable workers.
- [`managed-agent-cookbooks/*/subagents/*.yaml`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks): depth-1 worker definitions and output schemas.
- [`plugins/agent-plugins/*/.claude-plugin/plugin.json`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins): installable packaging surface for Cowork.
- [`plugins/vertical-plugins/*/commands/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins): explicit slash-command UX layer.
- [`claude-for-msft-365-install/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/claude-for-msft-365-install): extension point for firms that need the whole thing inside Excel, PowerPoint, Word, and Outlook.

## Practical questions and answers
**Is this an app or a content repo?**

Mostly a content-and-packaging repo. But that undersells it. The packaging discipline is the product.

**What is the best idea here?**

One source, two delivery surfaces. The same workflow definition feeds a Cowork plugin and a managed-agent deployment manifest.

**Where does the real leverage come from?**

Not from the prompts alone. From the combination of domain-specific skills plus enterprise data connectors plus packaging that makes those assets deployable.

**What would fail first in production?**

Connector reality. The repo looks elegant because it assumes access to high-quality MCP-backed finance systems. Without those subscriptions, entitlements, and stable schemas, the agents become much less compelling.

**What is the hidden operational tax?**

Skill drift. Because agents vendor shared skill copies, teams need the sync-and-lint discipline to stay religiously maintained.

**Is the multi-agent story mature?**

Not really. It is promising, and the repo is admirably careful, but the orchestration story is still scaffolded by reference scripts and preview features.

## What is smart
- Reusing the same canonical prompt and skill assets across plugin and managed-agent surfaces is genuinely good architecture.
- [`scripts/check.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/check.py) treats repo hygiene as part of system correctness, which is exactly right for manifest-heavy agent repos.
- [`scripts/orchestrate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/orchestrate.py) acknowledges prompt-injection risk in handoff flows instead of pretending delegation is safe by default.
- The central connector catalog in [`plugins/vertical-plugins/financial-analysis/.mcp.json`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis/.mcp.json) makes the repo feel like enterprise infrastructure rather than pure promptware.
- The separation between named agents, shared vertical skills, and managed-agent cookbooks keeps the system understandable.

## What is flawed or weak
- A lot of the repo's apparent power depends on expensive external data systems. That makes the public repo more aspirational than runnable for most teams.
- Vendoring skills into each agent is practical for packaging, but it creates constant drift risk and maintenance overhead.
- There is not much executable test depth here beyond validation and packaging checks. That is understandable for a prompt repo, but it still leaves behavior quality hard to verify automatically.
- The managed-agent layer still relies on preview-era assumptions and reference scripts. Good direction, not yet a fully battle-hardened orchestration platform.
- Some of the repo feels like a polished reference implementation more than a proven field manual. That is not bad, but it is worth recognizing.

## What we can learn / steal
- Treat prompts, skills, connector manifests, and deployment wrappers as one versioned product, not separate afterthoughts.
- Keep a single canonical workflow definition and project it into multiple runtime surfaces.
- If you must vendor shared content into deployable bundles, enforce sync and drift checks in code.
- Put explicit security skepticism into orchestration paths, especially when downstream text can trigger delegation behavior.
- Organize agent repos by workflow products and capability layers, not by random prompt categories.

## How we could apply it
If we were building a serious internal agent repo, I would copy these patterns first:

1. the source-of-truth split between shared expertise in [`plugins/vertical-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins) and standalone products in [`plugins/agent-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins)
2. the one-source, two-surfaces model shown by [`managed-agent-cookbooks/market-researcher/agent.yaml`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks/market-researcher/agent.yaml)
3. the drift-detection and manifest-validation discipline in [`scripts/check.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/check.py)
4. the security posture from [`scripts/orchestrate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/orchestrate.py)

What I would not copy blindly is the assumption that connector access will be easy. For many teams, the connector and entitlement layer is the real implementation project.

## Bottom line
Claude for Financial Services is interesting because it treats enterprise agent workflows as a packaging and deployment problem, not just a prompting problem.

The key insight is that the repo's real value is its source-of-truth architecture: shared vertical skills feed self-contained agent bundles, and those same bundles feed managed-agent manifests. The prompts matter, but the durable lesson is how carefully the repo turns domain expertise into shippable, multi-surface agent infrastructure.
