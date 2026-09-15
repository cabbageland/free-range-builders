# Ever Gauzy Platform

- Repo: `ever-co/ever-gauzy`
- URL: https://github.com/ever-co/ever-gauzy
- Date: 2026-09-15
- Repo snapshot studied: `develop` at commit `5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8`
- Why picked today: GitHub daily trending showed `ever-co/ever-gauzy` as a TypeScript project with 632 stars today after two higher-ranked candidates had already been covered in recent notes. It is not a small AI demo; it is a serious open-source ERP/CRM/HRM/time-tracking monorepo with a large NestJS API, Angular and Electron clients, plugins, deployment recipes, and real operational surface.

## Executive summary

[`ever-co/ever-gauzy`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8) is a broad business-management platform: ERP, CRM, HRM, ATS, project management, accounting, public sharing, integrations, desktop time tracking, screenshots, analytics, and plugin-driven AI/chat/provider features. The repo is interesting because it shows what happens when an open-source SaaS product grows into a full product platform instead of one clean service.

The top-level [`README.md`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/README.md) is product-heavy, but the source is not shallow. [`package.json`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/package.json) exposes a large Nx/Lerna workspace with API, web, worker, desktop, desktop timer, packages, plugins, seeds, migrations, Electron packaging, Docker, and CI scripts. The API starts at [`apps/api/src/main.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/main.ts), then delegates to the reusable bootstrap in [`packages/core/src/lib/bootstrap/index.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/bootstrap/index.ts).

The strongest lesson is not "copy this whole architecture." The useful lesson is how much explicit platform machinery a real multi-tenant business app accumulates: request context, tenant/organization base entities, global auth guards, safe error filters, raw body preservation for webhooks, Redis-backed sessions, feature flags, plugin lifecycle hooks, dual TypeORM/MikroORM repositories, background workers, desktop local queues, and a Docker composition that brings databases, cache, object storage, search, analytics, and BI along for the ride.

## What they built

Gauzy is a full-stack open business-management platform. The user-facing surface includes the Angular web app under [`apps/gauzy`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/gauzy), API and server entrypoints under [`apps/api`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api), desktop shells under [`apps/desktop`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/desktop) and [`apps/desktop-timer`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/desktop-timer), plus a worker in [`apps/worker`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/worker).

The server domain is concentrated in [`packages/core/src/lib`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib). That directory has many Nest modules for employees, organizations, invoices, products, reports, tasks, approvals, time off, integrations, payments, dashboards, public shares, and time tracking. The task module is representative: [`packages/core/src/lib/tasks/task.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/task.module.ts) wires TypeORM and MikroORM repositories, CQRS, notifications, roles, employees, projects, sprints, and an event bus; [`task.controller.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/task.controller.ts) exposes filtered task endpoints; [`task.service.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/task.service.ts) handles updates, HTML sanitization, activity logs, mentions, sprint movement history, and employee subscriptions.

There is also a serious plugin layer. [`apps/api/src/plugins.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugins.ts) registers Sentry, PostHog, Jitsu analytics, AI chat, AI providers, docs, changelog, Activepieces, GitHub, Hubstaff, Jira, Upwork, Plane, Zapier, job plugins, product reviews, video/docs plugins, screenshot/soundshot plugins, and a registry plugin. [`packages/plugin/src/lib/plugin.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/plugin/src/lib/plugin.module.ts) provides the lifecycle runner for `onPluginBootstrap` and `onPluginDestroy`.

## Why it matters

Most trending repos are easy to admire and hard to learn from because they hide the boring parts. Gauzy is the opposite: the boring parts are the point. A real ERP/HRM/time-tracking product has to bind together multi-tenancy, organization scoping, permissions, billing, file storage, search, analytics, background work, OAuth, desktop capture, offline behavior, and deployment.

The code is also a useful warning. This kind of platform is powerful, but it carries a lot of ceremony. [`packages/core/src/lib/app/app.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/app/app.module.ts) imports a very large set of domain modules into one Nest application. That is convenient for a mature monolith, but the dependency graph can become hard to reason about without strong boundaries and tooling.

## Repo shape at a glance

