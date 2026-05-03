# Browserbase Skills

- Repo: `browserbase/skills`
- URL: https://github.com/browserbase/skills
- Date: 2026-05-03
- Repo snapshot studied: `main@2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6`
- Why picked today: It is trending, AI-agent-adjacent, and more structurally interesting than it first appears. The hook is not just "browser automation," it is an attempt to package browser operations as installable agent-facing skills with opinionated workflows, tool routing rules, and concrete operational playbooks.

## Executive summary
`browserbase/skills` is not a traditional application repo. It is a distribution pack for agent skills, mostly aimed at Claude Code style environments, that teaches an agent when to browse, when to fetch, when to search, when to deploy a cloud function, when to sync cookies, and when to run adversarial UI testing.

The key architectural insight is that the real product here is a **behavior layer for coding agents**, not just a browser CLI. The repo turns operational knowledge into installable markdown-based skills, with a small plugin/marketplace wrapper around them. In other words, Browserbase is productizing agent instructions as a software surface.

## What they built
They built a skills bundle with a few distinct pieces:
- a lightweight plugin/package wrapper in [`package.json`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/package.json) and [`.claude-plugin/marketplace.json`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/.claude-plugin/marketplace.json)
- a catalog of installable skills in [`skills/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills), including browsing, Browserbase CLI usage, fetch, search, functions, cookie sync, tracing, UI testing, company research, and event prospecting
- a local `agent/` workspace for screenshots, downloads, and custom scripts in [`agent/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/agent)
- long-form operational guidance embedded directly inside skill markdown, for example [`skills/browser/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser/SKILL.md) and [`skills/ui-test/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/ui-test/SKILL.md)

So the repo is closer to an agent runtime knowledge pack than to a normal SDK.

## Why it matters
A lot of agent tooling stops at APIs and CLIs. This repo tackles the uglier but more practical layer: how do you teach an autonomous coding agent to use those tools consistently, choose the right mode, avoid expensive mistakes, and produce reproducible workflows?

That matters because in agent systems the fragile thing is often not the low-level API, it is the decision policy around the API. This repo externalizes that policy into versioned skill files.

## Repo shape at a glance
Top-level shape:

- [`skills/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills), the center of gravity
  - [`skills/browser/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser), interactive browse CLI guidance
  - [`skills/browserbase-cli/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browserbase-cli), `bb` command workflows for sessions, projects, contexts, and functions
  - [`skills/fetch/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/fetch), static retrieval guidance
  - [`skills/search/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/search), structured web-search guidance
  - [`skills/functions/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/functions), cloud-function deployment playbook
  - [`skills/cookie-sync/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/cookie-sync), authenticated browsing via synced local cookies
  - [`skills/browser-trace/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser-trace), observability and CDP firehose capture
  - [`skills/ui-test/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/ui-test), adversarial browser QA orchestration
  - [`skills/company-research/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/company-research) and [`skills/event-prospecting/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/event-prospecting), higher-level GTM workflows
- [`.claude-plugin/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/.claude-plugin), marketplace metadata and install surface
- [`agent/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/agent), runtime scratch area for browser artifacts
- [`README.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/README.md), high-level catalog and installation path

The repo shape says: the main asset is curated instruction, not source code volume.

## Layered architecture dissection
### High-level system shape
The system shape is:
agent environment -> plugin marketplace entry -> selected skill markdown -> external CLI or API -> browser / fetch / search / Browserbase platform.

This is a repo of adapters between human intent, agent decision-making, and Browserbase tooling.

### Main layers
**1. Packaging and marketplace layer**
- [`package.json`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/package.json)
- [`.claude-plugin/marketplace.json`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/.claude-plugin/marketplace.json)

This layer makes the repo installable as a skill/plugin source. One revealing detail is how thin it is. The packaging mostly exists to expose a marketplace and a binary entrypoint, while the real logic lives in markdown skill content.

**2. Core browser-operation skills**
- [`skills/browser/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser/SKILL.md)
- [`skills/fetch/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/fetch/SKILL.md)
- [`skills/search/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/search/SKILL.md)
- [`skills/browserbase-cli/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browserbase-cli/SKILL.md)

