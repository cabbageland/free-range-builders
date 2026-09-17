# AACR-Bench

- Source: Hugging Face
- Artifact: dataset
- URL: https://huggingface.co/datasets/Alibaba-Aone/aacr-bench
- Date: 2026-09-17
- Snapshot studied: Hugging Face dataset revision `47be1d6df1e7faf222cf531587772d92f79fe6b2`, last modified `2026-02-02T06:59:14.000Z`; linked source repo studied at `68a569759289a83654a59d06db2a72910edf0a4a`
- Why picked today: This is the evaluation substrate behind Alibaba's OpenCodeReview claims, and it is more useful than another generic model card because it exposes what "AI code review quality" is actually being measured against.

## Executive summary

[Alibaba-Aone/aacr-bench](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench) is a compact Hugging Face dataset for automated code-review evaluation. The hosted artifact has four files: [.gitattributes](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/.gitattributes), [README.md](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/README.md), [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json), and [readme_cn.md](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/readme_cn.md).

The dataset contains 2,145 review comments: 1,505 labeled correct and 640 labeled incorrect. It is not a full repository archive; it is a comment-level judgment set with PR URLs, source/target commits, line anchors, issue category, required context level, source model, and correctness label. The linked source project, [alibaba/aacr-bench](https://github.com/alibaba/aacr-bench), adds the broader evaluation framework under [evaluation/](https://github.com/alibaba/aacr-bench/tree/68a569759289a83654a59d06db2a72910edf0a4a/evaluation).

## What they built / released

On Hugging Face, they released a JSON dataset intended to test whether automated review systems can tell good review comments from low-quality ones. [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json) is a single JSON array of comment records. Each record includes fields such as `project_main_language`, `pr_url`, `pr_source_commit`, `pr_target_commit`, `pr_change_line_count`, `is_ai_comment`, `note`, `path`, `side`, `source_model`, `from_line`, `to_line`, `category`, `context`, and `label`.

The linked GitHub project [alibaba/aacr-bench](https://github.com/alibaba/aacr-bench) turns that raw benchmark idea into a runnable evaluation system. Its [evaluation/README.md](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/README.md) describes a pipeline for data loading, review execution, and evaluation across OCR, Claude Code, and Codex reviewers.

## Why it matters

Code-review agents are easy to demo and hard to evaluate. A bad review comment can look plausible, a good comment can require repository-level context, and line accuracy matters. This dataset makes the measurement problem visible.

The most useful part is the explicit context labeling. The inspected data distribution had 1,017 `Diff Level`, 744 `File Level`, and 384 `Repo Level` comments. That means the benchmark is not only asking "did the model find a bug?" It is also asking whether a review system can handle comments whose evidence lives outside the immediate hunk.

## Artifact shape at a glance

- [README.md](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/README.md) is the dataset card with schema, count, label meaning, and citation.
- [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json) is the actual 2.1 MB payload.
- [readme_cn.md](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/readme_cn.md) is the Chinese-language card.
- [.gitattributes](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/.gitattributes) is the standard repository metadata file.
- The linked source repo stores split raw data in [dataset/positive_samples.json](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/dataset/positive_samples.json) and [dataset/negative_samples.json](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/dataset/negative_samples.json).
- The linked source repo's evaluation engine lives in [evaluation/](https://github.com/alibaba/aacr-bench/tree/68a569759289a83654a59d06db2a72910edf0a4a/evaluation).

## Layered architecture dissection

### High-level system shape

The Hugging Face artifact is the distribution layer: it packages a normalized dataset for public download and citation. The source repo is the operational layer: it contains raw split files, conversion, cloning, reviewer execution, judging, metrics, and result directories.

That split is sensible. [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json) is easy to consume from Hugging Face, while [evaluation/pipeline.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/pipeline.py) is a heavier runnable harness with local repository checkouts and reviewer integrations.

### Main layers

The data-card layer is [README.md](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/README.md). It defines the field names and says labels are `1` for correct and `0` for incorrect.

The payload layer is [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json). The inspected payload has 1,505 positive labels and 640 negative labels; language counts are led by C++ with 508 comments, TypeScript with 422, Java with 272, Go with 245, C with 206, Python with 151, JavaScript with 141, Rust with 92, PHP with 56, and C# with 52.

The source-repo data layer is [dataset/](https://github.com/alibaba/aacr-bench/tree/68a569759289a83654a59d06db2a72910edf0a4a/dataset), which keeps positive and negative samples separate before conversion.

The standardization layer is [evaluation/schema.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/schema.py) and [evaluation/converters/aacr_bench.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/converters/aacr_bench.py). This maps benchmark-specific records into `ReviewInstance` rows with `repo`, `base_commit`, `head_commit`, and `reference_comments`.

The execution layer is [evaluation/pipeline.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/pipeline.py), which groups samples by repository to avoid checkout conflicts and dispatches reviewer backends from [evaluation/reviewers/](https://github.com/alibaba/aacr-bench/tree/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/reviewers).

### Inference / data / control flow

The full flow starts with raw benchmark data or the Hugging Face [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json). [evaluation/converters/aacr_bench.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/converters/aacr_bench.py) parses PR URLs into `owner/name`, derives an `instance_id`, maps commit fields, and converts comments into schema-level references. [evaluation/schema.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/schema.py) validates each JSONL line.

Then [evaluation/pipeline.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/pipeline.py) loads instances, groups them by repo, checks out the right base/head commits through [evaluation/repo_utils.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/repo_utils.py), runs a reviewer from [evaluation/reviewers/ocr.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/reviewers/ocr.py), [evaluation/reviewers/claude.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/reviewers/claude.py), or [evaluation/reviewers/codex.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/reviewers/codex.py), and sends outputs to [evaluation/evaluate.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/evaluate.py) and [evaluation/judge.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/judge.py).

## Key files, configs, cards, and artifacts

- [Hugging Face README.md](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/README.md): card, schema, label meaning, citation.
- [Hugging Face dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json): actual hosted records.
- [GitHub dataset/positive_samples.json](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/dataset/positive_samples.json): positive raw examples in the linked source project.
- [GitHub dataset/negative_samples.json](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/dataset/negative_samples.json): negative raw examples in the linked source project.
- [evaluation/schema.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/schema.py): standard format and validation rules.
- [evaluation/converters/aacr_bench.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/converters/aacr_bench.py): conversion from AACR records to standard JSONL.
- [evaluation/pipeline.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/pipeline.py): review/eval orchestration.
- [evaluation/README.md](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/README.md): runnable usage and directory conventions.
- [docs/metrics.md](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/docs/metrics.md): metric definitions.

## Important components

The hosted `label` field in [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json) is the key target: `1` means the comment is correct, `0` means it is incorrect. This makes the artifact useful for reflection/filtering tasks, not just generation.

The `context` field in [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json) is the most interesting diagnostic field. It distinguishes diff-level, file-level, and repo-level comments, which is exactly where many review agents over-claim.

[evaluation/schema.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/schema.py) is important because it refuses invalid lines, duplicate IDs, bad line numbers, empty paths, and malformed comments early. Benchmarks rot quickly without that kind of gate.

[evaluation/pipeline.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/pipeline.py) has a practical concurrency choice: it groups work by repo so samples sharing the same checkout run serially, while different repos can run concurrently. That is boring and correct.

## Important knobs / configs / extension points

The obvious knobs are in [evaluation/README.md](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/README.md): reviewer choice (`ocr`, `claude`, `codex`), `--stage`, `--limit`, `--line-k`, `--timeout-minutes`, `--eval-rounds`, `--concurrency`, `--preview`, and reviewer-specific knobs such as `--ocr-command` and `--max-tools`.

The converter extension point is [evaluation/converters/](https://github.com/alibaba/aacr-bench/tree/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/converters). The project wants new benchmarks to map into the schema in [evaluation/schema.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/schema.py), then reuse the same pipeline.

The reviewer extension point is [evaluation/reviewers/](https://github.com/alibaba/aacr-bench/tree/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/reviewers). This is where a new review engine would need an adapter that produces comparable finding output.

## Practical questions and answers

Q: Is this a model, a dataset, or an evaluation harness?

A: The Hugging Face artifact is a dataset. The linked [alibaba/aacr-bench](https://github.com/alibaba/aacr-bench) repo is the evaluation harness. Treat them as a pair: [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json) gives the material; [evaluation/pipeline.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/pipeline.py) gives the workflow.

Q: What can be tested with this?

A: Comment filtering, review-comment validation, line anchoring, issue categorization, and context-sensitive review ability. The dataset is especially relevant for judging whether a generated comment should survive a second-pass filter.

Q: What should not be overclaimed?

A: This does not automatically prove a review agent will perform well on your repository. The dataset is broad enough to be useful, but it is still a benchmark slice: 50 projects, 200 PRs, 10 languages, and 2,145 comments according to [README.md](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/README.md).

## What is smart

The smartest part is that the dataset includes negative comments, not just accepted findings. Review quality depends as much on suppressing plausible junk as discovering issues. The 640 negative labels in [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json) make it useful for reflection, calibration, and review filtering.

The second smart part is recording the source model. The inspected payload included comments from GPT-5.2, Claude-Code/Claude-4.5-Sonnet, Qwen-Coder-480B, GLM-4.7, Deepseek-V3.2, Gemini-3-Pro, and empty-source human comments. That lets evaluators reason about model-specific failure modes instead of flattening everything into one pile.

The third smart part is the standard schema in [evaluation/schema.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/schema.py). It translates benchmark records into repo/commit/comment instances, which is the right abstraction for evaluating actual review systems.

## What is flawed or weak

The Hugging Face artifact itself is thin. [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json) has rich fields, but the hosted repo does not include the runnable evaluation code; users must follow the linked GitHub project.

The public card's schema description in [README.md](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/README.md) is concise, but not enough to explain every judgment boundary. For example, a `label: 0` comment can be wrong for different reasons: false premise, bad location, missing context, duplicate issue, or non-actionable framing.

The benchmark is also naturally vulnerable to project freshness. It references GitHub PRs and commits; the evaluation harness in [evaluation/repo_utils.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/repo_utils.py) can clone and checkout commits, but availability and dependency setup remain real-world sources of friction.

## What we can learn / steal

Steal the context-level label. For our own review-agent evals, separate diff-level, file-level, and repo-level findings. Otherwise a model can look good by solving only the easy hunk-local cases.

Steal the positive/negative mix. A useful review benchmark should measure precision pressure, not just recall. The negative samples in [dataset/negative_samples.json](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/dataset/negative_samples.json) are as valuable as the positive samples in [dataset/positive_samples.json](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/dataset/positive_samples.json).

Steal the repo-grouped concurrency idea from [evaluation/pipeline.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/pipeline.py). Any benchmark that checks out mutable worktrees needs to serialize per repo or it will corrupt its own runs.

## How we could apply it

For a practical internal review benchmark, we could mirror the [evaluation/schema.py](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/schema.py) shape: one JSONL row per review instance, with repo, base commit, head commit, and reference comments. Then add internal fields for severity, confidence, and whether the comment was accepted by maintainers.

For review-agent product work, use the Hugging Face [dataset.json](https://huggingface.co/datasets/Alibaba-Aone/aacr-bench/blob/47be1d6df1e7faf222cf531587772d92f79fe6b2/dataset.json) to test a second-pass "should this comment be shown?" model. That is lower risk than using it only to score first-pass generation.

For evaluation operations, copy the separation in [evaluation/README.md](https://github.com/alibaba/aacr-bench/blob/68a569759289a83654a59d06db2a72910edf0a4a/evaluation/README.md): conversion, review execution, evaluation, results, and metrics all have their own directories. It makes reruns and comparisons much less messy.

## Bottom line

AACR-Bench is useful because it makes AI code-review evaluation concrete: real PR links, commit pairs, anchored comments, context labels, source-model labels, and positive/negative judgment. The Hugging Face artifact is small, but the measurement idea is exactly the kind of discipline AI review products need.
