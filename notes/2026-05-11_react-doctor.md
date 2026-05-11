# React Doctor

- Repo: `millionco/react-doctor`
- URL: https://github.com/millionco/react-doctor
- Date: 2026-05-11
- Repo snapshot studied: `main` @ `052cd20aa4a4a6a8caa47ea3348aedbca95f2222`
- Why picked today: It is hot right now, clearly AI-adjacent without being another flimsy wrapper, and it attacks a real 2026 problem: code agents generate React fast, but they also generate a lot of subtle React nonsense. This repo tries to turn that pain into a concrete scanner, score, and workflow.

## Executive summary

[React Doctor](https://github.com/millionco/react-doctor) is a monorepo for a React codebase diagnostic product, not just a lint preset. The core package, [`packages/react-doctor`](https://github.com/millionco/react-doctor/tree/main/packages/react-doctor), combines a large custom static-analysis rule set, an oxlint execution layer, dead-code detection via Knip, framework detection, config merging, scoring, JSON/report formatting, CI wiring, and an agent-skill installer. The separate [`packages/website`](https://github.com/millionco/react-doctor/tree/main/packages/website) package is the marketing and leaderboard site.

The key engineering idea is that they do not sell “yet another ESLint plugin.” They ship an opinionated diagnosis pipeline. The custom rules in [`packages/react-doctor/src/plugin`](https://github.com/millionco/react-doctor/tree/main/packages/react-doctor/src/plugin) are only one layer. Around that layer they added project discovery, rule auto-selection by framework and React version, suppression analysis, report rendering, optional remote score calculation, and GitHub Action packaging via [`action.yml`](https://github.com/millionco/react-doctor/blob/main/action.yml). That full stack is what makes the product feel like a doctor instead of a bag of rules.

## What they built

They built a CLI and embeddable API that scans a React app and produces a health score plus categorized findings across state/effects, correctness, performance, architecture, security, accessibility, server patterns, React Native, Next.js, TanStack, and dead code. The user entrypoint is the CLI in [`packages/react-doctor/src/cli.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/cli.ts), while the main orchestration engine lives in [`packages/react-doctor/src/scan.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/scan.ts).

They also built two distribution surfaces around the scanner. First, a GitHub Actions wrapper in [`action.yml`](https://github.com/millionco/react-doctor/blob/main/action.yml) that can annotate PRs and post score-bearing comments. Second, an agent-facing installation path in [`packages/react-doctor/src/install-skill.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/install-skill.ts), which copies bundled agent skills so coding agents learn the rule set before they write bad React.

## Why it matters

This matters because it packages a broad set of senior-review heuristics into something operational. Most teams already know that effects are abused, render paths are wasteful, framework conventions get violated, and dead code accumulates. The hard part is turning that into a low-friction, one-command artifact that developers and agents will actually run. React Doctor’s real product is the combination of breadth, packaging, and defaults.

It is also a useful signal about where tooling is going. The repo assumes code review is shifting from “read every line manually” toward “run strong automated taste checks, then focus humans on the weird parts.”

## Repo shape at a glance

At the top level this is a small pnpm monorepo defined by [`pnpm-workspace.yaml`](https://github.com/millionco/react-doctor/blob/main/pnpm-workspace.yaml) and root metadata in [`package.json`](https://github.com/millionco/react-doctor/blob/main/package.json).

The important top-level areas are:

- [`packages/react-doctor`](https://github.com/millionco/react-doctor/tree/main/packages/react-doctor): the actual product, including CLI, API, oxlint plugin export, ESLint plugin export, scan orchestration, scoring, config loading, ignore handling, agent-skill installation, and utility layers.
- [`packages/react-doctor/src/plugin`](https://github.com/millionco/react-doctor/tree/main/packages/react-doctor/src/plugin): the custom static-analysis engine surface, especially the rule registry in [`index.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/index.ts) and rule families under [`rules/`](https://github.com/millionco/react-doctor/tree/main/packages/react-doctor/src/plugin/rules).
- [`packages/react-doctor/src/utils`](https://github.com/millionco/react-doctor/tree/main/packages/react-doctor/src/utils): the glue code that makes this a product rather than a plugin, including oxlint execution in [`run-oxlint.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-oxlint.ts), dead-code execution in [`run-knip.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-knip.ts), project discovery in [`discover-project.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/discover-project.ts), config loading in [`load-config.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/load-config.ts), and score/report builders.
- [`packages/website`](https://github.com/millionco/react-doctor/tree/main/packages/website): a separate Next 16 + React 19 site package for the product site and leaderboard.
- [`action.yml`](https://github.com/millionco/react-doctor/blob/main/action.yml): the CI distribution layer.
- [`skills/react-doctor`](https://github.com/millionco/react-doctor/tree/main/skills/react-doctor) and bundled skill artifacts under [`packages/react-doctor/dist/skills`](https://github.com/millionco/react-doctor/tree/main/packages/react-doctor/dist): the agent-instruction channel.

Structurally, this is not “website plus library.” It is “scanner product plus thin website.” Nearly all of the interesting engineering weight is inside [`packages/react-doctor`](https://github.com/millionco/react-doctor/tree/main/packages/react-doctor).

## Layered architecture dissection

### High-level system shape

The system is a pipeline:

1. CLI/API receives a target directory through [`packages/react-doctor/src/cli.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/cli.ts) or [`packages/react-doctor/src/index.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/index.ts).
2. Scan orchestration in [`packages/react-doctor/src/scan.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/scan.ts) discovers project shape, merges config, selects scope, and coordinates checks.
3. Lint analysis runs through [`packages/react-doctor/src/utils/run-oxlint.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-oxlint.ts), which wires in the custom plugin and maps rules into product categories.
4. Dead-code analysis runs through [`packages/react-doctor/src/utils/run-knip.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-knip.ts).
5. Diagnostics are merged, filtered, suppression-aware, and scored.
6. Output is rendered as terminal UX, JSON, API objects, or GitHub Action comments.

### Main layers

**Interface layer.** The user-facing interfaces are the CLI in [`packages/react-doctor/src/cli.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/cli.ts), the programmatic API exported from [`packages/react-doctor/src/index.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/index.ts), and the GitHub Action in [`action.yml`](https://github.com/millionco/react-doctor/blob/main/action.yml).

**Discovery and config layer.** Project fingerprinting and option resolution happen in files like [`packages/react-doctor/src/utils/discover-project.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/discover-project.ts), [`packages/react-doctor/src/utils/load-config.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/load-config.ts), [`packages/react-doctor/src/utils/resolve-lint-include-paths.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/resolve-lint-include-paths.ts), and [`packages/react-doctor/src/utils/select-projects.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/select-projects.ts).

**Rule engine layer.** The rule registry in [`packages/react-doctor/src/plugin/index.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/index.ts) aggregates sixteen domain rule families from [`packages/react-doctor/src/plugin/rules`](https://github.com/millionco/react-doctor/tree/main/packages/react-doctor/src/plugin/rules), including [`state-and-effects.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/rules/state-and-effects.ts), [`performance.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/rules/performance.ts), [`nextjs.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/rules/nextjs.ts), and [`react-native.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/rules/react-native.ts).

**Execution adapters.** They do not write their own parser/runtime from scratch. They adapt oxlint through [`packages/react-doctor/src/utils/run-oxlint.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-oxlint.ts) and adapt Knip through [`packages/react-doctor/src/utils/run-knip.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-knip.ts).

**Presentation and scoring layer.** Terminal summaries, category grouping, share URLs, JSON reports, and score generation are built in [`packages/react-doctor/src/scan.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/scan.ts), [`packages/react-doctor/src/utils/build-json-report.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/build-json-report.ts), and [`packages/react-doctor/src/utils/calculate-score.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/calculate-score.ts).

**Distribution layer.** Packaging for agents and CI sits in [`packages/react-doctor/src/install-skill.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/install-skill.ts), [`skills/react-doctor`](https://github.com/millionco/react-doctor/tree/main/skills/react-doctor), and [`action.yml`](https://github.com/millionco/react-doctor/blob/main/action.yml).

### Request / data / control flow

The main control flow starts in [`packages/react-doctor/src/scan.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/scan.ts). It discovers framework and React version, determines whether diff mode is active, resolves a Node binary that oxlint can actually use, then launches lint and dead-code checks in parallel. The lint branch calls [`packages/react-doctor/src/utils/run-oxlint.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-oxlint.ts), where diagnostics from oxlint and adopted lint configs get normalized into React Doctor’s category model. The dead-code branch calls [`packages/react-doctor/src/utils/run-knip.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-knip.ts), where Knip output is translated into the same diagnostic shape.

Those diagnostic streams are merged back in [`packages/react-doctor/src/scan.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/scan.ts), scored, optionally uploaded for shareable score behavior, and finally rendered to terminal or serialized to JSON.

The clever part is that the repo is built around normalization. Different analyzers, framework detectors, config sources, and output surfaces all get funneled into one internal diagnostic model.

## Key directories and files

- [`packages/react-doctor/src/scan.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/scan.ts): the core conductor. If you want to understand the product, start here.
- [`packages/react-doctor/src/plugin/index.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/index.ts): the full rule registry and the clearest map of product ambition.
- [`packages/react-doctor/src/plugin/rules/state-and-effects.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/rules/state-and-effects.ts): a representative heavyweight rule file, full of AST heuristics and React-specific judgment.
- [`packages/react-doctor/src/utils/run-oxlint.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-oxlint.ts): the oxlint adapter and diagnostic categorizer.
- [`packages/react-doctor/src/utils/run-knip.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-knip.ts): the dead-code adapter with practical retry and noise-suppression logic.
- [`packages/react-doctor/src/install-skill.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/install-skill.ts): the agent integration path, which is more important to the product story than it first appears.
- [`packages/react-doctor/src/oxlint-config.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/oxlint-config.ts): the place where rules become a coherent scanning preset.
- [`action.yml`](https://github.com/millionco/react-doctor/blob/main/action.yml): the CI surface that turns a local CLI into a team workflow.
- [`packages/website/src/app`](https://github.com/millionco/react-doctor/tree/main/packages/website/src/app): the Next app shell for the site and leaderboard.

## Important components

The most important component is the scanner orchestration in [`packages/react-doctor/src/scan.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/scan.ts). It handles user experience, fallback behavior, scoring, and the practical ugliness of real projects.

The second important component is the rule registry in [`packages/react-doctor/src/plugin/index.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/index.ts). This file reveals the breadth of the product far better than the README does. The project spans React correctness, JS micro-performance, framework policy, design taste, server boundaries, and React Native.

The third important component is the AST helper machinery spread across [`packages/react-doctor/src/plugin/helpers.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/helpers.ts) and the large rule files like [`packages/react-doctor/src/plugin/rules/state-and-effects.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/rules/state-and-effects.ts). The comments in those files make it clear they are chasing edge cases, not just checking for toy patterns.

The fourth important component is the packaging glue in [`packages/react-doctor/src/install-skill.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/install-skill.ts) and [`action.yml`](https://github.com/millionco/react-doctor/blob/main/action.yml). This is how they push the rules upstream into CI and even earlier into the agent prompt layer.

## Important knobs / configs / extension points

The main user configuration surface is [`react-doctor.config.json`](https://github.com/millionco/react-doctor/blob/main/README.md#configuration), which the loader in [`packages/react-doctor/src/utils/load-config.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/load-config.ts) resolves. Important knobs include ignore rules, ignore files, override scopes, diff mode, offline mode, inline suppression behavior, and whether to adopt existing lint configuration.

The product also exposes two plugin surfaces: an oxlint plugin export via [`packages/react-doctor/src/eslint-plugin.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/eslint-plugin.ts) and a standalone oxlint plugin export path declared in [`packages/react-doctor/package.json`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/package.json). Those exports let teams either run the full doctor workflow or pull pieces into their own lint stacks.

A subtle but important knob is the framework-aware rule activation in [`packages/react-doctor/src/utils/discover-project.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/discover-project.ts) and [`packages/react-doctor/src/utils/run-oxlint.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-oxlint.ts). They are trying to avoid the usual static-analysis failure mode where every project gets the same noisy preset.

## Practical questions and answers

**Is this mostly a linter?** Yes, but “just a linter” undersells it. The better description is: a lint-and-analysis product with an opinionated diagnosis UX.

**Where is the real moat?** Not the concept of scoring. The moat is the taste encoded in the rule set, the framework-specific defaults, and the packaging across CLI, CI, and coding agents.

**What carries the real implementation weight?** The heavy center of gravity is inside [`packages/react-doctor/src/plugin/rules`](https://github.com/millionco/react-doctor/tree/main/packages/react-doctor/src/plugin/rules), [`packages/react-doctor/src/utils/run-oxlint.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-oxlint.ts), and [`packages/react-doctor/src/scan.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/scan.ts).

**Why is the agent installer interesting?** Because it shifts the product left. Instead of only detecting bad React after code is written, they also try to teach agents the rules before generation via [`packages/react-doctor/src/install-skill.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/install-skill.ts).

**Would this fail in a weird monorepo?** Probably sometimes. They already have monorepo-specific handling in files like [`packages/react-doctor/src/utils/find-monorepo-root.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/find-monorepo-root.ts) and [`packages/react-doctor/src/utils/select-projects.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/select-projects.ts), which is usually a sign the edge cases are real and ongoing.

## What is smart

The smartest decision is architectural: they wrapped analyzers instead of trying to replace them. Oxlint gives them speed, Knip gives them dead-code coverage, and React Doctor adds product opinion on top.

The second smart move is that the rule taxonomy in [`packages/react-doctor/src/plugin/index.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/index.ts) is much broader than “React performance.” They are aiming at full-stack React code health, including server boundaries, security, design linting, accessibility, and framework conventions.

The third smart move is the unusually practical edge-case handling in files like [`packages/react-doctor/src/utils/run-knip.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-knip.ts) and [`packages/react-doctor/src/plugin/rules/state-and-effects.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/rules/state-and-effects.ts). The code comments show they are fighting real false positives and runtime mess, not building a demo.

The fourth smart move is packaging for where modern development actually happens: local CLI, PR checks, and coding agents.

## What is flawed or weak

The biggest weakness is that the scope is starting to sprawl. The rule catalog already covers a huge amount of territory, and broad taste-based static analysis often drifts toward “productized opinions with some false-positive debt.” That may still be a winning trade, but it is a trade.

The second weakness is explainability pressure. Once you scan architecture, design, performance, and agent-generated code all at once, users will want very sharp remediation advice and very low false-positive rates. That is hard to sustain as the rule set grows.

The third weakness is that the score risks becoming the headline while the nuance does the real work. Scores are sticky and marketable, but they can also encourage shallow optimization or cargo-cult cleanup.

The fourth weakness is distribution dependency. The agent-skill path depends on users running an installation flow and on external agent ecosystems staying stable enough for the installer to matter.

## What we can learn / steal

Steal the packaging strategy. If you have strong engineering taste encoded as rules, do not ship it as a raw plugin only. Ship a full workflow with discovery, defaults, formatting, CI, and pre-generation agent integration.

Steal the normalization pattern. Different scanners and detectors should emit one internal diagnostic shape, the way [`packages/react-doctor/src/scan.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/scan.ts) and [`packages/react-doctor/src/utils/run-oxlint.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/utils/run-oxlint.ts) do.

Steal the “comments as battle scars” style in the rule files. The inline notes in [`packages/react-doctor/src/plugin/rules/state-and-effects.ts`](https://github.com/millionco/react-doctor/blob/main/packages/react-doctor/src/plugin/rules/state-and-effects.ts) explain why the heuristic exists, which is exactly what future maintainers need.

## How we could apply it

If we were building internal code health tooling, I would copy the product shape almost directly: a fast local scanner, a CI wrapper, a JSON API, a stable diagnostic schema, and optional agent-facing instructions.

If we were targeting a different domain, like backend reliability or data pipelines, I would especially copy the layer split here: domain-specific rules, execution adapters for best-in-class analyzers, then a product shell that handles scoring, report UX, and integrations.

## Bottom line

React Doctor is more serious than the marketing line suggests. Underneath the meme-friendly pitch is a pretty disciplined product architecture: custom AST rules, analyzer adapters, config/discovery glue, scoring, CI packaging, and agent distribution. The most reusable lesson is not any single rule. It is the decision to treat static analysis as a product surface, not a plugin dump.