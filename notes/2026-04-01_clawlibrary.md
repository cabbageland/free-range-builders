# ClawLibrary

- Repo: `shengyu-meng/ClawLibrary`
- URL: <https://github.com/shengyu-meng/ClawLibrary>
- Date: 2026-04-01
- Why picked today: This is not the super-popular daily candidate, but it is a fun and revealing example: a pixel-game-style interface for OpenClaw that turns a messy runtime/filesystem into a navigable little world. It is interesting because it is both playful and surprisingly architectural.

## What they built

ClawLibrary is a **2D pixel-game-style control and browsing interface for OpenClaw**.

The core idea is not just “make a prettier dashboard.”
It is:
- take OpenClaw’s assets, memory, skills, logs, schedules, gateway/config pieces, queue/runtime state, and active work signals
- map them into a **small explorable museum / library world**
- let the user browse those resources through themed rooms instead of raw folders and status panes
- tie runtime activity to visible spatial behavior so the system feels alive rather than administrative

That is a surprisingly good product move.

A lot of agent tooling feels like:
- JSON
- sidebars
- accordions
- generic admin panels

ClawLibrary instead asks:

> what if the system were a place?

And that one design question carries a lot of the project.

## Why it matters

The important thing here is not just that it is cute.

It matters because it is attacking a real UX problem:
- systems like OpenClaw accumulate many heterogeneous assets and state surfaces
- users need to answer both:
  - what exists?
  - what is happening right now?

The usual answer is:
- folder trees
- logs
- dashboards
- status lists

ClawLibrary says:
- classify resources into semantic partitions
- project those partitions into rooms
- give activity a physical route/movement metaphor
- make the runtime inspectable through spatial UI

That is a much more human-centered interface idea.

It is also a good example of how “playful” can still be serious product design.

## How it works

At a high level, the system seems to have four layers:

1. **render/runtime layer**
   - Phaser-based 2D UI
   - Vite + TypeScript app shell

2. **world-definition / protocol layer**
   - JSON manifests for map layout, assets, scene art, and work-state mapping

3. **telemetry bridge layer**
   - Node script that reads OpenClaw state/filesystem/runtime information and converts it into the shape the UI can consume

4. **interaction / inspection layer**
   - room routing
   - asset menus
   - preview modals
   - debug overlays
   - actor movement / status behavior

That split is one of the strongest things in the repo.

This project is not just “a canvas with hardcoded coordinates.”
It is trying to make the world data-driven.

## Architecture / components

## Frontend runtime

From `package.json`:
- `phaser` for the world/UI runtime
- `vite` for dev/build
- `typescript`
- `playwright`, `pixelmatch`, `sharp` for QA / visual regression support

That is a smart stack choice.

Why Phaser is a good fit here:
- room/world metaphor
- actor movement
- layered sprites/occlusion
- easy stateful 2D interaction
- enough game-engine affordances without needing a huge custom rendering system

This would have been much more awkward as a conventional React dashboard pretending to be spatial.

## Data / manifest layer

The repo README surfaces several core files:
- `src/data/map.logic.json`
- `src/data/asset.manifest.json`
- `src/data/scene-art.manifest.json`
- `src/data/work-output.protocol.json`

That is the real center of gravity.

### `map.logic.json`
This describes the spatial logic of the world:
- render layers
- rooms
- room bounds
- label anchors
- walk zones
- presumably graph/pathing semantics further down the file

From the visible sample, rooms include:
- document
- mcp
- images
- memory
- log
- schedule
- skills
- gateway
- agent
- break_room
- task_queues
- alarm

This is good because the room model is not hardcoded only in scene code.

### `asset.manifest.json`
This likely describes logical asset types/resources available to the UI.

### `scene-art.manifest.json`
This appears to separate visual bindings from logical room/resource structure.

That is a very good design choice.

It means:
- art can change
- themes can change
- actor skins can change
- layout/logic can remain stable

### `work-output.protocol.json`
This is especially interesting.

It suggests the project is formalizing how work-state / outputs map into the visual world, rather than just shoving arbitrary runtime events into the UI.

That is a sign of discipline.

