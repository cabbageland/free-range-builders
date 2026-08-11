# Agency Agents

- Repo: `msitarzewski/agency-agents`
- URL: https://github.com/msitarzewski/agency-agents
- Date: 2026-08-11
- Repo snapshot studied: `main` @ `ebe9c99acb5c96f9468de368d8bead775387d1a7`
- Why picked today: GitHub daily trending showed `971 stars today` when checked, and the repo API showed `142,732` stars and `23,229` forks. More importantly, this is not a toy "prompt pack." The interesting part is the build system around the prompts: one source catalog of agent definitions, a registry for divisions, validation scripts, and generated outputs for many agent hosts.

## Executive summary
`agency-agents` is best understood as a prompt compiler and distribution pipeline disguised as a big Markdown repo. The raw source material lives in division folders like [`engineering`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering), where each file such as [`engineering/engineering-ai-engineer.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering/engineering-ai-engineer.md) is a canonical agent spec with frontmatter plus a long instruction body. The important engineering move is that the repo does not stop there. [`divisions.json`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json) acts as a taxonomy registry, [`scripts/check-divisions.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/check-divisions.sh) and [`scripts/lint-agents.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/lint-agents.sh) guard the source tree, and [`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh) emits tool-specific packages into [`integrations`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations).

The useful builder lesson is that the repo treats prompt personas as source code with adapters, not as one-off blobs. [`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh) reads frontmatter fields, normalizes names, and generates formats for Codex, OpenClaw, Gemini CLI, Cursor, Aider, Qwen, Hermes, and more. That is a more serious distribution model than most agent-template repos.

The weakness is that the core asset is still prose, not executable behavior. There is a real pipeline, but the repo's confidence mostly comes from content scale and export coverage rather than from behavioral tests that prove these agent definitions actually work across all of those hosts.

## What they built
They built a multi-division agent library plus a conversion layer:

- Source agent definitions in folders like [`academic`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/academic), [`design`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/design), [`engineering`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering), and other domain folders.
- A division registry in [`divisions.json`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json) that assigns labels, icons, and colors to each top-level division.
- Validation and build scripts in [`scripts`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts), especially [`check-divisions.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/check-divisions.sh), [`lint-agents.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/lint-agents.sh), and [`convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh).
- Generated host-specific outputs in [`integrations`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations), including [`integrations/codex`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations/codex), [`integrations/openclaw`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations/openclaw), [`integrations/cursor`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations/cursor), and many others.
- Worked examples in [`examples`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/examples), with [`examples/README.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/examples/README.md) explaining multi-agent orchestration outputs.

## Why it matters
Most public "agent collections" stop at a pile of Markdown and vibes. This repo matters because it tries to solve three real product problems:

1. Keep one canonical prompt source instead of forking prompt text per host.
2. Encode taxonomy and metadata once in a registry file.
3. Generate many tool-specific adapters from that source instead of asking users to manually rewrite prompts for each runtime.

That is the right direction if you think agents are a distribution problem as much as a prompting problem.

## Repo shape at a glance
The repo shape is clearer than the giant README suggests:

- [`engineering`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering) and sibling domain directories hold the canonical source agents.
- [`divisions.json`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json) is the source-of-truth registry for division metadata.
- [`scripts/lib.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/lib.sh) provides helpers that the build scripts share.
- [`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh) is the central compiler from canonical agent Markdown to host-specific artifacts.
- [`integrations`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations) is the generated output tree.
- [`examples`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/examples) is the demonstration layer that shows how these agents are meant to collaborate.

## Layered architecture dissection
### High-level system shape
The system shape is: write a canonical agent in Markdown with frontmatter, register and validate the division taxonomy, convert the canonical prompt into many host-specific formats, then show example orchestrations that explain how the library is supposed to be used.

### Main layers
**1. Canonical agent-definition layer**  
Files like [`engineering/engineering-ai-engineer.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering/engineering-ai-engineer.md) are the true source artifacts. They carry fields like `name`, `description`, `color`, and `vibe`, then a large instruction body. That is the repo's equivalent of source code.

**2. Taxonomy and metadata layer**  
[`divisions.json`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json) is more important than it looks. It defines which top-level directories count as actual divisions, how they should be labeled, and what icon/color identity each gets. The `_note` block also documents the repo's contract around generated outputs versus source divisions.

**3. Validation layer**  
[`scripts/check-divisions.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/check-divisions.sh), [`scripts/lint-agents.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/lint-agents.sh), and [`scripts/check-tools.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/check-tools.sh) are the guardrail layer. This is how the repo tries to stop its prompt corpus from drifting into arbitrary folder chaos.

**4. Conversion layer**  
[`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh) is the architectural center. It enumerates `AGENT_DIRS`, parses frontmatter with shared helpers, and emits many target formats including Antigravity, Gemini CLI, OpenCode, Cursor, Aider, OpenClaw, Qwen, ZCode, Kimi, Codex, Osaurus, Hermes, and Vibe. This is the file that turns the repo from "content library" into "content build system."

**5. Distribution and demonstration layer**  
[`integrations`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations) is the distribution surface, while [`examples/README.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/examples/README.md) and files like [`examples/nexus-spatial-discovery.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/examples/nexus-spatial-discovery.md) are the narrative proof layer. They show how the maintainers want users to imagine these agents working together.

