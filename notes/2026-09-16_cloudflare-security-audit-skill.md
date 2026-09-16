# Security Audit Skill

- Repo: `cloudflare/security-audit-skill`
- URL: https://github.com/cloudflare/security-audit-skill
- Date: 2026-09-16
- Repo snapshot studied: `main` at commit `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`
- Why picked today: GitHub daily trending surfaced this repo near the top after several higher entries had already been covered this week. It is a compact but unusually serious example of packaging an AI security-audit workflow as a reusable coding-agent skill, with playbooks, schema contracts, validators, and tests instead of just a prompt.

## Executive summary

[`cloudflare/security-audit-skill`](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8) is a source-first security-audit workflow for coding agents. The interesting part is not that it tells an LLM to "find vulnerabilities." The interesting part is that it turns vulnerability research into a staged evidence machine: reconnaissance, deterministic coverage ledgers, isolated hunters, fresh verifiers, structured findings, schema validation, final record verification, and target-neutral reports.

The repository is small enough to read directly. The top-level [`README.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md) explains the six-phase flow. The real control surface is [`skills/security-audit/SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md), with phase playbooks in [`RECONNAISSANCE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md), [`HUNTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md), and [`VALIDATION-AND-REPORTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md).

The best builder lesson is that the skill treats agent output as untrusted until it survives independent verification and machine checks. [`report-schema.json`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/report-schema.json), [`validate-findings.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs), and [`validate-coverage-ledger.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs) are the parts that make the repo more than methodology prose.

## What they built

Cloudflare built a portable coding-agent skill for defensive security review. It has a single installable skill directory at [`skills/security-audit`](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit), and that directory contains the workflow contract, attack-class companions, validators, tests, and output schema.

The skill has two operating modes. Guidance mode answers focused security questions without creating a full audit directory. Full audit mode runs all six phases and writes artifacts such as `architecture.md`, `coverage-ledger.json`, `findings.json`, `REPORT.md`, `FINDINGS-DETAIL.md`, and `NEEDS-VALIDATION.md` as defined in [`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md).

The companion files split security domains cleanly: [`AI-AND-LLM.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/AI-AND-LLM.md), [`WEB-PROTOCOL-AND-AUTH.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/WEB-PROTOCOL-AND-AUTH.md), [`SUPPLY-CHAIN-AND-RELEASE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SUPPLY-CHAIN-AND-RELEASE.md), [`CLOUD-AND-DEPLOYMENT.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/CLOUD-AND-DEPLOYMENT.md), [`DATA-ISOLATION-AND-LIFECYCLE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/DATA-ISOLATION-AND-LIFECYCLE.md), and others. That keeps the parent workflow stable while letting reconnaissance select only the relevant hunting blocks.

## Why it matters

Most agent security-audit prompts fail because they collapse discovery, evidence, validation, and reporting into one persuasive answer. This repo pushes the opposite shape: every candidate has to be tied to a coverage unit, a source trace, a boundary, and a final verifier decision.

The strongest design choice is the separation between "candidate" and "finding." [`HUNTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md) lets hunters propose `confirmed` or `needs_validation` records, but [`VALIDATION-AND-REPORTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md) requires fresh verifiers to try to refute each candidate before it reaches `findings.json`.

This is also a good example of AI workflow engineering. The repo does not trust agent memory, prose, or vibes. It makes the parent own shared files, makes subagents write only to isolated scratch roots, validates JSON, sorts coverage units deterministically, and requires explicit terminal states.

## Repo shape at a glance

- [`README.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md): overview, installation, six phases, requirements, and principles.
- [`skills/security-audit/SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md): core skill contract, mode selection, execution safety, full-audit setup, write isolation, profiles, budget logic, and anti-patterns.
- [`skills/security-audit/RECONNAISSANCE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md): phase 1 source mapping and deterministic coverage-ledger construction.
- [`skills/security-audit/HUNTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md): phase 2 hunter prompts, structured hunter output, and parent consolidation.
- [`skills/security-audit/ATTACK-CLASSES.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/ATTACK-CLASSES.md): ordinary attack classes and companion-file routing.
- [`skills/security-audit/*-AND-*.md`](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit): domain companions for AI/LLM, client-side, cloud, data lifecycle, desktop/mobile/IPC, native binary, protocol/RPC, resource exhaustion, supply chain, and web/auth targets.
- [`skills/security-audit/VALIDATION-AND-REPORTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md): phases 3-6, verifier prompts, findings output, final verification, and report generation.
- [`skills/security-audit/report-schema.json`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/report-schema.json): exact contract for `confirmed`, `needs_validation`, and `rejected` records.
- [`skills/security-audit/validate-findings.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs) and [`validate-coverage-ledger.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs): dependency-free validators.
- [`validate-findings.test.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.test.cjs) and [`validate-coverage-ledger.test.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.test.cjs): tests for the machine contracts.

## Layered architecture dissection

### High-level system shape

The repo is a skill package, not an app server. The parent coding agent loads [`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md), decides guidance versus full-audit mode, then uses the phase files as prompt templates and operating rules.

