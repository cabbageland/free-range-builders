# OpenMontage

- Repo: `calesthio/OpenMontage`
- URL: https://github.com/calesthio/OpenMontage
- Date: 2026-06-22
- Repo snapshot studied: `main` @ `9066dcb2e319727789820c5bcd28274695f2a18a`
- Why picked today: It was the top GitHub trending repo when checked, but the real reason to study it is that it is not just "AI makes videos." It is a fairly opinionated control plane for agent-run media production, with explicit manifests, skill layers, tool discovery, and composition runtimes living in one repo.

## Executive summary
OpenMontage is best read as a workflow operating system for AI-assisted video production. The interesting boundary is not "prompt in, MP4 out." The interesting boundary is the stack split between declarative pipeline contracts in [`pipeline_defs/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs), orchestration helpers in [`lib/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/lib), provider-capability discovery in [`tools/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/tools), and actual render surfaces in [`remotion-composer/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/remotion-composer).

The most reusable idea is the repo's governance shape. [`lib/pipeline_loader.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/lib/pipeline_loader.py) does not merely read YAML. It validates every pipeline manifest against [`schemas/pipelines/pipeline_manifest.schema.json`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/schemas/pipelines/pipeline_manifest.schema.json), exposes stage order, required tools, review focus, sub-stages, and extension permissions, and turns "agent workflow" into something inspectable instead of folklore. [`tools/tool_registry.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/tools/tool_registry.py) then makes tool availability, provider grouping, stability, and fallbacks first-class runtime data.

The caution is that the repo is already sprawling. It wants to be a pipeline DSL, a capability registry, a skill encyclopedia, a composition library, a provider integration layer, and a QA framework at once. The architecture is more disciplined than the marketing copy, but the maintenance surface is large enough that drift between manifests, skills, tool contracts, and runtime behavior is the central long-term risk.

## What they built
They built a multi-layer production stack rather than a single video generator:

- [`pipeline_defs/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs) defines named production workflows such as [`documentary-montage.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs/documentary-montage.yaml), [`animation.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs/animation.yaml), and [`character-animation.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs/character-animation.yaml)
- [`skills/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/skills) provides the project-specific stage-director instructions that explain how those pipelines should actually be executed
- [`tools/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/tools) contains concrete provider and local-runtime integrations grouped by capability family
- [`remotion-composer/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/remotion-composer) contains the checked-in React composition runtime for the actual final render surface
- [`lib/playbook_generator.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/lib/playbook_generator.py) adds a style/playbook layer so the agent can derive palette, typography, motion, and audio defaults instead of hardcoding one look

So the repo is less "video model" and more "agentic production framework with pluggable media tools."

## Why it matters
Most agentic media repos collapse into prompt wrappers around third-party APIs. OpenMontage is more serious because it tries to make the production policy visible in source.

That matters for three reasons:

1. The repo encodes workflow as data, not only as prose. Pipeline manifests define stages, approvals, artifacts, tool availability, review criteria, and extension permissions.
2. The tool layer is capability-aware. Instead of hardcoding one TTS or one video provider, the registry groups tools by capability, provider, tier, stability, and availability.
3. The render layer is separate from the orchestration layer. The system can discuss budgets, approvals, and scene planning in one part of the repo while actual compositions stay in a dedicated runtime package.

## Repo shape at a glance
The top-level shape is more coherent than the "52 tools, 500+ skills" pitch suggests:

- [`README.md`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/README.md), the high-level product map and runtime overview
- [`config.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/config.yaml), global LLM, budget, checkpoint, and output defaults
- [`lib/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/lib), orchestration helpers, manifest loading, scoring, review logic, and playbook generation
- [`pipeline_defs/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs), the declarative workflow layer
- [`schemas/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/schemas), the contract layer that keeps pipeline and style artifacts schema-valid
- [`skills/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/skills), the project-specific "how to execute this stage" knowledge
- [`tools/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/tools), capability families such as audio, graphics, subtitle, video, capture, analysis, and publishers
- [`remotion-composer/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/remotion-composer), the checked-in composition app with reusable scenes and components
- [`tests/`](https://github.com/calesthio/OpenMontage/tree/9066dcb2e319727789820c5bcd28274695f2a18a/tests), split by contracts, pipelines, QA, styles, tools, and evaluation

This shape says the repo is trying to act like an internal media platform, not a one-shot demo.

## Layered architecture dissection
### High-level system shape
The cleanest reading of the architecture is:

1. a pipeline manifest chooses the production contract,
2. skill documents explain how each stage should behave,
3. the registry discovers tools that can satisfy the stage,
4. render runtimes like Remotion execute the final composition,
5. checkpoint and review rules constrain the agent so it does not improvise blindly.

### Main layers
**1. Declarative workflow layer**
[`lib/pipeline_loader.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/lib/pipeline_loader.py) is the key file here. It loads manifests, validates them against schema, exposes ordered stages, and extracts required tools and skills. This is the repo's strongest architectural move: workflow shape is introspectable Python data, not only prompt text.

