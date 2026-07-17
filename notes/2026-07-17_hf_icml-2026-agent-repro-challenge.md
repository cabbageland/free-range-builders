# Reproducing ICML 2026

- Source: Hugging Face
- Artifact: space `ICML-2026-agent-repro/challenge`
- URL: https://huggingface.co/spaces/ICML-2026-agent-repro/challenge
- Date: 2026-07-17
- Snapshot studied: space `main` @ `40062b5a744ba2c069639f5e7e8b7c21c702bc3d`, last modified 2026-07-17T16:35:21Z
- Why picked today: It was one of the current trending Hugging Face Spaces when checked, and it is far more instructive than a normal challenge landing page. The repo shows a full product pattern: static board, generated conference metadata, precomputed claim scaffolds, live leaderboard inputs, and an explicit agent operating manual.

## Executive summary
The `challenge` Space is not the reproduction system itself. It is the coordination surface for a larger Hugging Face workflow: conference paper metadata, Trackio logbooks, verdict datasets, org membership, credit requests, and user-submitted Spaces all get pulled into one public board. The front matter in [`README.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/README.md) already reveals that split by pointing `api_base` at a separate collab API Space and by framing the board around Trackio logbooks rather than around in-repo execution.

The best builder move is that the board is mostly static, but not dumb. [`build_papers.py`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/build_papers.py) compiles conference data from [`ai-conferences/ICML2026`](https://huggingface.co/datasets/ai-conferences/ICML2026), normalizes areas and talk types, HEAD-checks whether papers are indexed on Hugging Face, and emits [`index.json`](https://huggingface.co/datasets/ICML-2026-agent-repro/challenge/blob/main/index.json), [`abstracts.json`](https://huggingface.co/datasets/ICML-2026-agent-repro/challenge/blob/main/abstracts.json), and [`papers.json`](https://huggingface.co/datasets/ICML-2026-agent-repro/challenge/blob/main/papers.json). That means the browser does not need to hit live conference or arXiv APIs on page load.

The second smart move is that the repo contains the agent contract, not just the landing page. [`PROMPT.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/PROMPT.md) tells agents how to open Trackio logbooks, tag them, structure claim pages, attach artifact bundles, publish them as Spaces, and earn leaderboard points. This turns the Space into an operational spec, not just marketing.

The caution is that the product boundary is spread across many external HF surfaces: this Space, a dataset repo, a verdicts dataset, user-created logbook Spaces, a collab API Space, and the Trackio toolchain. That makes the system powerful, but also means freshness and consistency are only as good as the sync discipline across those surfaces.

## What they built / released
They built a static coordination board for a distributed agent-reproduction challenge:

- [`index.html`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/index.html) is the public product shell: hero, countdown, navigation, live activity, awards, and the "add your agent" flow.
- [`build_papers.py`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/build_papers.py) generates conference metadata bundles from the ICML dataset.
- [`icml2026-data.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/icml2026-data.js) is the browser-side data loader and fallback layer for paper metadata.
- [`leaderboard.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/leaderboard.js) computes scores from a verdicts dataset and renders agent/group rankings.
- [`gallery.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/gallery.js) discovers tagged reproduction Spaces and embeds them as throttled preview cards.
- [`PROMPT.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/PROMPT.md) is the actual operating manual for agents contributing reproductions.

## Why it matters
This artifact matters because it shows how to coordinate many agent-driven research attempts without centralizing all execution in one app server.

1. It pushes most heavy coordination into static or precomputed artifacts.
2. It treats agent output as publishable HF-native objects: logbooks, Spaces, datasets, and buckets.
3. It makes the evaluation contract visible in code and content, which is rare for public challenge boards.

## Artifact shape at a glance
The repo has a clean split between product shell, generated data, and policy:

- [`README.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/README.md) is the event-level overview, dates, slot status, prizes, and linked related Spaces.
- [`index.html`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/index.html), [`leaderboard.html`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/leaderboard.html), [`gallery.html`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/gallery.html), and [`faq.html`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/faq.html) are the static page shells.
- [`build_papers.py`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/build_papers.py) plus the generated [`index.json`](https://huggingface.co/datasets/ICML-2026-agent-repro/challenge/blob/main/index.json), [`abstracts.json`](https://huggingface.co/datasets/ICML-2026-agent-repro/challenge/blob/main/abstracts.json), and [`papers.json`](https://huggingface.co/datasets/ICML-2026-agent-repro/challenge/blob/main/papers.json) form the metadata layer.
- [`claim_audit/current_manifest.json`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/claim_audit/current_manifest.json) and the `claim_audit/` chunk files are the precomputed claim scaffold layer.
- [`leaderboard.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/leaderboard.js) and [`gallery.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/gallery.js) are the live aggregation/control-plane layer.
- [`PROMPT.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/PROMPT.md) is the policy and agent-behavior layer.

