# OpenRig

- Repo: mvschwarz/openrig
- URL: https://github.com/mvschwarz/openrig
- Date: 2026-09-30
- Repo snapshot studied: `main` commit `f8f3aff68bf425735173df9e2c5ac5ef19716f5b`
- Why picked today: It was high on GitHub daily trending, and unlike shallow agent wrappers it exposes a real local control plane: daemon, CLI, terminal UI, React UI, runtime adapters, queueing, restore logic, docs, demo rigs, and Docker testbeds.

## Executive summary

[OpenRig](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b) is a local operating system for teams of coding agents. The idea is simple: instead of a pile of independent Claude Code and Codex terminal sessions, define a rig in YAML, launch seats into tmux, keep identity/state in a local daemon, and give both humans and agents a command surface for sending work, restoring sessions, reading transcripts, and seeing what needs attention.

The strongest part is that OpenRig treats agent coordination as an infrastructure problem. It has a [daemon package](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon), a broad [CLI](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/cli), a keyboard-heavy [TUI](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/tui), and a maintenance-mode [React UI](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/ui). The most useful lesson is not "multi-agent teams are magic." It is that agent teams need explicit topology, delivery, restore honesty, queue state, and operator surfaces.

## What they built

OpenRig ships a TypeScript monorepo for running multi-agent coding topologies locally:

- [README.md](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/README.md) explains the product loop: define teams, launch with `rig up`, inspect with `rig tui`, send tasks, and use the same managed seats over time.
- [package.json](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/package.json) defines a Node 22/24 workspace with `packages/daemon`, `packages/ui`, `packages/cli`, and `packages/tui`.
- [packages/daemon/src/startup.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/startup.ts) wires the SQLite-backed daemon, migrations, tmux adapter, runtime adapters, queue, restore, context, transport, and route dependencies.
- [packages/daemon/src/server.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/server.ts) exposes the Hono HTTP API for rigs, sessions, adapters, packages, transport, queue, workflow, health, terminal, files, proof, gateway, restore checks, and more.
- [packages/daemon/src/domain/runtime-adapter.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/runtime-adapter.ts) defines the launch/projection/readiness contract for runtimes such as Claude Code, Codex, Pi, stub, and terminal.
- [packages/cli/src/index.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/cli/src/index.ts) registers the `rig` command surface.
- [packages/tui/src/main.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/tui/src/main.ts) implements the terminal UI entrypoint with live daemon hydration, command palette, crash recovery surface, keyboard/mouse input, and alternate-screen rendering.
- [docs/reference](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docs/reference), [docs/as-built](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docs/as-built), and [demo](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/demo) provide the operator docs, architecture docs, starter rig, and proof scripts.

## Why it matters

Most agent orchestration demos pretend the hard part is prompting. OpenRig points at the more stubborn operational layer: where sessions live, how they resume, how one agent hands work to another, how a human sees blocked work, and how to keep a local machine from becoming terminal sprawl.

It also matters because it is not cloud-first. The repo's contract is tmux, SQLite, local files, native agent CLIs, and optional terminal workspace tools. That gives builders a serious design reference for local-first agent infrastructure, even if they would not copy OpenRig directly.

## Repo shape at a glance

- [packages/daemon](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon): the local control plane. It owns SQLite migrations, Hono routes, runtime adapters, queue state, restore, transport, transcripts, bundles, health, and gateway surfaces.
- [packages/cli](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/cli): the `rig` executable. Command files cover setup, up/down, ps, send, queue, transcript, tui, terminal, workflow, gateway, provider, policy, restore, package, skill, plugin, and release tooling.
- [packages/tui](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/tui): a terminal-native operator UI with topology, attention, crash-cart, health, execution, terminal, and command-palette modules.
- [packages/ui](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/ui): a React/Vite UI with topology cards, rig graph, explorer, detail drawers, package/spec review, activity feed, workflow, and workspace pages.
- [packages/test-system](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/test-system): system scenarios and evaluation scaffolding.
- [docs/reference](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docs/reference): user/operator reference docs for getting started, specs, health, Slack, permissions, workspace, restore, and worktree builds.
- [docs/as-built/architecture](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docs/as-built/architecture): source-backed architecture modules. These are unusually detailed, though some version/count notes clearly trail current 0.6.2 source.
- [demo](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/demo): a runnable starter rig with lead, implementation, design, QA, and reviewer agents.
- [docker/testbed](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docker/testbed): testbed images and runbooks for repeatable scenarios.

