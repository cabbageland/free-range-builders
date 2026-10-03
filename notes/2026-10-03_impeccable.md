# Impeccable

- Repo: pbakaus/impeccable
- URL: https://github.com/pbakaus/impeccable
- Date: 2026-10-03
- Repo snapshot studied: main at e103efe779e2dd01274dabae83531fef00bf2563
- Why picked today: It was near the top of GitHub daily trending with 705 stars today and about 74.9k total stars. It is also a useful specimen: not just another prompt pack, but a cross-agent design skill, native detector engine, live-browser workflow, hooks, plugins, and distribution system in one repo.

## Executive summary

Impeccable is a design-quality layer for AI coding agents. The public pitch in the [README](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/README.md) says "1 skill, 24 commands, live browser iteration, and 61 deterministic detector rules," but the repo is more interesting than that slogan. It packages design taste as a portable agent skill, then backs that taste with a Rust binary that can install skills into many harnesses, scan UI source and rendered pages for recurring AI-design anti-patterns, run hooks after edits, and support a live browser variant loop.

The best builder lesson is the shape: subjective craft rules are treated as productized infrastructure. The [skill/SKILL.src.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/SKILL.src.md) file defines the agent-facing behavior; [skill/reference/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference) splits command playbooks into durable references; [crates/detect](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates/detect) and [crates/html](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates/html) make part of the taste executable; [scripts/build.js](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/scripts/build.js) fans the same source into Claude, Codex, Cursor, Gemini, Copilot, Grok, and other provider layouts.

## What they built

They built an agent-facing frontend design operating system. At the top, the user invokes `/impeccable` commands such as `init`, `shape`, `critique`, `audit`, `polish`, `harden`, `layout`, `typeset`, `animate`, `live`, and `generate`; the canonical command table lives in [skill/SKILL.src.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/SKILL.src.md). Under that, each command routes to a reference file such as [skill/reference/init.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference/init.md), [skill/reference/audit.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference/audit.md), [skill/reference/live.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference/live.md), or [skill/reference/generate.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference/generate.md).

The repo also ships a binary engine. The Node package in [package.json](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/package.json) is mostly an installer and shim; optional platform packages carry the native engine. The main Rust router in [crates/cli/src/main.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/cli/src/main.rs) dispatches verbs like `detect`, `skills`, `context`, `doctor`, `component-review`, `hook`, `hooks`, and every `live*` command.

## Why it matters

Most "AI design" repos are advice documents. This one tries to make taste operational: a prompt contract, a command vocabulary, a local product-context file, deterministic checks, per-edit hooks, screenshots and browser workflows, and provider-specific packaging. That is a stronger pattern for any AI-agent product: do not rely on one giant instruction blob. Split the system into authored guidance, machine-verifiable rules, setup state, install targets, and testable runtime tools.

The suspicious part is also important. Design quality cannot be fully linted, and some detector rules can become fashion police. But the project makes a serious bet that common failure modes are repetitive enough to catch cheaply. The rules in [crates/live/assets/antipatterns.json](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/live/assets/antipatterns.json) include concrete tells like nested cards, gradient text, AI color palettes, low contrast, hidden content, broken images, script errors, overused fonts, and layout overflow.

## Repo shape at a glance

- [skill/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/skill) is the canonical source skill: the [SKILL.src.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/SKILL.src.md) router, [reference/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference) playbooks, [agents/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/skill/agents) helper-agent prompts, and [scripts/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/skill/scripts) launcher/runtime assets.
- [crates/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates) is the native engine: CLI dispatch, skill installer, context manager, detector, HTML scanner, hook runner, live browser server, component review, browser capture, and support crates.
- [scripts/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/scripts) is the release/build layer. [scripts/build.js](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/scripts/build.js) turns one source tree into provider-specific dist folders, plugins, VS Code extension bits, zips, and count validation.
- [plugin/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/plugin), [cursor-plugin/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/cursor-plugin), [extension/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/extension), and provider directories such as [.claude/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/.claude), [.cursor/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/.cursor), [.github/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/.github), and [.agents/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/.agents) are generated or staged distribution surfaces.
- [ui/component-review/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/ui/component-review) is a front-end review interface with model, layout, review, and viewport modules.
- [tests/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/tests) is unusually broad for a skill repo: plugin tests, hook tests, live e2e tests, oracle tests, skill-behavior harnesses, workflow tests, and packaging tests.

