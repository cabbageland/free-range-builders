# Claude for Financial Services

- Repo: anthropics/financial-services
- URL: https://github.com/anthropics/financial-services
- Date: 2026-09-22
- Repo snapshot studied: main at 574ed3624aebd0418c7e96cd101262f30210ab26
- Why picked today: It was the top GitHub daily trending repo when scouted, with 36k+ stars and a fresh push on 2026-09-21. It is also a rare public example of a vertical agent pack that is mostly prompts, skills, manifests, connectors, and deployment glue instead of a demo app.

## Executive summary

[anthropics/financial-services](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26) is a reference kit for financial-services agents. The interesting part is not one clever algorithm. It is the packaging pattern: the same domain workflow is represented as a Claude plugin, a set of reusable skills, a set of slash commands, and a Managed Agents manifest.

The repo is strongest as a product architecture study. The [README.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/README.md) makes the promise explicit: install a workflow as a Cowork plugin, or deploy the same prompt and skills behind the Managed Agents API. The tree backs that up with [plugins/agent-plugins](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/agent-plugins), [plugins/vertical-plugins](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins), [managed-agent-cookbooks](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks), and [claude-for-msft-365-install](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/claude-for-msft-365-install).

The best lesson is that useful enterprise agents are mostly boundaries: who may read untrusted documents, who may call trusted data systems, who may write output, which files define the workflow, and how the same domain skill is reused without drift. The weakest part is polish. The fetched [plugins/vertical-plugins/financial-analysis/.mcp.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/.mcp.json) did not parse as JSON in my local check because the `egnyte` block and `box` block are missing a delimiter/closing shape.

## What they built

They built a financial-services agent catalog. At the top level, [README.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/README.md) lists named agents for pitch work, meeting prep, market research, earnings review, model building, GL reconciliation, month-end close, statement audit, KYC screening, and valuation review.

The repo ships those agents in two forms:

- Installable plugin entries in [.claude-plugin/marketplace.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/.claude-plugin/marketplace.json), pointing to concrete plugin directories.
- Headless deployment cookbooks in [managed-agent-cookbooks](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks), where each workflow gets an [agent.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/agent.yaml) and worker subagents.

The repo also includes a Microsoft 365 provisioning track in [claude-for-msft-365-install](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/claude-for-msft-365-install), with commands and scripts for add-in setup rather than analyst workflow logic.

## Why it matters

Most agent examples stop at one prompt plus a tool call. This repo shows the messier, more useful middle layer: a catalog of domain skills, prompt wrappers, manifests, MCP endpoints, security separations, and validation scripts. It is close to how a financial firm would actually want to evaluate an agent system, because it makes the operational shape inspectable.

The core move is file-based productization. A skill like the DCF model builder lives in [plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md), while agent bundles carry synced copies under their own plugin directories. The repo then uses [scripts/check.py](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/check.py) to detect drift between vertical skill sources and bundled agent skills.

## Repo shape at a glance

- [plugins](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/plugins) is the main product surface. It contains agent plugins, vertical plugins, and partner-built plugins.
- [plugins/agent-plugins](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/agent-plugins) packages end-to-end workflows such as `gl-reconciler`, `pitch-agent`, and `market-researcher`.
- [plugins/vertical-plugins](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins) holds reusable domain bundles such as financial analysis, investment banking, equity research, private equity, fund admin, and operations.
- [managed-agent-cookbooks](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks) mirrors many agent workflows as Managed Agents manifests with subagent definitions and steering examples.
- [claude-for-msft-365-install](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/claude-for-msft-365-install) is an admin install plugin for Microsoft 365 add-in deployment.
- [scripts](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/scripts) contains deployment, orchestration, validation, synchronization, and check tooling.
- [.github/workflows](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/.github/workflows) contains automation for plugin validation, secret scanning, and version bumping.

## Layered architecture dissection

### High-level system shape

The system has three main planes.

First, the catalog plane: [.claude-plugin/marketplace.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/.claude-plugin/marketplace.json) maps user-facing plugin names to source directories. This is what turns a filesystem tree into a marketplace.

Second, the domain plane: [plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md) and sibling skill files encode methods, constraints, and work standards. These files are not code libraries; they are operational playbooks for an agent.

Third, the runtime plane: [managed-agent-cookbooks/gl-reconciler/agent.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/agent.yaml) and its worker manifests specify models, tools, MCP servers, skills, and callable agents for headless execution.

### Main layers

The plugin layer is small and explicit. For example, [plugins/agent-plugins/gl-reconciler/.claude-plugin/plugin.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/agent-plugins/gl-reconciler/.claude-plugin/plugin.json) is just identity and description, while [plugins/agent-plugins/gl-reconciler/agents/gl-reconciler.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/agent-plugins/gl-reconciler/agents/gl-reconciler.md) contains the real workflow contract.

The skill layer is the reusable knowledge base. The DCF skill in [plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md) is unusually concrete: it calls out formulas over hardcodes, staged user verification, sensitivity table construction, cell comments, and recalculation expectations.