## Layered architecture dissection

### High-level system shape

OpenRig is a daemon-centered local control plane. A human or agent runs `rig` commands from [packages/cli](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/cli). The CLI talks to the daemon built in [packages/daemon/src/startup.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/startup.ts) and exposed by [packages/daemon/src/server.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/server.ts). The daemon stores topology/session/queue state in SQLite, creates tmux sessions through [packages/daemon/src/domain/node-launcher.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/node-launcher.ts), projects runtime resources, then asks a runtime adapter to start Claude, Codex, terminal, Pi, or stub harnesses.

The TUI and UI are just operator surfaces on top of this daemon. [packages/tui/src/main.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/tui/src/main.ts) hydrates fleet state from the daemon and redraws a terminal interface. [packages/ui/src/App.tsx](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/ui/src/App.tsx) and the UI components expose the same broad product model in React.

### Main layers

The spec layer turns YAML and starter names into an intended topology. The README points users at [docs/reference/getting-started.md](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docs/reference/getting-started.md), and the source has [packages/daemon/src/domain/rigspec-schema.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/rigspec-schema.ts), [rigspec-preflight.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/rigspec-preflight.ts), and [rigspec-instantiator.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/rigspec-instantiator.ts).

The daemon layer is the source of truth. [startup.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/startup.ts) opens the database, applies [all migrations](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/db/all-migrations.ts), constructs repositories and services, creates runtime adapters, and finally builds the Hono app. [server.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/server.ts) mounts a very wide API surface: rigs, sessions, packages, bootstrap, discovery, bundles, transport, queue, workspace, workflow, health, gateway, terminal, files, proof, steering, and more.

The runtime layer sits behind [RuntimeAdapter](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/runtime-adapter.ts). Adapters implement `listInstalled`, `project`, `deliverStartup`, `launchHarness`, and `checkReady`. The concrete adapters include [claude-code-adapter.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/adapters/claude-code-adapter.ts), [codex-runtime-adapter.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/adapters/codex-runtime-adapter.ts), [terminal-adapter.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/adapters/terminal-adapter.ts), [pi-runtime-adapter.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/adapters/pi-runtime-adapter.ts), and [stub-runtime-adapter.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/adapters/stub-runtime-adapter.ts).

The communication layer is tmux-aware but tries not to lie about tmux. [session-transport.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/session-transport.ts) classifies pane activity, detects permission prompts and mid-work spinners, and sends messages through paste-buffer style delivery rather than shell arguments. [transcript-store.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/transcript-store.ts) and [history-query.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/history-query.ts) own transcript storage/search.

The queue and restore layers are where OpenRig becomes more than a session launcher. [queue-repository.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/queue-repository.ts) has explicit states such as `pending`, `in-progress`, `blocked`, `done`, `failed`, `canceled`, and `handed-off`, plus typed gate blockers, hot-potato closure, pickup receipts, human routing, and wake mechanics. [restore-orchestrator.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/restore-orchestrator.ts) handles restore outcomes and refuses to report non-running statuses as successful launches.

### Request / data / control flow

A normal launch path looks like this:

1. `rig up <starter>` is registered by [packages/cli/src/index.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/cli/src/index.ts) and implemented by command modules under [packages/cli/src/commands](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/cli/src/commands).
2. The daemon resolves/preflights the rig spec through [rigspec-schema.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/rigspec-schema.ts) and related rigspec services.
3. [NodeLauncher](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/node-launcher.ts) validates node identity, creates a tmux session with `OPENRIG_*` environment variables, starts transcript rotation, and atomically registers session and binding rows.
4. The chosen runtime adapter projects resources and launches the harness. [RuntimeAdapter](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/runtime-adapter.ts) makes fresh launch, resume token, and fork source explicit.
5. The user watches through [rig tui](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/tui/src/main.ts), the React UI, or `rig ps`.
6. Work moves through [session-transport.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/session-transport.ts), [queue-repository.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/queue-repository.ts), and route modules such as [routes/transport.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/routes/transport.ts) and [routes/queue.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/routes/queue.ts).

## Key directories and files

