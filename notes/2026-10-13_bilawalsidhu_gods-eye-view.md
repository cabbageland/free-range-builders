# God's Eye View

- Repo: bilawalsidhu/gods-eye-view
- URL: https://github.com/bilawalsidhu/gods-eye-view
- Date: 2026-10-13
- Repo snapshot studied: main at commit 9beadbda6333b83f79aa03047e2d851830f01f6b
- Why picked today: It was near the top of GitHub daily trending with a real system behind the spectacle: a Cesium browser globe, many live public-data layers, Node provider middleware, a realtime voice controller, scene playback, offline-ish startup paths, and explicit source/license boundaries.

## Executive summary

[bilawalsidhu/gods-eye-view](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b) is a browser-based spatial-intelligence console. The README sells it as a "spy satellite simulator," but the useful builder story is how many messy public feeds are normalized into a single globe: aircraft, ships, satellites, launches, earthquakes, fires, weather, traffic, public cameras, street-level imagery, radio, and authored scene packs.

The source is much more structured than a viral demo usually is. [src/app/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/application.js) owns startup and teardown as four phases: scene, controls, data, and tools. [src/app/constructCatalog.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/constructCatalog.js) constructs a large catalog of layer modules. [server/providers](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/server/providers) owns Node-side API adapters and caches. [src/voice/realtimeController.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/voice/realtimeController.js) composes the OpenAI Realtime voice session. [src/director](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/director) and [docs/DIRECTOR.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/DIRECTOR.md) show a separate playback/document system for narrated scenes.

The smartest design move is that most features are shaped as explicit sources, layers, and services rather than a pile of globe callbacks. That does not make the app small. It is sprawling. But the sprawl is intentional enough to study.

## What they built

God's Eye View is a local web app built with Vite, Cesium, and browser modules. [package.json](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/package.json) describes it as a private app with exports for application construction, maps, sources, server providers, voice, scenes, annotations, and layer families. The dependency list is focused around Cesium, HLS playback, Mapillary, satellite orbital math, vector tiles, GRIB decoding, and test/build tooling.

The default product is the standalone app wired in [src/standalone/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/standalone/application.js). It creates place search, scene services, the layer catalog, controls, data registration, and tools. The same repo also exposes smaller construction APIs through [src/app/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/application.js), [src/app/viewer.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/viewer.js), [src/app/sources.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sources.js), and many package exports in [package.json](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/package.json).

The data story is mixed on purpose. [DATA_SOURCES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/DATA_SOURCES.md) lists live sources, bundled sources, licenses, attribution, and carve-outs. That document matters because the app is not just code. It is a product made of public APIs, provider terms, cached datasets, embedded assets, and browser-visible attribution.

## Why it matters

The project is interesting because it treats "live world dashboard" as a composition problem. The hard part is not rendering one feed on a map. The hard part is making many feed families feel coherent while preserving provider limits, different coordinate systems, camera behaviors, attribution, credential paths, offline fallbacks, and teardown.

For builders, the reusable lesson is the boundary discipline. [src/app/sourceComposition.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sourceComposition.js) defines contracts for each data family and turns missing providers into explicit "source unavailable" objects instead of silent empty datasets. [docs/CODE-BOUNDARIES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/CODE-BOUNDARIES.md) records which areas are portable browser exports, Node providers, standalone compatibility entries, and local setup code. [docs/VOICE-OWNERSHIP.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/VOICE-OWNERSHIP.md) does the same for realtime voice state.

## Repo shape at a glance

- [README.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/README.md): product narrative, quick start, key paths, feature list, and runtime caveats.
- [DATA_SOURCES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/DATA_SOURCES.md): attribution, live-source terms, bundled-source terms, and non-code license carve-outs.
- [src/app](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app): application lifecycle, source composition, layer catalog assembly, viewer/control/data/tool composition, and app-level services.
- [src/layers](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers): feature families such as flights, military aircraft, vessels, satellites, launches, CCTV, traffic, fires, transit, street level, ALPR, radio, and weather-related layers.
- [src/data](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/data): older data modules, parsers, source adapters, fixtures, local datasets, credits, state, and many unit tests.
- [server/providers](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/server/providers): Node middleware for live aircraft, vessels, places, terrain, weather, traffic, OpenAI voice, radio, Overpass, CCTVs, regional context, and space feeds.
- [src/maps](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/maps): map-source catalog, imagery, terrain, Google 3D tiles, provider availability, credits, tokens, and retry behavior.
- [src/voice](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/voice): realtime voice session, tool schemas, action runner, pointer context, viewport capture, turn metrics, radio handoff, and speech behavior.
- [src/director](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/director): scene playback, camera timelines, scene documents, data packs, interaction actions, and sharing.
- [docs](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/docs): architecture notes, ownership documents, QA notes, known issues, scene docs, voice docs, performance notes, and code-boundary records.
- [scripts](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/scripts): unit runner, boundary checks, source-generation utilities, many browser QA probes, Pinokio setup scripts, and source-specific validation scripts.

