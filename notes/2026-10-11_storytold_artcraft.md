# ArtCraft

- Repo: storytold/artcraft
- URL: https://github.com/storytold/artcraft
- Date: 2026-10-11
- Repo snapshot studied: main at commit d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373
- Why picked today: It was high on GitHub daily trending with same-day activity and a source tree that is much more than a product README: a Rust workspace, pure egui desktop app, Tauri app, provider router, typed API clients, credential storage, background job finishing, and creator-focused generation UI.

## Executive summary

[storytold/artcraft](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373) is an AI creation IDE for images, video, audio, 3D meshes, and worlds. The marketing pitch is "the IDE for artists," but the interesting builder story is the way the repo tries to turn many provider-specific generation systems into one desktop workflow.

The current source snapshot is centered on a Rust workspace in [Cargo.toml](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/Cargo.toml). It contains a legacy/default Tauri desktop app in [crates/desktop/artcraft](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/desktop/artcraft), a pure Rust egui app in [artcraft-native](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native), and shared API/client/router crates under [crates/api_clients](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients). The newest commit adds direct Midjourney and fal provider choice to the native app, which makes the repo a good study of product plumbing rather than just UI polish.

The key design idea is that ArtCraft does not make the UI know every provider's shape. The native app maps page fields into a shared router request in [artcraft-native/src/backend/providers/submit.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/submit.rs), then hands actual dispatch to router clients such as [RouterMidjourneyClient](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router/src/client/router_midjourney_client.rs) and [RouterFalClient](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router/src/client/router_fal_client.rs). It then treats provider jobs as local pending work and uploads the finished results back into the user's ArtCraft library.

## What they built

ArtCraft is a desktop-first creative tool that wraps prompt, reference, model, library, and generation workflows. The [README](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/README.md) describes image and video creation, 2D and 3D compositing, character posing, image-to-3D meshes, background removal, and a 62-model ArtCraft catalog.

The source reveals a more specific implementation: the repo is a Rust workspace of reusable clients and applications. [artcraft-native/README.md](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/README.md) describes the native app as an egui UI over the same API client crates used by the Tauri app. The native app has Create Image, Create Video, Create Audio, Home, Library, prompt box, feed, lightbox, account overlays, provider setup, media cache, audio playback, and custom window chrome.

The most current feature is provider choice for image generation. [artcraft-native/src/backend/providers/mod.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/mod.rs) defines `Provider::Artcraft`, `Provider::Midjourney`, and `Provider::Fal`, plus the model/provider compatibility table. Midjourney direct generation is constrained to four images and no image references. fal is allowed for selected ArtCraft models such as Flux and Nano Banana variants.

## Why it matters

This is the kind of product plumbing most AI apps underestimate. Users see one prompt box and one library, but the implementation has to coordinate account state, provider capabilities, prompt records, queued provider jobs, downloads, uploads, idempotency, and UI updates.

The useful lesson is the split between product surface and provider machinery. [artcraft-native/src/prompt_box/model_selector.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/prompt_box/model_selector.rs) can offer model/provider choices, while [artcraft-native/src/backend/providers/submit.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/submit.rs) owns the hard policy checks before a request leaves the app. [artcraft-native/src/backend/providers/worker.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/worker.rs) then owns long-running completion, retry, and library ingestion. That boundary keeps provider weirdness from leaking into every UI component.

## Repo shape at a glance

- [README.md](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/README.md): product overview, supported model families, downloads, and source-build links.
- [Cargo.toml](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/Cargo.toml): workspace map. It lists the native app, Tauri app, API clients, provider clients, router, shared libraries, schemas, testing crates, and a vendored Tauri HTTP plugin.
- [artcraft-native](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native): pure Rust egui desktop app with backend, feed, prompt box, pages, overlays, theme, UI widgets, and tests.
- [crates/api_clients/artcraft/artcraft_router](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router): provider-neutral request types and provider-specific client adapters.
- [crates/api_clients/artcraft/artcraft_api_defs](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_api_defs): typed API definitions for analytics, characters, folders, generate, jobs, media files, moderation, prompts, sessions, and other ArtCraft backend surfaces.
- [crates/api_clients](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients): first-party and third-party clients, including ArtCraft, fal, Grok, Midjourney, Sora, World Labs, and other provider clients.
- [crates/lib](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/lib): reusable support crates for browser emulation, Cloudflare mitigation, cookie stores, file conversion, image handling, JWT parsing, URLs, UUIDs, and memory stores.
- [frontend](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/frontend), [docs](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/docs), [_docs](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/_docs), and [script](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/script): web assets, developer docs, and build/development automation.

## Layered architecture dissection

### High-level system shape