- [`apps`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps): runnable applications: API, web app, desktop, desktop timer, CLI, MCP/server variants, and worker.
- [`packages/core`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core): main NestJS domain and platform core.
- [`packages/contracts`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/contracts): shared interfaces and enums consumed across API/UI/desktop.
- [`packages/plugin`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/plugin): plugin lifecycle and helper layer.
- [`packages/plugins`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/plugins): bundled functional plugins, including AI providers, integrations, docs, jobs, analytics, screenshots, and registry.
- [`packages/desktop-lib`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-lib), [`packages/desktop-activity`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-activity), and [`packages/desktop-window`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-window): Electron tracking, activity, window, tray, screenshot, local storage, and offline support.
- [`.deploy`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/.deploy), [`docker-compose.yml`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/docker-compose.yml), and [`docker-compose.infra.yml`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/docker-compose.infra.yml): production, demo, desktop, Kubernetes, Redis, MinIO, search, analytics, and worker deployment surface.

## Layered architecture dissection

### High-level system shape

Gauzy is a modular monolith with multiple clients. The web app and desktop shells call a shared API. The API loads a plugin config from [`apps/api/src/plugin.config.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugin.config.ts), starts through [`apps/api/src/main.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/main.ts), and boots the Nest app through [`packages/core/src/lib/bootstrap/index.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/bootstrap/index.ts). The domain modules are gathered in [`packages/core/src/lib/app/app.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/app/app.module.ts).

The desktop timer is not just a web wrapper. [`packages/desktop-lib/src/lib/desktop-timer.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-lib/src/lib/desktop-timer.ts) runs local activity capture, active-window tracking, screenshot timing, ActivityWatch integration, local queueing, offline state, and IPC messages to the timer window.

### Main layers

**Workspace and build layer**  
[`package.json`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/package.json), [`nx.json`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/nx.json), and [`lerna.json`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/lerna.json) hold the monorepo control plane. Scripts build API, web, worker, packages, plugins, and Electron targets separately.

**API bootstrap layer**  
[`packages/core/src/lib/bootstrap/index.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/bootstrap/index.ts) does the unglamorous but important work: secret validation, dynamic bootstrap-module import, global auth guard, raw-body capture for webhooks, CORS, Redis/in-memory sessions, Helmet, global `/api` prefix, database error filtering, validation container wiring, seeding, Swagger, and server listen.

**Domain module layer**  
[`packages/core/src/lib/app/app.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/app/app.module.ts) imports the business modules. The domain shape is wide: employees, candidates, goals, invoices, products, integrations, tasks, reports, tags, teams, time tracking, warehouse, and more.

**Persistence and multi-tenancy layer**  
Base entities such as [`packages/core/src/lib/core/entities/tenant-organization-base.entity.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/core/entities/tenant-organization-base.entity.ts) make organization and tenant scoping first-class. The task module's [`TypeOrmTaskRepository`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/repository) and `MikroOrmTaskRepository` pattern shows that the project carries dual ORM abstractions.

**CRUD/API convention layer**  
[`packages/core/src/lib/core/crud/crud.controller.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/core/crud/crud.controller.ts) centralizes count, pagination, find, create, update, delete, soft-remove, and restore behavior. Concrete controllers, such as [`packages/core/src/lib/tasks/task.controller.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/task.controller.ts), extend the base for ordinary CRUD and add product-specific endpoints.

**Plugin layer**  
[`packages/plugin/src/lib/plugin.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/plugin/src/lib/plugin.module.ts) imports configured plugin modules and calls their lifecycle hooks. [`apps/api/src/plugins.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugins.ts) is the concrete registry for this API build.

