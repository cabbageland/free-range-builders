# text-to-cad

- Repo: earthtojake/text-to-cad
- URL: https://github.com/earthtojake/text-to-cad
- Date: 2026-10-05
- Repo snapshot studied: main at d749a1980d806c7fed344b115651ccf1d8cfb28d
- Why picked today: Daily GitHub trending surfaced this as a hot agent/CAD project, and the repo has much more substance than the tagline suggests: a Python CAD runtime, agent skills, MCP app integration, shared viewer packages, and serious example models.

## Executive summary

[text-to-cad](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d) is not just a prompt-to-mesh wrapper. It is a local CAD operating layer for agents: the agent gets skills and plugin manifests, model scripts run through a pinned Python package named [cadgen](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen), CAD artifacts are saved as normal files, and an MCP app/viewer lets the human inspect STEP/STL/GLB/3MF/DXF/URDF/SDF outputs beside the chat.

The best idea is its artifact discipline. Source scripts are programs, generated documents are durable documents, and derived geometry/rendering state lives in a cacheable store. That separation shows up everywhere: in the cadgen package laws, the store builder, the viewer tunnel, and the skill docs that teach agents to edit source and inspect saved artifacts rather than hallucinate geometry from screenshots.

## What they built

They built a cross-agent CAD toolkit. The public install surface in the [root README](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/README.md) targets Claude Code, Claude Desktop, Codex, Cursor, Grok, Gemini, and generic skills.sh agents. Under that, the real runtime is [packages/cadgen](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen), a Python distribution that wraps build123d/Open CASCADE workflows, writes STEP and mesh outputs, manages a derived store, renders snapshots, and serves the CAD viewer.

The repo also ships a shared JavaScript viewer stack in [packages/core](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/core) and [packages/ui](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/ui), an MCP app host in [apps/mcp](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp), a browser app in [apps/web](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/web), and reusable agent-facing skills under [skills](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/skills).

## Why it matters

The common weak version of "AI CAD" is a model that emits a mesh or a script once. This repo treats CAD as an iterative engineering workflow: source files, deterministic-ish writers, sidecars, cache invalidation, file references, inspection tools, screenshots, model libraries, and agent-visible viewer state. That is the right frame if the goal is to let an agent safely revise a physical part instead of merely produce a pretty one-off asset.

It also matters because the integration target is the agent host, not a standalone SaaS UI. The [Codex plugin manifest](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/.codex-plugin/plugin.json), [Claude plugin manifest](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/.claude-plugin/plugin.json), [Cursor plugin manifest](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/.cursor-plugin/plugin.json), and [gemini-extension.json](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/gemini-extension.json) make the system portable across current agent shells.

## Repo shape at a glance

- [packages/cadgen](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen): Python engine, CLI, store, daemon, viewer server, MCP server, geometry readers, snapshot paths, and packaged browser/runtime assets.
- [packages/core](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/core): framework-independent JS/TS CAD client, render asset loading, geometry/render helpers, and worker-side mesh/surface machinery.
- [packages/ui](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/ui): reusable CAD viewer UI, file viewer, renderers, drawing tools, tab state, model library, host integration, and primitives.
- [apps/mcp](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp): MCP Apps page that hosts the shared viewer inside agent clients.
- [apps/web](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/web): browser-facing viewer/workbench adapter.
- [apps/docs](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/docs): documentation site and static examples.
- [skills](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/skills): agent instructions for CAD, DXF, DFM, 3D-printing/manufacturing checks, robot description formats, G-code, and vendor parts.
- [models](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/models): real example models and validation scripts, including complex showcases such as [models/w16](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/models/w16) and [models/tendon_hand](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/models/tendon_hand).
- [scripts](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/scripts): build, bundle, release, install, test, brand, and benchmark automation.

## Layered architecture dissection

### High-level system shape