## Layered architecture dissection

### High-level system shape

The system has four layers.

First is the instruction layer: [skill/SKILL.src.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/SKILL.src.md) defines when the skill applies, how setup works, command routing, modes, and design principles. The individual references in [skill/reference/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference) keep each workflow scoped instead of forcing the agent to carry every rule at once.

Second is the local runtime layer. [crates/cli/src/main.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/cli/src/main.rs) is the verb router. [crates/context](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates/context) owns product/design context, command metadata, surface briefs, palettes, and doctor-style checks. [crates/skills](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates/skills) owns install/update/link behavior.

Third is the detection and feedback layer. [crates/detect/src/cli.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/detect/src/cli.rs) exposes `impeccable detect`, with JSON/text output, scopes, viewport, config, inline ignores, advisory findings, and clear exit status semantics. [crates/html](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates/html) handles static HTML/CSS analysis; [crates/browser](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates/browser) plugs in browser-based URL scanning through the CLI router.

Fourth is live iteration. [crates/live](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates/live) contains server state, live boot, live generate, live accept, polling, browser assets, Svelte integration, source locking, manifests, and accepted-edit verification. The [crates/live/src/live_generate.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/live/src/live_generate.rs) command is especially revealing: it can target a DOM element by selector, connect to or open a browser, fire a generation session, then hand the agent structured follow-up instructions.

### Main layers

The authoring layer is markdown-first, but it is not loose prose. The [SKILL.src.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/SKILL.src.md) frontmatter declares allowed tools, invocation metadata, and command behavior. The playbooks in [skill/reference/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference) break apart workflows such as `craft`, `audit`, `polish`, `component-review`, and platform-specific `adapt.native`.

The engine layer is Rust-heavy. [crates/cli](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates/cli) decides which crate handles a command. [crates/foundation](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates/foundation) carries shared rule registry, findings, pages, colors, fonts, and JS compatibility utilities. [crates/core](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates/core) and [crates/html](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates/html) are the detector guts.

The provider layer turns the same idea into many harness-specific installs. [crates/skills/src/providers.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/skills/src/providers.rs) enumerates provider directories and aliases: `.claude`, `.cursor`, `.agents`, `.agent`, `.github`, `.grok`, `.hermes`, `.opencode`, `.pi`, `.qoder`, `.trae`, `.vibe`, and others. [scripts/lib/transformers/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/scripts/lib/transformers) is the JavaScript side of the same transformation pipeline.

### Request / data / control flow

A normal project flow starts with `/impeccable init`, which writes durable product context; the instruction for that is routed from [skill/SKILL.src.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/SKILL.src.md) to [skill/reference/init.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference/init.md). A later command loads context through the launcher in [skill/scripts/impeccable](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/scripts/impeccable), follows the relevant reference, edits the UI, and can then run detector or live-browser checks.

For detection, a target path or URL enters `impeccable detect`, dispatched by [crates/cli/src/main.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/cli/src/main.rs) into [crates/detect/src/cli.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/detect/src/cli.rs). That code expands targets, loads config and design-system context, applies inline ignores, chooses static or browser scanning, groups findings by file, separates advisory findings, and reports exit code 0, 1, or 2 according to scan status.

For hooks, an agent edit event enters [crates/hook/src/hook.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/hook/src/hook.rs). The hook normalizes the harness event, resolves target files, skips sensitive/generated/native-platform paths, applies config, and scans eligible UI files. This is the automation bridge between "advice" and "your agent will get nudged immediately after editing a bad UI file."

## Key directories and files

