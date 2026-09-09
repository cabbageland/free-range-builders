# TeamAI CLI

- Repo: `Tencent/teamai-cli`
- URL: https://github.com/Tencent/teamai-cli
- Date: 2026-09-09
- Repo snapshot studied: `main` @ `6ae0619d067b1699bb2c6e435abf3ffe11a21d71`
- Why picked today: GitHub's daily trending page listed `Tencent/teamai-cli` with 1,083 stars today. I picked it because it is not just another agent prompt wrapper: the repository has a real TypeScript CLI, provider adapters, hook reconciliation, team-resource sync, package distribution, and a graph-backed team knowledge subsystem.

## Executive summary
[`Tencent/teamai-cli`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71) is a command-line harness for making a team of AI-agent users share the same skills, rules, docs, hooks, MCP config, environment settings, agents, and learned knowledge. The top-level [`README.md`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/README.md) frames it as "Team Execution x Team Context x Team Improvement": distribute the team's operating system, recall team knowledge, and turn useful session friction into shared learnings.

The implementation is more serious than the slogan. [`src/index.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/index.ts) exposes a broad Commander command surface, but lazy-loads modules so each command owns its own behavior. [`src/config.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/config.ts) and [`src/types.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/types.ts) carry most of the schema and path discipline. [`src/providers/registry.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/registry.ts) routes GitHub, GitLab, GitCode, CNB, TGit, and generic Git remotes. [`src/hooks.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hooks.ts) reconciles host-specific hook formats, while [`src/hook-dispatch.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hook-dispatch.ts) fans a single hook event out to multiple isolated handlers.

The smartest part is that TeamAI treats team behavior as a Git-backed resource graph rather than one global prompt. The weakest part is surface area: sync, hooks, roles, projects, sources, package install, recall, dashboards, and codebase indexing are all in one CLI, so correctness depends on a lot of path, lock, and migration details staying boring.

## What they built
They built an npm-distributed TypeScript CLI. [`package.json`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/package.json) publishes the binary as `teamai`, builds with `tsup`, tests with `vitest`, and depends on practical CLI libraries such as `commander`, `simple-git`, `yaml`, `zod`, `gray-matter`, `tree-sitter-wasms`, and `web-tree-sitter`.

Functionally, the CLI does four jobs:

- Bootstrap a team repo and local install with [`src/init.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/init.ts).
- Pull shared resources into local AI tools through [`src/pull.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/pull.ts) and resource handlers under [`src/resources`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/resources).
- Push local changes back to the team repo and provider review flow through [`src/push.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/push.ts) and adapters under [`src/providers`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers).
- Build and recall team knowledge through [`src/codebase.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/codebase.ts), [`src/codebase-extract.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/codebase-extract.ts), [`src/code-knowledge-recall.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/code-knowledge-recall.ts), and the [`src/wiki-engine`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine) modules.

It also ships bundled resources: [`agents/teamai-recall.md`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/agents/teamai-recall.md), skills under [`skills/team-wiki-codebase`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/skills/team-wiki-codebase) and [`skills/teamai-share-learnings`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/skills/teamai-share-learnings), and design docs such as [`docs/designs/data-directory-layout.md`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/docs/designs/data-directory-layout.md).

## Why it matters
Most agent-team tools are either a shared prompt file or a hosted collaboration product. TeamAI sits in the middle: it uses Git as the transport and review layer, then reconciles team resources into whichever local agent tools a developer actually uses.

That is a useful architecture because AI-team consistency is not only a model problem. It is a distribution problem. If a team wants every member's Claude Code, Codex, Cursor, OpenCode, CodeBuddy, WorkBuddy, Qoder, and internal tools to inherit the same skills and rules, the hard parts are file formats, local paths, hook semantics, per-machine config, migration, and failure isolation. Those are exactly the places this repo spends code.

The codebase is also a good example of an agent product acknowledging that memory has two shapes. The static shape is skills, rules, docs, and env. The dynamic shape is learnings, codebase graphs, recall, session reporting, and dashboard data. The split is visible in [`README.md`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/README.md) and in the separate modules for pull/push versus [`src/codebase-extract.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/codebase-extract.ts) and [`src/code-knowledge-recall.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/code-knowledge-recall.ts).

## Repo shape at a glance
The top-level shape is:

