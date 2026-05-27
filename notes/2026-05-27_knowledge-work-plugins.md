# Knowledge Work Plugins

- Repo: `anthropics/knowledge-work-plugins`
- URL: https://github.com/anthropics/knowledge-work-plugins
- Date: 2026-05-27
- Repo snapshot studied: `main` @ `f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f`
- Why picked today: It was on GitHub Trending on 2026-05-27, it is directly about the current agent/plugin wave, and it is interesting precisely because it avoids the usual framework sprawl. The repo is mostly product grammar, not application code.

## Executive summary
This repo is Anthropic trying to standardize a new packaging unit for agent behavior: a plugin is a folder full of manifests, skill files, commands, and MCP connector definitions. The important idea is not any one skill. The important idea is that they are treating agent behavior as deployable configuration, with role-specific distribution and connector wiring, instead of as a monolithic app.

The strongest insight here is that the repo is intentionally low-code. The architecture is mostly markdown and JSON because the real product thesis is that a lot of agent specialization should be editable by operators, domain experts, and workflow owners, not only by engineers.

## What they built
They built a marketplace-style monorepo of role-specific Claude plugins for knowledge work. Each plugin packages some combination of:

- a plugin manifest such as [`engineering/.claude-plugin/plugin.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/.claude-plugin/plugin.json)
- MCP connector definitions such as [`engineering/.mcp.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/.mcp.json)
- slash-command specs such as [`product-management/commands/brainstorm.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/product-management/commands/brainstorm.md)
- auto-triggered skills such as [`engineering/skills/code-review/SKILL.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/skills/code-review/SKILL.md)
- special-purpose connector-backed plugins such as [`pdf-viewer/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/pdf-viewer)

The marketplace index in [`.claude-plugin/marketplace.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/.claude-plugin/marketplace.json) then ties those plugin folders into one distribution surface.

## Why it matters
A lot of agent-tooling repos are still secretly apps. This one is closer to a behavior catalog. That matters because it suggests a scaling path for AI workflows that is more operational than infrastructural: publish small, role-specific behavior bundles, wire them to MCP tools, and let teams customize the instructions without recompiling software.

That is a real product move. It lowers the editing surface from “change product code” to “change plugin contract.”

## Repo shape at a glance
Top-level structure:

- [`README.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/README.md): overall thesis, install model, and plugin structure
- [`.claude-plugin/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/.claude-plugin): marketplace metadata, especially [`marketplace.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/.claude-plugin/marketplace.json)
- role plugins like [`engineering/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering), [`product-management/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/product-management), [`sales/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/sales), [`finance/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/finance), and others
- utility/specialized plugins like [`pdf-viewer/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/pdf-viewer)
- external ecosystem entries under [`partner-built/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/partner-built)

Inside a typical plugin, the repeating shape is:

- [`.claude-plugin/plugin.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/.claude-plugin/plugin.json): identity and display metadata
- [`.mcp.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/.mcp.json): connector map
- [`README.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/README.md): human-facing workflow overview
- [`commands/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/product-management/commands): explicit slash-command behaviors when the plugin exposes them
- [`skills/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/skills): auto-invoked role knowledge and workflow instructions
- [`CONNECTORS.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/CONNECTORS.md): operator-facing tool wiring guidance

## Layered architecture dissection
### High-level system shape
At a high level the repo works like this:

1. a marketplace file declares available plugins
2. each plugin defines its identity, supported workflows, and external tool surface
3. skills provide reusable background behavior
4. commands provide explicit user-invoked flows
5. MCP config binds the plugin to external systems like Slack, Notion, Jira, GitHub, Datadog, or a local PDF server
6. end users customize the text files to fit company process

This is less “software application” and more “distribution format for agent operating procedures.”

### Main layers
**1. Marketplace and distribution layer**

[`.claude-plugin/marketplace.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/.claude-plugin/marketplace.json) is the catalog root. It defines the bundle as a plugin marketplace and also shows an important design choice: first-party plugins and partner-built plugins live in the same listing format.

**2. Plugin package layer**

Each plugin folder such as [`engineering/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering) or [`product-management/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/product-management) is effectively a deployable package boundary. The plugin manifest, connector map, and skills/commands all sit together, which keeps role behavior localized.

**3. Behavior layer: skills**