- [README.md](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/README.md): product promise, install path, starter rigs, machine modifications, and high-level architecture.
- [package.json](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/package.json): Node workspace and repo-level scripts.
- [packages/daemon/src/startup.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/startup.ts): dependency graph construction and daemon boot.
- [packages/daemon/src/server.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/server.ts): Hono route mount surface.
- [packages/daemon/src/domain/runtime-adapter.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/runtime-adapter.ts): runtime abstraction.
- [packages/daemon/src/domain/node-launcher.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/node-launcher.ts): tmux session creation, transcript rotation, and session/binding persistence.
- [packages/daemon/src/domain/session-transport.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/session-transport.ts): send/capture behavior and pane-activity classification.
- [packages/daemon/src/domain/queue-repository.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/queue-repository.ts): durable work queue state and handoff mechanics.
- [packages/daemon/src/domain/restore-orchestrator.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/restore-orchestrator.ts): snapshot/restore and launch outcome semantics.
- [packages/cli/src/index.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/cli/src/index.ts): CLI composition.
- [packages/tui/src/main.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/tui/src/main.ts): TUI runtime and live refresh loop.
- [docs/as-built/architecture/adapters-and-runtimes.md](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docs/as-built/architecture/adapters-and-runtimes.md): useful explanation of the runtime-adapter and resume-honesty model.
- [docs/as-built/architecture/transport-and-transcripts.md](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docs/as-built/architecture/transport-and-transcripts.md): useful explanation of tmux transport, transcripts, chat, and `rig ask`.

## Important components

- `createDaemon` in [startup.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/startup.ts): the dependency-composition root. It wires migrations, repositories, tmux, adapters, queues, restore, context monitor, and the app.
- `createApp` in [server.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/server.ts): the HTTP boundary and a quick view of how broad the daemon has become.
- `RuntimeAdapter` in [runtime-adapter.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/runtime-adapter.ts): the important seam. It stops runtime-specific details from leaking everywhere.
- `NodeLauncher` in [node-launcher.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/node-launcher.ts): the stateful bridge from rig topology to tmux process.
- `classifyPaneActivity` in [session-transport.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/session-transport.ts): a practical heuristic layer for "is this seat idle, active, or waiting for attention?"
- `QueueRepository` in [queue-repository.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/queue-repository.ts): where work items become durable coordination records instead of chat messages.
- `RestoreOrchestrator` in [restore-orchestrator.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/restore-orchestrator.ts): keeps restore outcomes explicit, including failed and attention-required states.
- `createProgram` in [packages/cli/src/index.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/cli/src/index.ts): shows how much operator surface the system exposes.
- TUI live loop in [packages/tui/src/main.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/tui/src/main.ts): the terminal UI is not a toy view; it has daemon startup, crash-cart, live invalidation, copy mode, and native attach behavior.

## Important knobs / configs / extension points

- Rig definitions and starters are the main extension point. See [demo/rig.yaml](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/demo/rig.yaml) and [docs/reference/rig-spec.md](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docs/reference/rig-spec.md).
- Runtime support is adapter-shaped. Adding a new harness means implementing the [RuntimeAdapter](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/runtime-adapter.ts) contract.
- Permission posture is explicit. The README's [machine-change section](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/README.md#what-openrig-changes-on-your-machine) and [docs/reference/getting-started.md](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docs/reference/getting-started.md) explain provider hooks, trust records, and command allowances.
- State location and daemon behavior are environment/config sensitive: `OPENRIG_HOME`, tmux availability, Codex/Claude auth, cmux/herdr terminal providers, and daemon bearer settings all matter.
- Queue behavior has many policy hooks in [queue-repository.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/queue-repository.ts), including priorities, gate blockers, handed-off lineage, evidence refs, and human routing.
- The TUI can run against a daemon URL, a local instance, or demo data through [packages/tui/src/main.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/tui/src/main.ts).

## Practical questions and answers

Q: Is OpenRig an agent framework?

A: Not in the usual "new prompt loop" sense. It is a control plane around existing native agent harnesses. The runtime adapters in [packages/daemon/src/adapters](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/adapters) launch and monitor Claude Code, Codex, terminal, Pi, and stub runtimes rather than replacing them.

Q: What is the core architectural bet?

A: Tmux plus SQLite is enough substrate for local multi-agent work if you add strong identity, queue, transcript, restore, and operator layers. [NodeLauncher](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/node-launcher.ts) is the bridge between tmux reality and daemon state.

Q: What is the best thing to copy?

A: The separation between transport and truth. [session-transport.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/session-transport.ts) does not treat "tmux accepted keystrokes" as "agent consumed the task." [queue-repository.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/queue-repository.ts) gives work durable state beyond chat scrollback.

