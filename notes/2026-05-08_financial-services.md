# Claude for Financial Services

- Repo: `anthropics/financial-services`
- URL: https://github.com/anthropics/financial-services
- Date: 2026-05-08
- Repo snapshot studied: `main` @ `57772c3f1607229fba0270f94abf3c976bbd852f`
- Why picked today: It is extremely hot right now, AI-native, and more interesting than the usual prompt-pack trend bait because it is trying to standardize real financial-services workflows as file-based agent packages that can run in two deployment modes.

## Executive summary
This repo is a catalog of domain-specific agent packages for financial work, not a software product in the normal sense. The core idea is smart: define workflows once as prompts, skills, commands, and connectors, then ship the same workflow either as a Cowork plugin or as a Claude Managed Agent deployment. The repo is mostly markdown, JSON, YAML, and a small amount of glue code, which makes it legible and easy to fork.

The most important architectural move is the split between reusable vertical skill bundles and self-contained workflow agents that vendor the skills they need. That buys portability and easier installation, but it also creates duplication and drift risk, which the sync script explicitly manages.

## What they built
They built a reference library of AI agents for common finance workflows like pitch creation, market research, earnings review, GL reconciliation, KYC screening, and month-end close.

The implementation has four main product surfaces:

- workflow agents under [`plugins/agent-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins)
- reusable vertical bundles under [`plugins/vertical-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins)
- headless deployment templates under [`managed-agent-cookbooks/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks)
- admin tooling for Microsoft 365 rollout under [`claude-for-msft-365-install/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/claude-for-msft-365-install)

## Why it matters
Most “AI for finance” repos are wrappers, toy demos, or vaguely described agent fantasies. This one is more concrete. It encodes actual workflow boundaries, tool scopes, handoff patterns, output expectations, and connector layouts. Even if you never use finance workflows, it is a useful pattern library for packaging domain agents in a way that is inspectable and forkable.

## Repo shape at a glance
Top-level structure:

- [`README.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/README.md), the contract for the repo’s two-mode packaging model
- [`plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins), the user-facing plugin surface
  - [`plugins/agent-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins), end-to-end agents like [`pitch-agent`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/pitch-agent) and [`gl-reconciler`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/gl-reconciler)
  - [`plugins/vertical-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins), reusable domain bundles such as [`financial-analysis`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis), [`equity-research`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/equity-research), and [`private-equity`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/private-equity)
  - [`plugins/partner-built/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/partner-built), partner-specific extensions
- [`managed-agent-cookbooks/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks), one deployment cookbook per workflow
- [`scripts/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/scripts), the thin glue layer that turns static files into deployable managed agents
- [`claude-for-msft-365-install/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/claude-for-msft-365-install), a separate installer plugin for M365 tenant rollout

This is a content-first repo with light deployment machinery, not an application codebase with a runtime-heavy core.

## Layered architecture dissection
### High-level system shape
The repo is built around “author once, ship twice”. A workflow definition lives as files, then gets consumed in two ways:

1. as a plugin package for Claude/Cowork
2. as a managed-agent manifest plus deployment harness

That is the central design decision in [`README.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/README.md).

### Main layers
**Layer 1: reusable domain knowledge and actions**

- skills under paths like [`plugins/vertical-plugins/financial-analysis/skills/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis/skills)
- explicit slash commands under paths like [`plugins/vertical-plugins/equity-research/commands/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/equity-research/commands)
- connector config in [`plugins/vertical-plugins/financial-analysis/.mcp.json`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis/.mcp.json)

This layer is the source of truth for methods and integrations.

**Layer 2: packaged workflow agents**

- agent prompts under paths like [`plugins/agent-plugins/pitch-agent/agents/pitch-agent.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/pitch-agent/agents/pitch-agent.md)
- bundled local skill copies under paths like [`plugins/agent-plugins/pitch-agent/skills/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/pitch-agent/skills)

These directories make each agent self-contained, which is useful operationally because install targets do not need to resolve a dependency graph at install time.

**Layer 3: managed-agent wrappers**

- manifests such as [`managed-agent-cookbooks/pitch-agent/agent.yaml`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks/pitch-agent/agent.yaml)
- handoff examples and subagents under each cookbook directory

This layer adapts the same workflow into headless API deployment.

**Layer 4: deployment and integrity tooling**

- [`scripts/deploy-managed-agent.sh`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/deploy-managed-agent.sh)
- [`scripts/orchestrate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/orchestrate.py)
- [`scripts/sync-agent-skills.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/sync-agent-skills.py)
- [`scripts/validate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/validate.py)

This layer is intentionally small. It mostly resolves file references, uploads skills, deploys agents, validates schema output, and routes handoffs.

### Request / data / control flow
Typical control flow looks like this:

1. User picks an installed agent plugin, or a firm deploys a managed agent from a cookbook.
2. The workflow prompt invokes bundled skills and vertical commands.
3. Data access happens through MCP connectors, mostly centralized in the core [`financial-analysis`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis) plugin.
4. For managed deployment, [`scripts/deploy-managed-agent.sh`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/deploy-managed-agent.sh) resolves manifest indirections, uploads skills, recursively creates callable subagents, and posts the orchestrator to `/v1/agents`.
5. During runtime, [`scripts/orchestrate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/orchestrate.py) watches streamed text for structured `handoff_request` payloads, validates them, allowlists the target slug, then steers the relevant managed subagent.

The interesting thing here is that orchestration is treated as a thin outer shell around mostly declarative agent assets.

## Key directories and files
- [`plugins/agent-plugins/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins): the clearest view of the finished “product units”
- [`plugins/vertical-plugins/financial-analysis/.mcp.json`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis/.mcp.json): the connector nexus, with Daloopa, FactSet, PitchBook, LSEG, Egnyte, and other provider endpoints
- [`plugins/agent-plugins/pitch-agent/agents/pitch-agent.md`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/agent-plugins/pitch-agent/agents/pitch-agent.md): a strong example of the repo’s style, showing concrete workflow steps, guardrails, and tool scope
- [`managed-agent-cookbooks/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/managed-agent-cookbooks): where the plugin-side assets become deployable API agents
- [`scripts/deploy-managed-agent.sh`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/deploy-managed-agent.sh): the repo’s most important machinery file
- [`scripts/sync-agent-skills.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/sync-agent-skills.py): the answer to “how do they manage duplicated skills?”
- [`scripts/orchestrate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/orchestrate.py): a small but revealing example of safe-ish handoff routing

## Important components
**The vertical-to-agent packaging model**

The repo authors skills once in vertical bundles, then vendors copies into individual agent packages. [`scripts/sync-agent-skills.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/sync-agent-skills.py) is a blunt but effective propagation mechanism: delete bundled copies, copy fresh versions from vertical sources.

**The managed-agent deploy script**

[`scripts/deploy-managed-agent.sh`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/deploy-managed-agent.sh) is the real backbone. It inlines `system.file`, expands `from_plugin` skill imports, uploads skill directories, recursively creates callable subagents, and turns a human-friendly YAML manifest into API payloads.

**The handoff parser and validator**

[`scripts/orchestrate.py`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/orchestrate.py) reveals a practical concern most agent demos skip: untrusted text may try to spoof internal routing events. The repo mitigates that with slug allowlists and JSON schema validation before steering.

**Connector centralization**

By keeping shared finance connectors in [`plugins/vertical-plugins/financial-analysis/.mcp.json`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/plugins/vertical-plugins/financial-analysis/.mcp.json), the repo avoids duplicating external integration config across every workflow.

## Important knobs / configs / extension points
- managed-agent manifests in cookbook `agent.yaml` files are the main deployment knobs
- `system.file`, `skills.path`, and `callable_agents.manifest` in [`scripts/deploy-managed-agent.sh`](https://github.com/anthropics/financial-services/blob/57772c3f1607229fba0270f94abf3c976bbd852f/scripts/deploy-managed-agent.sh) are the key indirection mechanisms
- `.mcp.json` files are the main external integration points
- agent prompt files under each `agents/` directory are where workflow behavior, stop points, and guardrails actually live
- [`claude-for-msft-365-install/`](https://github.com/anthropics/financial-services/tree/57772c3f1607229fba0270f94abf3c976bbd852f/claude-for-msft-365-install) is an adoption extension point, not part of core workflow logic

## Practical questions and answers
### Why vendor skill copies into each agent instead of referencing them dynamically?
Because install simplicity matters. A self-contained agent is easier to distribute and reason about than a plugin with transitive skill dependencies.

### Where is the real complexity?
Not in code volume. It is in packaging discipline, workflow boundaries, connector assumptions, and prompt/skill curation.

### What would fail first in production?
Connector reliability, provider entitlement mismatches, and workflow drift between the vendored agent skills and the vertical source of truth.

### Is the orchestration approach robust?
As a reference pattern, yes. As production infrastructure, not by itself. Text-parsed handoff detection is clever but still fragile compared with typed internal events.

### Is this mostly hype?
Less than average. The repo is still largely scaffolding and workflow templates, but it is concrete scaffolding with operational intent.

## What is smart
- The “same workflow, two deployment modes” idea is genuinely good.
- The repo stays file-first, which makes review and customization easy.
- Connector centralization is sane.
- The orchestrator acknowledges prompt-injection-style spoofing and tries to fence it.
- The prompts are workflow-specific enough to be useful, not generic “you are a helpful analyst” mush.

## What is flawed or weak
- Vendoring skills per agent is practical, but it is still duplication with drift risk.
- The runtime story depends heavily on third-party data providers and enterprise entitlements.
- The handoff parser works by regexing model text for a JSON blob, which is better than nothing but not a beautiful primitive.
- Because the repo is mostly templates, it is easier to admire than to prove. Real production quality will live in the firm-specific edits, not in the reference assets alone.

## What we can learn / steal
- Package domain agents as inspectable folders, not hidden platform config.
- Separate reusable domain skills from end-to-end workflow wrappers.
- Keep deployment glue thin and declarative.
- Treat handoff security and schema validation as first-class concerns, even in reference code.
- Centralize connectors and data access conventions instead of scattering them across agents.

## How we could apply it
A non-finance team could copy this pattern almost directly for legal ops, healthcare back office, procurement, security triage, or sales engineering:

- one shared vertical for common methods and connectors
- one self-contained agent per real workflow
- one cookbook per headless deployment target
- one tiny deploy/orchestration layer that resolves manifests and validates subagent output

The bigger reusable lesson is not “build finance agents”. It is “treat prompts, skills, connectors, and deployment manifests as versioned architecture artifacts”.

## Bottom line
This is one of the better current AI workflow repos because it is not pretending the magic is in a giant codebase. The magic, such as it is, is in good packaging boundaries: reusable skills, self-contained agent products, thin deployment glue, and explicit connector surfaces.

The main insight is that the repo is really a packaging system for domain workflows, with just enough code to keep the packaging honest.