This layer splits the web-access problem into distinct modes: interactive browser control, static fetch, structured search, and platform CLI operations. That decomposition is smart because it teaches the agent not to overuse a full browser when a cheaper primitive is enough.

**3. Session and identity layer**
- [`skills/cookie-sync/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/cookie-sync/SKILL.md)
- parts of [`skills/browser/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser/SKILL.md) covering local vs remote mode, context IDs, and persistence

This layer handles one of the hardest practical browser-agent problems: authenticated state. The cookie-sync pattern is especially pragmatic because it bridges local human login state into a persistent cloud browser context.

**4. Observability and QA layer**
- [`skills/browser-trace/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser-trace/SKILL.md)
- [`skills/ui-test/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/ui-test/SKILL.md)

This is where the repo gets more interesting. It does not stop at “drive a browser.” It adds debugging, evidence capture, adversarial testing, screenshot conventions, step budgets, and subagent orchestration rules. That is a real operational layer.

**5. Higher-level workflow products**
- [`skills/company-research/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/company-research/SKILL.md)
- [`skills/event-prospecting/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/event-prospecting/SKILL.md)

These skills turn the lower-level Browserbase primitives into GTM automation workflows. They are effectively vertical applications encoded as skill instructions.

### Request / data / control flow
A representative flow looks like this:
1. an agent installs the marketplace via [`.claude-plugin/marketplace.json`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/.claude-plugin/marketplace.json)
2. the agent picks a skill based on task type, for example [`skills/browser/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser/SKILL.md) for interaction or [`skills/fetch/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/fetch/SKILL.md) for static retrieval
3. the skill tells the agent which CLI or API primitive to invoke, with explicit mode-selection rules and fallback logic
4. artifacts land in local workspace paths like [`agent/`](https://github.com/browserbase/skills/tree/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/agent) or dedicated report directories described inside the skills
5. for advanced workflows, subagents are coordinated using planning, batching, and evidence rules embedded in the skill text, especially in [`skills/ui-test/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/ui-test/SKILL.md)

## Key directories and files
- [`skills/browser/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser/SKILL.md): the main interaction policy, including local vs remote choice, snapshot-first behavior, and browse command workflows
- [`skills/browserbase-cli/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browserbase-cli/SKILL.md): platform-control surface for `bb`
- [`skills/fetch/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/fetch/SKILL.md): the cheaper non-browser retrieval path
- [`skills/search/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/search/SKILL.md): search-before-browse decision boundary
- [`skills/cookie-sync/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/cookie-sync/SKILL.md): authenticated session bridge
- [`skills/browser-trace/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser-trace/SKILL.md): observability playbook and capture layout
- [`skills/ui-test/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/ui-test/SKILL.md): one of the most opinionated files, showing how the repo encodes adversarial QA methodology
- [`skills/company-research/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/company-research/SKILL.md): demonstrates how far they push skill files toward workflow products
- [`.claude-plugin/marketplace.json`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/.claude-plugin/marketplace.json): the install/discovery map for the plugin ecosystem

## Important components
**The browser skill as policy engine**  
[`skills/browser/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser/SKILL.md) is more important than any TypeScript file here. It tells the agent when to use local browsing, when to switch to Browserbase remote mode, why `snapshot` is preferred over `screenshot`, and how to structure interactions. That is effectively runtime policy.

**The CLI split between browse and bb**  
[`skills/browserbase-cli/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browserbase-cli/SKILL.md) clarifies a subtle but important product boundary: `browse` is for interaction, `bb` is for platform operations. That separation is easy to blur, and the repo works hard not to blur it.

**Cookie-sync as the identity bridge**  
[`skills/cookie-sync/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/cookie-sync/SKILL.md) is one of the most practically valuable ideas in the repo. It addresses the real-world authentication gap that breaks many browser-agent demos.

**UI-test as encoded QA methodology**  
[`skills/ui-test/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/ui-test/SKILL.md) is arguably the most ambitious file. It does not just list commands. It encodes planning rounds, group assignment, subagent limits, evidence protocols, failure screenshot conventions, and reporting shape.

**Company-research and event-prospecting as verticalized agent apps**  
[`skills/company-research/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/company-research/SKILL.md) and [`skills/event-prospecting/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/event-prospecting/SKILL.md) show the repo stretching from tool wrappers into full workflow products.

## Important knobs / configs / extension points
- plugin exposure and install metadata in [`.claude-plugin/marketplace.json`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/.claude-plugin/marketplace.json)
- binary entrypoint and build packaging in [`package.json`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/package.json)
- environment selection rules in [`skills/browser/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser/SKILL.md)
- Browserbase API key and project ID expectations in [`skills/browserbase-cli/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browserbase-cli/SKILL.md) and [`skills/functions/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/functions/SKILL.md)
- context reuse and proxy/stealth knobs in [`skills/cookie-sync/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/cookie-sync/SKILL.md)
- observability storage layout and capture boundaries in [`skills/browser-trace/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/browser-trace/SKILL.md)
- testing policy and subagent budgeting in [`skills/ui-test/SKILL.md`](https://github.com/browserbase/skills/blob/2a3bbb3b8b19bef0ebdbf0af0a6c8a7667f61dd6/skills/ui-test/SKILL.md)

## Practical questions and answers
**What is the real artifact here?**  
A reusable instruction layer for agents, not just a wrapper around Browserbase APIs.

**What is the smartest design choice?**  
Splitting web work into browse, fetch, search, platform CLI, auth-sync, trace, and QA modes, then teaching explicit routing rules between them.

**Where is the engineering weight?**  
Mostly in operational design, workflow decomposition, and policy encoding inside the skill files, not in application code.

**What is most reusable for other agent systems?**  
The idea that skills should encode decision boundaries, fallback rules, evidence requirements, and artifact conventions, not just command syntax.

**What is the main risk?**  
Because so much logic lives in markdown instruction files, consistency and long-term maintainability depend on discipline. The repo can sprawl into a large pile of semi-code playbooks.

## What is smart
- Treating skill files as first-class product surface instead of docs afterthoughts.
- Explicitly teaching agents when *not* to use a full browser.
- Handling authenticated state through cookie sync and persistent contexts.
- Adding serious observability and QA methodology rather than stopping at browser control.
- Using higher-level vertical workflows to prove the primitives can compose into real outcomes.

## What is flawed or weak
- The packaging layer is thin enough that the repo can feel more like curated promptware than durable software in places.
- The higher-level GTM skills are extremely prescriptive, which is useful operationally but can be brittle if the surrounding tools or permission models shift.
- A lot of critical behavior lives in long markdown files, which can become hard to validate and refactor compared with executable code.
- Some skills are effectively mini-products, which raises the maintenance burden fast.
- The repo’s value is tightly coupled to specific agent ecosystems and CLI conventions.

## What we can learn / steal
- Put decision policy close to the tool, not just the UI.
- Encode “which primitive to choose” as reusable logic.
- Treat auth, observability, and failure evidence as first-class parts of browser automation.
- Package workflows as composable skills rather than only exposing raw APIs.
- When an agent is doing expensive or risky work, make it follow explicit evidence and budgeting rules.

## How we could apply it
If we were building our own agent-tool ecosystem, I would copy:
- the browse vs fetch vs search decomposition
- the snapshot-first interaction style
- the cookie-sync pattern for bridging human auth state
- the QA/reporting conventions from the UI test skill
- the broader idea that workflow knowledge can be versioned as installable skill modules

I would avoid:
- letting too much critical behavior live only in prose without stronger validation
- turning every workflow into a giant monolithic skill file
- coupling the whole system too tightly to one agent host’s plugin conventions

## Bottom line
`browserbase/skills` is worth studying because it treats agent behavior design as a real software artifact. The most useful lesson is not “browser automation is powerful.” It is “the missing layer is often policy, routing, and operational discipline, and you can package that layer too.”