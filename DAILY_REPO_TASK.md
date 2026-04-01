# Daily Repo of the Day Task

## Mission

Every day at **9:00 AM**, find **one** interesting, very popular, hot/trending GitHub repository of the day and study it deeply enough to teach Tracy what they built, how they built it, how it works, what the major parts/components/knobs are, and what a serious builder should actually learn from it.

This should not be a shallow trending-post summary.
It should become a durable **builder's notebook** / **daily repo teardown**.

The repo should ideally be:
- AI-related when possible
- very popular / hot / trending right now
- genuinely interesting
- fun
- beautifully implemented
- well engineered enough to reward close study

It does **not** have to be the single most popular repo if a slightly less viral repo is clearly better engineered or more worth learning from.

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

If nothing AI-related is worthy that day, choose the best engineering-heavy repo anyway.

---

## Output cadence

- **One repo per day**
- **Medium-to-deep note**, with flexibility depending on the project
  - some repos deserve concise coverage
  - some deserve a fuller teardown

Aim for:
- enough depth to be useful later
- not so much rambling that the note becomes sludge

---

## Deliverables

For each daily run:

1. create a note in:
   - `notes/YYYY-MM-DD_<repo-slug>.md`
2. commit and push it to this repo
3. send Tracy a short Slack summary with:
   - repo chosen
   - one key insight
   - commit hash

---

## Required note structure

```md
# <Repo Name>

- Repo: <owner/repo>
- URL: <url>
- Date: <YYYY-MM-DD>
- Why picked today: <1-3 lines>

## What they built
## Why it matters
## How it works
## Architecture / components
## Important knobs / configs / extension points
## Practical questions and answers
## What is smart
## What is flawed or weak
## What we can learn / steal
## How we could apply it
## Bottom line
```

You can add sections if the project demands it.

---

## Study standard

Use the source-study framework.

Always ask:
- what is this project actually doing?
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

---

## Grounding / writing rules

- do not stop at README summary alone
- inspect actual code structure when possible
- be skeptical of marketing claims
- prefer mechanism over vibes
- prefer architecture over slogans
- include concrete components, flows, and knobs
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

---

## Schedule

- Run daily at **9:00 AM**

This file defines the standing workflow and grounding for that recurring task.