## Runtime scene

Key runtime files include:
- `src/runtime/scene/LibraryScene.ts`
- `src/runtime/systems/protocolStore.ts`
- `src/runtime/systems/growth.ts`
- `src/runtime/systems/touchController.ts`
- `src/core/pathfinder.ts`
- `src/core/geometry.ts`

This suggests the scene is backed by dedicated subsystems for:
- state/protocol ingestion
- movement/pathing
- interaction/input
- progression/growth logic

That is much cleaner than dumping everything into one giant scene file.

## Telemetry bridge

The most revealing backend-ish file is:
- `scripts/openclaw-telemetry.mjs`

This script appears to:
- read OpenClaw home/workspace roots from config
- inspect many classes of resources
- build resource partitions like:
  - documents
  - images
  - memory
  - skills
  - gateway
  - logs
  - schedule
  - alarms
  - agents
  - task queues
  - break room
- scan filesystem trees with heuristics and extension filters
- maintain caches
- emit activity/resource snapshots for the frontend

This is not just “read a single JSON status file.”
It is more like a domain-specific telemetry adapter for OpenClaw.

That is probably the most important hidden layer in the project.

## Important knobs / configs / extension points

One of the nicest things in the repo is that the config surface is visible and not absurd.

From the README / config example:
- `clawlibrary.config.json`

Includes:
- OpenClaw paths:
  - `openclaw.home`
  - `openclaw.workspace`
- server:
  - `host`
  - `port`
- UI:
  - `defaultLocale`
  - `showDebugToggle`
  - `defaultDebugVisible`
  - `showInfoToggle`
  - `defaultInfoPanelVisible`
  - `showThemeToggle`
- actor:
  - `defaultVariantId`
- telemetry:
  - `pollMs`

That is a healthy config design.

Good qualities:
- public-facing config file at repo root
- env overrides still possible
- no single hardcoded machine path
- standard OpenClaw default paths supported automatically

That is exactly how a shareable OpenClaw-adjacent app should behave.

## Practical questions and answers

## Q1. Is this mostly a skin, or is there real system design here?

It is more than a skin.

The evidence:
- separate protocol/data manifests
- dedicated telemetry bridge
- explicit resource partition model
- map logic / walk graph structure
- QA scripts for movement and visual regression

So yes, it is playful, but it also has real architecture under the art layer.

## Q2. What is the strongest design idea?

The strongest idea is:

> turning heterogeneous system state into a spatially organized world with semantic rooms.

That is the leap.

Everything else — actor movement, previews, menus, debug overlays — is downstream of that decision.

## Q3. Why Phaser instead of a normal web dashboard stack?

Because this is fundamentally a spatial, layered, animated interface.

Phaser gives them:
- scene graph-ish structure
- layering/depth
- world coordinates
- motion
- interaction primitives
- room/actor metaphors that feel natural

A plain dashboard stack would make this much more painful or fake.

## Q4. What is especially smart technically?

A few things:
- logic/art split through manifests
- public config entrypoint + env override fallback
- visual QA scripts
- telemetry caching and partition heuristics
- making the art layer explicitly replaceable

That last one matters: they are not fusing product concept to one immutable art pass.

## Q5. Where would this likely get painful?

The telemetry heuristic layer.

Why:
- once you classify many resource types via filesystem/runtime signals, edge cases grow fast
- weird custom installs or path layouts will stress the assumptions
- category boundaries can drift over time
- "what room should this belong to?" becomes a product+taxonomy problem, not just engineering

That is probably where the long-term entropy lives.

## Q6. Is the room metaphor just delight, or does it improve usability?

Potentially both.

If done well, it improves:
- orientation
- memorability
- emotional legibility
- “where should I look?” intuition

But there is a risk:
- if the metaphor gets too cute or overloaded, it can become harder to use than a plain panel

So the key challenge is keeping the spatial metaphor informative rather than ornamental.

## Q7. What does a builder notice that a casual viewer might miss?

A casual viewer sees:
- cute pixel game UI

A builder should notice:
- protocol/data-driven design under it
- configuration discipline
- telemetry adaptation layer
- art/logic separation
- QA support for movement and visuals