Q: Where is the biggest operational risk?

A: Setup touches provider and workspace configuration. The README is honest about writes to `~/.tmux.conf`, Claude/Codex settings, hooks, trust records, tmux sessions, and OpenRig state. That is powerful but invasive.

Q: Would I deploy this as-is for a normal team?

A: I would test it carefully on a disposable project first. The design is serious, but the route surface, docs, and policy layers are broad enough that upgrades and local machine effects need discipline.

## What is smart

The runtime adapter seam is smart. [RuntimeAdapter](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/runtime-adapter.ts) isolates resource projection, startup delivery, harness launch, and readiness from the rest of the daemon. That makes "Claude vs Codex vs terminal" a runtime concern instead of a cross-cutting condition.

The restore-honesty posture is smart. [restore-orchestrator.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/restore-orchestrator.ts), [native-resume-probe.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/native-resume-probe.ts), and the adapter docs avoid the tempting lie that any relaunched terminal is "resumed." For agent infrastructure, that distinction matters.

The TUI-first operator surface is smart. [packages/tui](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/tui) fits the actual runtime: terminals, tmux, keyboard workflow, crash recovery, live updates, and direct attach.

The queue is also smart. [queue-repository.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/queue-repository.ts) encodes enough state to distinguish pending work, blocked work, cancellations, handed-off tasks, human decisions, and delivery failures. That is the difference between a swarm and a manageable system.

## What is flawed or weak

The complexity is high. [server.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/server.ts) mounts a huge surface, and [packages/daemon/src/domain](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain) contains many specialized services. That may be earned complexity, but it is still a lot for a new operator to trust.

Some architecture docs are visibly stale. For example [docs/as-built/architecture/daemon-core.md](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docs/as-built/architecture/daemon-core.md) describes an older package version and counts, while the root [package.json](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/package.json) is 0.6.2 and [server.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/server.ts) has a broader route surface. The docs are still useful, but readers must verify against source.

The product is inherently invasive. The README's [machine-change section](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/README.md#what-openrig-changes-on-your-machine) is unusually clear, but the fact remains: provider hooks, trust settings, tmux config, workspace files, and native agent CLIs are a big blast radius.

Pane-state detection is necessarily heuristic. [session-transport.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/session-transport.ts) has thoughtful prompt and spinner patterns, but terminal UIs change. This is a brittle boundary in every tmux-based agent controller.

Platform support is narrow: the README calls out macOS/Linux, Node 22/24, tmux, and no native Windows support. That is a reasonable initial product boundary, but it limits who can use the system without friction.

## What we can learn / steal

Steal the explicit topology model. Teams of agents should have named seats, pods, edges, and workspaces, not only chat aliases. [docs/reference/rig-spec.md](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/docs/reference/rig-spec.md) is the pattern to study.

Steal the adapter contract. Even if we never use OpenRig, [runtime-adapter.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/runtime-adapter.ts) is a clean way to think about launching and supervising different agent runtimes.

Steal the "transport is not truth" stance. A delivery system needs its own receipts, states, and failure modes. [queue-repository.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/queue-repository.ts) and [session-transport.ts](https://github.com/mvschwarz/openrig/blob/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/daemon/src/domain/session-transport.ts) make that concrete.

Steal the operator surfaces. [packages/tui](https://github.com/mvschwarz/openrig/tree/f8f3aff68bf425735173df9e2c5ac5ef19716f5b/packages/tui) shows that terminal UI can be the primary cockpit when the underlying work is terminal-native.

## How we could apply it

For our own agent tooling, I would copy three ideas without copying the whole system:

1. Define a small runtime adapter contract for launch, resume, readiness, and resource projection.
2. Put work state in a durable queue with explicit blocked, handed-off, and human-decision states.
3. Build an operator view that shows topology, activity, restore status, and attention items before adding more agent roles.

If we need a local multi-agent lab, OpenRig is worth testing directly. If we only need one or two durable sessions, the full control plane may be too much, but the source gives a strong checklist for what eventually breaks in ad hoc multi-agent setups.

## Bottom line

OpenRig is one of the more serious open-source attempts to treat coding agents as a managed local fleet rather than a pile of shells. It is complex and invasive, but the architecture is full of reusable lessons: explicit topology, runtime adapters, tmux transport with honest receipts, durable queues, restore semantics, and operator-first visibility.