**Desktop activity layer**  
[`packages/desktop-lib/src/lib/desktop-timer.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-lib/src/lib/desktop-timer.ts) coordinates timers, screenshots, active-window events, keyboard/mouse activity, ActivityWatch services, local DB queues, offline flags, audit logs, and UI events. Supporting packages like [`packages/desktop-activity`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-activity) isolate event counting and queues.

**Deployment layer**  
[`docker-compose.yml`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/docker-compose.yml) runs API and webapp containers and includes [`docker-compose.infra.yml`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/docker-compose.infra.yml) for dependencies like database, Redis, MinIO, OpenSearch, Cube, Jitsu, and tracing.

### Request / data / control flow

A normal API run begins in [`apps/api/src/main.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/main.ts). It loads environment, imports core `bootstrap`, imports [`plugin.config.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugin.config.ts), then calls `bootstrap(pluginConfig)`.

Bootstrap builds the Nest app from [`BootstrapModule`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/bootstrap/bootstrap.module.ts), applies global guard/filter/middleware behavior, seeds when needed, and exposes the `/api` prefix. Requests then flow through global auth and tenant guards into controllers like [`TaskController`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/task.controller.ts). Task creation uses CQRS commands; task update in [`TaskService`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/task.service.ts) fetches the existing task, applies updates, records sprint movement, syncs mentions, changes subscriptions, and logs activity.

Desktop time tracking has a different control flow. The Electron timer invokes [`TimerHandler.startTimer`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-lib/src/lib/desktop-timer.ts), clears activity-watch events, starts event and active-window counters, updates local application settings, creates a local timer record, then periodically gathers activity and screenshots through local queues before syncing with the API.

## Key directories and files

- [`README.md`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/README.md): product scope, stack, deployment options, and quick-start paths.
- [`package.json`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/package.json): workspace scripts and the real shape of the build.
- [`apps/api/src/main.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/main.ts): production API entrypoint.
- [`apps/api/src/plugin.config.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugin.config.ts): API config, DB config, asset paths, logger wiring, and plugin list binding.
- [`apps/api/src/plugins.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugins.ts): configured plugin registry for this API.
- [`packages/core/src/lib/bootstrap/index.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/bootstrap/index.ts): server startup and cross-cutting middleware.
- [`packages/core/src/lib/app/app.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/app/app.module.ts): large Nest module aggregation point.
- [`packages/core/src/lib/core/entities/tenant-organization-base.entity.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/core/entities/tenant-organization-base.entity.ts): tenant/organization base relation pattern.
- [`packages/core/src/lib/core/crud/crud.controller.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/core/crud/crud.controller.ts): generic API controller surface.
- [`packages/core/src/lib/tasks/task.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/task.module.ts), [`task.controller.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/task.controller.ts), and [`task.service.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/task.service.ts): representative domain module.
- [`packages/plugin/src/lib/plugin.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/plugin/src/lib/plugin.module.ts): plugin lifecycle execution.
- [`packages/desktop-lib/src/lib/desktop-timer.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-lib/src/lib/desktop-timer.ts): local time-tracking loop.
- [`docker-compose.yml`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/docker-compose.yml): deployed service graph.

## Important components

The first important component is the bootstrapper in [`packages/core/src/lib/bootstrap/index.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/bootstrap/index.ts). It centralizes cross-cutting production behavior, including raw body capture for HMAC-verified webhooks and a database error filter that prevents query internals from leaking to clients.

The second is the tenant-aware domain model. [`TenantOrganizationBaseEntity`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/core/entities/tenant-organization-base.entity.ts) embeds `organization` and `organizationId` with relation decorators and validation. That pattern repeats because every ERP-ish record needs scoping.

The third is the plugin system. [`PluginModule`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/plugin/src/lib/plugin.module.ts) is simple but important: it imports configured plugins and calls lifecycle hooks. [`apps/api/src/plugins.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugins.ts) shows the platform is using plugins as a product-extension mechanism, not just as optional integrations.

The fourth is desktop tracking. [`TimerHandler`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-lib/src/lib/desktop-timer.ts) is where the employee-monitoring product surface becomes concrete: event counters, active-window state, periodic screenshots, ActivityWatch collection, local timers, offline sync flags, and UI pushes.

## Important knobs / configs / extension points

- [`apps/api/src/plugin.config.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugin.config.ts): API host/port/base URL, GraphQL path, TypeORM/MikroORM/Knex configs, asset paths, logger composition, and plugin list.
- [`apps/api/src/plugins.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugins.ts): product/plugin extension surface.
- [`packages/core/src/lib/bootstrap/validate-secrets.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/bootstrap/validate-secrets.ts): startup validation for auth/session secret hygiene.
- [`packages/core/src/lib/bootstrap/redis-store.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/bootstrap/redis-store.ts): session-store choice.
- [`packages/core/src/lib/app/app.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/app/app.module.ts): module inclusion, cache, i18n, throttling, scheduler, and feature flag wiring.
- [`package.json`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/package.json): build and seed scripts. The scripts reveal the operational lifecycle better than the README.
- [`docker-compose.yml`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/docker-compose.yml): runtime service graph and dependency assumptions.

## Practical questions and answers

**Is this a clean microservice architecture?**  
No. It is a large modular monolith with multiple app targets. [`packages/core/src/lib/app/app.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/app/app.module.ts) pulls a broad domain surface into one application. That is easier to deploy than a fleet of services, but the module graph needs discipline.

**Where is multi-tenancy handled?**  
At several layers. Entities inherit tenant/organization shape from base classes such as [`TenantOrganizationBaseEntity`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/core/entities/tenant-organization-base.entity.ts), request context is handled in core context modules, and controllers use tenant/permission guards like the ones on [`TaskController`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/task.controller.ts).

**What part would be hardest to reproduce?**  
The desktop time-tracking and offline-sync path. [`packages/desktop-lib/src/lib/desktop-timer.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-lib/src/lib/desktop-timer.ts) shows the amount of edge-case handling hidden behind a simple "track time" feature.