At the highest level, ArtCraft has four layers.

The user-facing layer is the desktop UI. The native app's module map in [artcraft-native/README.md](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/README.md) is the best compact guide: `pages` own Create Image, Create Video, Create Audio, Home, and Library; `prompt_box` owns references and model selection; `feed` renders jobs and generated media; `overlays` own settings, library picker, account setup, and the Midjourney sign-in window.

The app backend layer runs async work and translates service responses into UI events. [artcraft-native/src/backend/providers](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers) is a good example: it hides account loading, provider submission, job storage, and background completion from the UI.

The router/client layer turns a common generation request into provider-specific calls. [crates/api_clients/artcraft/artcraft_router/src/api/router_provider.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router/src/api/router_provider.rs) names the supported provider enum. [crates/api_clients/artcraft/artcraft_router/src/client/multi_router_client.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router/src/client/multi_router_client.rs) holds optional client adapters and fails explicitly when a client is not configured.

The platform/service layer is a collection of typed API definitions, third-party provider clients, credential helpers, file utilities, and schema crates under [crates](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates). This lets both desktop apps share the same low-level provider behavior.

### Main layers

The model capability layer starts in [artcraft-native/src/backend/providers/mod.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/mod.rs). `Provider::for_model` is a small but important policy table: it says which providers can run which model IDs, and puts the default provider first. `Provider::adapt` mutates exposed model capabilities when a provider cannot support the same controls as ArtCraft. For example, direct Midjourney clears resolution and quality choices and fixes batch size to four.

The credential layer is [artcraft-native/src/backend/providers/accounts.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/accounts.rs). It stores provider accounts in the same `~/Artcraft/credentials` files used by the Tauri app, loads Midjourney cookies through `MidjourneyCredentialManager`, stores a fal API key in `fal.api_key.txt`, masks displayed keys, and clears missing files idempotently.

The submission layer is [artcraft-native/src/backend/providers/submit.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/submit.rs). It validates provider/model compatibility, creates an ArtCraft prompt record when appropriate, builds a `GenerateImageRequestBuilder`, chooses `RouterProvider::Midjourney` or `RouterProvider::Fal`, and returns a local `ProviderJob`.

The completion layer is [artcraft-native/src/backend/providers/worker.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/worker.rs). It polls fal queue status and response URLs, watches Midjourney through both feed reads and websocket completion events, downloads finished images, uploads them into the ArtCraft library with idempotency tokens, and resumes partially uploaded jobs after failures.

### Request / data / control flow

A normal direct-provider image run starts with page fields from the Create Image UI. The model selector decides which providers are valid, but the backend still checks them in [providers/mod.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/mod.rs) and [providers/submit.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/submit.rs). That double check is good product hygiene: the UI can be friendly, while the backend remains authoritative.

For Midjourney, [submit.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/submit.rs) rejects non-Midjourney models, image references, and non-four-image batches. It creates a prompt record first, builds a router request, creates a [RouterMidjourneyClient](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router/src/client/router_midjourney_client.rs) from cookie header, user ID, and browser profile, then sends the request. The browser profile matters because the source comment notes Cloudflare cookies are bound to the user agent.

For fal, [submit.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/submit.rs) loads the raw key, maps references to URL inputs, optionally creates a prompt record, creates a [RouterFalClient](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router/src/client/router_fal_client.rs), and stores queue status/response URLs in the returned job.

After dispatch, [worker.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/worker.rs) owns the long tail. It marks upload tokens before each upload so a retry cannot duplicate a result, then calls `upload_image_media_file_from_file_with_idempotency_token` and finally removes the local job.

## Key directories and files

- [Cargo.toml](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/Cargo.toml): the architecture index. The workspace members are the fastest way to understand ownership boundaries.
- [artcraft-native/README.md](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/README.md): the best human-readable map of the egui app, its modules, and its parity with the Tauri/web app.
- [artcraft-native/src/backend/providers/mod.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/mod.rs): provider enum, provider labels/icons, model/provider policy, and capability adaptation.
- [artcraft-native/src/backend/providers/accounts.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/accounts.rs): shared credential files, Midjourney account state, fal key storage, masking, and tests.
- [artcraft-native/src/backend/providers/submit.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/submit.rs): provider dispatch entry point and request-builder bridge from app fields to router requests.
- [artcraft-native/src/backend/providers/worker.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/worker.rs): polling, websocket watching, result download, library upload, retry, and job completion.
- [crates/api_clients/artcraft/artcraft_router](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router): common request surface and provider adapters.
- [crates/api_clients/artcraft/artcraft_api_defs/src/generate](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_api_defs/src/generate): typed generation API definitions for image, video, audio, mesh, splat, and cost-estimation surfaces.