**2. Pipeline contract layer**
[`pipeline_defs/documentary-montage.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs/documentary-montage.yaml) shows the intended contract clearly: orchestration mode, revision caps, extension permissions, required skills, per-stage artifacts, tool availability, checkpoint behavior, and success criteria. The YAML is not decorative. It is the repo's operational constitution.

**3. Knowledge / skill layer**
[`skills/INDEX.md`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/skills/INDEX.md) documents a three-layer model: registry/tool facts, project-specific skills, and generic lower-level technology skills. That makes the repo less dependent on one giant system prompt and more dependent on named capability surfaces.

**4. Capability discovery layer**
[`tools/tool_registry.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/tools/tool_registry.py) auto-discovers tool modules, groups them by tier, provider, capability, and status, and exposes `support_envelope()`, `capability_catalog()`, and `provider_menu()` reports. This is builder-useful because it turns "what can the system do right now?" into a queryable interface instead of a stale README paragraph.

**5. Style and playbook layer**
[`lib/playbook_generator.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/lib/playbook_generator.py) generates schema-valid custom style playbooks from mood, tone, colors, fonts, and pace. That is a notable choice: the system treats visual identity as a first-class artifact rather than burying it inside scene prompts.

**6. Render runtime layer**
[`remotion-composer/src/Root.tsx`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/remotion-composer/src/Root.tsx) is the checked-in scene catalog: `Explainer`, `CinematicRenderer`, `TalkingHead`, `TitledVideo`, `ProductReveal`, and others. [`render_demo.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/render_demo.py) makes the runtime concrete by rendering JSON-driven demo fixtures instead of relying only on theory.

### Request / data / control flow
The best concrete path is the documentary montage pipeline:

1. [`documentary-montage.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs/documentary-montage.yaml) defines stages `idea -> scene_plan -> assets -> edit -> compose`.
2. Each stage names its required incoming artifacts, produced artifacts, available tools, checkpoint rules, and review focus.
3. The assets stage can route through `direct_clip_search`, `corpus_builder`, `clip_search`, and `music_gen`, which means the retrieval strategy is declared up front rather than improvised mid-run.
4. The compose stage hard-locks `video_compose` and explicitly warns against silent runtime swaps away from Remotion before end-tag parity lands.
5. Global defaults in [`config.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/config.yaml) then govern budgets, approvals, output codec, resolution, and checkpoint behavior across pipelines.

## Key directories and files
- [`README.md`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/README.md), high-level system map and free-vs-paid runtime positioning
- [`config.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/config.yaml), the global operating policy
- [`lib/pipeline_loader.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/lib/pipeline_loader.py), manifest loading and schema enforcement
- [`lib/playbook_generator.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/lib/playbook_generator.py), custom style artifact generation
- [`pipeline_defs/documentary-montage.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs/documentary-montage.yaml), the clearest example of the repo's pipeline contract style
- [`schemas/pipelines/pipeline_manifest.schema.json`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/schemas/pipelines/pipeline_manifest.schema.json), the guardrail behind the YAML layer
- [`skills/INDEX.md`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/skills/INDEX.md), the skill/knowledge architecture
- [`tools/tool_registry.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/tools/tool_registry.py), tool discovery and support-envelope reporting
- [`remotion-composer/src/Root.tsx`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/remotion-composer/src/Root.tsx), composition catalog and theme system
- [`render_demo.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/render_demo.py), the concrete Remotion demo harness

## Important components
**The manifest loader is the real backbone**
The strongest engineering idea in the repo is that a pipeline is a validated contract, not a blob of agent instructions. `load_pipeline`, `get_stage_order`, `get_required_tools`, and `check_extension_permitted` in [`pipeline_loader.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/lib/pipeline_loader.py) make the workflow machine-readable.

**The documentary pipeline shows the repo's serious side**
[`documentary-montage.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs/documentary-montage.yaml) is more convincing than the hero copy because it spells out stage-level review rubrics like corpus size, asset provenance, duration math, end-tag rendering, music mix, and ffprobe validation.