**Is the plugin story real?**  
Yes. [`apps/api/src/plugins.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugins.ts) has a concrete list, and [`PluginModule`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/plugin/src/lib/plugin.module.ts) executes lifecycle hooks. It is not just a folder named plugins.

**What is the main production risk?**  
Operational sprawl. [`docker-compose.yml`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/docker-compose.yml) and [`docker-compose.infra.yml`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/docker-compose.infra.yml) make clear that a serious deployment is more than an API and database. Search, storage, cache, analytics, tracing, worker processes, and secret hygiene all matter.

## What is smart

- The bootstrapper in [`packages/core/src/lib/bootstrap/index.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/bootstrap/index.ts) centralizes production cross-cutting concerns instead of scattering them through controllers.
- The repo keeps tenant/organization scoping explicit through base entities like [`TenantOrganizationBaseEntity`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/core/entities/tenant-organization-base.entity.ts).
- The generic [`CrudController`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/core/crud/crud.controller.ts) gives many modules a consistent API baseline.
- The plugin config in [`apps/api/src/plugins.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugins.ts) makes optional product capabilities visible.
- The desktop timer treats offline/local state as first-class, not as an afterthought.

## What is flawed or weak

- The main Nest module in [`packages/core/src/lib/app/app.module.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/app/app.module.ts) is extremely wide. It is understandable for a mature monolith, but it is not easy to scan or test mentally.
- The public [`README.md`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/README.md) mixes platform documentation, marketing, SaaS notes, downloads, and deployment advice. Builders need to read source to understand the actual system.
- Dual ORM support is powerful but expensive. [`TaskModule`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/tasks/task.module.ts) carrying both TypeORM and MikroORM repositories is a useful example of flexibility increasing surface area.
- Time/activity monitoring is inherently sensitive. [`desktop-timer.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-lib/src/lib/desktop-timer.ts) is technically interesting, but any product using this pattern needs unusually clear consent, policy, retention, and audit behavior.

## What we can learn / steal

- Put production hygiene in one bootstrap layer. Raw-body capture, CORS, Helmet, secret validation, auth guards, database error filters, and request limits belong somewhere explicit like [`bootstrap/index.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/core/src/lib/bootstrap/index.ts).
- Use base entities and DTOs to make tenant scoping repetitive in a good way.
- Keep plugin discovery and plugin lifecycle separate. [`apps/api/src/plugins.ts`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/api/src/plugins.ts) says what is loaded; [`PluginModule`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/plugin/src/lib/plugin.module.ts) says how lifecycle runs.
- Treat desktop offline behavior as a real subsystem. Local queues, audit logs, active-window events, screenshots, and sync status need their own library boundary.
- Use compose/deploy files as architecture documentation. [`docker-compose.yml`](https://github.com/ever-co/ever-gauzy/blob/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/docker-compose.yml) is more honest about runtime needs than most architecture diagrams.

## How we could apply it

For a multi-tenant internal platform, I would copy the base-entity pattern, the centralized bootstrap hygiene, and the plugin lifecycle shape. I would not copy the whole breadth of modules unless the product truly needs it.

For an app with web and desktop clients, I would copy the separation between application shell and reusable desktop libraries. Gauzy's [`apps/desktop-timer`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/apps/desktop-timer) is an app; [`packages/desktop-lib`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-lib) and [`packages/desktop-activity`](https://github.com/ever-co/ever-gauzy/tree/5576e9ad07ef6711afc2d5cd0e7309a7c1fc76e8/packages/desktop-activity) are reusable capability layers.

For our own builder notes, Gauzy is also a reminder to inspect product repos below the README. The interesting code is often in bootstrap files, config files, base entities, queues, and deployment glue, not just in the main feature controller.

## Bottom line

`ever-co/ever-gauzy` is worth studying because it is a real platform repo with real platform weight. The clean takeaway is not a glamorous algorithm; it is the source shape of a large open SaaS product: monorepo apps, a big Nest domain core, explicit tenant scoping, plugin lifecycle, Electron activity tracking, and operational deployment files.

The best thing to steal is its explicitness around platform machinery. The thing to distrust is the cost of carrying so much breadth in one repo unless the product and team are ready to own it.
