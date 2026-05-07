# Agent Skills

- Repo: `addyosmani/agent-skills`
- URL: https://github.com/addyosmani/agent-skills
- Date: 2026-05-07
- Repo snapshot studied: `main@742dca58ae557bc67afec9ea8e6de59c085f0534`
- Why picked today: It is one of the hottest GitHub repos right now, clearly AI-related, and more worth studying than the average agent wrapper because its real product is workflow structure, not model novelty.

## Executive summary
Agent Skills is a repo that packages senior-engineering process into portable instruction modules for coding agents.

The important thing is that this is not really a “bag of prompts”. It is a layered control system: lifecycle commands pick workflows, workflows load only when relevant, personas provide specialist viewpoints, references hold detailed checklists, and plugin manifests adapt the whole thing to multiple agent harnesses.

The smartest idea here is that the repo treats good software process as an installable runtime primitive. The weakness is that this kind of system only works if the host agent actually obeys it. There is no hard enforcement layer beyond what each harness supports.

## What they built
They built a cross-harness skill/plugin repo that tries to make coding agents behave more like disciplined software engineers.

The main pieces are:

- a lifecycle-facing front door in [`README.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/README.md) and the slash-command set under [`.claude/commands/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude/commands)
- a skill library under [`skills/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/skills) with 21 skill directories, each centered on a `SKILL.md`
- a meta-skill at [`skills/using-agent-skills/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/using-agent-skills/SKILL.md) that teaches the agent how to choose the other skills
- specialist reviewer personas under [`agents/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/agents)
- detailed checklists and orchestration references under [`references/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/references)
- harness adapters and packaging metadata in [`AGENTS.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/AGENTS.md), [`.claude-plugin/plugin.json`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude-plugin/plugin.json), and [`.claude-plugin/marketplace.json`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude-plugin/marketplace.json)
- optional hook scripts under [`hooks/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/hooks) that preload or optimize parts of the workflow

## Why it matters
A lot of agent tooling still focuses on model routing, tool calling, or IDE chrome. Agent Skills focuses on something more durable: behavioral scaffolding.

That matters because many agent failures are not raw model-IQ failures. They are process failures: skipping specs, failing to test, hiding uncertainty, overbuilding, or shipping without review. This repo tries to attack exactly that layer.

## Repo shape at a glance
Top-level structure:

- [`skills/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/skills) is the core product. It contains the skill workflows grouped implicitly by lifecycle stage.
- [`.claude/commands/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude/commands) is the orchestration layer for Claude-style slash commands like `spec`, `plan`, `build`, `test`, `review`, and `ship`.
- [`agents/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/agents) contains persona prompts for specialized review roles like code reviewer, security auditor, and test engineer.
- [`references/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/references) contains lower-level checklists and patterns that skills can pull in on demand.
- [`docs/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/docs) explains installation and harness-specific integration for Cursor, Gemini CLI, Copilot, OpenCode, Windsurf, and others.
- [`hooks/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/hooks) adds operational behavior such as session-start injection and web-fetch caching.
- [`.github/workflows/test-plugin-install.yml`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.github/workflows/test-plugin-install.yml) is a small but important CI check that validates plugin structure and installation behavior.

This is a documentation-first repo, but it is not flat documentation. It is organized like a behavior framework.

## Layered architecture dissection
### High-level system shape
The clean mental model is:

1. expose lifecycle entry points
2. map user intent to a workflow skill
3. optionally fan out to specialist personas
4. pull in references only when needed
5. adapt the same content to multiple agent harnesses through manifests, agent files, and hooks

So the repo behaves like a prompt-and-policy compiler for coding-agent behavior.

### Main layers
**1. Product entry and lifecycle framing**

- [`README.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/README.md) is not just marketing. It defines the lifecycle model: define, plan, build, verify, review, ship.
- The slash-command files in [`.claude/commands/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude/commands) turn that lifecycle into harness-facing entry points.
- [`AGENTS.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/AGENTS.md) mirrors the same orchestration logic for OpenCode-style agent environments.

**2. Skill selection and mandatory behavior layer**

- [`skills/using-agent-skills/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/using-agent-skills/SKILL.md) is the most important file in the repo because it defines the governing behavior for every other skill.
- It forces skill lookup before work, surfaces assumptions, tells the agent to stop when confused, pushes back on bad plans, and insists on verification.
- This file is basically the repo’s policy kernel.

**3. Domain workflow layer**