The connector layer sits behind [plugins/vertical-plugins/financial-analysis/.mcp.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/.mcp.json), which enumerates providers such as Daloopa, Morningstar, S&P Global, FactSet, Moodys, Aiera, LSEG, PitchBook, Chronograph, Egnyte, and Box. That file is the boundary between an analyst workflow and external financial data sources.

The managed-agent layer adds role separation. [managed-agent-cookbooks/gl-reconciler/agent.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/agent.yaml) lets the orchestrator read, grep, glob, and call read-only MCP servers. The reader worker in [managed-agent-cookbooks/gl-reconciler/subagents/reader.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/subagents/reader.yaml) can read untrusted statements but has no MCP servers and no write tool. The resolver in [managed-agent-cookbooks/gl-reconciler/subagents/resolver.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/subagents/resolver.yaml) has write tools but does not read counterparty files.

### Request / data / control flow

The GL reconciler flow is the cleanest concrete example. A user asks for a GL to subledger reconciliation. The prompt in [plugins/agent-plugins/gl-reconciler/agents/gl-reconciler.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/agent-plugins/gl-reconciler/agents/gl-reconciler.md) says the orchestrator pulls balances, dispatches readers per asset class, traces root cause, asks a critic to re-check reported breaks, and hands the verified break set to the resolver.

The headless manifestation of that flow is [managed-agent-cookbooks/gl-reconciler/agent.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/agent.yaml). It binds read-only MCP servers named `internal-gl` and `subledger`, imports skills from the plugin, and lists callable workers. The reader output is constrained by the schema embedded in [managed-agent-cookbooks/gl-reconciler/subagents/reader.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/subagents/reader.yaml), including field limits and allowed character classes for evidence references.

The deployment path is handled by [scripts/deploy-managed-agent.sh](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/deploy-managed-agent.sh). It expands manifest conveniences like `system.file`, uploads skills, creates callable subagents, and posts to `/v1/agents`. The orchestration reference in [scripts/orchestrate.py](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/orchestrate.py) watches for handoff requests, validates target agent and payload shape, then steers the destination session.

## Key directories and files

- [README.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/README.md) explains the two delivery modes and the repo taxonomy.
- [.claude-plugin/marketplace.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/.claude-plugin/marketplace.json) is the plugin catalog index.
- [plugins/agent-plugins/gl-reconciler/agents/gl-reconciler.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/agent-plugins/gl-reconciler/agents/gl-reconciler.md) shows the workflow prompt style: deliverables, workflow, guardrails, and bundled skills.
- [plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md) is the best example of a detailed, testable financial skill.
- [plugins/vertical-plugins/financial-analysis/.mcp.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/.mcp.json) is the connector map, but the snapshot I fetched appears syntactically broken.
- [managed-agent-cookbooks/gl-reconciler/agent.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/agent.yaml) is the orchestrator manifest.
- [managed-agent-cookbooks/gl-reconciler/subagents/reader.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/subagents/reader.yaml) is the untrusted-document reader boundary.
- [managed-agent-cookbooks/gl-reconciler/subagents/resolver.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/subagents/resolver.yaml) is the write-enabled report producer boundary.
- [scripts/check.py](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/check.py) is the repo's consistency gate.
- [scripts/deploy-managed-agent.sh](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/deploy-managed-agent.sh) is the Managed Agent deployment harness.
- [scripts/orchestrate.py](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/orchestrate.py) is a reference handoff event loop.

## Important components

The marketplace index in [.claude-plugin/marketplace.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/.claude-plugin/marketplace.json) is the product menu. It lists vertical plugins, agent plugins, partner plugins, and the Microsoft 365 install plugin.

The GL reconciler prompt in [plugins/agent-plugins/gl-reconciler/agents/gl-reconciler.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/agent-plugins/gl-reconciler/agents/gl-reconciler.md) is the best security story: untrusted statements are separated from trusted MCP access, and only the resolver writes the final report.

The DCF skill in [plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md) is a good example of encoding craft. It is opinionated about Office JS versus openpyxl, merged-cell pitfalls, formulas, comments, staged validation, and sensitivity table sanity checks.

The Managed Agent deployment script in [scripts/deploy-managed-agent.sh](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/deploy-managed-agent.sh) is the bridge from file templates to API objects. It resolves manifest references, uploads skills, recursively creates callable agents, and uses a cache so repeated skill uploads can be avoided.

The validation script in [scripts/check.py](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/check.py) is the repo's immune system. It parses manifests, validates JSON, checks markdown frontmatter, resolves manifest references, checks bundled skill drift, verifies marketplace sources, and enforces ASCII for PowerShell scripts without a UTF-8 BOM.

## Important knobs / configs / extension points

The obvious extension point is [.claude-plugin/marketplace.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/.claude-plugin/marketplace.json): add a plugin entry, point it at a directory, and the catalog grows.

The domain extension point is [plugins/vertical-plugins](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins). New skills should originate there before being bundled into agent plugins.

