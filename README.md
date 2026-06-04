# Free Range Builders

A daily builder's notebook.

This repo is for daily **builder teardowns**: one interesting hot/trending GitHub project and one interesting Hugging Face artifact per day, studied with a builder's eye.

The goal is not shallow link sharing.
The goal is to answer:
- what did they build?
- how does it work?
- what are the parts and knobs?
- what is smart?
- what is weak?
- what can we learn, steal, adapt, or distrust?

## Format

Daily notes live in:
- `notes/YYYY-MM-DD_<github-repo-slug>.md`
- `notes/YYYY-MM-DD_hf_<hugging-face-slug>.md`

Each note aims to be:
- concrete
- skeptical
- architecture-aware
- practical
- medium-to-deep depending on the project

## Selection taste

We prefer GitHub repos and Hugging Face artifacts that are:
- hot / trending / very popular
- AI-related when possible
- genuinely interesting
- fun
- beautifully implemented
- worth studying, not just hyped

Popularity matters, but engineering quality and reusable lessons matter too.

## Standing task

See:
- `DAILY_REPO_TASK.md`

That file defines the recurring workflow and grounding for the daily builder scout task.

For each target date, `python3 scripts/verify_daily.py --date YYYY-MM-DD` checks that the expected GitHub and Hugging Face notes exist and have the required teardown shape.

Current study-note bias:
- make the notes feel like a **source dissection**
- describe the project, model, dataset, or Space hierarchically and structurally
- explain high-level layers, subsystem boundaries, configs, artifacts, and what each layer does
- identify the concrete source files/directories/model-card/config/artifacts that matter most
- whenever a file, directory, config, model card, dataset card, or artifact is mentioned in the note, link it to the actual source path