- [README.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/README.md): concise product pitch, install methods, provider list, and the "1 skill / 24 commands / 61 rules" claim.
- [package.json](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/package.json): Node package facade, binary mapping to [cli/bin/cli.js](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/cli/bin/cli.js), platform optional dependencies, and test/release scripts.
- [scripts/build.js](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/scripts/build.js): the build orchestrator for provider transforms, plugin staging, extension staging, zips, version validation, manifest validation, and count generation.
- [crates/cli/src/main.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/cli/src/main.rs): the native engine's command router and the cleanest entry point for understanding the runtime.
- [crates/detect/src/cli.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/detect/src/cli.rs): detector CLI contract, output semantics, advisory section, config flags, and target expansion.
- [crates/live/assets/antipatterns.json](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/live/assets/antipatterns.json): human-readable rule registry for the AI-design anti-patterns.
- [crates/hook/src/hook.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/hook/src/hook.rs): post-edit hook event processing and scan-target filtering.
- [crates/live/src/live_generate.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/live/src/live_generate.rs): a concrete example of browser-connected agent workflow orchestration.
- [plugin/skills/impeccable/SKILL.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/plugin/skills/impeccable/SKILL.md) and [cursor-plugin/skills/impeccable/SKILL.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/cursor-plugin/skills/impeccable/SKILL.md): packaged variants for plugin ecosystems.
- [extension/manifest.json](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/extension/manifest.json): VS Code/GitHub Copilot distribution surface, with popup, devtools, offscreen, content, and background files under [extension/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/extension).

## Important components

The command router in [skill/SKILL.src.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/SKILL.src.md) is the center of the agent experience. It chooses a reference file, defines setup, decides when `init` is required, and gives commands a shared vocabulary.

The provider registry in [crates/skills/src/providers.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/skills/src/providers.rs) is the center of distribution. It makes "install into many AI harnesses" a first-class problem, with aliases, display names, input order, home-directory rules, and provider-specific global skill locations.

The detector CLI in [crates/detect/src/cli.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/detect/src/cli.rs) is the center of enforcement. It is careful about stdout/stderr split, JSON mode, advisory findings, config bypasses, and inline ignore comments, which is the kind of operational detail that makes a linter usable instead of merely correct.

The live workflow in [crates/live/src/live_generate.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/live/src/live_generate.rs) is the center of the interactive story. It treats the browser as a session host with leased events and explicit follow-up instructions, not just a screenshot generator.

## Important knobs / configs / extension points

The obvious knobs are the command references under [skill/reference/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference): each file changes one slice of agent behavior without rewriting the whole skill.

Detector users get runtime knobs through `impeccable detect`, defined in [crates/detect/src/cli.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/detect/src/cli.rs): `--json`, `--quiet`, `--scope`, `--viewport`, `--no-config`, `--no-inline-ignores`, `--no-design-system`, and `--no-advisory`. Project-level ignores and design-system behavior come from `.impeccable/config.json` and `.impeccable/config.local.json`, which the detector code names directly.

Installer extension points sit in [crates/skills/src/providers.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/skills/src/providers.rs) and [scripts/lib/transformers/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/scripts/lib/transformers). Adding a provider is partly filesystem convention, partly transform semantics, and partly hook-manifest support.

The hook system exposes user-facing controls through `impeccable hooks`, routed in [crates/cli/src/main.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/cli/src/main.rs) and documented in [skill/reference/hooks.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference/hooks.md): on/off/status, ignored rules, ignored files, ignored values, and reset.

## Practical questions and answers

Q: Is this mainly prompts?  
A: No. The prompts are the front door, but the meaningful structure is the combination of [skill/SKILL.src.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/SKILL.src.md), native runtime crates under [crates/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates), provider transforms in [scripts/build.js](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/scripts/build.js), and detector rules in [crates/live/assets/antipatterns.json](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/live/assets/antipatterns.json).

Q: Where would it fail?  
A: It can overgeneralize taste. A rule like "overused font" in [antipatterns.json](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/live/assets/antipatterns.json) may be right for AI-generated SaaS sameness and wrong for a brand with an established type system. The project mitigates that with design-system context, advisory findings, and inline ignores, but teams still need judgment.

