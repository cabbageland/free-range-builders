# Thunderbolt

- Repo: [thunderbird/thunderbolt](https://github.com/thunderbird/thunderbolt)
- URL: https://github.com/thunderbird/thunderbolt
- Date: 2026-04-18
- Repo snapshot studied: [`main@9d9c18ba511decfd3b45fc0f72c265d83355fe95`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95)
- Why picked today: It is clearly hot right now, AI-related, and more interesting than another thin agent shell. The repo is trying to build a serious cross-platform AI client with on-prem/self-hosted posture, offline-first sync ambitions, optional end-to-end encryption, and actual backend/deployment machinery.

## Executive summary

Thunderbolt is best understood as a **full-stack, self-hostable AI client platform**, not just “a chat app with model switching.” The interesting move is that it treats the AI interface as only one layer inside a broader product stack: local app state, offline storage, sync, auth, integrations, inference proxying, deployment surfaces, and enterprise-ish operational concerns all live in the same repo.

The repo’s strongest idea is architectural separation. The frontend at [`src/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src) is a React/Tauri client that wants local-first behavior via PowerSync + SQLite, while the backend at [`backend/src/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src) acts as a control plane for auth, inference routing, sync APIs, and protected proxying. The deployment layer under [`deploy/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/deploy) makes the self-hosted story concrete rather than ornamental.

The main caveat is that the product promise is slightly ahead of its hard guarantees. The README explicitly says it is early, not yet fully offline-first, and still under security audit. That honesty is good. But it also means you should read this repo as **an ambitious system under active construction**, not as finished infrastructure.

## What they built

They built a cross-platform AI client with a lot more surface area than the average “desktop wrapper for LLM APIs” repo:

- a shared React application in [`src/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src)
- native shells and mobile/desktop packaging through [`src-tauri/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src-tauri)
- a Bun/Elysia backend in [`backend/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend)
- local-first persistence and sync plumbing around [`src/db/powersync/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/db/powersync)
- optional E2E encryption described in [`docs/e2e-encryption.md`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/docs/e2e-encryption.md)
- deployment targets for Docker Compose, Kubernetes, and Pulumi in [`deploy/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/deploy)
- a separate marketing site in [`marketing/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/marketing)
- a surprisingly large internal automation layer in [`.thunderbot/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/.thunderbot) and [`.claude/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/.claude)

So the real product is: **local app + hosted control plane + deployable enterprise stack + internal AI-assisted development workflow**.

## Why it matters

A lot of AI client repos are fake-serious: pretty UI, vague “bring your own models,” no real data model, no deployment discipline, no sync story, and no security posture beyond vibes.

Thunderbolt matters because it is trying to solve the real ugly parts too:

- how an AI client works across web, desktop, and mobile
- how data sync works when you want local state and optional cloud sync
- how auth, device approval, revocation, and recovery work
- how to route multiple model providers through a backend proxy
- how to add tools/integrations without turning the whole thing into a security clown car
- how to package the whole stack for enterprise self-hosting

Whether it fully succeeds yet is a separate question. But the repo is worth studying because it is aiming at the right level of system complexity.

## Repo shape at a glance

Top-level shape:

- [`src/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src)
  - the main React app: chat UI, settings, automations, hooks, widgets, data layer, AI logic
- [`src-tauri/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src-tauri)
  - native container, platform bindings, mobile/desktop packaging, updater/signing support
- [`backend/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend)
  - Bun/Elysia backend with auth, inference, sync-related APIs, MCP proxy, pro features, DAL, DB schema, email templates
- [`deploy/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/deploy)
  - concrete deployment assets for Docker, Kubernetes, and Pulumi
- [`docs/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/docs)
  - architecture, encryption, development, PowerSync, testing, widget, and roadmap docs
- [`e2e/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/e2e)
  - Playwright-style end-to-end tests around login/session flows
- [`marketing/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/marketing)
  - separate site/app shell for public-facing positioning
- [`.thunderbot/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/.thunderbot) and [`.claude/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/.claude)
  - internal agent-command workflows, review rituals, and team automation scaffolding
- [`.github/workflows/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/.github/workflows)
  - release, CI, security, enterprise deploy, mobile release, and PR metrics automation

Structurally, this is a **product monorepo** with four real pillars:

1. client app
2. backend control plane
3. deployable infra
4. internal build/release/AI-dev ops

## Layered architecture dissection

### High-level system shape

The repo’s shape is roughly this:

1. user interacts with a local React/Tauri app
2. app stores state locally and syncs selectively through PowerSync/Postgres
3. auth and account/device lifecycle run through backend routes
4. model calls go through either direct provider adapters or the Thunderbolt backend proxy, depending on model/provider choice
5. tool/integration access is assembled dynamically from enabled integrations and MCP clients
6. enterprise/self-hosted deployment packages the backend, auth, PowerSync, and storage together

The architecture diagram in [`docs/architecture.md`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/docs/architecture.md) matches the actual source surprisingly well.

### Main layers

**1. App shell and route orchestration**

- [`src/app.tsx`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/app.tsx)
- [`src/layout/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/layout)
- [`src/settings/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/settings)

This layer wires routing, providers, auth gates, onboarding, pending/revoked device UX, settings pages, and feature surfaces like tasks and automations. It is less “chat screen” than “full application shell.”

**2. Local state, persistence, and sync**

- [`src/chats/chat-store.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/chats/chat-store.ts)
- [`src/db/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/db)
- [`src/db/powersync/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/db/powersync)
- [`docs/powersync-sync-middleware.md`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/docs/powersync-sync-middleware.md)

This is one of the repo’s real cores. Thunderbolt is not just keeping transient client state in memory; it is trying to make SQLite-backed local data the operational center, then layer sync over it.

**3. AI runtime and model/tool assembly**

- [`src/ai/fetch.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/ai/fetch.ts)
- [`src/ai/prompt.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/ai/prompt.ts)
- [`src/ai/step-logic.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/ai/step-logic.ts)
- [`src/lib/tools.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/lib/tools.ts)

This layer chooses models, builds prompts from stored settings and profiles, injects toolsets, integrates MCP tools, handles streaming, and mediates multi-step tool-call behavior.

**4. Backend control plane**

- [`backend/src/index.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/index.ts)
- [`backend/src/api/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/api)
- [`backend/src/auth/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/auth)
- [`backend/src/inference/routes.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/inference/routes.ts)
- [`backend/src/mcp-proxy/routes.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/mcp-proxy/routes.ts)

This layer provides the serious-product stuff: auth, rate limiting, inference routing, secure-ish proxying, encryption routes, data access, pro features, and observability.

**5. Security and cryptography layer**

- [`docs/e2e-encryption.md`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/docs/e2e-encryption.md)
- [`src/services/encryption.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/services/encryption.ts)
- [`src/db/encryption/config.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/db/encryption/config.ts)
- [`backend/src/api/encryption.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/api/encryption.ts)

This is aspirational-but-real: optional E2E encryption, device approval/revocation, recovery keys, and config-driven encrypted columns.

**6. Deployment and release layer**

- [`deploy/docker-compose.yml`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/deploy/docker-compose.yml)
- [`deploy/k8s/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/deploy/k8s)
- [`deploy/pulumi/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/deploy/pulumi)
- [`.github/workflows/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/.github/workflows)

This is where the repo separates itself from hobby wrappers. It is shipping a whole deployment and release posture, not just source code.

### Request / data / control flow

A practical control flow looks like this:

1. the app boots through [`src/app.tsx`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/app.tsx), initializing auth, DB, PowerSync, PostHog, tray/window hooks, MCP, and UI providers
2. chat/session state is managed in [`src/chats/chat-store.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/chats/chat-store.ts), with selected models/modes persisted back into the database
3. when the user sends a message, [`src/ai/fetch.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/ai/fetch.ts) loads settings, model config, model profile, active integrations, and MCP tools, then builds the prompt/tool execution context
4. model traffic either uses direct provider adapters or routes through the Thunderbolt backend using OpenAI-compatible transport semantics
5. the backend endpoint in [`backend/src/inference/routes.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/inference/routes.ts) maps the user-facing model name to a provider/internal model, sanitizes post-first privileged message roles, and re-streams provider output as SSE
6. sync/auth/device state flows through backend auth/API routes plus PowerSync/Postgres infrastructure
7. MCP traffic can be proxied through [`backend/src/mcp-proxy/routes.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/mcp-proxy/routes.ts), which adds URL validation, body-size caps, timeout caps, header filtering, and response sandboxing

That last part is especially worth noticing: they are not just saying “we support MCP,” they are inserting a defensive proxy boundary around it.

## Key directories and files

The source paths carrying the most architectural weight:

- [`README.md`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/README.md)
  - honest status framing and product promise
- [`docs/architecture.md`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/docs/architecture.md)
  - compact but useful system diagram; it is not fluff
- [`src/app.tsx`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/app.tsx)
  - the clearest front-door to the app’s provider graph and feature routing
- [`src/ai/fetch.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/ai/fetch.ts)
  - the real AI orchestration file: model creation, provider handling, prompt construction, tool assembly, streaming behavior
- [`src/lib/tools.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/lib/tools.ts)
  - where enabled integrations get turned into actual callable tools
- [`src/chats/chat-store.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/chats/chat-store.ts)
  - useful for seeing what the app considers the persistent/interactive chat state contract
- [`backend/src/inference/routes.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/inference/routes.ts)
  - the key backend boundary for hosted inference
- [`backend/src/mcp-proxy/routes.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/mcp-proxy/routes.ts)
  - maybe the most quietly interesting backend file because it shows where they are actually thinking about SSRF/proxy abuse
- [`docs/e2e-encryption.md`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/docs/e2e-encryption.md)
  - the best concise explanation of their security ambition and its current maturity caveats
- [`deploy/docker-compose.yml`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/deploy/docker-compose.yml)
  - where the “self-hostable” claim stops being marketing copy

## Important components

### `App` and provider graph

- [`src/app.tsx`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/app.tsx)

This file tells you Thunderbolt is a real app platform. It composes PowerSync, DB, HTTP client, auth, PostHog, tray/window bindings, MCP, haptics, sidebar state, content-view state, and auth/device UX into one boot sequence.

### `aiFetchStreamingResponse`

- [`src/ai/fetch.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/ai/fetch.ts)

This is the repo’s center of gravity for AI behavior. It pulls settings from local DB, resolves the selected model, builds a mode/system prompt, injects integration tools, merges MCP tools, and runs the stream loop with retry/step logic. This is where “model agnostic” becomes implementation rather than slogan.

### Tool assembly layer

- [`src/lib/tools.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/lib/tools.ts)
- [`src/integrations/google/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/integrations/google)
- [`src/integrations/microsoft/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/integrations/microsoft)
- [`src/integrations/thunderbolt-pro/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/integrations/thunderbolt-pro)

This is a clean design choice: tool availability is derived from settings and entitlements, not hardwired blindly into the model loop.

### Inference router

- [`backend/src/inference/routes.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/inference/routes.ts)

The backend currently keeps a tight model map and routes user-facing names like `sonnet-4.5` or `gpt-oss-120b` to provider-specific internal names. It also downgrades developer/system roles after the first message, which is a subtle but good hardening move against prompt-role abuse.

### MCP proxy boundary

- [`backend/src/mcp-proxy/routes.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/mcp-proxy/routes.ts)

This component is more impressive than the average “MCP support” checkbox. It validates target URLs, wraps fetch with DNS-level SSRF protection, strips dangerous headers, caps request/response size, applies a timeout, strips cookies, and forces CSP/content-disposition hardening on proxied responses.

### E2E encryption service model

- [`docs/e2e-encryption.md`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/docs/e2e-encryption.md)
- [`src/services/encryption.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/services/encryption.ts)

The design uses per-device hybrid envelopes around a shared content key, plus a recovery mnemonic and canary verification. That is serious product thinking, even if it is not yet audit-mature.

## Important knobs / configs / extension points

A few knobs that actually matter:

- model/provider selection and provider-specific behavior in [`src/ai/fetch.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/ai/fetch.ts)
  - local Ollama, Anthropic, OpenAI, custom OpenAI-compatible, OpenRouter-compatible paths, plus Thunderbolt backend mode
- tool availability in [`src/lib/tools.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/lib/tools.ts)
  - gated by integration enablement and pro access
- supported backend models in [`backend/src/inference/routes.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/inference/routes.ts)
  - explicit mapping of public model ids to internal provider names
- auth mode and waitlist behavior in [`src/app.tsx`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/app.tsx)
  - OIDC mode, waitlist bypass, dev-only routes
- encrypted columns config in [`src/db/encryption/config.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/src/db/encryption/config.ts)
  - one source of truth for which synced fields are encrypted
- deployment target choice in [`deploy/docker-compose.yml`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/deploy/docker-compose.yml), [`deploy/k8s/values.yaml`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/deploy/k8s/values.yaml), and [`deploy/pulumi/src/`](https://github.com/thunderbird/thunderbolt/tree/9d9c18ba511decfd3b45fc0f72c265d83355fe95/deploy/pulumi/src)
  - clear extension points for ops posture

## Practical questions and answers

### Is this mostly a frontend app or mostly infrastructure?

Both, and that is why the repo is interesting. The UI is the visible surface, but the backend/sync/deploy layers are doing a lot of the real systems work.

### What is the most reusable idea here?

Treat the AI interface as one subsystem inside a broader local-first product architecture. The important insight is not “support many models”; it is “store real app state locally, sync deliberately, and keep providers/tooling swappable.”

### What is the most impressive concrete implementation choice?

The MCP proxy hardening in [`backend/src/mcp-proxy/routes.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/mcp-proxy/routes.ts). Lots of AI repos boast about tool protocols. Very few immediately show SSRF-aware proxy discipline.

### What feels unfinished?

The project says it plainly: offline-first is still incomplete, E2E crypto has not yet had a crypto audit, and enterprise production readiness is still being prepared. That does not make it bad; it makes it honest.

### Does the repo feel overbuilt?

Slightly, yes — but in a mostly healthy way. There is definitely monorepo sprawl, especially once you include marketing, release automation, and internal AI-dev workflows. But the sprawl maps to real product ambitions, not pure vanity.

### Where would this be brittle in production?

The pressure points are predictable:

- sync correctness across devices and local-first conflict edges
- auth/device lifecycle complexity
- provider compatibility drift for AI SDK integrations
- E2E encryption recovery/revocation flows
- the usual operational pain of shipping the same codebase to web + desktop + iOS + Android

## What is smart

A few things are genuinely smart:

- **Local-first posture with a real data layer.** Using PowerSync/SQLite as a first-class architectural concern is the right move if you want this to feel like software rather than a web tab with delusions.
- **Backend inference abstraction.** [`backend/src/inference/routes.ts`](https://github.com/thunderbird/thunderbolt/blob/9d9c18ba511decfd3b45fc0f72c265d83355fe95/backend/src/inference/routes.ts) gives them a place to enforce policy, telemetry, rate limits, and provider substitutions.
- **Defensive MCP proxying.** This is the standout engineering choice.
- **Config-driven encryption scope.** The encrypted-columns map in the crypto docs is a clean way to avoid scattered “oh right, encrypt this field too” footguns.
- **Deployment seriousness.** Docker, k8s, and Pulumi support in one repo makes the self-hostable claim more believable.
- **Explicit maturity caveats.** The README and docs say what is unfinished. That is healthy.

## What is flawed or weak

The weak spots are also visible:

- **Promise > current reality.** “AI you control” is a good pitch, but the repo still depends on backend/auth/search pieces and is openly not fully offline-first yet.
- **Monorepo weight.** There is a lot here: app, backend, infra, marketing, native packaging, internal agent workflows. That increases maintenance drag fast.
- **Potential abstraction churn.** AI provider stacks, SDK compatibility, and MCP conventions move quickly. Some of this code will age badly unless maintained aggressively.
- **Security ambition outruns validation.** Optional E2E crypto is exciting, but until audited, it should be treated as promising engineering rather than settled trust infrastructure.
- **Internal automation clutter.** The `.thunderbot` / `.claude` command universe is interesting but also a sign that the repo may be carrying a lot of team-process sediment in-tree.

## What we can learn / steal

Things worth stealing:

- build AI apps around a **real local data model**, not just ephemeral request/response UI
- keep model/provider choice behind a backend or adapter seam instead of smearing provider logic everywhere
- derive tool availability from entitlements/configuration instead of static magical tool injection
- put hostile-protocol traffic like MCP behind a hardened proxy boundary
- make the self-hosted story explicit in source control rather than leaving it as enterprise sales fog
- document unfinished security claims honestly

## How we could apply it

For our own systems, the most reusable pattern is:

1. local-first state as the default product center
2. provider-agnostic inference adapter layer
3. tool/plugin assembly from explicit capability flags
4. hardened proxy boundaries for anything that can reach arbitrary network targets
5. deployment assets treated as part of product architecture, not afterthoughts

I would especially copy the **MCP proxy discipline** and the idea that model selection, auth, sync, and tools are separate layers with clear seams.

I would not copy the whole monorepo sprawl unless the product genuinely needs cross-platform native packaging plus self-hosted infra plus a backend control plane.

## Bottom line

Thunderbolt is one of the more serious trending AI repos because it is not just showing off chat UX. It is trying to be a deployable, local-first, enterprise-credible AI client platform.

The repo’s best insight is that the hard part is not “talk to many models.” The hard part is the surrounding system: local persistence, sync, auth, device trust, tool safety, and deployment boundaries. Thunderbolt is built around that reality.

It is still early, and the repo says so. But it is worth studying because the engineering center of gravity is in the right place: not hype layers, but the ugly infrastructure that makes an AI client feel like real software.