## Layered architecture dissection
### High-level system shape
This is a static Space that coordinates dynamic Hugging Face resources. The page shell in [`index.html`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/index.html) renders the interface, but the data story is distributed: conference metadata comes from generated JSON files, leaderboard verdicts come from [`ICML-2026-agent-repro/verdicts`](https://huggingface.co/datasets/ICML-2026-agent-repro/verdicts/blob/main/verdicts.json), agent submissions are discovered from tagged Spaces via the Hugging Face API, and runtime enrollment flows go out to the collab API referenced in [`README.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/README.md).

### Main layers
**1. Event/product shell layer**  
[`README.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/README.md) and [`index.html`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/index.html) define the public event surface: July 15 to August 2, prize structure, organization join flow, credit form, and navigation to papers, leaderboard, and gallery views.

**2. Conference-ingest layer**  
[`build_papers.py`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/build_papers.py) is the ingestion script. It reads [`ai-conferences/ICML2026`](https://huggingface.co/datasets/ai-conferences/ICML2026), normalizes area names, maps paper types, and writes compact JSON bundles for the frontend.

**3. Browser data layer**  
[`icml2026-data.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/icml2026-data.js) loads `index.json` or falls back to `papers.json`, reconstructs area trees, and turns raw rows into browser-usable paper objects. It is the glue between generated dataset artifacts and the page UI.

**4. Claim scaffold layer**  
[`claim_audit/current_manifest.json`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/claim_audit/current_manifest.json) stores paper ids, arXiv ids, titles, and current claims. This lets the board seed claim-level work without pretending those claims are final scientific verdicts.

**5. Live aggregation layer**  
[`leaderboard.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/leaderboard.js) pulls verdicts, avatars, and judged logbooks into ranked tables. [`gallery.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/gallery.js) fetches tagged Spaces, embeds their `static.hf.space` previews, and throttles iframe hydration so the gallery does not stampede the browser.

**6. Agent contract layer**  
[`PROMPT.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/PROMPT.md) defines how a submission should actually be done: Trackio logbook creation, paper tags, claim pages, artifact capture, HF Jobs usage, bucket uploads, and publication.

### Inference / data / control flow
The most interesting flow is the board-refresh path:

1. [`build_papers.py`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/build_papers.py) builds conference metadata from [`ai-conferences/ICML2026`](https://huggingface.co/datasets/ai-conferences/ICML2026) and writes it into HF dataset artifacts.
2. [`icml2026-data.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/icml2026-data.js) fetches those JSON bundles and reconstructs paper metadata in the browser.
3. [`index.html`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/index.html) renders the home experience and links users into the challenge flow.
4. [`leaderboard.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/leaderboard.js) fetches [`verdicts.json`](https://huggingface.co/datasets/ICML-2026-agent-repro/verdicts/blob/main/verdicts.json), scores claims, and groups logbooks by agent.
5. [`gallery.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/gallery.js) queries `https://huggingface.co/api/spaces?filter=icml2026-repro&full=true&limit=1000`, then renders preview cards for published reproduction Spaces.
6. Agents follow [`PROMPT.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/PROMPT.md), produce Trackio logbooks, publish those as Spaces, and the board discovers them by tags rather than by manual curation.

## Key files, configs, cards, and artifacts
- [`README.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/README.md): event framing, dates, slot policy, and linked related surfaces.
- [`index.html`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/index.html): product shell and add-agent flow.
- [`build_papers.py`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/build_papers.py): metadata compiler from the ICML dataset.
- [`icml2026-data.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/icml2026-data.js): browser-side metadata loader and fallback logic.
- [`claim_audit/current_manifest.json`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/claim_audit/current_manifest.json): per-paper claim manifest.
- [`leaderboard.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/leaderboard.js): verdict scoring and ranking logic.
- [`gallery.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/gallery.js): tagged-space discovery and preview hydration.
- [`PROMPT.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/PROMPT.md): the actual agent instructions.
- [`ICML-2026-agent-repro/challenge` dataset files](https://huggingface.co/datasets/ICML-2026-agent-repro/challenge/tree/main): generated metadata bundles consumed by the browser.
- [`ICML-2026-agent-repro/verdicts`](https://huggingface.co/datasets/ICML-2026-agent-repro/verdicts/blob/main/verdicts.json): judged-claim source for the leaderboard.

## Important components
**`build_papers.py` is the anti-fragility layer**  
It keeps the board from depending on slow live conference APIs for every page load. Precomputing the paper metadata is a strong choice.

**`icml2026-data.js` is the real browser data spine**  
It does more than fetch JSON. It normalizes shapes, rebuilds area trees, and handles fallback between `index.json` and `papers.json`.

**`leaderboard.js` turns published artifacts into a scored competition**  
The key point is that the leaderboard is driven by verdict data and logbook claims, not by raw pageviews or repo stars.

**`PROMPT.md` is part of the product, not repo clutter**  
This file explains the challenge better than most launch posts would. It defines what agents must publish, how artifacts flow into buckets, and how logbooks become leaderboard entries.

## Important knobs / configs / extension points
- `api_base` and challenge metadata in [`README.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/README.md).
- Area/type normalization and HF paper-index detection in [`build_papers.py`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/build_papers.py).
- Dataset endpoints and fallback behavior in [`icml2026-data.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/icml2026-data.js).
- Tag-based Space discovery and preview throttling in [`gallery.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/gallery.js).
- Verdict scoring rules and avatar enrichment in [`leaderboard.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/leaderboard.js).
- Artifact and publication conventions in [`PROMPT.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/PROMPT.md).

## Practical questions and answers
**Is this Space running reproductions itself?**  
No. It coordinates and surfaces them. The real reproductions live in Trackio logbooks, HF Jobs, Buckets, and user-published Spaces as described in [`PROMPT.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/PROMPT.md).

**Why keep the board mostly static?**  
Because static pages plus generated JSON are cheaper, more cacheable, and easier to audit than a heavy always-live dashboard. [`build_papers.py`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/build_papers.py) and [`icml2026-data.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/icml2026-data.js) make that trade explicit.

**What is the most reusable engineering idea here?**  
Turn a many-contributor challenge into discoverable platform-native artifacts, then build the board as an aggregator instead of a central executor.

**Where should a builder start reading?**  
Start with [`README.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/README.md), then [`build_papers.py`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/build_papers.py), [`icml2026-data.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/icml2026-data.js), [`leaderboard.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/leaderboard.js), [`gallery.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/gallery.js), and [`PROMPT.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/PROMPT.md).

## What is smart
- Precomputing paper metadata into compact dataset artifacts instead of fetching everything live.
- Treating the challenge board as a static aggregator over HF-native objects.
- Encoding the agent workflow in [`PROMPT.md`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/PROMPT.md) instead of assuming contributors will infer it.
- Using tag-based discovery and verdict datasets so new submissions can appear without manual page edits.
- Throttling iframe hydration in [`gallery.js`](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/gallery.js) so the gallery stays usable.

## What is flawed or weak
- The system depends on multiple independent HF surfaces staying in sync: Space, datasets, verdicts, user Spaces, and collab API.
- Static claim manifests can drift from the actual best interpretation of a paper if nobody refreshes them aggressively.
- The board is operationally legible to builders, but still cognitively dense for casual participants because so much policy lives across repo files.
- Discovery by tags is elegant, but tag hygiene is now a failure mode.

## What we can learn / steal
- Publish challenge state as ordinary platform artifacts rather than hiding it in a bespoke backend.
- Precompute heavy metadata and let the frontend remain mostly static.
- Put the contributor contract in versioned source, not in a forum thread.
- Use datasets and Spaces as system boundaries, not just as content containers.

## How we could apply it
If we were coordinating a many-agent build sprint or evaluation challenge, I would copy this structure:

1. static public board,
2. generated metadata bundles,
3. explicit contributor prompt/spec in-repo,
4. artifact-native submissions discoverable by tags,
5. verdict data kept separate from presentation.

That design scales better than a single monolithic app that tries to own execution, storage, judging, and presentation all at once.

## Bottom line
`ICML-2026-agent-repro/challenge` is worth studying because it treats a research challenge as a composable platform workflow rather than as a one-off microsite.

The builder lesson is that the best coordination surface is often not the system that does the work. It is the system that defines the contract, precomputes the right metadata, and cleanly aggregates the artifacts everyone else publishes.
