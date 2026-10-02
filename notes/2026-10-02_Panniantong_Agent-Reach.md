# Agent Reach

- Repo: Panniantong/Agent-Reach
- URL: https://github.com/Panniantong/Agent-Reach
- Date: 2026-10-02
- Repo snapshot studied: `main` commit `a19a171fa980a0785849596492e0af4db800c82f`
- Why picked today: It was the top AI-shaped GitHub daily trending repo I found, with roughly 88k stars and a very current trending badge. The interesting part is not the marketing claim that it gives agents "eyes"; it is the source-visible pattern of ordered platform backends, read-only diagnostics, credential boundaries, and packaged agent instructions.

## Executive summary

[Agent Reach](https://github.com/Panniantong/Agent-Reach/tree/a19a171fa980a0785849596492e0af4db800c82f) is a Python CLI and installable agent skill that standardizes how coding agents get web and social-platform reach. It does not try to become a universal scraper. The core bet, stated in [agent_reach/core.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/core.py), is that agents should install and diagnose the best upstream tools, then call those upstream tools directly.

The useful architecture is a capability layer: [agent_reach/channels](https://github.com/Panniantong/Agent-Reach/tree/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels) contains per-platform channel adapters, each with an ordered backend list and a real health probe. [agent_reach/doctor.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/doctor.py) merely collects those channel results and scrubs outputs. [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py) owns installation, configuration, skill registration, transcription, formatting, and safety defaults.

The builder lesson is that "agent internet access" is better treated as an operating layer than a single API. Agent Reach keeps channel choice, backend probing, credential handling, and user-facing repair advice close to the platform-specific code.

## What they built

Agent Reach ships a Python package named `agent-reach`, exposed through the `agent-reach` CLI in [pyproject.toml](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/pyproject.toml). The declared dependency surface is intentionally ordinary: `requests`, `feedparser`, `python-dotenv`, `pyyaml`, `rich`, `loguru`, and `yt-dlp[default]`.

The package has four main jobs:

- Install and check upstream platform tools through [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py).
- Store local configuration through [agent_reach/config.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/config.py).
- Model each platform as a channel under [agent_reach/channels](https://github.com/Panniantong/Agent-Reach/tree/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels).
- Register an agent-facing skill from [agent_reach/skill](https://github.com/Panniantong/Agent-Reach/tree/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/skill), including reference guides in [agent_reach/skill/references](https://github.com/Panniantong/Agent-Reach/tree/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/skill/references).

There is also a minimal MCP integration in [agent_reach/integrations/mcp_server.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/integrations/mcp_server.py), but it exposes status only. The actual reading and searching are deliberately left to upstream tools such as `yt-dlp`, `gh`, `twitter-cli`, OpenCLI, `bili-cli`, `rdt-cli`, Jina Reader, and `feedparser`.

## Why it matters

The "give your agent the internet" space is usually full of thin wrappers. Agent Reach is more interesting because it owns the messy operational matrix: which platform works without login, which requires browser state, which backend is stale, which health check is safe, which credential path should never be read automatically, and which install mode is allowed to mutate the system.

That is a practical problem for agents. The right backend for Twitter, Reddit, Bilibili, YouTube, GitHub, RSS, or Xiaohongshu changes often. Agent Reach's design makes a platform a replaceable ordered backend list rather than a hardcoded integration.

## Repo shape at a glance

- [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py): CLI entry point and command handlers for `install`, `configure`, `doctor`, `uninstall`, `skill`, `format`, `transcribe`, `watch`, and `check-update`.
- [agent_reach/channels](https://github.com/Panniantong/Agent-Reach/tree/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels): platform adapters for GitHub, Twitter, YouTube, Reddit, Facebook, Instagram, Bilibili, Xiaohongshu, LinkedIn, Boss, Xiaoyuzhou, V2EX, Xueqiu, RSS, Exa search, and web pages.
- [agent_reach/channels/base.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/base.py): channel contract, ordered backend semantics, user override handling, and `active_backend` convention.
- [agent_reach/doctor.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/doctor.py): channel aggregation, exception isolation, credential scrubbing, and Rich report formatting.
- [agent_reach/probe.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/probe.py): side-effect-free command probing that distinguishes missing, broken, timeout, and error states.
- [agent_reach/config.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/config.py) and [agent_reach/utils/paths.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/utils/paths.py): local config storage, owner-only writes, symlink rejection, bounded reads, and masking.
- [agent_reach/backends/opencli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/backends/opencli.py): OpenCLI-specific health check that avoids side-effectful `opencli doctor`.
- [agent_reach/cookie_extract.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cookie_extract.py): explicit browser-cookie import machinery for supported platforms.
- [agent_reach/integrations/mcp_server.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/integrations/mcp_server.py): status-only MCP bridge.
- [tests](https://github.com/Panniantong/Agent-Reach/tree/a19a171fa980a0785849596492e0af4db800c82f/tests): a surprisingly large regression suite for channel contracts, credential boundaries, URL security, doctor behavior, install behavior, and private file writes.
- [docs](https://github.com/Panniantong/Agent-Reach/tree/a19a171fa980a0785849596492e0af4db800c82f/docs): install, update, troubleshooting, dependency locking, cookie export, and localized READMEs.

## Layered architecture dissection

### High-level system shape

The user-facing flow is:

1. A user or agent runs `agent-reach install`, `agent-reach doctor`, or `agent-reach configure` through [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py).
2. Config reads and writes go through [Config](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/config.py), which uses owner-only local files under `~/.agent-reach`.
3. Health checks call [doctor.check_all](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/doctor.py), which iterates the registry from [agent_reach/channels/__init__.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/__init__.py).
4. Each channel probes candidate backends in order and sets `active_backend` only when the backend is actually usable.
5. The installed [agent_reach/skill/SKILL.md](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/skill/SKILL.md) tells the agent which upstream tool to call for the user's requested platform.

The important negative space: [AgentReach](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/core.py) only wraps doctor status. It does not wrap every read/search request.

### Main layers

The channel layer starts with [Channel](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/base.py). A channel has a name, description, ordered `backends`, a setup tier, `can_handle`, and `check`. `ordered_backends` lets config move a preferred backend to the front without hiding unknown or stale values.

The probe layer is [agent_reach/probe.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/probe.py). It executes harmless version/status commands and classifies the result. This matters because `shutil.which` cannot distinguish a working CLI from a stale `pipx` shim whose interpreter disappeared.

The safety layer is split between [agent_reach/config.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/config.py), [agent_reach/utils/paths.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/utils/paths.py), and [agent_reach/utils/text.py](https://github.com/Panniantong/Agent-Reach/tree/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/utils). It rejects symlinked private paths, writes atomically with owner-only permissions, bounds reads, and masks sensitive config keys.

The CLI layer in [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py) is both installer and policy gate. It defaults `install` into safe check-only behavior unless `--system` is passed. It caps configure values with `_MAX_CONFIGURE_VALUE_CHARS`, supports `--stdin`, and refuses browser-cookie extraction for Twitter and Xiaohongshu because those platforms require explicit Cookie-Editor exports.

The agent instruction layer is [agent_reach/skill](https://github.com/Panniantong/Agent-Reach/tree/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/skill). The install command copies localized `SKILL.md` plus reference docs to known agent skill roots for Agent, OpenCode, OpenClaw, and Claude Code.

### Request / data / control flow

For a doctor run, [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py) constructs a [Config](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/config.py) and calls [check_all](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/doctor.py). `check_all` loads singleton channel objects from [agent_reach/channels/__init__.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/__init__.py), calls each `check`, catches channel exceptions, scrubs messages, and returns a status dictionary.

[TwitterChannel](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/twitter.py) is a good example. It probes `twitter-cli`, OpenCLI, and legacy `bird`, but refuses to run upstream `twitter status` because that upstream command can fall back to reading browser cookies. Saved explicit credentials are passed only to child processes through `twitter_cli_child_env`; `os.environ` is not mutated.

[BilibiliChannel](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/bilibili.py) shows the multi-backend pattern in a less credential-sensitive case: `bili-cli`, OpenCLI, then a direct search API fallback. The file documents why `yt-dlp` was removed for Bilibili while remaining the YouTube backend.

[YouTubeChannel](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/youtube.py) illustrates operational diagnosis. It probes `yt-dlp`, checks for Node or Deno JavaScript runtime support, reads the `yt-dlp` config through [read_small_text_no_follow](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/utils/paths.py), and reports exactly which remediation command is needed.

For actual user requests after installation, the control flow leaves Agent Reach. The installed skill tells the agent to call the upstream tool directly, keeping Agent Reach out of the hot path.

## Key directories and files

- [README.md](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/README.md): product framing and current backend map. It is marketing-heavy, but the channel table matches the source layout.
- [pyproject.toml](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/pyproject.toml): package metadata, CLI entry point, dependency set, optional extras, and lint/type-check settings.
- [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py): main policy surface.
- [agent_reach/channels/base.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/base.py): the most important design contract.
- [agent_reach/channels/twitter.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/twitter.py): credential-boundary-aware channel probe.
- [agent_reach/channels/youtube.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/youtube.py): a detailed backend readiness check.
- [agent_reach/channels/bilibili.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/bilibili.py): a concise record of backend rotation when one upstream path stops working.
- [agent_reach/backends/opencli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/backends/opencli.py): side-effect-aware OpenCLI probing.
- [agent_reach/probe.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/probe.py): reusable command-health classification.
- [agent_reach/config.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/config.py): secure config load/save behavior.
- [tests/test_doctor_credential_boundaries.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/tests/test_doctor_credential_boundaries.py): regression tests proving doctor does not execute credential-backed CLIs or refresh cookies.
- [tests/test_cookie_security.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/tests/test_cookie_security.py): explicit platform and domain-bound cookie extraction tests.

## Important components

- `Channel` in [agent_reach/channels/base.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/base.py): the platform abstraction.
- `probe_command` in [agent_reach/probe.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/probe.py): the difference between a real health check and a PATH check.
- `check_all` and `format_report` in [agent_reach/doctor.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/doctor.py): aggregation and user-facing diagnosis.
- `Config` in [agent_reach/config.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/config.py): private local config with masking.
- `atomic_write_private_text`, `read_small_text_no_follow`, and `ensure_no_symlink_path` in [agent_reach/utils/paths.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/utils/paths.py): the filesystem hardening primitives.
- `opencli_status` in [agent_reach/backends/opencli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/backends/opencli.py): a backend-specific probe that avoids accidentally starting daemons or mutating state.
- `_cmd_install`, `_cmd_configure`, and `_install_skill` in [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py): install policy, config writes, and agent skill registration.

## Important knobs / configs / extension points

- Channel backend order is declared in each channel, then adjusted by `ordered_backends` in [agent_reach/channels/base.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/base.py) through config keys such as `<channel>_backend`.
- Install mutation is gated by `--system`; safe check-only mode is the default in [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py).
- Optional channels are requested with `--channels`, validated before config or system changes in [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py).
- Sensitive config is written via `agent-reach configure`, preferably `--stdin`, with sensitive keys enumerated in [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py).
- Transcription provider selection flows through the `transcribe` command in [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py) and [agent_reach/transcribe.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/transcribe.py).
- The agent-facing behavior is extended by editing [agent_reach/skill/SKILL.md](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/skill/SKILL.md) and files in [agent_reach/skill/references](https://github.com/Panniantong/Agent-Reach/tree/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/skill/references).

## Practical questions and answers

Q: Is Agent Reach a scraper?

A: Mostly no. [agent_reach/core.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/core.py) says reading and searching should be done by upstream tools. Agent Reach installs, diagnoses, configures, and teaches agents which route to use.

Q: Where is the main abstraction?

A: [Channel](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/base.py). Each platform is a small object with ordered backend candidates and a `check` method. That is simple, but it matches the failure mode of platform access better than a central matrix.

Q: How does it avoid lying about tool availability?

A: Channels use [probe_command](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/probe.py) or equivalent lightweight API checks. They distinguish missing commands, broken shims, timeouts, and runtime errors.

Q: What is the strongest safety decision?

A: Doctor avoids credential-refresh side effects. [TwitterChannel](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/twitter.py) refuses to run upstream commands that could read browser cookies, and [tests/test_doctor_credential_boundaries.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/tests/test_doctor_credential_boundaries.py) locks that behavior down.

Q: Where could this fail in production?

A: The project depends heavily on upstream CLIs and platforms that change often. The architecture makes backend rotation cheap, but it cannot remove the operational burden. The test suite helps with local policy, not with live platform volatility.

Q: What would I copy?

A: The channel-owned backend ordering and the doctor-as-aggregator pattern from [agent_reach/channels/base.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/base.py) plus [agent_reach/doctor.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/doctor.py). It is a clean way to keep platform-specific health knowledge with platform code.

## What is smart

The best idea is that Agent Reach is a capability layer, not a proxy. By installing an agent skill and upstream tools, it avoids being a brittle central API surface.

The second smart idea is real probing. [agent_reach/probe.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/probe.py) exists because a command on PATH may still be unusable. That is exactly the kind of boring operational truth agent tooling often skips.

The OpenCLI probe in [agent_reach/backends/opencli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/backends/opencli.py) is especially grounded. It documents why `opencli doctor` is not safe for a read-only health check and instead reads the loopback status endpoint plus disk evidence.

The security posture is better than expected for a trending repo. [agent_reach/config.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/config.py), [agent_reach/utils/paths.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/utils/paths.py), and credential-boundary tests show an actual threat model around symlinks, broad browser-cookie reads, and leaked URL credentials.

## What is flawed or weak

The repo has a lot of marketing mass in [README.md](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/README.md), including sponsor blocks and sweeping platform claims. A builder should evaluate it by source and tests, not by the star count or headline.

The core value depends on upstream projects with uneven maturity. If `twitter-cli`, OpenCLI, `bili-cli`, or any platform policy changes, Agent Reach must chase that breakage. The ordered backend design reduces the cost but does not eliminate it.

The skill-install behavior in [agent_reach/cli.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/cli.py) knows multiple agent directories and may create a default `~/.agents/skills` install. That is useful, but any tool writing into agent instruction roots deserves caution and clear review.

## What we can learn / steal

Steal the "backend list belongs to the platform" structure from [agent_reach/channels/base.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/channels/base.py). Platform integrations break differently, so the repair logic should live near the platform.

Steal the `doctor` pattern from [agent_reach/doctor.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/doctor.py): collect results, isolate exceptions per integration, scrub outputs at the final rendering boundary, and report exact status.

Steal the probe vocabulary from [agent_reach/probe.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/agent_reach/probe.py). "Missing", "broken", "timeout", and "error" are more actionable than "not working."

Steal the credential tests from [tests/test_doctor_credential_boundaries.py](https://github.com/Panniantong/Agent-Reach/blob/a19a171fa980a0785849596492e0af4db800c82f/tests/test_doctor_credential_boundaries.py). For agent infrastructure, a health check should never quietly become a credential extractor.

## How we could apply it

For our own agent tooling, I would copy the capability-layer stance. If a tool's job is to prepare agent access to external systems, it should publish a small diagnosis/configuration surface and let the agent invoke the best upstream command directly.

I would also reuse the channel registry shape for any integration matrix: one file per system, ordered backends, a real probe, user-visible remediation, and an `active_backend` field. That scales better than one giant installer with platform-specific conditionals scattered everywhere.

Finally, I would make every diagnostic command side-effect classified. Agent Reach shows that "doctor" commands can accidentally mutate state or read credentials unless someone names that risk in code.

## Bottom line

Agent Reach is noisy at the README layer but serious in the source. The reusable piece is the architecture: a platform capability registry, real backend probes, careful credential boundaries, safe local config writes, and source-controlled agent instructions that route agents to upstream tools instead of hiding the internet behind one brittle wrapper.