**The registry is better than a hardcoded tool menu**
[`tool_registry.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/tools/tool_registry.py) treats tool discovery as runtime state. That is the right move for agent systems where provider availability changes with environment variables, local installs, and API keys.

**The Remotion catalog makes the system less hand-wavy**
[`Root.tsx`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/remotion-composer/src/Root.tsx) shows this is not merely a planner. There is a checked-in composition runtime with named deliverable types, theme definitions, and concrete reusable scene components.

## Important knobs / configs / extension points
- `budget.mode`, `budget.total_usd`, `budget.reserve_pct`, and `checkpoint.policy` in [`config.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/config.yaml)
- `extensions.custom_scripts`, `extensions.custom_playbooks`, `extensions.custom_skills`, and `extensions.custom_tools` in [`documentary-montage.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs/documentary-montage.yaml)
- `orchestration.budget_default_usd`, `max_revisions_per_stage`, and `max_send_backs` in the same manifest
- runtime capability grouping and fallback resolution in [`tool_registry.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/tools/tool_registry.py)
- custom palette, typography, motion, and audio defaults in [`playbook_generator.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/lib/playbook_generator.py)

## Practical questions and answers
**Is this mostly a provider wrapper, or a real system design?**
It is a real system design. The repo's center of gravity is not any one media API. It is the contract between manifests, skills, registry state, and composition runtime.

**Where does the actual "intelligence" live?**
Mostly in workflow structure and capability mediation, not in one magical algorithm. The manifests encode stage policy, the skills encode project-specific method, and the registry decides what tools exist and whether they are available.

**What should a serious builder read first?**
Read [`README.md`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/README.md), then [`lib/pipeline_loader.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/lib/pipeline_loader.py), then [`pipeline_defs/documentary-montage.yaml`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/pipeline_defs/documentary-montage.yaml), then [`tools/tool_registry.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/tools/tool_registry.py), then [`remotion-composer/src/Root.tsx`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/remotion-composer/src/Root.tsx).

**What is the most reusable pattern here?**
The split between declarative workflow contracts, capability discovery, and concrete render runtimes. That is more portable than any single provider integration.

## What is smart
- Making pipelines schema-valid artifacts instead of vague stage lists.
- Treating extension permissions as an explicit governance surface.
- Auto-discovering tools and exposing runtime support envelopes instead of hand-maintained menus.
- Keeping render compositions in a dedicated runtime package with reusable scene IDs.
- Framing style as its own artifact layer through playbooks rather than hiding it in ad hoc prompts.

## What is flawed or weak
- The repo surface is already wide enough to drift. Manifests, skills, tools, docs, tests, and runtimes all have to stay aligned.
- The playbook generator in [`playbook_generator.py`](https://github.com/calesthio/OpenMontage/blob/9066dcb2e319727789820c5bcd28274695f2a18a/lib/playbook_generator.py) still falls back to fairly generic defaults like Inter-based typography and stock palette templates, which undercuts some of the repo's anti-generic design rhetoric.
- The tool registry is clean, but the actual provider explosion underneath it will be operationally expensive to keep healthy.
- A lot of the repo's value still depends on external services, keys, and runtime setup. The control plane is solid, but the execution plane inherits all the fragility of media APIs and local environment drift.

## What we can learn / steal
- Turn agent workflows into validated data structures.
- Treat capability discovery as runtime state, not documentation.
- Separate orchestration policy from rendering implementation.
- Put budget and approval rules near the pipeline definition instead of in scattered prose.
- Model style and visual language as artifacts with schemas and defaults.

## How we could apply it
If we were building our own agentic production stack, I would copy the architecture more than the feature list:

1. a schema-validated workflow manifest layer,
2. a capability registry that can report live support,
3. a skill/instruction layer mapped to named stages,
4. dedicated render runtimes with concrete scene libraries,
5. budget and approval policy in config instead of in tribal knowledge.

That same pattern would work outside video too. It would translate well to research agents, content pipelines, or any system where tool choice and quality gates matter as much as raw model output.

## Bottom line
OpenMontage is worth studying because it is not merely another "AI video studio" slogan repo. It is a fairly thoughtful attempt to encode agentic production as contracts, capabilities, and render surfaces.

The builder lesson is structural: make the workflow explicit, make the capability envelope queryable, and keep the execution runtime separate from the planning layer. That is the part worth stealing even if you do not care about video generation at all.