- The individual workflow modules under [`skills/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/skills) are the actual product units.
- They are organized around practical engineering activities, for example [`skills/spec-driven-development/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/spec-driven-development/SKILL.md), [`skills/incremental-implementation/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/incremental-implementation/SKILL.md), [`skills/test-driven-development/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/test-driven-development/SKILL.md), [`skills/code-review-and-quality/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/code-review-and-quality/SKILL.md), and [`skills/shipping-and-launch/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/shipping-and-launch/SKILL.md).
- Each one follows a common anatomy described in [`docs/skill-anatomy.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/docs/skill-anatomy.md): overview, when to use, process, rationalizations, red flags, verification.

**4. Persona fan-out layer**

- [`agents/code-reviewer.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/agents/code-reviewer.md), [`agents/security-auditor.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/agents/security-auditor.md), and [`agents/test-engineer.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/agents/test-engineer.md) provide viewpoint-specific lenses.
- The interesting design choice is that personas are kept distinct from skills. Skills are workflow. Personas are perspective. The repo is explicit about that boundary in [`AGENTS.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/AGENTS.md).
- [`.claude/commands/ship.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude/commands/ship.md) shows the pattern clearly: fan out to personas in parallel, then merge centrally.

**5. Progressive-disclosure reference layer**

- [`references/testing-patterns.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/references/testing-patterns.md), [`references/security-checklist.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/references/security-checklist.md), [`references/performance-checklist.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/references/performance-checklist.md), and [`references/orchestration-patterns.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/references/orchestration-patterns.md) are not the product front door.
- They exist so the main skill files can stay concise and only expand when a task actually needs detail.
- That is a good token-economy design.

**6. Harness adaptation and runtime support layer**

- [`.claude-plugin/plugin.json`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude-plugin/plugin.json) and [`.claude-plugin/marketplace.json`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude-plugin/marketplace.json) package the repo as an installable Claude plugin.
- The harness docs in [`docs/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/docs) explain how the same content maps into other environments.
- The hook config in [`hooks/hooks.json`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/hooks/hooks.json) plus scripts like [`hooks/session-start.sh`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/hooks/session-start.sh) and [`hooks/sdd-cache-pre.sh`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/hooks/sdd-cache-pre.sh) add some actual runtime behavior beyond static prompt files.

### Request / data / control flow
A typical use path looks like this:

1. the user enters through a lifecycle command like one of the files in [`.claude/commands/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude/commands) or through an agent environment that reads [`AGENTS.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/AGENTS.md)
2. the meta-skill in [`skills/using-agent-skills/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/using-agent-skills/SKILL.md) decides which workflow applies
3. the chosen workflow skill under [`skills/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/skills) provides the process, rationalization guardrails, and verification checklist
4. if the task needs specialist review, a command like [`.claude/commands/ship.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude/commands/ship.md) fans out to personas under [`agents/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/agents)
5. when extra detail is needed, the workflow reaches into [`references/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/references) rather than bloating the core entry file
6. packaging files and hook scripts adapt that behavior to the host harness and can preload the meta-skill or optimize fetch-heavy workflows

The “data flow” here is mostly instruction flow. That sounds softer than code architecture, but it is the real architecture of the repo.

## Key directories and files
- [`README.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/README.md): top-level lifecycle model and skill catalog.
- [`AGENTS.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/AGENTS.md): OpenCode-oriented orchestration rules and composition model.
- [`skills/using-agent-skills/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/using-agent-skills/SKILL.md): the governing meta-skill.
- [`skills/spec-driven-development/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/spec-driven-development/SKILL.md): representative “define first” workflow.
- [`skills/incremental-implementation/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/incremental-implementation/SKILL.md): representative build discipline.
- [`skills/test-driven-development/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/test-driven-development/SKILL.md): proof-oriented verification workflow.
- [`.claude/commands/ship.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude/commands/ship.md): clearest example of orchestration-by-command.
- [`agents/code-reviewer.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/agents/code-reviewer.md): representative persona design.
- [`docs/skill-anatomy.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/docs/skill-anatomy.md): explains the reusable content schema.
- [`.claude-plugin/plugin.json`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude-plugin/plugin.json): plugin packaging contract.
- [`hooks/session-start.sh`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/hooks/session-start.sh): meta-skill injection hook.
- [`.github/workflows/test-plugin-install.yml`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.github/workflows/test-plugin-install.yml): installability check in CI.

## Important components
**The meta-skill is the real control center**

[`skills/using-agent-skills/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/using-agent-skills/SKILL.md) is the most central component because it controls discovery, assumption handling, confusion management, scope discipline, and verification. Without it, the rest of the repo is just a menu.

**The command layer turns workflows into a usable product**

