# Scrapling

- Repo: `D4Vinci/Scrapling`
- URL: https://github.com/D4Vinci/Scrapling
- Date: 2026-06-01
- Repo snapshot studied: `main` @ `a6a57eee448a6246b5f6610ac5662ecd1c5f6adc`
- Why picked today: It was one of GitHub Trending's hotter repos on June 1, 2026, it is practical rather than purely vibes, and it has real implementation surface across parsing, stealth fetching, session management, and a full crawler layer.

## Executive summary
Scrapling is trying to collapse three usually separate tools into one Python package: an HTML parser with selector recovery, a stealth/browser fetching layer, and a Scrapy-like crawler runtime.

The most interesting part is not the anti-bot pitch. It is the way the repo joins adaptive element lookup to the request/crawl machinery. The parser can save element fingerprints into storage and later relocate them when markup shifts, which is a more durable idea than yet another "headless browser wrapper."

The main caveat is that the repo also leans hard into stealth/bypass positioning and a sponsor-heavy README. The code is more serious than the marketing, but some of the product story is still tuned for scraper-operator desire more than architectural clarity.

## What they built
They built a layered scraping toolkit centered on the Python package in [`scrapling/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling):
- core parsing and adaptive selector logic in [`scrapling/parser.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/parser.py) and [`scrapling/core/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/core)
- fetcher abstractions in [`scrapling/fetchers/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/fetchers) that wrap plain HTTP, browser automation, and stealth browser sessions
- engine internals in [`scrapling/engines/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/engines) for browser control, fingerprints, navigation helpers, and proxy rotation
- a crawler framework in [`scrapling/spiders/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/spiders) with requests, scheduler, sessions, checkpointing, robots.txt support, and streaming results
- operator surfaces in [`scrapling/cli.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/cli.py), [`scrapling/core/ai.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/ai.py), and the docs tree in [`docs/`](https://github.com/D4Vinci/Scrapling/tree/main/docs)

This is not just a parser library. It is trying to be the full scraping stack from one-off extraction to long-running crawls.

## Why it matters
Most scraping repos are strong in exactly one area:
- parsing
- browser automation
- anti-bot tactics
- or crawler orchestration

Scrapling is interesting because it tries to unify all four. That is ambitious, and the repo shape shows the ambition is real.

The reusable lesson is that resilient scraping is mostly a systems integration problem. Selector durability, session reuse, proxy rotation, request scheduling, blocked-request handling, and development-mode replay matter as much as raw browser stealth.

## Repo shape at a glance
Top-level structure:
- [`scrapling/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling), main package
- [`tests/`](https://github.com/D4Vinci/Scrapling/tree/main/tests), coverage across parser, fetchers, spiders, CLI, and AI surfaces
- [`docs/`](https://github.com/D4Vinci/Scrapling/tree/main/docs), fairly large user and API documentation set
- [`agent-skill/`](https://github.com/D4Vinci/Scrapling/tree/main/agent-skill), agent-oriented packaging around the project
- [`.github/workflows/`](https://github.com/D4Vinci/Scrapling/tree/main/.github/workflows), CI
- root config files like [`pyproject.toml`](https://github.com/D4Vinci/Scrapling/blob/main/pyproject.toml), [`pytest.ini`](https://github.com/D4Vinci/Scrapling/blob/main/pytest.ini), [`ruff.toml`](https://github.com/D4Vinci/Scrapling/blob/main/ruff.toml), and [`tox.ini`](https://github.com/D4Vinci/Scrapling/blob/main/tox.ini)

Inside [`scrapling/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling), the major split is:
- [`scrapling/parser.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/parser.py), selector model and adaptive lookup surface
- [`scrapling/core/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/core), storage, type plumbing, shell helpers, AI support, and selector translation
- [`scrapling/fetchers/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/fetchers), public request APIs
- [`scrapling/engines/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/engines), low-level HTTP/browser/session machinery
- [`scrapling/spiders/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/spiders), crawl runtime
- [`scrapling/cli.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/cli.py), command-line entrypoint

The repo is structured more like a framework than a utility package.

## Layered architecture dissection
### High-level system shape
At a high level the system looks like this:
1. users enter through the parser API in [`scrapling/parser.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/parser.py), fetchers in [`scrapling/fetchers/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/fetchers), spiders in [`scrapling/spiders/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/spiders), or CLI in [`scrapling/cli.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/cli.py)
2. fetchers route into static and browser engines under [`scrapling/engines/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/engines)
3. fetched HTML becomes `Selector` objects in [`scrapling/parser.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/parser.py)
4. adaptive selector state is persisted via storage implementations in [`scrapling/core/storage.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/storage.py)
5. larger crawls are orchestrated by [`scrapling/spiders/engine.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/engine.py), [`scrapling/spiders/scheduler.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/scheduler.py), and [`scrapling/spiders/session.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/session.py)
6. optional operator layers expose shell and MCP entrypoints through [`scrapling/cli.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/cli.py) and [`scrapling/core/ai.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/ai.py)

### Main layers
**1. Packaging and dependency layer**
- [`pyproject.toml`](https://github.com/D4Vinci/Scrapling/blob/main/pyproject.toml) is the first important file because it reveals the real split: a small core, then optional `fetchers`, `ai`, and `shell` extras.
- The core dependency set is lightweight for parsing, but the optional extras pull in `curl_cffi`, Playwright, Patchright, browser fingerprint tooling, and MCP support.

This is smart because it keeps the parser usable without forcing everyone to install the browser stack.

**2. Parsing and adaptive selection layer**
- [`scrapling/parser.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/parser.py) is the center of gravity.
- The `Selector` object wraps lxml nodes, normalizes parsing options, and can globally enable adaptive behavior.
- [`scrapling/core/storage.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/storage.py) provides the default SQLite-backed persistence for saved element fingerprints, keyed by normalized base URL and identifier.
- [`scrapling/core/mixins.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/mixins.py) and [`scrapling/core/translator.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/translator.py) support selector generation and CSS/XPath translation.

This is the layer that gives Scrapling a real technical identity.

**3. Fetching and browser execution layer**
- [`scrapling/fetchers/requests.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/fetchers/requests.py) exposes sync and async HTTP fetchers over a shared client.
- [`scrapling/fetchers/stealth_chrome.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/fetchers/stealth_chrome.py) exposes the stealth browser surface and merges parser config into request-time selector settings.
- [`scrapling/engines/_browsers/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/engines/_browsers) holds browser config, controllers, page wrappers, stealth behavior, and validators.
- [`scrapling/engines/toolbelt/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/engines/toolbelt) contains practical support pieces like [`proxy_rotation.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/engines/toolbelt/proxy_rotation.py), [`fingerprints.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/engines/toolbelt/fingerprints.py), and [`navigation.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/engines/toolbelt/navigation.py).

This layer is broad, but the public API is kept fairly compact.

**4. Spider and crawl runtime layer**
- [`scrapling/spiders/spider.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/spider.py) defines the user-facing spider contract, hooks, retry policies, logging, and session configuration.
- [`scrapling/spiders/engine.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/engine.py) runs the crawl, handles callbacks, blocked-request retries, domain throttling, cache replay, and checkpointing.
- [`scrapling/spiders/session.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/session.py) is one of the more important files because it lets a single spider mix plain HTTP and browser-backed sessions behind stable IDs.
- [`scrapling/spiders/checkpoint.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/checkpoint.py), [`scrapling/spiders/cache.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/cache.py), and [`scrapling/spiders/robotstxt.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/robotstxt.py) make the runtime feel like a real framework rather than a thin async loop.

This is the least toy-like part of the repo.

**5. Operator and agent layer**
- [`scrapling/cli.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/cli.py) packages install flows, extraction commands, a shell, and an MCP server launch command.
- [`scrapling/core/ai.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/ai.py) wraps browser sessions and extraction operations in an MCP server.
- [`agent-skill/`](https://github.com/D4Vinci/Scrapling/tree/main/agent-skill) shows the team wants the project to be consumed by AI agents, not just human scraper authors.

This layer is a good example of a repo chasing distribution, not just library purity.

### Request / data / control flow
A typical flow looks like this:
1. a request is created through a fetcher in [`scrapling/fetchers/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/fetchers) or a spider in [`scrapling/spiders/request.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/request.py)
2. the request is executed by HTTP or browser session logic in [`scrapling/engines/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/engines)
3. the response is converted into parsing-friendly objects and surfaced as selectors via [`scrapling/parser.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/parser.py)
4. if `auto_save` or adaptive lookup is used, element characteristics are persisted in [`scrapling/core/storage.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/storage.py)
5. in crawl mode, [`scrapling/spiders/engine.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/engine.py) dispatches results, retries blocked requests, obeys robots and rate limits when configured, and emits items or new requests
6. optional CLI or MCP wrappers in [`scrapling/cli.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/cli.py) and [`scrapling/core/ai.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/ai.py) expose that machinery to operators and agent tools

The key insight is that adaptive parsing is not bolted on later. It sits close to the selector layer and can therefore influence the whole stack.

## Key directories and files
- [`pyproject.toml`](https://github.com/D4Vinci/Scrapling/blob/main/pyproject.toml), dependency and extra layout
- [`scrapling/parser.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/parser.py), core selector API
- [`scrapling/core/storage.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/storage.py), default adaptive-state persistence
- [`scrapling/fetchers/requests.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/fetchers/requests.py), public HTTP fetcher interface
- [`scrapling/fetchers/stealth_chrome.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/fetchers/stealth_chrome.py), public stealth browser interface
- [`scrapling/engines/_browsers/`](https://github.com/D4Vinci/Scrapling/tree/main/scrapling/engines/_browsers), browser control internals
- [`scrapling/engines/toolbelt/proxy_rotation.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/engines/toolbelt/proxy_rotation.py), proxy rotation support
- [`scrapling/spiders/spider.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/spider.py), spider contract and hooks
- [`scrapling/spiders/engine.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/engine.py), crawl orchestrator
- [`scrapling/spiders/session.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/session.py), unified session registry
- [`scrapling/cli.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/cli.py), operator CLI
- [`scrapling/core/ai.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/ai.py), MCP surface

## Important components
**`Selector` is the real product core**
[`scrapling/parser.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/parser.py) is the most important file because it owns the parser abstraction, the adaptive toggle, and the conversion layer that makes all fetchers feel unified.

**SQLite-backed adaptive storage is a pragmatic choice**
[`scrapling/core/storage.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/storage.py) uses an `RLock`, SQLite WAL mode, and URL-scoped keys. That is not glamorous, but it is exactly the kind of practical persistence choice that keeps “self-healing selectors” from being vapor.

**The session manager is an underappreciated piece**
[`scrapling/spiders/session.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/session.py) lets the crawl layer route requests through named sessions, lazily start expensive browser sessions, and reuse stateful clients. That is a strong design move.

**The crawler engine is where the framework earns its keep**
[`scrapling/spiders/engine.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/engine.py) shows real attention to blocked-request retries, per-domain limiters, cached replay, robots directives, and graceful pause/resume.

**The MCP layer is a distribution tactic**
[`scrapling/core/ai.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/ai.py) is not the intellectual center, but it is strategically useful. It turns the scraper into a tool server that agent environments can call directly.

## Important knobs / configs / extension points
- [`pyproject.toml`](https://github.com/D4Vinci/Scrapling/blob/main/pyproject.toml) controls the major install shapes via extras.
- [`scrapling/spiders/spider.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/spider.py) exposes crawler knobs like `concurrent_requests`, `concurrent_requests_per_domain`, `download_delay`, `robots_txt_obey`, `development_mode`, and `max_blocked_retries`.
- [`scrapling/spiders/session.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/session.py) is the main extension seam for mixing session types.
- [`scrapling/fetchers/stealth_chrome.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/fetchers/stealth_chrome.py) exposes a large stealth/browser tuning surface, including proxy, WebRTC, WebGL, Cloudflare solving, and selector config.
- [`scrapling/core/storage.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/storage.py) defines the storage abstraction, so the default SQLite strategy can be swapped for something else.
- [`scrapling/cli.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/cli.py) provides a user-facing extension surface through shell, extract, and MCP commands.

## Practical questions and answers
**Is this mostly a parser or mostly a crawler?**
It is trying to be both, with browser automation and anti-bot support glued in between.

**What is the most reusable idea here?**
Persist selector fingerprints near the parsing layer so element recovery becomes a first-class feature instead of an afterthought in crawler code.

**What looks production-minded?**
Checkpointing, development replay mode, robots handling, lazy browser session startup, per-domain concurrency control, and blocked-request retry hooks.

**What looks the most marketing-heavy?**
The anti-bot bypass framing and sponsor-heavy README. The codebase has substance, but the first impression is louder than the implementation needs.

**Would I trust the “automatically relocates your elements” claim blindly?**
No. I would treat it as a helpful resilience feature, not magic. Similarity-based recovery can save you from mild DOM drift, but not from severe semantic redesigns.

**Where is the likely maintenance burden?**
In the breadth of browser stealth internals and the promise to support everything from simple HTTP requests to multi-session crawls and MCP workflows in one package.

## What is smart
- Keeping the core parser usable without forcing the full browser stack.
- Making adaptive selection a storage-backed subsystem instead of a README claim.
- Treating sessions as named, reusable crawl resources in [`scrapling/spiders/session.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/session.py).
- Supporting development-mode response replay in [`scrapling/spiders/engine.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/engine.py), which is exactly the kind of thing scraper authors actually need.
- Shipping CLI and MCP surfaces so the project can travel into agent tooling ecosystems.

## What is flawed or weak
- The README is overstuffed. There is a lot of sponsor and bypass positioning before the architecture gets a chance to speak.
- The repo is taking on several hard problems at once: parsing, browser stealth, crawler orchestration, and AI-tool packaging. That breadth is useful but risky.
- The public surface area is large enough that long-term coherence could get harder as more fetcher/session modes accumulate.
- Any project that advertises anti-bot bypass so prominently will attract users whose expectations outrun what a general-purpose library can reliably guarantee.

## What we can learn / steal
- Put resilience close to the selector model, not only in the crawler loop.
- Treat browser sessions as durable named resources, not disposable helper objects.
- Add development replay to crawling frameworks so parse iteration does not require constant re-hits.
- Use optional extras to keep the core install clean while still supporting heavyweight workflows.

## How we could apply it
If we were building scraping or browser-automation infrastructure, I would copy three things first:
1. the session-manager pattern from [`scrapling/spiders/session.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/session.py)
2. the checkpoint and replay mindset from [`scrapling/spiders/engine.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/spiders/engine.py)
3. the storage-backed adaptive selector idea from [`scrapling/parser.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/parser.py) and [`scrapling/core/storage.py`](https://github.com/D4Vinci/Scrapling/blob/main/scrapling/core/storage.py)

I would be more cautious about copying the broad anti-bot promise. Better to adopt the architecture than the bravado.

## Bottom line
Scrapling is one of the more substantial scraping repos to trend recently because it is not just wrapping Playwright with nicer syntax. The repo is making a serious attempt to unify parser durability, stealth fetching, and crawler operations.

The best insight is simple: resilient scraping is not one trick. It is a stack. Scrapling understands that better than most repos in this category.