### Request / data / control flow
1. A maintainer authors or edits an agent file such as [`engineering/engineering-ai-engineer.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering/engineering-ai-engineer.md).
2. Division metadata is reconciled through [`divisions.json`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json), which distinguishes source divisions from output-only or support folders.
3. Validation scripts in [`scripts`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts) check structure and prompt hygiene.
4. [`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh) reads fields like name and description, extracts the body, slugifies names, and writes target files into [`integrations`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations).
5. Example outputs in [`examples`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/examples) show the intended orchestration story for end users.

## Key directories and files
- [`divisions.json`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json): source-of-truth taxonomy plus repo contract notes.
- [`engineering/engineering-ai-engineer.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering/engineering-ai-engineer.md): representative canonical agent file.
- [`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh): the key build step.
- [`scripts/lib.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/lib.sh): shared field/body parsing helpers for the conversion pipeline.
- [`scripts/check-divisions.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/check-divisions.sh): structural integrity guard.
- [`integrations/codex`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations/codex) and [`integrations/openclaw`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations/openclaw): concrete output surfaces.
- [`examples/README.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/examples/README.md): explanation of the orchestration layer.

## Important components
The most important component is [`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh). It is the reason this repo deserves study instead of dismissal.

The second is [`divisions.json`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json). It gives the library an explicit ontology rather than letting top-level folders become accidental product design.

The third is the canonical agent corpus, especially representative files like [`engineering/engineering-ai-engineer.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering/engineering-ai-engineer.md). Those files are the product, and everything else exists to validate or distribute them.

The fourth is the generated output tree under [`integrations`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations). That proves the maintainers are optimizing for installability across ecosystems, not just for GitHub browsing.

## Important knobs / configs / extension points
- [`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh): `--tool`, `--out`, `--parallel`, and `--jobs` control output targeting and build concurrency.
- [`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh): `AGENT_DIRS` defines which source divisions are compiled.
- [`divisions.json`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json): division labels, icons, and colors define the catalog identity and constrain what counts as a division.
- [`engineering/engineering-ai-engineer.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering/engineering-ai-engineer.md): frontmatter fields like `name`, `description`, `color`, and `vibe` are the schema surface that downstream converters consume.

## Practical questions and answers
**Is this really a software project or mostly a prompt library?**  
It is both, but the software part is narrow and important. The source assets are prompt files, yet the repo becomes a real engineering artifact because [`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh) and the validation scripts make those prompts buildable and distributable.

**Where should a builder start reading?**  
Start with [`divisions.json`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json), then [`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh), then one representative source prompt like [`engineering/engineering-ai-engineer.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering/engineering-ai-engineer.md), and only then browse [`integrations`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations).

**What is the most reusable idea here?**  
Treat prompt definitions as canonical source objects with a conversion pipeline. That is much more maintainable than manually keeping separate prompt packs for Codex, Cursor, OpenClaw, Gemini CLI, and other hosts.

**What would fail first in production?**  
Semantic drift across hosts. The repo can generate many output formats, but a long instruction document like [`engineering/engineering-ai-engineer.md`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/engineering/engineering-ai-engineer.md) will not behave identically across every runtime named in [`scripts/convert.sh`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/scripts/convert.sh).

## What is smart
- Keeping one canonical source prompt per agent instead of forking per host.
- Using [`divisions.json`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json) as an explicit catalog registry rather than relying on folder names alone.
- Shipping generated outputs for many ecosystems under [`integrations`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/integrations) so the repo is immediately useful.
- Adding validation scripts so the library does not decay into a random archive of prompts.

## What is flawed or weak
- The core asset is prose, so correctness is much harder to test than code correctness.
- The conversion layer can normalize syntax, but it cannot guarantee consistent behavior across tools with different system-prompt semantics.
- The repo is heavily invested in large instruction bodies, which makes maintenance expensive and raises the risk of subtle duplication or drift.
- The example layer in [`examples`](https://github.com/msitarzewski/agency-agents/tree/ebe9c99acb5c96f9468de368d8bead775387d1a7/examples) is compelling but still narrative; it is not the same as a reproducible benchmark suite.

## What we can learn / steal
- Use a canonical Markdown-plus-frontmatter schema for agent definitions.
- Add a registry file like [`divisions.json`](https://github.com/msitarzewski/agency-agents/blob/ebe9c99acb5c96f9468de368d8bead775387d1a7/divisions.json) so the catalog has explicit structure.
- Build adapters from source prompts into each host format instead of maintaining many slightly different copies.
- Treat prompt distribution as a packaging problem with validation, not just as a copywriting exercise.

## How we could apply it
If we ever build our own shared agent catalog, I would copy the overall shape here: one canonical definition format, one registry for categories and metadata, one converter layer for target platforms, and a small set of validation scripts. I would add stronger behavioral evaluation than this repo currently shows, but the structural pattern is solid.

## Bottom line
`agency-agents` is worth studying because it pushes prompt libraries one step closer to software supply chains. The repo's real idea is not "many agents." The real idea is "one canonical source corpus, many generated host adapters."

The builder lesson is that agent catalogs become more durable when you treat prompt text like source code with taxonomy, validation, and build outputs, even if the last mile of behavior is still much fuzzier than normal software.