The files in [`.claude/commands/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude/commands) are what make the system feel ergonomic instead of academic. They map a developer’s immediate intent to a workflow trigger.

**Personas are deliberately separated from workflows**

The split between [`agents/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/agents) and [`skills/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/skills) is one of the best design decisions in the repo. It avoids mixing “how to work” with “from what perspective to evaluate the work”.

**Hooks make the repo slightly more than static prompt content**

[`hooks/session-start.sh`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/hooks/session-start.sh) injects the meta-skill at session start, while [`hooks/sdd-cache-pre.sh`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/hooks/sdd-cache-pre.sh) adds a clever HTTP-validator cache around WebFetch. That is small operational code, but it proves the repo is thinking about runtime costs and compliance.

**CI protects packaging, not just prose**

[`.github/workflows/test-plugin-install.yml`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.github/workflows/test-plugin-install.yml) validates plugin structure and installation through Claude’s tooling. That matters because packaging breakage would quietly kill the whole project.

## Important knobs / configs / extension points
- [`.claude-plugin/plugin.json`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude-plugin/plugin.json): declares commands, skills, and persona files to Claude’s plugin system.
- [`.claude-plugin/marketplace.json`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude-plugin/marketplace.json): marketplace-facing packaging metadata.
- [`hooks/hooks.json`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/hooks/hooks.json): hook registration surface.
- [`docs/gemini-cli-setup.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/docs/gemini-cli-setup.md), [`docs/cursor-setup.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/docs/cursor-setup.md), and [`docs/opencode-setup.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/docs/opencode-setup.md): harness-specific adaptation points.
- [`docs/skill-anatomy.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/docs/skill-anatomy.md): the content schema that keeps new skills structurally consistent.

## Practical questions and answers
**Is this just prompt engineering with better branding?**

Partly, yes, but that undersells it. The repo is better understood as process engineering for agents.

**What is the best idea in the repo?**

Separating lifecycle commands, workflow skills, specialist personas, and deep references into different layers instead of dumping everything into one giant instruction file.

**What is the main thing to copy?**

The meta-skill pattern plus progressive disclosure. Put the policy kernel in one governing file, then keep specialist workflows modular and load them only when triggered.

**Where is it brittle?**

At enforcement boundaries. If the host harness ignores hook behavior, skips skill invocation, or gives the model too much latitude, the whole system degrades back into “best effort prompting”.

**Does it feel engineered or merely curated?**

More engineered than curated. The repo is mostly Markdown, but the structure, packaging, orchestration, and hook behavior are intentional enough that it behaves like a software product.

## What is smart
- The repo decomposes agent behavior into layers instead of one monolithic system prompt.
- The meta-skill in [`skills/using-agent-skills/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/using-agent-skills/SKILL.md) gives the whole library a governing center.
- [`docs/skill-anatomy.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/docs/skill-anatomy.md) standardizes authoring so the library can scale without turning into chaos.
- [`.claude/commands/ship.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude/commands/ship.md) shows a strong orchestration instinct: fan out specialist reviews, then merge centrally.
- [`hooks/sdd-cache-pre.sh`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/hooks/sdd-cache-pre.sh) is a subtle but very good idea for keeping source-driven workflows cheaper.

## What is flawed or weak
- The repo cannot fully guarantee compliance. It can strongly suggest process, but final behavior still depends on the host agent and harness.
- There is some risk of cargo-culting process. Less capable users may install the whole system and assume discipline is automatic.
- The framework currently leans heavily toward software-engineering tasks. It is less clear how well the same structure generalizes to product, research, or ops work without further specialization.
- Cross-harness portability is a strength, but also a constraint. The lowest-common-denominator effect can limit deeper harness-specific features.
- A repo built mostly from Markdown can look simpler than it really is, which may cause casual contributors to underestimate the importance of boundary discipline.

## What we can learn / steal
- Treat process as a modular artifact, not a giant team handbook.
- Separate orchestration, workflow, perspective, and deep reference into different layers.
- Use a meta-skill or policy-kernel file to govern how all other modules are chosen.
- Keep heavy reference material out of the main execution path and load it progressively.
- Add light operational code where it materially improves compliance or cost, like session-start injection and fetch caching.

## How we could apply it
If we were building our own agent-facing workflow system, I would copy these pieces first:

1. the governing meta-skill pattern from [`skills/using-agent-skills/SKILL.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/skills/using-agent-skills/SKILL.md)
2. the separation between commands in [`.claude/commands/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/.claude/commands), workflows in [`skills/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/skills), and perspectives in [`agents/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/agents)
3. the standard skill anatomy in [`docs/skill-anatomy.md`](https://github.com/addyosmani/agent-skills/blob/742dca58ae557bc67afec9ea8e6de59c085f0534/docs/skill-anatomy.md)
4. the small but useful runtime hooks in [`hooks/`](https://github.com/addyosmani/agent-skills/tree/742dca58ae557bc67afec9ea8e6de59c085f0534/hooks)

I would be more cautious about assuming prompt-level workflows alone are enough. If a task is high-risk, I would still want harder enforcement through tooling, CI gates, or approval boundaries.

## Bottom line
Agent Skills is interesting because it treats engineering discipline as installable infrastructure for coding agents.

The key insight is that the repo’s real product is not any one skill. It is the layered architecture that turns vague “best practices” into a usable workflow system: command entry points, a policy kernel, modular skills, specialist personas, progressive references, and light runtime hooks.