That is where the project becomes much more respectable.

## What is smart

## 1. The logic/art separation

This is the strongest engineering instinct in the repo.

By separating:
- map logic
- asset manifests
- scene art bindings

…the project becomes much more maintainable and extensible.

That is exactly the right move for something with a strong aesthetic layer.

## 2. Telemetry as an adapter layer

The `openclaw-telemetry.mjs` approach is smart because it isolates the mess of:
- filesystem reality
- OpenClaw runtime state
- resource heuristics

…from the frontend scene itself.

That keeps the scene more about presentation and interaction.

## 3. Quality checks exist

Scripts like:
- `npm run validate`
- `npm run qa:movement`
- `npm run qa:visual`
- `npm run qa:visual:baseline`

show this is not pure toyland.

It is a playful app with at least some respect for regression control.

## 4. Public install/config story is decent

The README does a good job of making the project look shareable instead of one-machine-only.

That matters a lot for projects like this.

## What is flawed or weak

## 1. Heuristic resource classification is inherently brittle

The telemetry script appears to infer a lot through path patterns and extension classes.

That is practical, but brittle.

Likely weaknesses:
- misclassification
- edge cases across user setups
- category drift as OpenClaw evolves
- hard-to-explain "why did this appear in that room?"

## 2. The metaphor could overgrow the product

A spatial museum UI is cool.
But it can also become:
- too precious
- too slow to navigate
- too abstract for power users

The project has to keep proving that the room metaphor improves comprehension rather than just aesthetics.

## 3. It may be more convincing as a concept than as a daily work surface

This is a common risk with beautifully themed interfaces.

Questions I’d still want answered by actual use:
- Is it faster than a plain dashboard for repeated tasks?
- Does the novelty wear off?
- Does the spatial model stay mentally stable as the system grows?

## 4. The data schema burden is real

Once a project has:
- map logic schema
- art manifest schema
- asset manifest schema
- output/work protocol schema

…it gains structure, but also maintenance overhead.

That is worth it if the UI keeps evolving. Less worth it if the project stalls.

## What we can learn / steal

## 1. “Make the system a place”

This is the biggest stealable idea.

Not always literally, but conceptually:
- spatialize complex state
- group by meaning, not raw storage layout
- tie runtime activity to visible regions

That is a powerful interface move.

## 2. Separate world logic from art aggressively

Very reusable lesson.

If a UI is aesthetic-heavy, keep:
- behavior/layout semantics
- visual assets/bindings

separate from the start.

## 3. Build a telemetry adapter instead of letting UI read everything directly

This is important.

The UI should not have to understand every filesystem/runtime wrinkle.
A translation layer helps a lot.

## 4. Delight can coexist with engineering discipline

This repo is a nice example that:
- playful does not have to mean sloppy
- pixel art does not mean unserious

That is a useful reminder.

## How we could apply it

A few concrete applications:

## For OpenClaw / related systems
- build more room/world-like interfaces for complicated runtime state
- use semantic zones instead of admin-panel buckets
- expose active work spatially, not only textually

## For our own product ideas
- use the “living archive” metaphor where systems are otherwise too abstract
- separate visual identity from control logic early
- if a system has lots of heterogeneous artifacts, consider a browseable world model instead of a raw tree

## For repo-study taste
- this is a good example of a project that is interesting not because it is huge, but because it has a **clear aesthetic thesis backed by real implementation structure**

## Bottom line

ClawLibrary is a fun repo, but it is not just cute.

At its best, it is trying to solve a serious interface problem:
- how do you make a complex agent system’s assets and runtime state feel legible, alive, and navigable?

Its best ideas are:
- world-as-interface
- protocol/manifests for spatial logic
- telemetry bridge as adapter
- replaceable art layer
- enough QA to take the experience seriously

Its biggest risk is that the metaphor and heuristics could become more fragile than the payoff.

If I had to summarize it in one line:

> ClawLibrary is a pixel-museum interface for OpenClaw that is interesting precisely because it tries to turn operational complexity into a place you can understand, not just a dashboard you can click through.
