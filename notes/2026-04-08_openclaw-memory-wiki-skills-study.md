# OpenClaw study notes — memory, wiki, and skills framework

Date: 2026-04-08
Studied repo: `openclaw/openclaw`
Repo snapshot studied: `main` @ `210ee4cfd2c3ba760c28758efdd72762382d9570`
Latest upstream commit at study time: `fix(qqbot): support HTML entities in media tags (&lt; &gt;) (#60493)`

## Why this matters

OpenClaw is quietly building something more interesting than a normal chat assistant shell.

The important pattern is:

1. **plain markdown workspace memory for transparency and editability**
2. **semantic retrieval over that memory**
3. **an optional compiled wiki layer for structured, provenance-aware knowledge**
4. **a skill system that keeps the base prompt small but loads domain instructions on demand**
5. **plugin seams that let memory and wiki cooperate without becoming one tangled subsystem**

That combination is unusually strong. It feels practical, inspectable, and extensible instead of magical and opaque.

---

## Executive summary

My read: the newest OpenClaw memory/wiki/skills design is good in exactly the places many assistant systems are weak.

### Core architectural split

OpenClaw cleanly separates three things:

- **bootstrap identity/context**: `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, optional `BOOTSTRAP.md`, and `MEMORY.md`
- **retrieval memory runtime**: `memory_search`, `memory_get`, indexing, promotion, dreaming, recall
- **knowledge compilation layer**: `memory-wiki`, which builds a structured wiki beside memory rather than replacing it

That separation is important. It prevents “memory” from collapsing into one giant vague blob.

### Strongest ideas

- **Markdown-first memory** instead of hidden vector soup
- **On-demand recall** for `memory/*.md` instead of always injecting everything into prompt
- **Skills listed compactly, loaded lazily by reading the specific `SKILL.md` only when needed**
- **Wiki as a companion layer, not a replacement layer**
- **Public plugin seams** for corpus supplements and prompt supplements
- **Deterministic generated artifacts** (`agent-digest.json`, `claims.jsonl`) so agents/runtime do not need to scrape markdown
- **Bridge mode** that reuses public memory artifacts without violating plugin boundaries
- **Narrow mutation tools** like `wiki_apply` instead of encouraging raw freeform edits to generated sections

### What I think is most reusable for us

If we borrow anything, borrow the **layering**:

- raw notes/logs
- curated long-term memory
- retrieval/search layer
- compiled knowledge layer
- lightweight task-specific skill docs

That stack is better than trying to solve everything with “just vector DB” or “just prompt stuffing.”

---

## What the newest repo says, concretely

### 1) Workspace memory is file-based and explicit

OpenClaw’s docs are extremely clear: memory is persisted as plain markdown in the workspace.

Main files:

- `MEMORY.md` → durable facts, preferences, decisions
- `memory/YYYY-MM-DD.md` → daily notes / running context
- `DREAMS.md` → optional human-readable dreaming output

Important design detail:

- `MEMORY.md` is injected into normal sessions when present
- `memory/*.md` daily files are **not auto-injected**; they are accessed via `memory_search` / `memory_get`

Why this is smart:

- stable identity and durable facts remain easy to access
- daily notes do not bloat prompt context by default
- memory remains inspectable and editable by humans
- the system avoids pretending the model has persistent hidden memory

This is one of the best practical tradeoffs in the whole design.

---

### 2) Memory retrieval is not just dumb file grep

The builtin memory engine indexes `MEMORY.md` and `memory/*.md` into a per-agent SQLite DB.

From the docs:

- chunks are about **400 tokens with 80-token overlap**
- keyword search uses **FTS5 / BM25**
- vector search uses embeddings when a provider is configured
- hybrid search merges vector + BM25
- optional MMR reduces duplicate hits
- optional temporal decay downranks older daily notes
- evergreen files like `MEMORY.md` are not decayed

This is a very sane retrieval stack.

What I like here:

- it preserves exact string matching for IDs / config keys / symbols
- it also handles semantic recall for paraphrased facts
- it does not require external infra by default
- it stays local and per-agent

This is materially better than “embeddings only.” Exact keyword retrieval matters a lot in technical workflows.

---

### 3) The wiki is a second layer, not memory itself

This is the key conceptual move.

`memory-wiki` does **not** replace the active memory plugin.

Instead:

- the active memory plugin owns recall, promotion, indexing, dreaming
- `memory-wiki` compiles durable knowledge into a navigable wiki with claims, evidence, dashboards, and digests

This prevents a common category mistake:

- raw memory/logging is not the same thing as
- maintained knowledge synthesis

OpenClaw explicitly models them as different layers.

That’s right.

A good system should distinguish:

- what happened
- what seems important
- what we currently believe
- why we believe it
- where the evidence came from

The wiki layer is their answer to that distinction.

---

### 4) The wiki has actual structure, not just nicer notes

The wiki vault layout is deterministic:

- `entities/`
- `concepts/`
- `syntheses/`
- `sources/`
- `reports/`
- `.openclaw-wiki/cache/`

It also supports structured claim/evidence metadata, including fields like:

- claim `id`
- `text`
- `status`
- `confidence`
- `evidence[]`
- timestamps / update markers

This matters because it moves from “page prose” to “machine-usable belief objects.”

That unlocks:

- contradiction tracking
- freshness tracking
- low-confidence surfacing
- question surfacing
- claim-level provenance
- stable machine-facing digests

That is much closer to a serious knowledge system than a pile of markdown notes with backlinks.

---

### 5) The compile step is the real trick

The wiki compile step emits stable artifacts under:

- `.openclaw-wiki/cache/agent-digest.json`
- `.openclaw-wiki/cache/claims.jsonl`

This is excellent design.

Why:

- agents/runtime can consume structured digests directly
- they do not need to scrape markdown pages
- prompt supplements can stay compact and high-signal
- dashboards can be regenerated deterministically

The prompt supplement code in `extensions/memory-wiki/src/prompt-section.ts` is revealing.

It can append a **Compiled Wiki Snapshot** with only top pages / top claims / contradiction counts / question counts.

That means the wiki can influence prompt context **without dumping the whole vault into the model**.

That’s one of the strongest design patterns here:

> keep the human-readable layer rich, but generate a smaller machine-facing digest for the model.

We should copy that pattern aggressively.

---

### 6) Bridge mode is a surprisingly mature design choice

The wiki supports three modes:

- `isolated`
- `bridge`
- `unsafe-local`

The interesting one is **bridge**.

Bridge mode reads public memory artifacts and memory events from the active memory plugin **through public SDK seams**.

That phrase matters.

It means:

- the wiki doesn’t reach into private internals
- memory plugins can remain replaceable
- the wiki can compile from exported artifacts without becoming tightly coupled to one backend implementation

This is exactly how plugin ecosystems should be built.

There is also an `unsafe-local` mode for same-machine private path access, but it is explicitly labeled experimental and trust-boundary-breaking.

That honesty is good. They know where the abstraction ends.

---

### 7) Skills are lightweight prompt modules, not giant agent personas

OpenClaw’s skill framework is also strong.

A skill is just a directory with `SKILL.md` frontmatter + instructions, AgentSkills-compatible.

Important behavior:

- the base system prompt includes a compact `<available_skills>` list
- each skill entry includes `name`, `description`, and `location`
- the model is instructed to read the specific `SKILL.md` only if the skill applies
- only one clearly relevant skill should be read up front
- skills are filtered by environment/config/binary presence before prompt injection

This is elegant for three reasons:

1. **Small prompt footprint**
2. **Skills are inspectable files, not hidden magic**
3. **Tool-specific procedure can live outside the base system prompt**

This is one of the best answers I’ve seen to “how do you keep an agent capable without making the prompt enormous?”

---

### 8) Skills have real gating, not just conventions

The skill framework supports gating via frontmatter metadata, for example:

- OS restrictions
- required binaries on `PATH`
- required env vars
- required config keys
- install metadata for UI/onboarding

It also supports multiple skill locations with precedence:

- workspace skills
- project agent skills
- personal agent skills
- managed/shared skills
- bundled skills
- extra dirs

This gives a clean override model.

Why it matters:

- you can safely ship bundled defaults
- users can locally override without patching upstream
- skills can be context-sensitive instead of always present
- the model only sees skills that are actually usable

That last point is underrated. A lot of agent systems leak unusable capabilities into prompt context and then wonder why the model hallucinates workflows.

---

### 9) Memory and wiki are joined through supplements, not a hard merge

I found this especially interesting in the code.

OpenClaw has a memory plugin state layer with registrations for:

- `registerMemoryCapability(...)`
- `registerMemoryCorpusSupplement(...)`
- `registerMemoryPromptSupplement(...)`

So the main memory plugin can own the primary runtime, while another plugin like `memory-wiki` can add:

- extra searchable corpus results
- extra prompt guidance

without taking over the whole memory subsystem.

That is a clean extensibility seam.

Conceptually:

- one plugin owns the memory engine
- others can enrich memory-related retrieval/prompt behavior
- the runtime can still present a unified experience

This is much better than a monolith.

---

### 10) They understand that editing generated knowledge needs guardrails

The wiki tooling is not just search/get.

It includes:

- `wiki_status`
- `wiki_search`
- `wiki_get`
- `wiki_apply`
- `wiki_lint`

The important one is `wiki_apply`.

Instead of telling the model to freely rewrite generated markdown, they give it a **narrow mutation surface** for:

- synthesis updates
- metadata changes
- question/contradiction updates
- confidence/status updates
- structured claims

That is exactly the right instinct.

Freeform model editing of generated knowledge bases is how drift and formatting corruption happen.

`wiki_lint` is also strong: it treats contradiction/provenance/open-question health as first-class maintenance, not afterthoughts.

---

## Specific source-backed takeaways

### System prompt design

OpenClaw’s prompt architecture makes a few important moves:

- bootstrap files are injected automatically
- daily memory is **not** automatically injected
- skills are only listed compactly and read on demand
- subagents use a more minimal prompt mode

That means they’re actively managing context bloat instead of ignoring it.

### Memory path handling

In `src/memory-host-sdk/host/internal.ts`, memory file discovery is conservative:

- accepts `MEMORY.md`, `memory.md`, `DREAMS.md`, and `memory/`
- avoids symlinks
- dedupes by realpath
- supports extra paths

That’s boring in a good way. Boring is what you want in persistence and indexing code.

### Plugin registration shape

`extensions/memory-wiki/index.ts` shows the plugin wiring cleanly:

- register memory prompt supplement
- register memory corpus supplement
- register gateway methods
- register wiki tools
- register wiki CLI

This means wiki is not a doc-only concept; it is integrated all the way through runtime, tool surface, and CLI surface.

### Prompt supplement behavior

The wiki prompt-section code does two useful things:

1. adds workflow guidance about when to use `memory_search corpus=all` vs `wiki_search/wiki_get`
2. optionally appends a compact compiled digest

That’s subtle but important. It teaches the model **retrieval strategy**, not just tool existence.

---

## What we can learn from this

## A. Do not blur raw memory and compiled knowledge

This is probably the biggest lesson.

We should avoid treating these as one thing:

- chat logs
- daily scratch notes
- long-term curated memory
- source-backed knowledge pages
- machine-optimized retrieval summaries

They should be different layers with different maintenance rules.

If we merge them all into one bucket, we get noise, drift, and prompt obesity.

### Recommended adaptation

For our systems, I’d use something like:

- `memory/daily/` or dated notes for raw short-term context
- `MEMORY.md` or curated profile docs for durable preferences/rules
- `wiki/` or `knowledge/` for maintained concepts/entities/projects
- generated `cache/*.json` digests for machine-facing recall

---

## B. Use markdown as source of truth, but compile for the machine

This is the second big lesson.

Human-editable markdown is great for:

- trust
- portability
- git diffability
- repairability
- easy inspection

But markdown is a mediocre machine interface.

So the answer is not “abandon markdown.”
The answer is:

- keep markdown for human-authoritative content
- compile structured artifacts for runtime consumption

This is likely the single most reusable pattern from OpenClaw.

---

## C. Retrieval should combine semantic and exact matching

OpenClaw’s hybrid retrieval is the right default.

If we build similar systems, do not choose between:

- embeddings
n- keyword search

Use both.

Exact string retrieval matters for:

- issue numbers
- config fields
- class names
- commit hashes
- URLs
- error strings

Semantic retrieval matters for paraphrase and latent concept matching.

You want both.

---

## D. Skills should be modular, lazy, and file-backed

OpenClaw’s skill system is better than a giant omniprompt.

What we should emulate:

- keep the always-on prompt small
- expose a compact available-skills index
- let the model load the relevant procedure file only when needed
- gate skills by actual environment capability

That gives you procedural specialization without turning the core prompt into sludge.

---

## E. Use narrow mutation tools for structured knowledge

If a model is going to maintain a knowledge layer, do not rely only on arbitrary text editing.

Provide operations like:

- add/update synthesis
- attach evidence
- raise question
- mark contradiction
- set confidence/freshness
- lint health

This is a lot safer and produces less entropy than “edit the page however you want.”

OpenClaw is very right about this.

---

## F. Plugin seams matter more than plugin counts

The elegant thing is not “many plugins.”
The elegant thing is the seam:

- primary capability owner
- supplements from neighbors
- public artifact bridge
- runtime tools + CLI + prompt integration all aligned

That is a healthy architecture.

We can learn from that when designing our own extension points.

---

## What I would steal almost directly

### 1. The memory/wiki split

I would absolutely steal the conceptual split between:

- memory engine
- wiki compiler / knowledge layer

That’s the cleanest part of the whole design.

### 2. Compiled digests

I would also steal the idea of a generated small digest for prompt use.

For example:

- `agent-digest.json`
- `claims.jsonl`
- maybe `hot-questions.json`
- maybe `stale-entities.json`

These are excellent machine interfaces.

### 3. Corpus supplements

The “non-exclusive memory corpus supplement” pattern is lovely.

It lets multiple systems participate in recall without pretending they are one database.

### 4. Skill lazy loading

Also worth stealing almost unchanged.

### 5. Contradiction / freshness / open-question dashboards

This is more ambitious, but it’s exactly the kind of thing that makes long-lived systems less stupid over time.

---

## What I would be careful about

### 1. Wiki complexity could outrun actual usage

The wiki layer is strong, but it can also become elaborate enough that maintenance overhead starts dominating value.

Structured claims, dashboards, backlinks, bridge imports, Obsidian integration, digests, linting — all good, but only if people actually maintain them.

So if we borrow it, we should start thinner:

- pages
- claims/evidence
- compiled digest
- lint

Then add dashboards and deeper workflows only if they pay for themselves.

### 2. Prompt supplements must stay genuinely compact

The compiled wiki snapshot is a good idea, but only if it remains small.

If the digest prompt grows into mini-document dumps, we lose the benefit.

So “top pages / top claims / key contradictions” is the correct discipline.

### 3. Bridge mode is only as good as the public artifacts

Bridge mode is elegant, but if exported artifacts are thin or stale, the wiki will inherit that weakness.

So the real dependency is not the bridge itself — it is the quality and stability of the public memory artifacts.

### 4. Tool routing needs the model to actually understand strategy

OpenClaw helps by injecting guidance about when to use:

- `memory_search corpus=all`
- `wiki_search`
- `wiki_get`

That strategy guidance is crucial. Without it, the model might use the wrong retrieval path.

Any system copying this should preserve that teaching layer.

---

## Concrete ideas for free-range-builders / our own stack

## Near-term

1. **Adopt the memory layer split explicitly**
   - raw notes
   - curated memory
   - compiled knowledge

2. **Create a small “knowledge compile” pass**
   - markdown in
   - compact JSON digest out

3. **Design claims/evidence minimally**
   - `id`
   - `claim`
   - `confidence`
   - `evidence`
   - `updated_at`
   - `status`

4. **Add a lint/health pass**
   - missing evidence
   - stale claims
   - duplicate entities
   - contradictions/open questions

5. **Use lazy procedure docs instead of fat prompts**
   - exactly what OpenClaw does with skills

## Medium-term

6. **Build corpus supplements / federated recall**
   - let project knowledge, daily logs, and structured wiki all participate in search without flattening them into one thing

7. **Build machine-facing digests for context engines**
   - not full markdown scrape
   - small selective summaries

8. **Prefer narrow structured update tools over raw freeform edits**
   - especially for generated or semi-generated knowledge pages

---

## My overall judgment

This part of OpenClaw is genuinely well thought through.

Not perfect, not trivial, but unusually sane.

The strongest underlying philosophy is:

- keep memory visible
- keep retrieval layered
- keep prompts small
- keep structured knowledge distinct from logs
- let plugins cooperate through narrow public seams

That’s the right direction.

If we learn one sentence from it, I’d phrase it like this:

> Treat memory as an editable filesystem, retrieval as a search/runtime layer, and knowledge as a compiled, provenance-aware product built on top — not as one undifferentiated blob.

That idea is worth carrying forward.

---

## Pointers into the repo

Files most worth rereading:

- `docs/concepts/memory.md`
- `docs/concepts/memory-search.md`
- `docs/concepts/memory-builtin.md`
- `docs/plugins/memory-wiki.md`
- `docs/cli/wiki.md`
- `docs/tools/skills.md`
- `docs/tools/creating-skills.md`
- `docs/concepts/system-prompt.md`
- `src/plugins/memory-state.ts`
- `src/memory-host-sdk/host/internal.ts`
- `extensions/memory-core/index.ts`
- `extensions/memory-wiki/index.ts`
- `extensions/memory-wiki/src/prompt-section.ts`
- `extensions/memory-wiki/skills/wiki-maintainer/SKILL.md`

## Practical takeaway in one page

If I were implementing a memory system tomorrow, I would do this:

1. Store durable memory in markdown + dated notes.
2. Build hybrid search over chunked notes.
3. Keep daily logs out of the default prompt.
4. Add a compiled wiki layer only for durable synthesized knowledge.
5. Emit JSON digests for machine consumption.
6. Provide structured update/lint tools for the knowledge layer.
7. Use small lazy-loaded skill docs for procedures.

That’s the OpenClaw pattern I think is most worth stealing.