The system is a stack around saved CAD documents. Agent-facing skills teach the agent how to create or edit Python source. Source scripts use cadgen decorators from files such as [packages/cadgen/src/cadgen/step.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/step.py) to write documents. The store code packages geometry into reusable trees and components. The viewer reads those documents and derived artifacts. MCP and web adapters make the same viewer available inside agent UIs or a browser.

### Main layers

The bottom layer is Open CASCADE/build123d access, isolated inside cadgen so heavy imports do not run at namespace load. The published package config in [packages/cadgen/pyproject.toml](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/pyproject.toml) is explicit about direct dependencies, the build123d version ceiling, Playwright, OCP, and bundled runtime assets.

The model/document layer is cadgen. [packages/cadgen/README.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/README.md) is unusually valuable because it documents laws: generated files must stand alone, the store contains only derived results, one sidecar belongs to one artifact, STEP/DXF bytes are pure geometry, and CLI doors operate on documents rather than source scripts.

The cache/packaging layer lives in [packages/cadgen/src/cadgen/store](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/store). [packages/cadgen/src/cadgen/store/build.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/store/build.py) walks a returned compound, decides whether child geometry remains an intact link or becomes this model's own components, publishes content-addressed BREP/component objects, and separates native geometry readiness from later surface extraction.

The UI/data-access layer is split between [packages/core/src/lib/renderAssetClient.js](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/core/src/lib/renderAssetClient.js), which caches and loads CAD render assets, and [packages/ui/src/cad-viewer/CadViewer.tsx](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/ui/src/cad-viewer/CadViewer.tsx), which composes the shared viewer, model library, renderers, host actions, settings, thumbnails, and error states.

The host layer lives in both Python and TypeScript. [packages/cadgen/src/cadgen/mcp/server.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/mcp/server.py) defines the MCP tool surface and host presentation modes. [apps/mcp/src/host/tunnel.ts](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp/src/host/tunnel.ts) turns viewer HTTP traffic into `cad_http` tool calls with 4 MiB chunking so large model assets do not blow up JSON-RPC message limits.

### Request / data / control flow

A typical creation flow starts with the agent reading [skills/cad/SKILL.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/skills/cad/SKILL.md), writing or editing a Python model, and running the model as a program. A decorated function from [packages/cadgen/src/cadgen/step.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/step.py) emits a STEP document and optional sidecar. The store code under [packages/cadgen/src/cadgen/store](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/store) derives trees, bounds, tessellations, surfaces, and records from the saved document.

When a human or agent opens the file, [packages/cadgen/src/cadgen/viewer](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/viewer) serves catalog and artifact routes. In MCP mode, [packages/cadgen/src/cadgen/mcp/server.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/mcp/server.py) exposes `cad_show`, `cad_view`, `cad_screenshot`, and HTTP tunnel tools. The page in [apps/mcp/src/ModelView.tsx](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp/src/ModelView.tsx) renders the same [CadViewer](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/ui/src/cad-viewer/CadViewer.tsx) used elsewhere.

## Key directories and files

- [packages/cadgen/README.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/README.md): the architectural contract. This is the first file to read if changing the runtime.
- [packages/cadgen/pyproject.toml](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/pyproject.toml): dependency and packaging reality, including shipped runtime assets.
- [packages/cadgen/src/cadgen/step.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/step.py): public STEP decorator/verbs and the document-vs-source boundary.
- [packages/cadgen/src/cadgen/store/build.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/store/build.py): component/link packaging and content-addressed tree publication.
- [packages/cadgen/src/cadgen/_internal/cli_from_function.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/_internal/cli_from_function.py): generated CLI mirror layer, preventing drift between function signatures and command flags.
- [packages/cadgen/src/cadgen/mcp/server.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/mcp/server.py): MCP app server and presentation detection.
- [apps/mcp/src/host/tunnel.ts](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp/src/host/tunnel.ts): browser fetch over MCP tool calls, with chunking/range reads.
- [packages/core/src/lib/renderAssetClient.js](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/core/src/lib/renderAssetClient.js): cache-aware asset loader for GLB/STL/3MF/topology/URDF/SDF inputs.
- [packages/ui/src/cad-viewer/CadViewer.tsx](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/ui/src/cad-viewer/CadViewer.tsx): shared viewer composition.
- [skills/cad/SKILL.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/skills/cad/SKILL.md): agent workflow contract.
- [skills/cad/references/project-template.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/skills/cad/references/project-template.md): minimal model/assembly starters that reveal the intended source shape.