The workflow is intentionally parent-owned. Hunters and verifiers are delegated workers, but the parent writes shared files, updates the ledger, runs validators, and decides whether the run has reached a terminal state. That boundary is repeated across [`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md), [`HUNTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md), and [`VALIDATION-AND-REPORTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md).

### Main layers

**Skill contract layer**  
[`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md) defines activation, modes, platform terminology, sandbox rules, output directory rules, write isolation, profiles, budget handling, core principles, and the six-phase workflow.

**Reconnaissance and coverage layer**  
[`RECONNAISSANCE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md) maps product, principals, entry surfaces, local execution visibility, and prior runs. Its most important output is not prose; it is `coverage-ledger.json`, a deterministic list of surface x boundary x subsystem x attack-class units.

**Hunting orchestration layer**  
[`HUNTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md) turns ledger units into isolated hunter assignments. It forces hunters to return exactly one structured JSON object with units, candidates, hardening notes, and uncovered areas.

**Attack-class companion layer**  
[`ATTACK-CLASSES.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/ATTACK-CLASSES.md) routes to companion files. [`AI-AND-LLM.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/AI-AND-LLM.md), for example, insists that prompt injection alone is not a finding; there must be a code-level boundary failure. [`SUPPLY-CHAIN-AND-RELEASE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SUPPLY-CHAIN-AND-RELEASE.md) applies the same source-grounded standard to CI, release, artifacts, and updates.

**Validation and reporting layer**  
[`VALIDATION-AND-REPORTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md) is the quality gate. It requires a fresh verifier for every candidate, then a final record-verification pass before reports are derived.

**Machine contract layer**  
[`report-schema.json`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/report-schema.json) defines the three verdict shapes. [`validate-findings.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs) enforces JSON schema plus semantic rules such as sorted fingerprints, safe repository-relative paths, trace ordering, verdict-specific forbidden fields, and severity not exceeding demonstrated impact. [`validate-coverage-ledger.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs) enforces the ledger state machine and ownership rules.

### Request / data / control flow

A full audit starts in [`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md) by resolving the skill directory, target, repo name, output directory, and source ref. The parent writes `run-metadata.json`, then runs reconnaissance from [`RECONNAISSANCE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md) and seeds `coverage-ledger.json`.

Hunters receive ledger units and selected blocks from [`ATTACK-CLASSES.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/ATTACK-CLASSES.md) plus any companion files. They return structured output as defined in [`HUNTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md). The parent updates the ledger and validates it with [`validate-coverage-ledger.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs).

Every candidate then goes through [`VALIDATION-AND-REPORTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md). A fresh verifier returns one JSON object with a `confirmed`, `needs_validation`, or `rejected` record. The parent writes `findings.json`, validates it with [`validate-findings.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs), performs final record verification, and only then derives reports.

## Key directories and files

- [`README.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/README.md): public packaging story and phase overview.
- [`skills/security-audit/SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md): the main operating system for the skill.
- [`skills/security-audit/RECONNAISSANCE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md): coverage-unit generation and prior-run handling.
- [`skills/security-audit/HUNTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md): hunter prompt contract and structured-result format.
- [`skills/security-audit/VALIDATION-AND-REPORTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md): verifier prompts, findings generation, final verification, and reports.
- [`skills/security-audit/report-schema.json`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/report-schema.json): verdict schema.
- [`skills/security-audit/validate-findings.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs): findings schema and semantic validator.
- [`skills/security-audit/validate-coverage-ledger.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs): ledger state validator.
- [`skills/security-audit/AI-AND-LLM.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/AI-AND-LLM.md): concrete model/tool/memory security hunting rules.
- [`skills/security-audit/SUPPLY-CHAIN-AND-RELEASE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SUPPLY-CHAIN-AND-RELEASE.md): CI, dependency, artifact, signing, and update handoff rules.

## Important components

[`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md) is the coordinator. It defines when the complete workflow is allowed, how write isolation works, what sandbox properties are required, and how quick, standard, and deep profiles change breadth without lowering the evidence bar.

[`RECONNAISSANCE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md) is the coverage engine. Its deterministic `coverage_id` rules are overbuilt in a good way: stable canonical refs, percent-encoded IDs, sorted units, prior-run carry-forward, and explicit out-of-scope/deferred states.

[`HUNTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/HUNTING.md) is the hunter harness. It tells agents to trace concrete invariants, stop at the smallest affected dummy result, avoid live targets, and return JSON rather than prose.

[`VALIDATION-AND-REPORTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md) is the adversarial checkpoint. It requires fresh verifiers, rejects malformed verifier output instead of repairing it, and prevents final reports from drifting away from the schema-shaped records.

The two validators are the repo's hidden muscle. [`validate-findings.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs) includes limits for input size, nesting depth, uniqueness, diagnostics, path safety, and verdict-specific semantic checks. [`validate-coverage-ledger.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs) makes the coverage ledger a real state machine instead of a spreadsheet.

## Important knobs / configs / extension points