The workflow extension point is [plugins/agent-plugins](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/agent-plugins). Each agent gets a prompt, bundled skills, and a plugin manifest.

The headless runtime extension point is [managed-agent-cookbooks](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks). Each cookbook can pick tools, MCP servers, skills, and callable agents.

The data-provider extension point is [plugins/vertical-plugins/financial-analysis/.mcp.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/.mcp.json), though this snapshot needs a syntax fix before it can be trusted as a config file.

## Practical questions and answers

Q: Is this a finance app or an agent template repo?
A: It is an agent template repo. The real artifacts are prompt files, skill files, plugin manifests, Managed Agent manifests, MCP connector configs, and deployment scripts.

Q: What is the cleverest design move?
A: The same workflow has a plugin surface and a headless Managed Agent surface. [README.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/README.md) calls this out, and [managed-agent-cookbooks/gl-reconciler/agent.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/agent.yaml) demonstrates it.

Q: Where is the real finance knowledge?
A: Mostly in skill files like [plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md), not in Python code.

Q: Where would this fail first in production?
A: Connector setup and governance. The [plugins/vertical-plugins/financial-analysis/.mcp.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/.mcp.json) file enumerates the right kind of providers, but access, licensing, secrets, rate limits, and audit controls are outside the repo. The malformed JSON in the studied snapshot is also a reminder that config hygiene matters.

Q: What would I copy?
A: The untrusted-reader, trusted-data-orchestrator, write-only-resolver split from [managed-agent-cookbooks/gl-reconciler](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler).

## What is smart

The repo treats agent work as a packaging and boundary problem. That is more mature than most agent demos.

The GL reconciler isolation model is especially good. [managed-agent-cookbooks/gl-reconciler/subagents/reader.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/subagents/reader.yaml) reads untrusted statements with no MCP servers and no write tool. [managed-agent-cookbooks/gl-reconciler/subagents/resolver.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/subagents/resolver.yaml) writes only after it receives verified structured data. That is a concrete prompt-injection mitigation pattern.

The repo's drift-checking idea is also worth stealing. [scripts/check.py](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/check.py) compares bundled skills against vertical skill sources and tells contributors to run the sync script if they diverge. That is exactly the kind of boring mechanism that keeps template repos useful.

## What is flawed or weak

The studied [plugins/vertical-plugins/financial-analysis/.mcp.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/.mcp.json) appears invalid. Locally, `python3 -m json.tool` failed with `Expecting ',' delimiter: line 47 column 5`. Since the repo positions connector config as a core installation path, that is not cosmetic.

There is also a lot of preview surface. [scripts/deploy-managed-agent.sh](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/deploy-managed-agent.sh) explicitly targets beta headers and preview managed-agent APIs. Builders should read this as a reference shape, not a drop-in production system.

The repo leans hard on markdown operational discipline. That is elegant when maintained, but brittle if teams edit prompts and skills without review. [scripts/check.py](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/check.py) catches structure and drift, but it cannot prove that a financial workflow is accurate.

## What we can learn / steal

For our own agent products, copy the four-layer split: catalog, domain skills, workflow agents, and headless runtime manifests.

Copy the GL reconciler trust separation from [plugins/agent-plugins/gl-reconciler/agents/gl-reconciler.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/agent-plugins/gl-reconciler/agents/gl-reconciler.md) and [managed-agent-cookbooks/gl-reconciler](https://github.com/anthropics/financial-services/tree/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler): isolate untrusted document reading from privileged system access and final writes.

Copy the skill specificity from [plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md). The best skills are not vague instructions; they encode failure modes, step gates, file-format details, and validation rituals.

Copy the boring repo checks from [scripts/check.py](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/scripts/check.py). Agent template repos need linters as much as code repos do.

## How we could apply it

For a vertical product, start with one workflow and build it in both plugin and headless form. For example, a support-escalation agent could have a plugin prompt, reusable escalation skills, connector config for ticketing/search systems, and a headless manifest that separates customer-content readers from privileged account tools.

Use a marketplace file like [.claude-plugin/marketplace.json](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/.claude-plugin/marketplace.json) to make the product catalog explicit.

Use a manifest like [managed-agent-cookbooks/gl-reconciler/agent.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/agent.yaml) to define privileged tools and callable workers.

Use worker schemas like [managed-agent-cookbooks/gl-reconciler/subagents/reader.yaml](https://github.com/anthropics/financial-services/blob/574ed3624aebd0418c7e96cd101262f30210ab26/managed-agent-cookbooks/gl-reconciler/subagents/reader.yaml) to ensure that untrusted input is reduced to bounded structured output before it crosses a privilege boundary.

## Bottom line

This is a strong source study because it shows what enterprise agent systems actually need: not just prompts, but installable packaging, reusable skills, connector boundaries, headless manifests, role-separated workers, and validation scripts. The repo has rough edges, including a malformed connector config in the studied snapshot, but the architectural pattern is worth copying.