- [`README.md`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/README.md) and [`README.zh-CN.md`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/README.zh-CN.md): product explanation and usage.
- [`package.json`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/package.json): npm binary, build/test scripts, dependencies, and package metadata.
- [`src`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src): the CLI implementation.
- [`src/__tests__`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/__tests__): a large Vitest suite covering config, hooks, providers, sync, recall, path safety, package distribution, and migrations.
- [`src/providers`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers): provider-specific Git hosting adapters.
- [`src/resources`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/resources): handlers for skills, rules, docs, env, agents, hooks, MCP, and format conversion.
- [`src/wiki-engine`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine): code-fact extraction, AST adapters, graph index, call-chain tracing, and wiki protocol.
- [`docs`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/docs): usage docs and design notes.
- [`examples/ci`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/examples/ci): CI examples for codebase linting and MR extraction.
- [`skills`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/skills) and [`agents`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/agents): bundled agent-facing resources the CLI can distribute.

## Layered architecture dissection
### High-level system shape
TeamAI is a Git-backed resource synchronizer plus local agent integration layer. A team admin puts skills, rules, docs, hooks, MCP config, env, and knowledge in a shared repo. A developer runs `teamai init`, then hooks and commands keep local agent directories synchronized. Higher-level commands push changes back through the team's Git provider and recall useful team knowledge into future AI sessions.

### Main layers
**1. CLI and command routing layer**  
[`src/index.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/index.ts) is the outer shell. It defines commands such as `init`, `pull`, `push`, `status`, `list`, `skill`, `roles`, `projects`, `tags`, `source`, `env`, `hooks`, `mcp`, `digest`, `dashboard`, `contribute`, and `recall`. The file also runs a narrow pre-action migration hook for write commands so old `.teamai` layouts can move before `init`, `pull`, or `push` touch state.

**2. Config, path, schema, and safety layer**  
[`src/types.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/types.ts) defines `zod` schemas for tool paths, sharing config, source subscriptions, hooks, MCP policy, recall, co-authoring, and more. [`src/config.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/config.ts) loads team and local config, resolves project/user scope, migrates legacy role state, and separates persisted config from runtime-only `dataHome`.

**3. Git and provider layer**  
[`src/providers/registry.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/registry.ts) detects providers from URLs and package distribution. It maps GitHub, TGit, CNB, GitLab, GitCode, self-hosted GitLab, and generic Git. Provider implementations live under [`src/providers/github`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/github), [`src/providers/gitlab`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/gitlab), [`src/providers/gitcode`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/gitcode), [`src/providers/cnb`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/cnb), [`src/providers/tgit`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/tgit), and [`src/providers/git`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/git).

**4. Resource sync layer**  
[`src/pull.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/pull.ts) refreshes the team repo or HTTP backend, resolves active role/project namespaces, filters resources by tags, and deploys through handlers from [`src/resources/index.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/resources/index.ts). [`src/push.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/push.ts) stages selected local resources, filters missing top-level paths before `git add`, creates or reuses a branch, and asks the selected provider to create a PR or MR.

**5. Hook integration layer**  
[`src/hooks.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hooks.ts) knows that Claude-like tools, Cursor, Codex, ZCode, and OpenClaw-family tools use different hook file formats and trust semantics. It reconciles built-in and team-declared hooks idempotently. [`src/hook-dispatch.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hook-dispatch.ts) turns one hook command into a fan-out dispatcher with `Promise.allSettled`, per-handler timeouts, background handlers, and output merging.

**6. Knowledge and recall layer**  
[`src/codebase.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/codebase.ts) gathers repository context and generates `codebase.md`. [`src/codebase-extract.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/codebase-extract.ts) builds structured code facts, graph indexes, evidence pages, routers, hot pages, interface inventories, call chains, and knowledge gaps using adapters from [`src/wiki-engine/adapters`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine/adapters) and extractors under [`src/wiki-engine/code-knowledge`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine/code-knowledge). [`src/code-knowledge-recall.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/code-knowledge-recall.ts) searches those pages with BM25 plus graph-neighbor boosts.

### Request / data / control flow
1. A developer runs a command registered in [`src/index.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/index.ts), or an AI-tool hook fires `teamai hook-dispatch`.
2. The CLI loads local/team config through [`src/config.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/config.ts) and validates schemas from [`src/types.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/types.ts).
3. For sync, [`src/pull.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/pull.ts) refreshes the team repo, resolves roles/projects/tags, and hands resources to [`src/resources`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/resources) handlers.
4. For contribution, [`src/push.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/push.ts) copies selected resources into the team repo, commits a branch, and routes PR/MR creation through [`src/providers/registry.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/registry.ts).
5. For hooks, [`src/hooks.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hooks.ts) writes host-specific hook entries, and [`src/hook-dispatch.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hook-dispatch.ts) isolates concurrent handlers when events arrive.
6. For knowledge, [`src/codebase-extract.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/codebase-extract.ts) produces graph-backed wiki material, and [`src/code-knowledge-recall.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/code-knowledge-recall.ts) retrieves relevant pages later.