Q: What makes the engineering credible?  
A: The tests and contracts. There are dedicated tests for plugin manifests, version drift, hooks, browser sessions, live flows, workflow behavior, and release machinery under [tests/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/tests), plus Rust tests inside many [crates/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/crates).

Q: What would I copy first?  
A: The layered approach: one canonical source skill, command-specific references, provider transforms, a native runtime with clear CLI semantics, and a detector that supports local config and inline ignores.

## What is smart

The smartest move is keeping the agent instruction layer and enforcement layer separate. [skill/SKILL.src.md](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/skill/SKILL.src.md) can be opinionated and aspirational; [crates/detect/src/cli.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/detect/src/cli.rs) has to be boring, stable, parseable, and automation-safe.

The second smart move is treating provider distribution as a core system. The provider constants in [crates/skills/src/providers.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/skills/src/providers.rs) and build transforms in [scripts/lib/transformers/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/scripts/lib/transformers) acknowledge that the agent market is fragmented. A good skill that only works in one harness has a much smaller learning surface.

The third smart move is making hooks always exit cleanly while still returning structured audit data. [crates/hook/src/hook.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/hook/src/hook.rs) is built for real agent event streams, including malformed input, recursion depth, disabled env flags, sensitive paths, generated paths, native platforms, quiet mode, and deduping.

## What is flawed or weak

The repo has a lot of surface area. The top-level tree includes source, generated provider folders, plugin staging folders, browser extension code, UI code, native crates, tests, and examples. That makes it easy to study but potentially hard to maintain. The build script in [scripts/build.js](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/scripts/build.js) is doing substantial orchestration and validation work.

The detector rules are inherently culturally timed. "AI slop" tells change as models and trends change. The project partly solves this by keeping the rules explicit in [crates/live/assets/antipatterns.json](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/live/assets/antipatterns.json), but any team using this seriously should expect to prune, override, or fork rules.

The live-browser workflow is powerful but operationally delicate. [crates/live/src/live_generate.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/live/src/live_generate.rs) has to reason about dev servers, harness browsers, browser-open failures, connected overlays, selectors, leases, polling, and accept flows. That is the right complexity for the feature, but it is still complexity.

## What we can learn / steal

Steal the "source skill plus compiled distributions" pattern. Write the canonical behavior once, then build provider-specific variants from it, as [scripts/build.js](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/scripts/build.js) does.

Steal the advisory-vs-primary finding split from [crates/detect/src/cli.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/detect/src/cli.rs). It is a good pattern for automation that wants to educate without blocking every nuanced case.

Steal the command-reference decomposition from [skill/reference/](https://github.com/pbakaus/impeccable/tree/e103efe779e2dd01274dabae83531fef00bf2563/skill/reference). A growing skill should not become one unreadable markdown file.

Steal the provider registry approach from [crates/skills/src/providers.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/skills/src/providers.rs). If your agent tool must install into many hosts, make host layouts data, not folklore.

## How we could apply it

For Free Range Builders itself, the reusable idea is "taste as a layered product." A writing-review skill could copy this architecture: a markdown skill with command references, a detector for recurring weak prose patterns, a hook that runs after note edits, a context file that stores audience and voice, and provider transforms for different agent harnesses.

For product work, the most useful slice is the detector contract. A team can build a domain-specific `detect` command with advisory and primary findings, project config, inline ignores, JSON output, and clear exit codes, mirroring [crates/detect/src/cli.rs](https://github.com/pbakaus/impeccable/blob/e103efe779e2dd01274dabae83531fef00bf2563/crates/detect/src/cli.rs), without copying Impeccable's design opinions.

## Bottom line

Impeccable is worth studying because it turns an aesthetic argument into a multi-layer agent product: skill text, references, native runtime, lintable rules, hooks, browser sessions, tests, and packaging. The design opinions may need local calibration, but the architecture is the real prize.
