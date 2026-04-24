# OSV-Scanner

- Repo: `google/osv-scanner`
- URL: https://github.com/google/osv-scanner
- Date: 2026-04-24
- Repo snapshot studied: `main` @ `123ef8060defa52b3b4b239819866e0ac18f03ca`
- Why picked today: It is hot enough to matter, AI-adjacent only indirectly, but much more worth studying than the usual flimsy prompt-wrapper trend bait. It is also a good example of a security tool that treats repo scanning as a real extraction and analysis pipeline instead of a pile of regexes around lockfiles.

## Executive summary

OSV-Scanner is a serious Go CLI for dependency vulnerability scanning, container scanning, license inspection, guided remediation, GitHub Action reporting, and now an experimental MCP surface. The repo’s strongest idea is that the scanner itself is fairly thin while the hard ecosystem-specific extraction work is pushed down into the [`osv-scalibr`](https://github.com/google/osv-scalibr) plugin system. That gives the project a clean architecture: CLI command layer at the top, scanner orchestration in the middle, extractor and enricher plugins underneath, then output/reporting surfaces on the side.

The key insight is that this is not “just a vulnerability checker.” It is really a translation layer from messy real-world artifacts, lockfiles, repos, git commits, images, and SBOMs into a normalized inventory that can then be matched, filtered, enriched, rendered, and even remediated. That inventory-first design is why the repo feels extensible.

The main weakness is also the cost of that design: a lot of complexity is delegated to plugin resolution, transitive resolution backends, remote services, and a growing matrix of scan modes. It is well engineered, but it is not small, and trust in the final result depends heavily on the fidelity of its extractors and external data sources.

## What they built

They built a multi-mode vulnerability and dependency analysis tool centered on the OSV ecosystem.

Concretely, the repo contains:

- the main CLI in [`cmd/osv-scanner`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner)
- a scanner library entrypoint in [`pkg/osvscanner`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner)
- extraction, plugin, reporting, and internal integration layers in [`internal`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal)
- GitHub Action wrappers in [`actions/scanner`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/actions/scanner) and [`actions/reporter`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/actions/reporter)
- docs and static site material in [`docs`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/docs)

Feature-wise, the repo supports source scanning, image scanning, offline databases, license summaries, guided remediation, CI report generation, and an experimental MCP server via [`cmd/osv-scanner/mcp/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/mcp/command.go).

## Why it matters

A lot of dependency security tooling is either too shallow, just parse a few lockfiles, or too enterprise-black-box to learn from. OSV-Scanner is useful because it is explicit about the real problem shape:

- extract package and artifact metadata from many ecosystems
- normalize it into one inventory model
- query vulnerability and license backends
- filter and enrich the findings
- emit results in formats that match developer workflows

That is a better mental model for builder-facing security tooling than “scanner equals API call.”

It also matters because it shows a sane way to compose a fast-moving CLI around a larger extraction platform without dumping everything into one impossible `main.go`.

## Repo shape at a glance

The repo has five main structural zones:

- [`cmd`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd), executable entrypoints for the main scanner and the CI-oriented reporter
- [`pkg/osvscanner`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner), the reusable scanner orchestration layer and public-ish package surface
- [`internal`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal), most of the machinery: config handling, clients, extraction adapters, output renderers, CI helpers, reporter logic, source analysis, and utility code
- [`actions`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/actions), GitHub Action packaging for scanner and reporter flows
- [`docs`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/docs), published documentation and static assets

Inside that, the important sub-shape is:

- command routing in [`cmd/osv-scanner/main.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/main.go)
- subcommands split into [`cmd/osv-scanner/scan`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/scan), [`cmd/osv-scanner/fix`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/fix), [`cmd/osv-scanner/update`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/update), and [`cmd/osv-scanner/mcp`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/mcp)
- output formatters concentrated in [`internal/output`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output)
- extractor adaptations and special scan support in places like [`internal/scalibrextract`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/scalibrextract), [`internal/scalibrplugin`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/scalibrplugin), and [`internal/sourceanalysis`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/sourceanalysis)

This is a healthy repo shape. The top-level folders correspond to product surfaces rather than arbitrary ownership lines.

## Layered architecture dissection

### High-level system shape

At a high level, the repo works like this:

1. CLI subcommands parse intent and flags in [`cmd/osv-scanner`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner)
2. the scanner orchestration layer turns those flags into `ScannerActions` in [`pkg/osvscanner/osvscanner.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/osvscanner.go)
3. plugin resolution and extraction happen through [`pkg/osvscanner/scan.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/scan.go) plus internal scalibr helpers
4. scan results are matched against OSV or local databases, optionally enriched with licenses and call analysis, then normalized into result models
5. output layers render text, HTML, SARIF, SPDX, CycloneDX, Markdown, GitHub annotations, and CI deltas via [`internal/output`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output) and [`internal/reporter`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/reporter)

The architecture is basically: command shell -> scan planner -> plugin-based inventory extraction -> matcher/enricher layer -> reporting surfaces.

### Main layers

#### 1) Command and UX layer

[`cmd/osv-scanner/main.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/main.go) is deliberately tiny. It just wires in four command builders: scan, fix, update, and MCP.

That simplicity is a strong signal. The CLI entrypoint is not carrying business logic. Each major capability has its own command package:

- [`cmd/osv-scanner/scan`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/scan)
- [`cmd/osv-scanner/fix`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/fix)
- [`cmd/osv-scanner/update`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/update)
- [`cmd/osv-scanner/mcp`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/mcp)

The source scan subcommand in [`cmd/osv-scanner/scan/source/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/scan/source/command.go) is a good example. It mostly translates CLI flags into a scanner action object and leaves the actual work to the scanning package.

#### 2) Scanner orchestration layer

[`pkg/osvscanner/osvscanner.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/osvscanner.go) is the real control center. It defines `ScannerActions`, sets up external accessors for online and offline modes, initializes matchers, runs scans, applies filtering, performs vulnerability and license matching, and finalizes normalized results.

This layer is where the repo’s design gets sharp. It gives the CLI a stable internal contract instead of letting every subcommand directly poke lower-level scanning machinery.

#### 3) Extraction and plugin layer

[`pkg/osvscanner/scan.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/scan.go) shows the heart of the system. It resolves plugins, configures capability flags, maps user-provided paths into scan roots, handles extractor overrides, and executes scans via `osv-scalibr`.

Important supporting pieces include:

- [`internal/scalibrplugin`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/scalibrplugin), plugin resolution helpers
- [`internal/scalibrextract/filesystem/vendored/vendored.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/scalibrextract/filesystem/vendored/vendored.go), vendored-code extraction support
- [`internal/scalibrextract/vcs/gitrepo/extractor.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/scalibrextract/vcs/gitrepo/extractor.go), Git repo extraction support
- [`internal/scalibrextract/vcs/gitcommitdirect/extractor.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/scalibrextract/vcs/gitcommitdirect/extractor.go), direct git commit extraction

This is the most reusable architectural idea in the repo: the scanner does not hardcode every ecosystem path itself. It relies on a plugin graph and a normalized inventory abstraction.

#### 4) Matching, enrichment, and analysis layer

After extraction, the repo matches packages against vulnerability data and optionally enriches the result set.

Key files and directories here include:

- [`internal/clients`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/clients), client abstractions and implementations
- [`internal/clients/clientimpl/osvmatcher`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/clients/clientimpl/osvmatcher), remote OSV matching
- [`internal/clients/clientimpl/localmatcher`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/clients/clientimpl/localmatcher), offline matching
- [`internal/clients/clientimpl/licensematcher`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/clients/clientimpl/licensematcher), deps.dev-backed license matching
- [`internal/sourceanalysis`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/sourceanalysis), extra code-level analysis support
- Java reachability toggling inside plugin configuration in [`pkg/osvscanner/scan.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/scan.go)

This layer matters because it is where the tool tries to reduce false positives and add practical context, not just dump raw advisory hits.

#### 5) Output and workflow integration layer

[`internal/output`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output) is unusually rich. It includes renderers for:

- HTML via [`internal/output/html.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output/html.go)
- SARIF via [`internal/output/sarif.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output/sarif.go)
- SPDX via [`internal/output/spdx.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output/spdx.go)
- CycloneDX via [`internal/output/cyclonedx.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output/cyclonedx.go)
- GitHub annotations via [`internal/output/githubannotation.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output/githubannotation.go)

Then the CI-oriented reporter command in [`cmd/osv-reporter`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-reporter) computes diffs between old and new scan outputs to highlight newly introduced vulnerabilities.

This is smart product design. The repo does not assume terminal output is the only consumer.

### Request / data / control flow

A typical source scan flow looks like this:

1. user runs `osv-scanner scan source` via [`cmd/osv-scanner/scan/source/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/scan/source/command.go)
2. flags are translated into `ScannerActions` in [`pkg/osvscanner/osvscanner.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/osvscanner.go)
3. [`pkg/osvscanner/scan.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/scan.go) resolves plugins, roots, filters, capabilities, and extractor overrides
4. `osv-scalibr` walks the filesystem or image artifacts and emits a normalized inventory of packages and findings
5. matchers query OSV or local databases, and optionally deps.dev for license data
6. filters and overrides prune ignored or unscannable packages
7. renderers in [`internal/output`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output) produce terminal, machine, HTML, or CI-friendly output

The key architectural point is that the extraction pass is separate from the output pass. That sounds obvious, but many scanners blur them together and become hard to extend.

## Key directories and files

- [`README.md`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/README.md), product overview and supported scan modes
- [`go.mod`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/go.mod), dependency surface showing just how much ecosystem handling and reporting breadth the tool carries
- [`cmd/osv-scanner/main.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/main.go), minimal top-level command dispatcher
- [`cmd/osv-scanner/scan/source/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/scan/source/command.go), clean example of CLI-to-core translation
- [`cmd/osv-scanner/fix/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/fix/command.go), guided remediation command with real risk warnings and strategy controls
- [`cmd/osv-scanner/mcp/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/mcp/command.go), experimental MCP service layer
- [`pkg/osvscanner/osvscanner.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/osvscanner.go), orchestration core
- [`pkg/osvscanner/scan.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/scan.go), plugin-driven scan execution
- [`internal/output`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output), multi-format rendering subsystem
- [`internal/scalibrextract`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/scalibrextract), repo-specific and VCS-aware extraction helpers
- [`cmd/osv-reporter`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-reporter), CI delta reporter for GitHub workflows
- [`actions/scanner/action.yml`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/actions/scanner/action.yml) and [`actions/reporter/action.yml`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/actions/reporter/action.yml), packaged automation surfaces

## Important components

### `ScannerActions` and `DoScan`

[`pkg/osvscanner/osvscanner.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/osvscanner.go) is the component to read first if you want the real system shape. It defines the operational contract for scanning and coordinates online/offline matchers, config loading, filtering, matching, and finalization.

### Plugin resolution and scan execution

[`pkg/osvscanner/scan.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/scan.go) matters because it is where the repo turns “please scan this repo” into a capability-aware plugin run. This is the repo’s center of engineering gravity.

### Source scan command

[`cmd/osv-scanner/scan/source/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/scan/source/command.go) is important as the main UX surface. It demonstrates how many knobs the tool exposes without letting the CLI become the scanner.

### Guided remediation command

[`cmd/osv-scanner/fix/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/fix/command.go) is notable because it moves the tool from reporting into action. The built-in risk warning is also refreshingly honest.

### Output subsystem

[`internal/output`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output) is central because this scanner has to live in terminals, HTML reports, machine pipelines, and CI platforms at once.

### MCP service layer

[`cmd/osv-scanner/mcp/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/mcp/command.go) is strategically interesting. It reframes the scanner as a tool-serving component for agents, not just a human CLI.

## Important knobs / configs / extension points

- CLI scan flags in [`cmd/osv-scanner/scan/source/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/scan/source/command.go), especially recursive scanning, ignore handling, data source choice, and experimental excludes
- remediation strategy flags in [`cmd/osv-scanner/fix/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/fix/command.go), including strategy, severity threshold, dependency depth, and upgrade policy
- plugin enable/disable behavior in [`pkg/osvscanner/scan.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/scan.go)
- offline-vs-online matcher selection in [`pkg/osvscanner/osvscanner.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/osvscanner.go)
- config file override path through `ConfigOverridePath` in [`pkg/osvscanner/osvscanner.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/osvscanner.go)
- local defaults and scanner config in [`osv-scanner.toml`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/osv-scanner.toml)
- output format choice through files in [`internal/output`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output)

The biggest extension point is clearly the plugin layer inherited from `osv-scalibr`. That is what lets the repo support more ecosystems without rewriting the whole tool.

## Practical questions and answers

### What is the smartest architectural choice?

Keeping the CLI layer small and treating scanning as inventory construction plus later matching. That separation is what makes the repo extensible.

### What is the repo’s real center of gravity?

Not the command parser. Not the README. It is [`pkg/osvscanner/scan.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/scan.go) plus the surrounding extraction and plugin machinery.

### What makes this more than a thin wrapper over OSV.dev?

The extractor stack, inventory model, offline mode, transitive resolution options, license scanning, HTML/SARIF/SPDX outputs, remediation flow, CI diffing, and MCP exposure. The OSV API is just one dependency in a wider workflow engine.

### Where would this fail or get brittle in production?

Mostly at the ecosystem edges: incomplete extractors, weird lockfiles, ambiguous transitive resolution, network dependence on upstream services, and the classic scanner problem where users assume silence means safety. The complexity ceiling is hidden in the plugin matrix.

### What part feels most reusable for our own work?

The pattern of making extraction the first-class problem. If you can turn many messy inputs into one normalized intermediate model, the rest of the product gets easier.

### What is the most strategically interesting recent direction?

The experimental MCP mode in [`cmd/osv-scanner/mcp`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/mcp). It suggests the team sees scanners becoming callable infrastructure for coding agents, not just standalone binaries.

## What is smart

- tiny executable root in [`cmd/osv-scanner/main.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/main.go)
- strong separation between command parsing, orchestration, extraction, and rendering
- plugin-driven scan engine in [`pkg/osvscanner/scan.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/pkg/osvscanner/scan.go)
- rich output subsystem in [`internal/output`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/internal/output)
- honest security warning on the remediation command in [`cmd/osv-scanner/fix/command.go`](https://github.com/google/osv-scanner/blob/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-scanner/fix/command.go)
- CI delta reporting in [`cmd/osv-reporter`](https://github.com/google/osv-scanner/tree/123ef8060defa52b3b4b239819866e0ac18f03ca/cmd/osv-reporter), which is exactly how teams actually consume scanner output
- experimental MCP surface, which is a forward-looking bet that feels correct

## What is flawed or weak

- the repo’s logic depends on a broad external ecosystem, `osv-scalibr`, deps.dev, OSV.dev, registries, and that creates hidden correctness risk
- the feature surface is growing toward “security platform CLI,” which can make discoverability and mental simplicity worse over time
- plugin and mode interactions are powerful but not especially small, which means debugging edge-case scan behavior could get ugly
- as with most scanners, there is still an interpretability gap between “finding exists” and “you should care right now”

None of these are fatal. They are the normal tax of building a real scanner instead of a toy.

## What we can learn / steal

- use a normalized intermediate model between input extraction and output rendering
- keep executable entrypoints embarrassingly small
- isolate product surfaces as separate commands instead of one giant flag swamp
- treat output formats as a serious subsystem, not an afterthought
- build the CI delta layer as a first-class product surface
- if a command is risky, say so plainly in the UX instead of hiding it in docs

## How we could apply it

If we were building our own analysis-heavy CLI or agent tool, the copyable pattern is:

1. define one action object that represents user intent
2. translate diverse inputs into one inventory or graph model
3. run enrichment and matching against that shared model
4. emit multiple views without changing core execution
5. expose the same core through CLI, CI, and agent protocols

That last step is especially relevant now. OSV-Scanner’s MCP mode hints at a better future where infrastructure tools are reusable by both humans and coding agents with the same core behavior.

## Bottom line

OSV-Scanner is a well-structured repo that solves the right problem at the right layer. It is not just “a CLI for the OSV API.” It is a plugin-backed inventory engine with multiple workflow surfaces wrapped around it. The big lesson is that good security tooling starts with artifact extraction and normalization, not vulnerability lookups. If I were borrowing one idea from this repo, it would be that inventory-first architecture.