Files like [`engineering/skills/code-review/SKILL.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/skills/code-review/SKILL.md) are the real product core. They encode trigger conditions, workflow steps, output formats, and fallback behavior. This is the part most teams will actually want to edit.

**4. Explicit workflow layer: commands**

Files like [`product-management/commands/brainstorm.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/product-management/commands/brainstorm.md) or [`pdf-viewer/commands/annotate.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/pdf-viewer/commands/annotate.md) define explicit operator entry points. The repo separates “Claude should know this automatically” from “Claude should do this when invoked,” which is a healthy boundary.

**5. Connector layer**

Connector maps like [`engineering/.mcp.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/.mcp.json) and [`pdf-viewer/.mcp.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/pdf-viewer/.mcp.json) are a big deal. They make the plugin not just a prompt bundle, but an executable role surface connected to real systems.

### Request / data / control flow
A simplified flow looks like this:

- user installs a plugin described in [`README.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/README.md)
- the runtime reads the plugin manifest and connector config from a chosen plugin folder like [`engineering/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering)
- auto-triggered help comes from `skills/*/SKILL.md` files such as [`engineering/skills/code-review/SKILL.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/skills/code-review/SKILL.md)
- explicit slash actions come from command files such as [`product-management/commands/brainstorm.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/product-management/commands/brainstorm.md)
- MCP servers from [`.mcp.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/.mcp.json) provide tool access for richer execution
- the resulting user experience is a role-specific agent shell instead of a generic chat model

## Key directories and files
- [`README.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/README.md): repo thesis and file-based plugin contract
- [`.claude-plugin/marketplace.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/.claude-plugin/marketplace.json): marketplace index and distribution metadata
- [`engineering/.mcp.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/.mcp.json): good example of multi-tool connector wiring for one role
- [`engineering/skills/code-review/SKILL.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/skills/code-review/SKILL.md): representative auto-skill structure
- [`product-management/commands/brainstorm.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/product-management/commands/brainstorm.md): representative command structure
- [`pdf-viewer/.mcp.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/pdf-viewer/.mcp.json): example of a local tool-backed specialist plugin
- [`pdf-viewer/commands/annotate.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/pdf-viewer/commands/annotate.md): concrete human-in-the-loop workflow contract

## Important components
**Marketplace registry**

[`.claude-plugin/marketplace.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/.claude-plugin/marketplace.json) is the composition root. It shows this repo is not just a folder dump. It is a curated install surface.

**Role package boundary**

A folder like [`engineering/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering) is the main packaging primitive: identity, connectors, docs, and behavior are all colocated.

**Skill contract format**

[`engineering/skills/code-review/SKILL.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/skills/code-review/SKILL.md) is a strong representative example because it includes trigger language, dimensions of review, output schema, and fallback rules. It reads like executable operations documentation.

**Command contract format**

[`product-management/commands/brainstorm.md`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/product-management/commands/brainstorm.md) shows how the repo handles explicit session modes differently from passive expertise.

**Connector abstraction**

[`engineering/.mcp.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/.mcp.json) is important because it turns the plugin into a portable role adapter over Slack, Linear, Atlassian, GitHub, PagerDuty, and Datadog. That is the practical substrate behind the workflow promises.

**Specialized local-tool plugin**

[`pdf-viewer/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/pdf-viewer) is especially interesting because it shows the pattern can also package an interactive local capability, not just remote SaaS connectors.

## Important knobs / configs / extension points
- marketplace composition in [`.claude-plugin/marketplace.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/.claude-plugin/marketplace.json)
- per-plugin metadata in [`engineering/.claude-plugin/plugin.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/.claude-plugin/plugin.json)
- tool wiring in [`engineering/.mcp.json`](https://github.com/anthropics/knowledge-work-plugins/blob/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/.mcp.json)
- human-editable role logic in [`engineering/skills/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/engineering/skills)
- explicit command surfaces in [`product-management/commands/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/product-management/commands)
- partner ecosystem extension under [`partner-built/`](https://github.com/anthropics/knowledge-work-plugins/tree/f2c8f30b5b9b42301ad7c3696f4bf93d5b872e2f/partner-built)

## Practical questions and answers
**What is the deepest idea in the repo?**

That agent specialization can be shipped as editable file bundles rather than full-blown software features.

**What is the key architectural bet?**

That markdown and JSON are enough of a control plane for many business workflows, as long as MCP provides the tool plane.

**What is most reusable here?**

The plugin folder contract itself: manifest, connectors, commands, skills, operator docs.

**Where is the real leverage?**

In the repeated package shape. Once the runtime understands the shape, new roles become mostly content and connector work.

**What would fail first in the wild?**

Connector drift and instruction entropy. A repo like this only stays sharp if someone curates stale workflows, renamed tools, bad trigger phrases, and overgrown skill text.

## What is smart
- choosing a low-code packaging model for workflow specialization
- separating passive skills from explicit commands
- making connector wiring first-class instead of hiding it in prose
- colocating role docs, behavior, and integration config in one folder
- allowing partner-built plugins into the same marketplace structure

## What is flawed or weak
- there is very little executable validation in the repo itself, so instruction quality can drift silently
- markdown-based behavior specs are easy to edit but also easy to bloat
- consistency across dozens of plugins will become a governance problem fast
- some workflow promises are only as good as the external MCP servers, which are outside this repo's control

## What we can learn / steal
- treat agent behaviors as packages, not just prompts
- make the integration surface explicit and inspectable
- separate automatic expertise from user-invoked workflows
- use a repeatable plugin folder contract so non-engineers can safely customize behavior
- keep the artifact human-readable so operational owners can maintain it

## How we could apply it
If we built internal agent tooling, I would steal the packaging model before I stole any specific workflow. A good internal version would have:

1. one standard plugin folder format
2. explicit connector config per role
3. skills for ambient expertise
4. commands for high-stakes explicit workflows
5. lightweight linting so the text-based control plane does not rot

The extra thing I would add is validation. This repo has the right ergonomic instinct, but it needs stronger quality rails if it keeps growing.

## Bottom line
Knowledge Work Plugins is interesting because it treats agent behavior like an operational product surface instead of like a demo prompt.

The best idea is simple: standardize the package, externalize the workflows, wire the tools, and let teams edit the behavior in files. That is much more durable than shipping one giant “AI coworker” blob and hoping everyone bends around it.