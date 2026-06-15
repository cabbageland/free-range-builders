# SkillSpector

- Repo: `NVIDIA/SkillSpector`
- URL: https://github.com/NVIDIA/SkillSpector
- Date: 2026-06-14
- Repo snapshot studied: `main` @ `cff7ecc4f2881d9e23ea4bb801a6353e1dbe39e6`
- Why picked today: A hot agent-security repo from NVIDIA is exactly in the Free Range Builders strike zone. It had roughly 5.7k stars and 427 forks when checked, but the better reason to study it is that it turns "agent skills are executable trust bundles" into a concrete scanner with a LangGraph pipeline, static rules, behavioral checks, MCP-specific analyzers, optional LLM review, SARIF output, and tests.

## Executive summary
SkillSpector is a security scanner for AI agent skills. The core product question is simple: before installing a skill for Claude Code, Codex CLI, Gemini CLI, or a similar agent, can we inspect the bundle for prompt injection, exfiltration, privilege creep, supply-chain risk, tool poisoning, and unsafe executable behavior?

The implementation is a Python package with a Typer CLI, a LangGraph workflow, a file/input resolver, a context builder, a fan-out set of analyzers, an optional LLM meta-analyzer, and a report node that emits terminal, JSON, Markdown, or SARIF. The repo is not just a README around a prompt. It has a real analyzer registry in [`src/skillspector/nodes/analyzers/__init__.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/__init__.py), a graph in [`src/skillspector/graph.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/graph.py), and a meaningful test tree under [`tests/`](https://github.com/NVIDIA/SkillSpector/tree/main/tests).

The strongest part is the framing: agent skills are supply-chain artifacts, not just docs. The weaker part is that many checks are necessarily heuristic, and the repo still carries TODOs/stub-like edges in places. That is fine for an alpha scanner, but builders should treat it as a lint/security-assist layer, not a proof of safety.

## What they built
They built a command-line and LangGraph-based scanner that can accept a Git repo, URL, zip, Markdown file, or directory, normalize it into a local scan directory, inspect the files, collect findings, optionally pass them through LLM filtering/enrichment, compute a risk score, and generate reports.

The main entrypoint is the Typer CLI in [`src/skillspector/cli.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/cli.py). It maps `skillspector scan <path-or-url>` options into graph state, invokes the compiled graph, prints or writes the report, and exits non-zero when risk is high enough. The graph itself is built in [`src/skillspector/graph.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/graph.py).

The scanner covers static pattern classes, dangerous Python AST behavior, taint-style flows, YARA signatures, MCP least privilege, MCP tool poisoning, semantic LLM checks, and report generation. The docs in [`docs/DEVELOPMENT.md`](https://github.com/NVIDIA/SkillSpector/blob/main/docs/DEVELOPMENT.md) are unusually useful because they describe the state fields, graph flow, node roles, and extension path.

## Why it matters
Agent skills are attractive because they compress workflows into portable instructions and scripts. That is also why they are dangerous. A skill can combine natural-language instructions, triggers, metadata, shell/Python scripts, dependency files, and permissions. A human may skim the nice description while the agent later consumes the whole bundle as authority.

SkillSpector matters because it treats this as a product security problem. It asks for a pre-install review loop, not just a moral hope that marketplace skills are safe. That is the right direction for any open skill ecosystem.

## Repo shape at a glance
The repo is compact and readable:

- [`README.md`](https://github.com/NVIDIA/SkillSpector/blob/main/README.md), user-facing overview, install path, feature list, rule categories, and CLI examples
- [`pyproject.toml`](https://github.com/NVIDIA/SkillSpector/blob/main/pyproject.toml), package metadata, Python 3.12/3.13 support, dependencies, script entrypoint, and build config
- [`src/skillspector/cli.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/cli.py), Typer CLI wrapper
- [`src/skillspector/graph.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/graph.py), LangGraph workflow assembly
- [`src/skillspector/state.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/state.py) and [`src/skillspector/models.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/models.py), state and finding schemas
- [`src/skillspector/input_handler.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/input_handler.py), Git/URL/zip/file/directory normalization
- [`src/skillspector/nodes/`](https://github.com/NVIDIA/SkillSpector/tree/main/src/skillspector/nodes), graph nodes for input resolution, context building, analysis, meta-analysis, and reporting
- [`src/skillspector/nodes/analyzers/`](https://github.com/NVIDIA/SkillSpector/tree/main/src/skillspector/nodes/analyzers), the analyzer implementations and registry
- [`src/skillspector/providers/`](https://github.com/NVIDIA/SkillSpector/tree/main/src/skillspector/providers), LLM provider adapters and bundled model registries
- [`src/skillspector/yara_rules/`](https://github.com/NVIDIA/SkillSpector/tree/main/src/skillspector/yara_rules), packaged YARA signatures
- [`tests/`](https://github.com/NVIDIA/SkillSpector/tree/main/tests), fixtures plus unit, node, and integration coverage

## Layered architecture dissection
### High-level system shape
The graph is the center. [`src/skillspector/graph.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/graph.py) wires this flow:

1. `resolve_input` normalizes the input into `skill_path`.
2. `build_context` walks the skill directory and builds `components`, `file_cache`, parsed manifest metadata, component metadata, and executable-script flags.
3. Analyzer nodes fan out from the shared context.
4. Analyzer findings fan into `meta_analyzer`.
5. `report` builds SARIF, computes risk score, and formats the requested output.

That shape is good because it keeps the scanner extensible. New analyzers register in [`src/skillspector/nodes/analyzers/__init__.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/__init__.py); the graph loops over the registry instead of hardcoding every edge.

### Main layers
**Input normalization layer**
[`src/skillspector/input_handler.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/input_handler.py) recognizes Git URLs, raw file URLs, zips, Markdown files, single files, and directories. Git repos are cloned with `--depth 1`, URLs are downloaded through httpx, and single files are wrapped in a temporary directory. This is the right boring layer because scanners become useless if users must pre-shape every input by hand.

**Context layer**
[`src/skillspector/nodes/build_context.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/build_context.py) walks files, skips caches and virtualenvs, infers file types, reads file contents, parses `SKILL.md` frontmatter, and marks executable components. The scanner's later risk multiplier depends on `has_executable_scripts`, which is a practical signal: a docs-only skill and a skill with scripts should not feel equally dangerous.

**Analyzer layer**
The analyzer registry includes static pattern nodes, AST and taint analyzers, MCP analyzers, semantic LLM analyzers, and YARA. Static pattern conversion is centralized in [`src/skillspector/nodes/analyzers/static_runner.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/static_runner.py), while common pattern labels/remediations live in [`src/skillspector/nodes/analyzers/pattern_defaults.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/pattern_defaults.py).

**LLM review layer**
[`src/skillspector/nodes/meta_analyzer.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/meta_analyzer.py) treats skill contents as adversarial, batches per file, and asks an LLM to decide whether static findings are real vulnerabilities. This is the right use of an LLM: adjudication and enrichment after cheap static passes, not blind free-form scanning as the only defense.

**Reporting layer**
[`src/skillspector/nodes/report.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/report.py) computes a 0-100 risk score, applies a multiplier when executable scripts exist, emits SARIF through [`src/skillspector/sarif_models.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/sarif_models.py), and formats terminal/JSON/Markdown/SARIF reports.

### Request / data / control flow
A CLI scan starts in [`src/skillspector/cli.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/cli.py). `_scan_state()` builds graph state with `input_path`, `output_format`, and `use_llm`. The graph invokes [`src/skillspector/nodes/resolve_input.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/resolve_input.py), then [`src/skillspector/nodes/build_context.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/build_context.py). Analyzer nodes append `Finding` objects into the state reducer. `meta_analyzer` either filters/enriches those findings or falls back when LLM use is disabled. `report` writes the final `report_body`, `risk_score`, `risk_severity`, and `sarif_report`.

The resulting control flow is pleasantly explicit. You can follow a finding from regex/AST detection to `Finding` conversion to LLM filtering to SARIF output without reverse-engineering a framework blob.

## Key directories and files
- [`src/skillspector/graph.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/graph.py), the graph assembly and analyzer fan-out/fan-in
- [`src/skillspector/cli.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/cli.py), CLI state mapping, output writing, cleanup, and exit codes
- [`src/skillspector/input_handler.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/input_handler.py), input resolver for repos/files/zips/URLs
- [`src/skillspector/nodes/build_context.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/build_context.py), inventory and manifest parsing
- [`src/skillspector/nodes/analyzers/static_patterns_prompt_injection.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/static_patterns_prompt_injection.py), prompt-injection pattern examples
- [`src/skillspector/nodes/analyzers/static_patterns_data_exfiltration.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/static_patterns_data_exfiltration.py), exfiltration pattern examples
- [`src/skillspector/nodes/analyzers/static_patterns_supply_chain.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/static_patterns_supply_chain.py), dependency, OSV, and trigger checks
- [`src/skillspector/nodes/analyzers/behavioral_ast.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/behavioral_ast.py), AST checks for exec/eval/subprocess/os execution
- [`src/skillspector/nodes/analyzers/mcp_least_privilege.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/mcp_least_privilege.py), declared permissions vs detected capabilities
- [`src/skillspector/nodes/analyzers/mcp_tool_poisoning.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/mcp_tool_poisoning.py), hidden metadata and Unicode deception checks
- [`docs/DEVELOPMENT.md`](https://github.com/NVIDIA/SkillSpector/blob/main/docs/DEVELOPMENT.md), architecture guide

## Important components
The graph registry is the extension spine. The combo of [`src/skillspector/graph.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/graph.py) and [`src/skillspector/nodes/analyzers/__init__.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/__init__.py) makes "add another analyzer" an ordinary node-registration task.

The context builder is the scanner's data plane. [`src/skillspector/nodes/build_context.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/build_context.py) decides what files count, what content is cached, what manifest fields exist, and whether executable scripts are present.

The pattern defaults file is underrated. [`src/skillspector/nodes/analyzers/pattern_defaults.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/pattern_defaults.py) gives rule IDs stable explanations, categories, names, and remediations. That turns scattered regex hits into a coherent report language.

The MCP analyzers are the most domain-specific pieces. [`mcp_least_privilege.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/mcp_least_privilege.py) and [`mcp_tool_poisoning.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/mcp_tool_poisoning.py) show the scanner is not just a generic static-analysis toy; it understands that agent tool metadata can itself be an attack surface.

## Important knobs / configs / extension points
- [`pyproject.toml`](https://github.com/NVIDIA/SkillSpector/blob/main/pyproject.toml) defines the package entrypoint, Python versions, dependencies, and build artifacts.
- [`model_registry.yaml`](https://github.com/NVIDIA/SkillSpector/blob/main/model_registry.yaml) and provider registries under [`src/skillspector/providers/`](https://github.com/NVIDIA/SkillSpector/tree/main/src/skillspector/providers) carry model context-window metadata.
- Environment variables like `SKILLSPECTOR_PROVIDER`, `SKILLSPECTOR_MODEL`, `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `ANTHROPIC_API_KEY`, and `NVIDIA_INFERENCE_KEY` configure the optional LLM layer.
- [`src/skillspector/nodes/analyzers/__init__.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/nodes/analyzers/__init__.py) is the analyzer registration point.
- [`src/skillspector/yara_rules/`](https://github.com/NVIDIA/SkillSpector/tree/main/src/skillspector/yara_rules) is the packaged signature-extension surface.
- The CLI flags `--no-llm`, `--format`, `--output`, `--yara-rules-dir`, and `--verbose` are the main operator knobs.

## Practical questions and answers
**Is this a real scanner or mostly marketing?**
It is a real scanner. The graph, rules, AST checks, MCP-specific logic, reports, and tests are inspectable. Some analyzer areas are early, but there is enough implementation to learn from.

**What is the architectural center?**
The LangGraph state machine: [`src/skillspector/graph.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/graph.py), [`src/skillspector/state.py`](https://github.com/NVIDIA/SkillSpector/blob/main/src/skillspector/state.py), and the analyzer registry.

**Would I trust a "safe" result blindly?**
No. A scanner like this can reduce obvious risk, create CI gates, and focus review attention. It cannot prove that a skill is safe, especially when semantic intent and future tool behavior are involved.

**What would I copy?**
The staged pipeline: cheap inventory and static passes first, domain-specific analyzers second, optional LLM judgment third, structured reports last.

**Where would I be careful?**
Regex-heavy scanners get noisy. The LLM meta-analyzer can reduce noise, but then you inherit model quality, provider credentials, cost, and adversarial prompt exposure as part of the scanner's own threat model.

## What is smart
- Treating skill bundles as supply-chain artifacts.
- Using LangGraph as a clear workflow rather than hiding the scan in one giant function.
- Separating raw analyzer findings from meta-analysis and final reporting.
- Including MCP least-privilege and tool-poisoning checks; those are agent-native risks.
- Producing SARIF, which makes the scanner useful in CI and code-review systems.
- Maintaining fixtures for malicious, safe, overprivileged, underdeclared, and poisoned skills under [`tests/fixtures/`](https://github.com/NVIDIA/SkillSpector/tree/main/tests/fixtures).

## What is flawed or weak
- Several checks are heuristic by nature. That is unavoidable, but it means severity and confidence need human interpretation.
- The README's broad feature claims are ahead of what I would call mature proof. The repo is useful, but still alpha-shaped.
- LLM-based semantic review is valuable but creates operational complexity: credentials, model selection, token budgets, and adversarial content handling.
- The scanner focuses on pre-install artifacts. Runtime behavior, external services, and post-install updates still need separate controls.
- Static pattern categories can overlap, so report UX has to keep improving to avoid noisy duplicate findings.

## What we can learn / steal
- Build skill marketplaces around scanners from the beginning, not after abuse shows up.
- Keep rule IDs stable and reportable. A finding without a stable ID is hard to automate around.
- Split scanner work into inventory, static rules, behavioral analysis, semantic review, and reporting.
- Treat metadata as executable-adjacent input. Tool descriptions and parameter docs are model-facing attack surfaces.
- Emit SARIF early so security tooling can consume results without custom glue.

## How we could apply it
For our own skill ecosystem, I would borrow the shape:

1. normalize every install candidate into a local bundle,
2. inventory files and parse skill metadata,
3. run cheap rules and AST checks,
4. add agent-specific checks for permissions, triggers, tool descriptions, and hidden metadata,
5. use an LLM only as a second-pass reviewer,
6. produce both human-readable notes and machine-readable SARIF,
7. make scans idempotent enough to run in CI, cron, and pre-install hooks.

The biggest reusable lesson is social, not technical: "install this skill" should feel more like installing a package than reading a blog post.

## Bottom line
SkillSpector is a timely, useful security scanner for the agent-skill era. It is not a magic safety oracle, and builders should not pretend it is. But the architecture is the right kind of boring: normalize inputs, build context, run analyzers, filter findings, score risk, output SARIF.

The sharp lesson is that agent capabilities have become supply chain. If the assistant will read, execute, and trust a bundle, the bundle deserves preflight inspection.