## Key directories and files
- [`package.json`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/package.json): binary, scripts, dependencies, package name, and npm release shape.
- [`src/index.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/index.ts): command registration and migration guard.
- [`src/init.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/init.ts): initialization, scope resolution, role/project setup, repo handling, and local agent selection.
- [`src/pull.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/pull.ts): resource deployment and role/project/tag filtering.
- [`src/push.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/push.ts): branch, commit, PR/MR, and pending-push handling.
- [`src/config.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/config.ts): config loading, migration, project data homes, and scope detection.
- [`src/types.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/types.ts): shared schemas and policy defaults.
- [`src/hooks.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hooks.ts): hook reconciliation across AI tools.
- [`src/hook-dispatch.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hook-dispatch.ts): concurrent hook handler fan-out and output merging.
- [`src/providers`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers): platform adapters and provider detection.
- [`src/resources`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/resources): install/sync handlers for each resource kind.
- [`src/wiki-engine`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine): graph-backed team wiki engine.
- [`src/__tests__`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/__tests__): the strongest evidence that this is production-minded rather than a demo CLI.

## Important components
`detectProvider` and `getProvider` in [`src/providers/registry.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/registry.ts) are central because every team repo operation depends on the right hosting adapter. The file's distribution-based fallback, where public `teamai-cli` defaults to GitHub and Tencent's internal package defaults to TGit, is a clever way to make one codebase serve two ecosystems.

The hook reconciler in [`src/hooks.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hooks.ts) is the gnarly integration component. It has to know the difference between Claude-shaped settings, Cursor hooks JSON, Codex hooks JSON and trust gates, ZCode process hooks, and OpenClaw-family `HOOK.md` behavior.

The dispatcher in [`src/hook-dispatch.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hook-dispatch.ts) is a good local reliability pattern. It reads one event, filters matched handlers, runs them concurrently with timeouts, uses `Promise.allSettled`, and merges compatible JSON outputs so one slow or broken handler does not break all hook behavior.

The wiki engine under [`src/wiki-engine`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine) is the ambitious component. Files such as [`src/wiki-engine/code-knowledge/code-collector.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine/code-knowledge/code-collector.ts), [`src/wiki-engine/code-knowledge/code-graph.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine/code-knowledge/code-graph.ts), [`src/wiki-engine/code-knowledge/ast/parser-registry.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine/code-knowledge/ast/parser-registry.ts), and [`src/wiki-engine/core/graph-index.schema.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine/core/graph-index.schema.ts) turn a codebase into evidence pages instead of dumping unstructured text into recall.

## Important knobs / configs / extension points
- [`teamai.yaml`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/types.ts): represented by `TeamaiConfigSchema` in [`src/types.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/types.ts), with sharing controls for hooks, recall, MCP, env, co-authoring, and contribution hints.
- Install scope in [`src/init.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/init.ts): `project` versus `user` scope changes where resources and machine state live.
- Tool paths in [`src/types.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/types.ts): `skills`, `rules`, `settings`, `claudemd`, `agents`, `mcp`, and `mcpProject` define how each local agent is touched.
- Provider override in [`src/providers/registry.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/registry.ts): `TEAMAI_DEFAULT_PROVIDER`, package name, and URL host all influence provider selection.
- Hook sharing policy in [`src/types.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/types.ts): `autoApply` and `requireTeamScripts` let teams choose how much hook power to distribute automatically.
- Recall enablement in [`src/types.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/types.ts): team default and user override decide whether the built-in [`agents/teamai-recall.md`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/agents/teamai-recall.md) becomes active.
- Source subscriptions in [`src/types.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/types.ts): `sources` and public skill settings make cross-team skill reuse a first-class path.