## Layered architecture dissection

### High-level system shape

The top layer is browser application composition. [src/app/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/application.js) gives the app a small lifecycle kernel: create scene, create controls, create data, create tools, then destroy in reverse ownership order. The design forces constructors to register cleanup immediately through `defer`, and it uses one shared abort signal for cancellation.

The next layer is standalone wiring. [src/standalone/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/standalone/application.js) chooses the real scene, controls, data, tools, place search, source catalog, and key handling used by the default product. It also enforces one standalone application per page because several lower-level modules still contain page-scoped state.

The catalog layer is the heart of the product. [src/app/constructCatalog.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/constructCatalog.js) creates the layer graph and passes each family its source and surface services. It also shares a military aircraft registry, a weather clock, terrain/ground services, and source-availability lookup.

The layer layer is where each feed becomes an interaction surface. [src/layers/flights/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/flights/index.js) composes state, rendering, motion, tracking, controller, enrichment, lifecycle, evidence, tests, queries, and ingestion for civil flights. [src/layers/cctv/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/cctv/index.js) does the same for cameras, with calibration, geometry queues, projection overlays, cards, selection, hover, health, and playback. [src/layers/vessels/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/vessels/index.js) and [src/layers/satellites/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/satellites/index.js) show the same factory style.

The server-provider layer is a set of compatibility adapters around outside APIs. [server/providers/live.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/server/providers/live.js) is a barrel for aircraft, AIS, capped HTTP reads, query helpers, and proxies. The deeper [server/providers/aircraft](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/server/providers/aircraft), [server/providers/vessels](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/server/providers/vessels), [server/providers/openai](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/server/providers/openai), and [server/providers/space](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/server/providers/space) directories own specific acquisition/caching concerns.

### Main layers

The application lifecycle layer is deliberately small. [src/app/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/application.js) does not know about aircraft, cameras, maps, or voice. Its job is phase ordering, cleanup, status publishing, and cancellation. That is a good separation because the rest of the app is too large to debug if lifetime is implicit.

The source-contract layer is where a lot of product correctness lives. [src/app/sourceComposition.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sourceComposition.js) enumerates each source contract and the methods a consumer expects. If a provider is omitted, the replacement source throws `SourceUnavailableError`. That means unavailable traffic, satellites, or CCTV is represented as an unavailable capability, not as "zero records."

The layer-factory layer makes each live feed independently testable. [src/layers/flights/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/flights/index.js), [src/layers/cctv/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/cctv/index.js), and [src/layers/satellites/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/satellites/index.js) all use a parts/context pattern. The pattern is verbose, but it makes ownership clearer than one huge class.

The voice layer is a state-machine composition rather than a single monolith. [src/voice/realtimeController.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/voice/realtimeController.js) composes connection, turns, viewport capture, diagnostics, radio handoff, cost tracking, physical input, narration, earcons, pointer context, and action execution. [docs/VOICE-OWNERSHIP.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/VOICE-OWNERSHIP.md) documents which owner holds which state.

The Director layer is a product-within-the-product. [src/director/playback.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/director/playback.js) runs scenes through adapter phases, while [src/director/document.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/director/document.js), [src/director/packs](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/director/packs), and [src/director/sharing](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/director/sharing) handle authored scene content.

### Request / data / control flow

On startup, [src/standalone/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/standalone/application.js) creates place search, scene services, and the layer catalog. It calls [src/app/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/application.js), which starts scene first, then controls, then data, then tools. Each phase can register cleanup and receives the shared abort signal.

Before layers are registered, [src/app/sources.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sources.js) can configure live source implementations. [src/app/sourceComposition.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sourceComposition.js) validates those sources against the layer contract table. Missing sources become inert but explicit failures.

A live layer then follows a family-specific ingestion flow. For flights, [src/layers/flights/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/flights/index.js) asks its controller for a spatial query, pulls a feed snapshot, and sends it through the snapshot renderer, motion, tracking, enrichment, and rendering parts. For CCTV, [src/layers/cctv/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/cctv/index.js) moves through source catalog, health, frame/media URLs, calibration, ground/geometry, projection, cards, and navigation.

Server-side live data enters through [server/providers](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/server/providers). Those providers shield browser code from upstream details such as capped reads, coalescing, cache lifetimes, rate limits, same-origin proxy rules, and credential resolution.

