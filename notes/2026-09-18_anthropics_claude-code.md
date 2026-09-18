# Claude Code

- Repo: anthropics/claude-code
- URL: https://github.com/anthropics/claude-code
- Date: 2026-09-18
- Repo snapshot studied: main at `31a3b00bef145a0393d9dbf840a98674fec07712`
- Why picked today: It was one of the hottest daily GitHub repos, and unlike a pure product announcement it exposes the plugin, mod, policy, workflow, and example surface around Claude Code. The useful teardown is not "how the closed CLI works"; it is how Anthropic is carving a coding-agent product into installable plugins, built-in mods, enterprise controls, and event hooks.

## Executive summary

[anthropics/claude-code](https://github.com/anthropics/claude-code) is not the full source of the Claude Code terminal agent. It is the public repo around the product: plugin marketplace metadata, bundled plugins, built-in mod source, examples for gateways and managed settings, GitHub workflows, changelog, security docs, and a small set of local Claude commands.

The most interesting source is [mods/diff/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff), a built-in plugin that implements `/diff` as an event-driven pane. It watches session, UI, tool, prompt, command, store, clock, process, filesystem, and telemetry surfaces through one `register(on)` module in [mods/diff/hooks/register.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/register.ts). The lesson is that serious agent UX is becoming a plugin runtime problem: the agent needs policy layers, observable hooks, durable UI state, and deterministic source-control reads around the model.

## What they built

The repo publishes three related things.

First, it is a product distribution and documentation repo with [README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/README.md), [CHANGELOG.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/CHANGELOG.md), [SECURITY.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/SECURITY.md), and operational examples under [examples/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples).

Second, it is a plugin catalog. [.claude-plugin/marketplace.json](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/.claude-plugin/marketplace.json) lists bundled plugins such as [plugins/code-review/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/code-review), [plugins/feature-dev/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/feature-dev), [plugins/frontend-design/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/frontend-design), [plugins/hookify/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/hookify), [plugins/plugin-dev/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/plugin-dev), and [plugins/security-guidance/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/security-guidance).

Third, it exposes built-in mods under [mods/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods). [mods/README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/README.md) says these are complete plugins with TypeScript hooks, tests, and typed contracts. The key built-in mods are [mods/sec-default/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/sec-default), [mods/diff/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff), and [mods/telemetry/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/telemetry).

## Why it matters

The repo matters because it shows what a mature coding-agent product has to make configurable. The LLM is not the whole system. Users need commands, installable workflows, policy defaults, managed settings, hookable events, review agents, security nudges, local UI extensions, and enterprise deployment examples.

[mods/diff/README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/README.md) is the best single example. `/diff` is not a prompt. It is a UI and git subsystem that opens a pane, renders changed files and hunks, refreshes after edits and shell commands, stores per-repository base-mode choices, hides pre-session/noise files until asked, polls HEAD, and can attach a selected file's hunks to the next prompt. That is the kind of deterministic product machinery agent builders should study.

## Repo shape at a glance

- [.claude-plugin/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/.claude-plugin) contains marketplace metadata; [marketplace.json](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/.claude-plugin/marketplace.json) is the catalog index.
- [.claude/commands/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/.claude/commands) contains repo-local Claude commands such as commit, dedupe, and issue triage.
- [.github/workflows/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/.github/workflows) automates issue handling, duplicate closure, mod tests, and lifecycle chores.
- [examples/gateway/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/gateway) has AWS and GCP gateway deployment examples with Docker, Terraform, and sample config.
- [examples/hooks/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/hooks) has hook examples such as [bash_command_validator_example.py](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/examples/hooks/bash_command_validator_example.py).
- [examples/mdm/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/mdm) contains macOS and Windows managed-settings examples, including [managed-settings.json](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/examples/mdm/managed-settings.json).
- [examples/settings/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/settings) shows strict, lax, and bash-sandbox settings profiles.
- [plugins/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins) contains installable user-facing plugins made from commands, agents, hook handlers, scripts, and README files.
- [mods/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods) contains built-in hook modules that ship inside Claude Code.
- [scripts/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/scripts) and [Script/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/Script) support repository and devcontainer workflows.

## Layered architecture dissection

### High-level system shape

The public repository is an extensibility shell around a closed product. The core CLI/runtime is not here, but the public boundary is meaningful: plugins and mods are authored as files, tested as hooks, indexed as marketplace entries, and exercised through the engine's event API.

The repo's central architectural split is between ordinary installable plugins in [plugins/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins) and built-in mods in [mods/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods). Plugins mostly package commands, agents, docs, hook scripts, and workflow instructions. Mods are TypeScript hook modules that can sit inside the runtime and add engine nouns or UI behavior.

### Main layers

The marketplace layer is [.claude-plugin/marketplace.json](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/.claude-plugin/marketplace.json). It gives each bundled plugin a name, description, source path, category, version, and author information. That is the install/discovery contract.

The plugin layer is [plugins/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins). Some plugins are mostly agent-command packs, such as [plugins/pr-review-toolkit/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/pr-review-toolkit) and [plugins/feature-dev/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/feature-dev). Others include executable hooks, such as [plugins/hookify/core/rule_engine.py](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/hookify/core/rule_engine.py) and [plugins/security-guidance/hooks/security_reminder_hook.py](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/security-guidance/hooks/security_reminder_hook.py).

The built-in mod layer is [mods/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods). [mods/README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/README.md) explains the contract: a mod exposes one `register(on, options)` entry, hooks engine events, uses typed contracts under [mods/types/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/types), and is tested with `claude plugin test`.

The most concrete runtime layer is [mods/diff/hooks/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks). It has small modules for ask context, backend probing, classification, command spec, git parsing/probing/tiers, pane state, pane toggles, transcript turn diffs, tools, and views.

### Request / data / control flow

The `/diff` flow starts in [mods/diff/hooks/register.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/register.ts). On `session.start`, `register` binds a host object around engine nouns such as `clock`, `process`, `fs`, `store`, `session`, `ui`, `command`, and `telemetry`, then registers the `/diff` command. On `ui.render` for `PromptHint`, it learns viewport width and fullscreen state. On `command.run` for `diff`, it pins a backend, opens or closes a pane, and persists the user's open/closed preference.

Git access is separated into [mods/diff/hooks/backend/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/backend) and [mods/diff/hooks/git/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/git). [mods/diff/hooks/git/git-backend-of.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/git/git-backend-of.ts) probes the repository once, pins `--git-dir` and `--work-tree`, tracks the dirty-at-start baseline, and exposes `fetchDiff`, `fetchFileHunks`, and `headKeyOf`. [mods/diff/hooks/git/fetch-diff/fetch-diff.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/git/fetch-diff/fetch-diff.ts) refuses transient git states such as merge/rebase/cherry-pick/revert and then dispatches to branch or working-tree tiers.

Rendering flows through [mods/diff/hooks/views/pane-view.tsx](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/views/pane-view.tsx), which chooses a docked sidebar, inline dialog, or "resize terminal" note. State shaping lives in [mods/diff/hooks/pane-state/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/pane-state); [partition-of.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/pane-state/partition-of.ts) sorts files, splits pre-session files, and hides generated/test noise unless the user expands it.

After agent actions, `register.ts` listens to `tool.call` for editing and shell tools, refreshes an open pane, and can auto-open on the first successful edit when the terminal is wide enough. On `prompt.submit`, an armed file's hunks are fitted into prompt context using [mods/diff/hooks/ask/fitted-ask-text-of.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/ask/fitted-ask-text-of.ts). That makes the pane both UI and context-selection mechanism.

## Key directories and files

- [.claude-plugin/marketplace.json](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/.claude-plugin/marketplace.json): bundled plugin catalog.
- [plugins/README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/README.md): entry point for installable plugins.
- [plugins/hookify/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/hookify): a plugin with Python rule engine and hooks, useful as a nontrivial plugin shape.
- [plugins/security-guidance/hooks/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/security-guidance/hooks): hook code for security reminders.
- [mods/README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/README.md): built-in mod architecture and testing contract.
- [mods/diff/.claude-plugin/plugin.json](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/.claude-plugin/plugin.json): plugin metadata for the built-in diff mod.
- [mods/diff/hooks/register.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/register.ts): event registration and runtime state for `/diff`.
- [mods/diff/hooks/git/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/git): repository probing, diff tiers, parse utilities, and hunk fetching.
- [mods/diff/hooks/views/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/views): UI rendering for docked and inline panes.
- [mods/diff/tests/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/tests): hook tests and fixtures for the built-in mod.
- [examples/gateway/aws/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/gateway/aws) and [examples/gateway/gcp/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/gateway/gcp): deployment examples for API gateway use.
- [examples/mdm/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/mdm): managed device configuration for organizations.

## Important components

[mods/diff/hooks/register.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/register.ts) is the spine. It carries in-memory pane state, backend pinning, timers, selected/armed file state, body-load promises, polling state, and UI refresh coalescing. It is long, but the shape is clear: bind host, probe repository, fetch data, draw pane, react to commands/tools/prompts, and clean up on `clear` or `resume`.

[mods/diff/hooks/git/git-backend-of.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/git/git-backend-of.ts) is important because it keeps git boring. It resolves the repository once, pins later git commands with `--git-dir` and `--work-tree`, uses a timeout and locale, and holds a baseline of paths dirty at first fetch.

[mods/diff/hooks/pane-state/partition-of.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/pane-state/partition-of.ts) shows the product taste: pre-session files, test files, and generated files are not ignored, but they are partitioned so the UI can fold them. That is a better default than dumping every noisy changed path in front of the user.

[mods/diff/hooks/turns/turn-diffs-of.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/turns/turn-diffs-of.ts) extracts edited turns from transcript messages. That lets the pane switch between current working tree changes and earlier turn diffs, which is a specifically agent-native affordance.

[mods/diff/hooks/views/pane-view.tsx](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/views/pane-view.tsx) keeps layout decisions centralized: docked sidebar when seated, inline dialog when not fullscreen, and a width warning when fullscreen is too narrow.

## Important knobs / configs / extension points

The most visible extension knob is plugin installation through [.claude-plugin/marketplace.json](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/.claude-plugin/marketplace.json). Each plugin is a folder with a `.claude-plugin/plugin.json` and optional `commands`, `agents`, `hooks`, `scripts`, or README content.

The built-in mod extension point is described in [mods/README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/README.md): a hooks module exports `register(on, options)`, uses event hooks, imports typed engine contracts, and can be tested with the plugin test kit.

For `/diff`, runtime knobs are spread through [mods/diff/hooks/limits/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/limits), [mods/diff/hooks/names/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/names), and pane/base-mode store keys in [mods/diff/hooks/pane-state/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/pane-state). The important product knobs are width thresholds, refresh debounce, body-fetch concurrency, prompt-context maximum, base comparison mode, and whether tests/generated/pre-session files are shown.

Enterprise and deployment knobs live under [examples/mdm/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/mdm), [examples/settings/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/settings), and [examples/gateway/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/gateway). Those examples are not glamorous, but they are exactly what makes an agent adoptable inside real organizations.

## Practical questions and answers

Q: Is this the Claude Code core source?

A: No. The actual core agent runtime is not public here. The public value is the extension boundary: plugin catalog, built-in mods, hook tests, examples, and organizational policy surfaces.

Q: What is the deepest source to read first?

A: Start with [mods/README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/README.md), then [mods/diff/README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/README.md), then [mods/diff/hooks/register.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/register.ts). That path teaches the engine model better than the product README.

Q: What should a builder copy?

A: Copy the event-boundary discipline. `register.ts` does not ask the model to understand git state. It uses deterministic hooks and typed host methods, then gives the model/user a better context surface.

Q: What should a builder distrust?

A: Do not assume the public hook API is stable. [mods/README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/README.md) explicitly says these hooks are early access and may change between releases.

## What is smart

The smartest design move is treating built-in UX as plugins. [mods/diff/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff) is not hardcoded magic in a hidden UI layer; it is structured like a plugin with metadata, hooks, views, tests, and typed contracts.

The second smart move is the host wrapper inside [mods/diff/hooks/register.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/register.ts). It turns the engine's many `$` nouns into a narrow `Host` interface for the mod. That makes the hook logic easier to test and keeps runtime dependencies explicit.

The third smart move is making git reads bounded and pinned in [mods/diff/hooks/git/git-backend-of.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/git/git-backend-of.ts). Agent tools often fail by casually re-reading an unstable working tree. This one freezes enough context to render consistently.

The fourth smart move is the plugin catalog in [.claude-plugin/marketplace.json](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/.claude-plugin/marketplace.json). It shows that useful agent behavior is being productized as installable skills, commands, agents, and hook packs rather than only as model releases.

## What is flawed or weak

The main weakness is obvious: the most interesting runtime is closed. You can inspect the extension surface and built-in mods, but not the scheduler, terminal engine, model loop, permission system, or core tool execution internals.

The second weakness is API churn. [mods/README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/README.md) says the hooks API is early access. Builders can learn patterns from this repo, but copying exact APIs into long-lived tooling would be risky.

The third weakness is complexity. [mods/diff/hooks/register.ts](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks/register.ts) has to juggle UI state, git state, timers, prompt context, transcript history, telemetry, and store preferences. The design is justified for a built-in product feature, but it is too much for most one-off plugins.

## What we can learn / steal

Steal the split between user-installable plugin packs and privileged built-in mods. It gives ordinary users an extension system while reserving deeper engine behavior for code that ships with the product.

Steal the test shape from [mods/README.md](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/mods/README.md): tests answer engine events from memory and assert how the mod responds. Hook systems need this kind of simulator or they become impossible to trust.

Steal the `/diff` idea for agent products: after every successful edit or shell command, show what changed in a durable side surface, and let the user attach a specific file's diff to the next prompt. That workflow is more precise than "look at my changes."

Steal the organizational examples under [examples/mdm/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/mdm) and [examples/settings/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/settings) as a reminder that enterprise agent adoption is a controls problem as much as a model-quality problem.

## How we could apply it

For an internal coding agent, build a first-class extension manifest similar to [.claude-plugin/marketplace.json](https://github.com/anthropics/claude-code/blob/31a3b00bef145a0393d9dbf840a98674fec07712/.claude-plugin/marketplace.json). A plugin should declare its commands, hooks, category, source, author, and version instead of being copied into a loose scripts folder.

For UI features, copy the `diff` mod's architecture: state model, git backend, render views, command spec, tool-event refresh, and prompt-context arm/disarm. The exact code is Claude-specific, but the boundaries in [mods/diff/hooks/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/diff/hooks) are portable.

For security and governance, treat [mods/sec-default/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/mods/sec-default), [plugins/security-guidance/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/plugins/security-guidance), and [examples/mdm/](https://github.com/anthropics/claude-code/tree/31a3b00bef145a0393d9dbf840a98674fec07712/examples/mdm) as three separate layers: protected defaults, user-facing reminders, and managed deployment policy.

## Bottom line

Claude Code's public repo is worth studying because it reveals the non-model product shell around a serious coding agent. The core engine is not open, but the plugin/mod surface is concrete enough to teach good lessons: event hooks beat prompt hacks, git/UI state should be deterministic, and agent products need installable workflows plus enterprise controls to be more than a clever terminal demo.