## Important components

The `cadgen` package is the center. It exposes format namespaces such as [cadgen.step](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/step.py), format-specific CLI modules under [packages/cadgen/src/cadgen/cli](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/cli), geometry helpers in [packages/cadgen/src/cadgen/geometry.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/geometry.py), scene readers in [packages/cadgen/src/cadgen/step_scene.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/step_scene.py), and the daemon/build pool under [packages/cadgen/src/cadgen/daemon](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/daemon).

The viewer stack is more mature than a demo. [CadViewer.tsx](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/ui/src/cad-viewer/CadViewer.tsx) keeps one file on screen, follows the catalog, renders home/library states, generates offscreen thumbnails, and lets host adapters supply navigation, settings, links, prompt destinations, update notices, analytics prompts, and full-size controls. That is product code, not a toy viewport.

The skill layer is also a component, not just docs. [skills/cad/SKILL.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/skills/cad/SKILL.md) turns the runtime into a reliable agent behavior: run model scripts, inspect saved STEP files, use `read_scene` for references, render snapshots for self-review, and avoid adding STEP just to satisfy a workflow when the model is mesh-only.

## Important knobs / configs / extension points

The most important runtime knobs are in [packages/cadgen/pyproject.toml](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/pyproject.toml): Python version, cadgen version, build123d/OCP bounds, Playwright pin, and bundled package data. For operators, install channels flow through manifests such as [claude.mcp.json](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/claude.mcp.json), [codex.mcp.json](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/codex.mcp.json), [cursor.mcp.json](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/cursor.mcp.json), and [gemini-extension.json](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/gemini-extension.json).

For authors, decorators in [packages/cadgen/src/cadgen/step.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/step.py), mesh exporters under [packages/cadgen/src/cadgen/stl.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/stl.py), [packages/cadgen/src/cadgen/glb.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/glb.py), and [packages/cadgen/src/cadgen/threemf.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/threemf.py), plus sidecar-capability areas like [packages/cadgen/src/cadgen/kinematics.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/kinematics.py), are the real extension points.

For host integrators, the extension point is presentation. [packages/cadgen/src/cadgen/mcp/server.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/mcp/server.py) distinguishes tabs, inline apps, and text clients. [apps/mcp/src/host/presentation.ts](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp/src/host/presentation.ts), [apps/mcp/src/host/sync.ts](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp/src/host/sync.ts), and [apps/mcp/src/host/prompt.ts](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp/src/host/prompt.ts) show where host capabilities are adapted.

## Practical questions and answers

Q: Is this a model generator or a CAD workflow runtime?  
A: Workflow runtime. The agent may generate source, but the system's durable contract is source scripts plus saved CAD documents plus derived store artifacts.

Q: What makes it robust for agents?  
A: The agent-facing instructions in [skills/cad/SKILL.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/skills/cad/SKILL.md) force a loop of edit source, run source, inspect saved artifacts, snapshot, and report checks. That turns vague "make me a bracket" behavior into a repeatable engineering loop.

Q: Where would I start if debugging a wrong render?  
A: First check whether the source wrote the intended document. Then follow document compilation through [packages/cadgen/src/cadgen/step.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/step.py), store publication in [packages/cadgen/src/cadgen/store/build.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/store/build.py), and viewer loading in [packages/core/src/lib/renderAssetClient.js](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/core/src/lib/renderAssetClient.js).