Voice control crosses the layers through an action runner. [src/voice/realtimeController.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/voice/realtimeController.js) coordinates WebRTC session state and hands model tool calls to action execution. The important control-flow detail is that viewport capture, radio handoff, pointer context, and cost tracking have separate owners, so a stale capture or cancelled voice turn should not leak into a replacement session.

## Key directories and files

- [src/app/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/application.js): lifecycle kernel, phase ordering, cleanup registration, abort handling, and status subscriptions.
- [src/standalone/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/standalone/application.js): default product assembly.
- [src/app/constructCatalog.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/constructCatalog.js): the best single file for seeing the full layer surface.
- [src/app/sourceComposition.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sourceComposition.js): source contracts and unavailable-source behavior.
- [src/layers/flights/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/flights/index.js): representative aircraft layer composition.
- [src/layers/cctv/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/cctv/index.js): representative high-complexity layer with video, geometry, calibration, and interaction.
- [server/providers/live.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/server/providers/live.js): Node provider barrel for aircraft, AIS, common HTTP, and query helpers.
- [src/voice/realtimeController.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/voice/realtimeController.js): voice session composition and control handoff.
- [docs/VOICE-OWNERSHIP.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/VOICE-OWNERSHIP.md): state ownership map for realtime voice.
- [src/director/playback.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/director/playback.js): portable scene playback runner.
- [docs/DIRECTOR.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/DIRECTOR.md): source-level explanation of scene playback, documents, packs, and sharing.
- [scripts/check-import-directions.mjs](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/scripts/check-import-directions.mjs) and [scripts/check-package-boundaries.mjs](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/scripts/check-package-boundaries.mjs): boundary gates that make the architecture notes enforceable.

## Important components

The lifecycle kernel in [src/app/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/application.js) is deceptively important. It gives a chaotic app a deterministic startup and shutdown spine.

The layer catalog in [src/app/constructCatalog.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/constructCatalog.js) is the second important component. It is where product scope becomes code: Bhote Koshi scene layers, live contacts, local ADS-B, fire perimeters, ALPR, street level, launches, traffic, CCTV, radio, transit, vessels, installations, awareness, weather, infrastructure, submarine cables, and NASA FIRMS all enter the same manager.

The source contract table in [src/app/sourceComposition.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sourceComposition.js) is the quiet reliability feature. It prevents a provider omission from masquerading as successful empty data.

The realtime voice controller in [src/voice/realtimeController.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/voice/realtimeController.js) is the most ambitious interaction component. It coordinates microphone input, WebRTC transport, model turns, globe actions, viewport capture, pointer context, radio playback, and usage/cost feedback.

The attribution and source register in [DATA_SOURCES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/DATA_SOURCES.md) is a product component, not just documentation. An app made from public data lives or dies on whether it treats licenses, credits, and provider terms as first-class design constraints.

## Important knobs / configs / extension points