- Operating mode in [`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md): guidance mode versus full audit mode.
- Run profile in [`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md): `quick`, `standard`, or `deep`.
- Budget handling in [`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md): reserves reconnaissance, critics, and validation before assigning hunters.
- Companion selection through [`ATTACK-CLASSES.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/ATTACK-CLASSES.md): choose domain-specific files only when reconnaissance found the matching trust boundary.
- Verdict contract in [`report-schema.json`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/report-schema.json): `confirmed`, `needs_validation`, and `rejected` are intentionally incompatible shapes.
- Validator behavior in [`validate-findings.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs): no dependency install, hard input limits, path safety, trace ordering, duplicate fingerprint rejection, and severity guardrails.
- Ledger behavior in [`validate-coverage-ledger.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs): planned, in-progress, blocked, covered, candidate, deferred, and out-of-scope states have different ownership and evidence requirements.

## Practical questions and answers

**Is this a scanner?**  
No. It is an orchestration and evidence framework. The skill delegates source review to agents, but the value comes from coverage planning, isolation, independent validation, and structured outputs.

**What prevents hallucinated vulnerabilities?**  
Several things together: source-relative traces in [`report-schema.json`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/report-schema.json), verifier prompts in [`VALIDATION-AND-REPORTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md), semantic checks in [`validate-findings.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs), and final record verification.

**Where does coverage live?**  
In `coverage-ledger.json`, whose construction is specified by [`RECONNAISSANCE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/RECONNAISSANCE.md) and whose state rules are enforced by [`validate-coverage-ledger.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-coverage-ledger.cjs).

**Can it safely run target code?**  
Only if a strict OS-enforced sandbox is available. [`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md) requires no external network, sanitized environment, read-only target/toolchain, scratch-only writes, and resource limits. If that cannot be enforced, the workflow keeps the issue as `needs_validation`.

**What part would I copy first?**  
The verdict split and validators. [`report-schema.json`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/report-schema.json) makes uncertainty explicit, while [`validate-findings.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs) prevents prose-shaped convenience from becoming a finding.

## What is smart

- The workflow makes "coverage" a durable object, not a claim in the final paragraph.
- [`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md) distinguishes guidance from full audit mode, which avoids creating heavyweight artifacts for ordinary security questions.
- [`AI-AND-LLM.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/AI-AND-LLM.md) has the right posture: prompt injection alone is not a vulnerability without a deterministic boundary failure.
- [`VALIDATION-AND-REPORTING.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/VALIDATION-AND-REPORTING.md) makes adversarial verification normal, not optional.
- The validators are dependency-free Node scripts, which is exactly the right boring choice for a skill that should run in many target repos.

## What is flawed or weak

- The process is heavy. A full standard or deep audit can burn many agent calls before it produces anything owner-readable.
- The safety model depends on the host platform actually enforcing the sandbox described in [`SKILL.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SKILL.md). If the platform cannot do that, many checks become unresolved.
- The repo has strong validators for outputs, but the actual agent quality still depends on the model reading code well and following the prompts.
- The domain companions are extensive; a weak parent implementation could over-select blocks and drown hunters in irrelevant instructions.
- The artifact-promotion procedure is careful, but it is complex enough that platform-specific implementations need their own scrutiny.

## What we can learn / steal

- Treat agent workers as untrusted producers. Make a parent own shared state, machine-check every artifact, and require fresh verification before final output.
- Split methodology into small companion files like [`AI-AND-LLM.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/AI-AND-LLM.md) and [`SUPPLY-CHAIN-AND-RELEASE.md`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/SUPPLY-CHAIN-AND-RELEASE.md), then route to them from reconnaissance instead of loading every checklist every time.
- Use separate data shapes for certainty states. A `needs_validation` record should not carry severity, remediation, or reproduction fields that make it look confirmed.
- Write validators that enforce semantics, not just JSON shape. [`validate-findings.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs) checks sorted fingerprints, safe paths, trace ordering, and severity constraints.
- Keep reports derived from structured records. That prevents the final narrative from inventing a stronger finding than the evidence supports.

## How we could apply it

For any multi-agent workflow, I would copy the separation between planner, hunters, verifiers, and reporters. The same pattern applies to migrations, incident review, dependency upgrades, and architecture audits: coverage plan first, isolated work units second, independent verification third, generated report last.

For security specifically, I would start with a smaller version of [`report-schema.json`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/report-schema.json) and [`validate-findings.cjs`](https://github.com/cloudflare/security-audit-skill/blob/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit/validate-findings.cjs), then add deterministic coverage units after the first painful false-positive cleanup. The repo's key move is making the output contract harder to satisfy than a persuasive paragraph.

## Bottom line

`cloudflare/security-audit-skill` is worth studying because it shows what a serious AI security-audit workflow looks like when it is packaged as source, not as a blog-post prompt. The reusable idea is simple and powerful: do not ask agents for confidence; ask them for source traces, bounded results, structured records, and verification that can fail.

The repo's strongest lesson is that agentic audit quality is mostly orchestration quality. The model matters, but the ledger, schema, validators, isolation rules, and verifier independence are what turn a pile of observations into something an owner might trust.