## Practical questions and answers
**Is this an agent framework or a config sync tool?**  
It is both, but the reliable core is config/resource sync. The agent-framework story comes from the resources it syncs and the hooks it installs. [`src/resources`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/resources) and [`src/hooks.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hooks.ts) are more important than any single prompt.

**Where is the highest-risk code?**  
Anything touching local paths, hooks, and Git state. [`src/config.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/config.ts), [`src/hooks.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hooks.ts), [`src/pull.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/pull.ts), and [`src/push.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/push.ts) are the places where a bad assumption could overwrite local behavior or dirty the wrong repo.

**What is the real product insight?**  
Team learning has to be operationalized. [`src/codebase-extract.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/codebase-extract.ts) and [`src/code-knowledge-recall.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/code-knowledge-recall.ts) show an opinionated path: transform repo facts into navigable evidence pages, then retrieve with both text relevance and graph neighborhood signals.

**Would I deploy this casually across a team?**  
Not without piloting. The hook system is powerful, and [`src/hooks.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hooks.ts) explicitly has to manage trust gates and host differences. I would start with skills/rules/docs sync, then enable hooks and recall after auditing the exact resources in the team repo.

## What is smart
- The command shell in [`src/index.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/index.ts) lazy-loads implementations, which keeps startup and command ownership sane.
- The provider registry in [`src/providers/registry.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/registry.ts) handles public and internal Git host defaults from one package.
- [`src/hooks.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hooks.ts) treats hook reconciliation as idempotent state management, not append-only string hacking.
- [`src/hook-dispatch.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hook-dispatch.ts) isolates hook handlers with `Promise.allSettled` and timeouts, which is the right failure model for host hooks.
- [`src/code-knowledge-recall.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/code-knowledge-recall.ts) combines BM25 with graph boosts instead of pretending vector search alone solves codebase memory.
- The test suite under [`src/__tests__`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/__tests__) covers many regression-prone areas: hook formats, provider detection, path safety, partitions, recall, package commands, and migration.

## What is flawed or weak
- The CLI surface in [`src/index.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/index.ts) is very wide. Wide command surfaces need relentless docs and compatibility discipline.
- The product depends on many external host conventions: Claude-style settings, Cursor hooks, Codex trust behavior, ZCode config, OpenClaw-family hooks, and multiple Git providers. [`src/hooks.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hooks.ts) has to encode those differences manually.
- The knowledge layer in [`src/wiki-engine`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine) is ambitious enough that quality will depend on extractor precision. The repo has AST adapters, but code knowledge can degrade quickly if extraction confidence is not surfaced clearly to users.
- The README's table of supported agent features in [`README.md`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/README.md) is broad. A builder should verify the specific host/tool version they care about before trusting every checkmark.

## What we can learn / steal
- Use Git as the reviewable transport for team agent behavior before building a bespoke server.
- Separate team-owned resources from machine-local state, the way [`src/config.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/config.ts) separates persisted config from runtime `dataHome`.
- Reconcile generated hook/config state idempotently, as [`src/hooks.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hooks.ts) does, instead of appending snippets repeatedly.
- Route provider differences behind small adapters like [`src/providers/github/index.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/github/index.ts) and [`src/providers/gitlab/index.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/providers/gitlab/index.ts).
- Make recall inspectable. [`src/codebase-extract.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/codebase-extract.ts) writes evidence pages and graph indexes, which are easier to debug than opaque memory blobs.

## How we could apply it
For our own agent-team workflows, I would copy the Git-backed resource model and the hook-dispatch isolation pattern first. A minimal version would have a shared repo with `skills`, `rules`, `docs`, and `hooks`, plus an idempotent installer per host. I would add the knowledge graph only after the sync layer is boring, because [`src/wiki-engine`](https://github.com/Tencent/teamai-cli/tree/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/wiki-engine) is useful but much harder to keep trustworthy.

The most reusable local pattern is from [`src/hook-dispatch.ts`](https://github.com/Tencent/teamai-cli/blob/6ae0619d067b1699bb2c6e435abf3ffe11a21d71/src/hook-dispatch.ts): one host hook, multiple handlers, isolated failure, merged output. That is a clean building block for any agent harness.

## Bottom line
`Tencent/teamai-cli` is worth studying because it attacks the unglamorous part of agent adoption: getting a whole team to share behavior, context, and lessons without everyone maintaining their own pile of local prompts. The architecture is heavy, but the pieces are concrete: a Commander CLI, Git provider adapters, resource handlers, hook reconciliation, a safe dispatcher, and a graph-backed knowledge subsystem.

The builder lesson is to treat agent behavior as source-controlled infrastructure. The caution is that once you manage local hooks and multiple agent configs, the product becomes a reliability system, not just a clever prompt distribution tool.