- Source replacement goes through [src/app/sources.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sources.js) and [src/app/sourceComposition.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sourceComposition.js).
- New data families are added to the catalog through [src/app/constructCatalog.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/constructCatalog.js) and usually need a matching [src/layers](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers) factory plus a source contract.
- Map-source behavior is concentrated under [src/maps](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/maps), with Google 3D, imagery, terrain, token, and availability helpers.
- Voice backend and action behavior are configured through [src/voice/commands.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/voice/commands.js), [src/voice/realtimeBackend.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/voice/realtimeBackend.js), [server/providers/openai](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/server/providers/openai), and [server/standalone/key-setup.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/server/standalone/key-setup.js).
- Scene playback and authored content extend through [src/director](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/director), [src/scenes](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/src/scenes), and the document specs under [docs](https://github.com/bilawalsidhu/gods-eye-view/tree/9beadbda6333b83f79aa03047e2d851830f01f6b/docs).
- Boundary discipline is checked by [scripts/check-import-directions.mjs](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/scripts/check-import-directions.mjs) and [scripts/check-package-boundaries.mjs](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/scripts/check-package-boundaries.mjs).

## Practical questions and answers

Q: Is this mostly a Cesium demo?
A: No. Cesium is the visual substrate, but the repo's real work is source composition, layer ownership, provider adapters, input/voice systems, scene playback, and attribution. [src/app/constructCatalog.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/constructCatalog.js) is a better guide to the product than a globe screenshot.

Q: What would I copy first?
A: Copy the lifecycle spine from [src/app/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/application.js) and the explicit source contracts from [src/app/sourceComposition.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sourceComposition.js). Those patterns help even in a much smaller dashboard.

Q: What is likely brittle?
A: The many third-party live sources. [DATA_SOURCES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/DATA_SOURCES.md) is honest about provider terms, public endpoints, caches, and bundled data. A serious deployment would need monitoring, quotas, self-hosted fallbacks, and product-specific legal review.

Q: Is the voice layer just a wrapper around a model?
A: No. [src/voice/realtimeController.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/voice/realtimeController.js) is an orchestration layer around transport, physical input, model turns, action execution, viewport capture, radio handoff, diagnostics, and cost. [docs/VOICE-OWNERSHIP.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/VOICE-OWNERSHIP.md) is worth copying as an ownership map.

Q: Where does the project show maturity?
A: The docs and tests around boundaries. [docs/CODE-BOUNDARIES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/CODE-BOUNDARIES.md), [docs/DIRECTOR.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/DIRECTOR.md), and [docs/VOICE-OWNERSHIP.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/VOICE-OWNERSHIP.md) record architectural decisions that could otherwise disappear into folklore.

## What is smart

The phase-based application lifecycle in [src/app/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/application.js) is smart because it gives resource ownership a single center without forcing every feature into one framework.

The missing-source behavior in [src/app/sourceComposition.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sourceComposition.js) is smart because it preserves the difference between "not configured" and "configured but no records." That matters for a dashboard where empty data can be dangerously misleading.

The parts/context factory pattern in [src/layers/flights/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/flights/index.js) and [src/layers/cctv/index.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/layers/cctv/index.js) is smart for a large visualization app. It is more verbose than classes, but it exposes subsystem seams for tests.

The source/license discipline in [DATA_SOURCES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/DATA_SOURCES.md) is smart. Public-data apps often bury terms until late; this project brings them to the front.

## What is flawed or weak

The app is heavy. [package.json](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/package.json) and [src/app/constructCatalog.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/constructCatalog.js) reveal a lot of moving parts. That is exciting for demos but hard for ordinary users to reason about when something fails.

The source ecosystem is fragile by nature. [DATA_SOURCES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/DATA_SOURCES.md) lists many public endpoints and terms. Any serious production fork needs provider-specific failure UX and a policy for stale, partial, or legally constrained feeds.

Some compatibility debt is visible. [docs/CODE-BOUNDARIES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/CODE-BOUNDARIES.md) explicitly calls out retained compatibility entries and standalone-import exceptions. That honesty is good, but it means the extraction is still in progress.

The viral positioning can obscure the engineering. The README's "forbidden cockpit" energy helps adoption, but builders should read [src/app/sourceComposition.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sourceComposition.js), [src/app/constructCatalog.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/constructCatalog.js), and [DATA_SOURCES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/DATA_SOURCES.md) before copying the style.

## What we can learn / steal

Steal the lifecycle shape from [src/app/application.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/application.js): explicit startup phases, shared cancellation, reverse cleanup, immutable state snapshots, and listener isolation.

Steal the source contract table from [src/app/sourceComposition.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sourceComposition.js): each provider should declare the consumer methods it supports, and missing providers should be an explicit capability state.

Steal the ownership docs. [docs/VOICE-OWNERSHIP.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/VOICE-OWNERSHIP.md) is a useful template for complicated realtime features where different owners hold transport, UI, action, cost, input, and diagnostics state.

Steal the attribution-first data ledger from [DATA_SOURCES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/DATA_SOURCES.md). If a product is built from public signals, attribution and data terms are not a release-note afterthought.

## How we could apply it

For a smaller ops dashboard, use the same source/layer/service separation without copying the whole visual stack. A dashboard could define a [src/app/sourceComposition.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/sourceComposition.js)-style contract table, a [src/app/constructCatalog.js](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/src/app/constructCatalog.js)-style registry, and per-layer factories that own ingestion/rendering/selection.

For voice-controlled tools, copy the ownership thinking in [docs/VOICE-OWNERSHIP.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/docs/VOICE-OWNERSHIP.md) before writing code. Decide who owns the session, input, action execution, viewport context, diagnostics, and interruption semantics.

For public-data products, start with a [DATA_SOURCES.md](https://github.com/bilawalsidhu/gods-eye-view/blob/9beadbda6333b83f79aa03047e2d851830f01f6b/DATA_SOURCES.md)-style source ledger and wire attribution into the UI early. That will save pain later.

## Bottom line

God's Eye View is worth studying because it is both theatrical and mechanically grounded. The best part is not the globe. The best part is the scaffolding around the globe: explicit application lifecycle, source contracts, layer factories, provider adapters, voice ownership, Director scene playback, and a serious data-source ledger. The weak point is the same as the strength: this many live sources and interaction modes make a thrilling app, but also a large operational surface.