## Important components

The provider policy table is small but central. [Provider::for_model](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/mod.rs) keeps "which provider can run this model" as data rather than sprinkling conditionals through the UI.

The router clients are deliberately thin. [RouterMidjourneyClient](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router/src/client/router_midjourney_client.rs) is mostly cookie header, user ID, and browser profile. [RouterFalClient](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router/src/client/router_fal_client.rs) is API key plus optional webhook URL. That thinness is useful: behavior lives in request builders and endpoint wrappers rather than in a bloated client object.

The worker is the real reliability component. [worker.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/worker.rs) handles cases the happy-path UI never wants to explain: fal finished but returned no image URLs, Midjourney websocket unavailable, feed polling lag, upload failures, partially completed batches, and stale jobs that never finish.

## Important knobs / configs / extension points

- Add a provider by extending [RouterProvider](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router/src/api/router_provider.rs), adding a router client, and wiring it into [MultiRouterClient](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router/src/client/multi_router_client.rs).
- Add native-app provider eligibility by changing [Provider::for_model](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/mod.rs).
- Adjust direct Midjourney product limits through [Provider::adapt](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/mod.rs) and [submit_midjourney](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/submit.rs).
- Change worker retry and latency behavior through constants in [worker.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/worker.rs), including tick interval, Midjourney feed interval, websocket retry interval, request timeout, transfer timeout, and give-up time.

## Practical questions and answers

Q: Is this just a wrapper around a generation API?
A: No. [Cargo.toml](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/Cargo.toml) shows a full client/router/app workspace, and [artcraft-native/README.md](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/README.md) shows real UI state, media cache, audio playback, feed, library, account, and prompt-box behavior.

Q: What is the most reusable implementation idea?
A: Treat third-party jobs as local state until they become first-party library items. [worker.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/worker.rs) is a useful pattern for making outside providers feel native without pretending their queues are first-party jobs.

Q: What is brittle?
A: Direct Midjourney integration depends on captured cookies, browser profile compatibility, feed polling, and websocket state. [RouterMidjourneyClient](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router/src/client/router_midjourney_client.rs) even calls out the Cloudflare/user-agent binding. That is useful, but operationally fragile.

Q: Does the code separate UI and provider rules enough?
A: Mostly yes. The provider rules live in [providers/mod.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/mod.rs) and [providers/submit.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/submit.rs), while the UI-facing modules can present selectors and dialogs.

## What is smart

The repo treats provider diversity as a routing problem, not a pile of feature flags. [artcraft_router](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/crates/api_clients/artcraft/artcraft_router) is a real abstraction boundary.

The native app shares account files with the Tauri app. That is a small product decision with large UX value, and [accounts.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/accounts.rs) keeps it simple.

The worker stores upload tokens before uploads, which is exactly the kind of defensive ordering needed when a retry can otherwise duplicate generated media.

## What is flawed or weak

The provider matrix is still partly hard-coded. [Provider::for_model](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/mod.rs) is clear, but as the provider/model catalog grows it may need to come from server-provided model capabilities rather than app releases.

Midjourney direct mode is inherently delicate. Cookie capture, Cloudflare mitigation, account expiration, feed reads, and websocket tokens can fail outside the app's control.

The workspace is broad enough that onboarding will be expensive. The architecture is understandable, but a contributor has to know egui, Tauri, router crates, provider clients, ArtCraft backend APIs, and local credential conventions before touching a user-visible generation path.

## What we can learn / steal

Steal the pattern of keeping one library/feed even when results come from multiple providers. Users should not have to know which queue produced an image after it lands.

Steal the strict backend validation behind friendly selectors. UI affordances are hints; [submit.rs](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native/src/backend/providers/submit.rs) is the contract.

Steal the thin-client router shape. A `RouterClient` should carry authentication and transport identity, while request builders and endpoint modules carry the model-specific behavior.

## How we could apply it

For any multi-provider AI product, define a provider router early, even if only one provider works on day one. The moment a second provider arrives, capability adaptation, request validation, job state, result ingestion, and billing errors need a home.

For generated assets, treat external provider jobs as temporary local jobs and ingest results into a first-party library with idempotency tokens. That gives the product one durable state model.

For desktop apps that wrap web services, copy the "native backend, UI events out" shape from [artcraft-native](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/artcraft-native). It makes long-running generation less likely to contaminate the UI layer.

## Bottom line

ArtCraft is worth studying because it is a real multi-provider creative app, not just a shiny prompt box. The strongest lesson is its separation of model/provider policy, router clients, provider job lifecycle, and final library ingestion. The weakest point is the unavoidable fragility of direct third-party account integrations, especially when cookies and provider UIs become part of the API.