Q: What is the biggest implementation risk?  
A: The dependency stack is sharp. [packages/cadgen/pyproject.toml](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/pyproject.toml) admits cadgen reaches into build123d internals, so minor upstream changes can silently break assumptions. The repo counters this with strict version ceilings and tests, but it is still a real maintenance cost.

Q: Is the MCP viewer just a thin iframe?  
A: No. [apps/mcp/src/host/tunnel.ts](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp/src/host/tunnel.ts) implements an HTTP tunnel over tool calls with byte-range continuation. [packages/cadgen/src/cadgen/mcp/server.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/mcp/server.py) manages view state, presentation mode, analytics controls, and host instructions.

## What is smart

The strongest design choice is refusing to let source and artifact semantics blur. [packages/cadgen/README.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/README.md) states that generated files must be readable without source, the store must contain only derived data, and CLIs should take documents rather than scripts. That is exactly the line that keeps an agent workflow inspectable and recoverable.

The generated CLI layer in [packages/cadgen/src/cadgen/_internal/cli_from_function.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/_internal/cli_from_function.py) is also smart. It treats function signatures as the public contract and derives command parsers where possible, reducing the usual drift between Python API, CLI docs, and tests.

The viewer tunnel is pragmatic. Rather than pretending agent-host iframes have ordinary network access, [apps/mcp/src/host/tunnel.ts](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp/src/host/tunnel.ts) explicitly chunks responses, validates range continuity, and builds a CAD client over that transport.

## What is flawed or weak

The system is powerful but heavy. A first install can pull Python, build123d, OCP, Playwright browser assets, bundled JavaScript, and model/viewer caches. The [root README](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/README.md) explains this, but the user experience will still depend on network reliability and disk space.

The stack has many host-specific seams even though the authors work hard to centralize them. [packages/cadgen/src/cadgen/mcp/server.py](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/src/cadgen/mcp/server.py) carries tabs/inline/text distinctions, while [apps/mcp/src/host](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp/src/host) adapts presentation, sync, capture, clipboard, and prompt capabilities. That is unavoidable today, but every new agent host is another integration surface.

The repo is also broad enough that onboarding could be hard. The laws in [packages/cadgen/README.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/README.md) are good, but a contributor still has to understand Python CAD kernels, browser rendering, MCP Apps, packaging, plugin distribution, and agent skills.

## What we can learn / steal

Steal the artifact boundary. If an agent creates something durable, make the saved artifact readable without the source, keep derived caches disposable, and put author intent in explicit sidecars only when the artifact needs it. That pattern from [packages/cadgen/README.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/cadgen/README.md) applies outside CAD.

Steal the "skills as operational contract" style. [skills/cad/SKILL.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/skills/cad/SKILL.md) is not a marketing tutorial; it defines what the agent should do, which references to read, how to validate, and what not to fake.

Steal the shared viewer split. Keeping domain client logic in [packages/core](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/core), reusable UI in [packages/ui](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/ui), and host adapters in [apps/mcp](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/mcp) and [apps/web](https://github.com/earthtojake/text-to-cad/tree/d749a1980d806c7fed344b115651ccf1d8cfb28d/apps/web) is the right shape for multi-host tools.

## How we could apply it

For any builder tool that produces inspectable artifacts, copy this pattern: source programs under version control, generated artifacts as first-class files, sidecars for non-geometric intent, derived caches that can be rebuilt, and a viewer that can be embedded in the agent workflow. The same architecture could work for PCB layouts, simulations, ETL artifacts, notebook outputs, or game assets.

If we were building our own agent plugin, I would also copy the package boundary from [packages/README.md](https://github.com/earthtojake/text-to-cad/blob/d749a1980d806c7fed344b115651ccf1d8cfb28d/packages/README.md): a runtime package, a framework-independent client/core package, a reusable UI package, and thin host apps.

## Bottom line

text-to-cad is interesting because it treats agentic CAD as a systems problem, not a prompt trick. The repo's best reusable lesson is that agent tools need durable artifact contracts, inspection loops, and host-aware UI plumbing if they are going to touch real engineering work.
