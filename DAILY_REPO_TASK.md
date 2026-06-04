# Daily Builder Scout Task

## Mission

Every day, run **two** builder scouts:

1. **GitHub scout:** find one interesting, very popular, hot/trending GitHub repository of the day and study it deeply enough to teach Tracy what they built, how they built it, how it works, what the major parts/components/knobs are, and what a serious builder should actually learn from it.
2. **Hugging Face scout:** find one interesting, hot/trending, useful, or unusually revealing Hugging Face artifact of the day and study it in the same builder-teardown style. The source is different, but the standard is the same: inspect the actual model/dataset/Space/repo files, configs, card, examples, artifacts, and implementation surface when available.

These should not be shallow trending-post summaries.
They should become a durable **builder's notebook** / **daily source teardown**.

The picks should ideally be:
- AI-related when possible
- very popular / hot / trending right now
- genuinely interesting
- fun
- beautifully implemented
- well engineered enough to reward close study

The GitHub pick does **not** have to be the single most popular repo if a slightly less viral repo is clearly better engineered or more worth learning from.

The Hugging Face pick can be a model, dataset, Space, collection, demo repo, or other Hugging Face-hosted artifact. Prefer things with enough inspectable structure to reward a teardown. Skip pure leaderboard noise unless there is a real mechanism, workflow, or product lesson inside.

---

## Selection rule

Balance:
- **popularity / heat / trendiness**
- **engineering quality**
- **beauty / fun / delight**
- **practical relevance**

Do **not** choose:
- empty hype wrappers
- low-substance prompt packs
- repos whose entire value is marketing
- obviously shallow glue projects unless there is a truly interesting implementation angle

If the top trending repo is boring or fake-interesting, skip it and choose a better candidate.

If nothing AI-related is worthy on GitHub that day, choose the best engineering-heavy repo anyway.

If Hugging Face's top item is mostly hype, skip it and choose a model/dataset/Space with better inspectable substance.

---

## Output cadence

- **Two scouts per day**
  - one GitHub note
  - one Hugging Face note
- **Medium-to-deep notes**, with flexibility depending on the project or artifact
  - some picks deserve concise coverage
  - some deserve a fuller teardown

Aim for:
- enough depth to be useful later
- not so much rambling that the note becomes sludge

---

## Deliverables

For each daily run:

1. create a note in:
   - `notes/YYYY-MM-DD_<github-repo-slug>.md` for the GitHub scout
   - `notes/YYYY-MM-DD_hf_<hugging-face-slug>.md` for the Hugging Face scout
2. run `python3 scripts/verify_daily.py --date YYYY-MM-DD` before committing
3. commit and push both notes to this repo in one daily commit, unless only one note changed during an idempotent repair
4. send Tracy a short Slack summary with:
   - GitHub pick
   - Hugging Face pick
   - one key insight from each
   - commit hash

---

## Required note structure

Every note should feel like a **source dissection**, not a loose essay.

Use this GitHub structure by default unless the project strongly demands a variation:

```md
# <Repo Name>

- Repo: <owner/repo>
- URL: <url>
- Date: <YYYY-MM-DD>
- Repo snapshot studied: <branch/commit>
- Why picked today: <1-3 lines>

## Executive summary
## What they built
## Why it matters
## Repo shape at a glance
## Layered architecture dissection
### High-level system shape
### Main layers
### Request / data / control flow
## Key directories and files
## Important components
## Important knobs / configs / extension points
## Practical questions and answers
## What is smart
## What is flawed or weak
## What we can learn / steal
## How we could apply it
## Bottom line
```

For Hugging Face notes, adapt the metadata while keeping the same teardown spirit:

```md
# <Artifact Name>

- Source: Hugging Face
- Artifact: <model/dataset/space/collection>
- URL: <url>
- Date: <YYYY-MM-DD>
- Snapshot studied: <revision/commit/last-modified marker when available>
- Why picked today: <1-3 lines>

## Executive summary
## What they built / released
## Why it matters
## Artifact shape at a glance
## Layered architecture dissection
### High-level system shape
### Main layers
### Inference / data / control flow
## Key files, configs, cards, and artifacts
## Important components
## Important knobs / configs / extension points
## Practical questions and answers
## What is smart
## What is flawed or weak
## What we can learn / steal
## How we could apply it
## Bottom line
```

Notes on the structure:

- **Repo shape at a glance** should summarize the repository hierarchically: major top-level directories, packages, apps, services, libraries, docs, infra, tests, generated assets, and how they relate.
- **Artifact shape at a glance** should summarize the Hugging Face object structurally: card, configs, model files, tokenizer/preprocessor files, examples, dataset splits, Space app files, demos, evaluations, and linked source repos when available.
- **Layered architecture dissection** should explain the repo structurally at multiple levels: high-level system intent, major layers/subsystems, what each layer does, and how the layers connect.
- **Key directories and files** should identify the concrete source paths that matter most for understanding the system.
- **Important components** should call out specific modules/classes/services/scripts/files that are central to how the project works.

You can add sections if the project demands it, but do not skip the structural dissection.

---

## Study standard

Use the source-study framework.

Always ask:
- what is this project actually doing?
- what is the repository or Hugging Face artifact shape?
- what are the main layers and boundaries?
- what source files/components/configs/artifacts are carrying the real weight?
- what is creative?
- what is smart?
- what can we learn / steal?
- what is broken / weak / over-clever?

And also answer practical builder questions like:
- what assumptions does this system make?
- where would it fail in production?
- what is elegant here?
- what is likely brittle?
- what is mostly hype?
- what would I copy?
- what would I avoid?
- how could we apply the good parts to our own work?

The Q&A section must be meaningful, not filler.
The structural sections must be concrete, with links to the relevant GitHub or Hugging Face source paths.

---

## Grounding / writing rules

- do not stop at README summary alone
- do not stop at a Hugging Face model card, dataset card, or Space landing page alone
- inspect actual code structure when possible
- inspect actual Hugging Face files/configs/artifacts/examples when possible
- be skeptical of marketing claims
- prefer mechanism over vibes
- prefer architecture over slogans
- include concrete components, flows, and knobs
- dissect the repo or Hugging Face artifact hierarchically and structurally, not just conceptually
- identify the major layers, packages, directories, configs, artifacts, and key source files
- when you mention a file, directory, config, model card, dataset card, Space file, or artifact in the note, link it to the actual source URL for that path
- prefer direct source links to vague references like “the server code” or “the core package”
- point out flaws honestly
- note what is beautiful, fun, or delightfully engineered when it exists
- write like a builder talking to another builder, not a tech journalist farming SEO sludge

Tone:
- sharp
- concrete
- curious
- skeptical
- not cynical for its own sake
- not hypey

---

## Success criteria

A good daily note should make Tracy feel:
- "I understand what they made"
- "I understand how they built it"
- "I understand why it matters or doesn't"
- "I learned something reusable"
- "I know what to admire, steal, or distrust"

If the note does not achieve that, it is not good enough.

The daily run is not complete until `scripts/verify_daily.py` passes for the target date. If the cron is rerun and both notes already exist, run the verifier and finish with the existing commit state instead of creating duplicates.

---

## Schedule

- Run daily.

This file defines the standing workflow and grounding for that recurring task.
