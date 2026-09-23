# Laya

- Source: Hugging Face
- Artifact: model family, convaiinnovations/laya
- URL: https://huggingface.co/convaiinnovations/laya
- Date: 2026-09-23
- Snapshot studied: 5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b, lastModified 2026-09-23T08:09:01Z
- Why picked today: It was the first model listed on the Hugging Face trending models page when scouted, with 2.9k+ likes and a fresh 2026-09-23 update. It is also unusually inspectable for a decision model because the card ships configs, inference code, shared model code, tokenizer files, evaluation tables, and three checkpoints.

## Executive summary

[convaiinnovations/laya](https://huggingface.co/convaiinnovations/laya/tree/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b) is an open, non-autoregressive decision model family. Instead of generating text, it takes a state plus typed questions and returns structured answers: `choice`, `score`, or `noul` probabilities. The root checkpoint uses ModernBERT-large; the bundled [multilingual](https://huggingface.co/convaiinnovations/laya/tree/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/multilingual) checkpoint uses mmBERT-base; the bundled [typed-decisions](https://huggingface.co/convaiinnovations/laya/tree/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/typed-decisions) checkpoint specializes the same pattern for a typed decision benchmark.

The release is interesting because the mechanism is visible. [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_api.py) loads the tokenizer, encoder config, decision head, and safetensors weights. [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py) shows how questions are rendered, where option markers go, how scores are computed, and how calibration buckets work.

The strongest idea is "structured decision as one forward pass." The weakest part is that the card itself admits real limits: high-cardinality labels suffer from option-token budget pressure, zero-shot typed decisions are weak, and the action/escalate head is not useful yet.

## What they built / released

They released a three-checkpoint model family plus the lightweight inference machinery needed to run it locally. The Hugging Face artifact includes:

- [README.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/README.md), the model card and benchmark report.
- [model.safetensors](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/model.safetensors), the root English checkpoint weights.
- [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/encoder/config.json), the ModernBERT-large encoder config.
- [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_config.json), the decision-head and calibration config.
- [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_api.py), the Jev-shaped local inference wrapper.
- [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py), the shared rendering, model, reward, batching, and metric code.
- [email_utils.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/email_utils.py), a small domain helper for email triage states and questions.
- [eval/results.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/eval/results.md) and [eval/results.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/eval/results.json), the local evaluation outputs.

## Why it matters

Lots of agent systems use LLMs for tiny classification and routing calls, then parse prose back into JSON. Laya is a counterproposal: make the output schema the model's native action space. That can be faster, cheaper, and easier to calibrate if the task fits.

This matters especially for guardrails, ticket routing, moderation, email triage, and workflow branching. Those jobs often need probabilities and bounded labels more than eloquent text.

## Artifact shape at a glance

The root artifact is the English checkpoint. [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_config.json) says it uses `answerdotai/ModernBERT-large`, two decision-head layers, `max_len` 512, `head_max_len` 192, bf16 AMP, and per-question-type temperature settings.

The [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/encoder/config.json) reveals a 28-layer ModernBERT config with 1024 hidden size, 16 heads, alternating full/sliding attention layers, and 8192 max positions, even though the root decision config caps runtime context lower.

The [multilingual](https://huggingface.co/convaiinnovations/laya/tree/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/multilingual) subfolder carries its own [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/multilingual/rl_agent_config.json), [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/multilingual/encoder/config.json), tokenizer, and safetensors. It switches to `jhu-clsp/mmBERT-base`, `max_len` 1024, and `head_max_len` 256.

The [typed-decisions](https://huggingface.co/convaiinnovations/laya/tree/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/typed-decisions) subfolder mirrors that shape with a fine-tuned ModernBERT checkpoint and [typed-decisions/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/typed-decisions/rl_agent_config.json).

## Layered architecture dissection

### High-level system shape

Laya has three layers. The outer layer is a Jev-compatible API shape: state plus named questions, each with instructions, type, and criteria. The middle layer renders each question into a masked sequence. The inner layer is a bidirectional encoder plus a small transformer decision head that scores option marker positions.

The important difference from an LLM is that output length is zero. [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_api.py) returns answers and probabilities directly after softmax over markers. There is no text decoder and no JSON parser.

### Main layers

The request-normalization layer is `RLAgent._to_internal` in [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_api.py). It maps external `choice`, `score`, and `noul` question definitions into compact internal fields.

The rendering layer is [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py). `render_options` turns criteria into option strings, and `build_sequence` creates `[CLS] <type> instructions [SEP] [MASK] option ... [SEP] state [SEP]`. Each option gets its own mask marker, so the model scores labels at request time.

The model layer is `DecisionModel` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py). It wraps a pretrained encoder, adds a question-type embedding, optionally applies two transformer layers, gathers hidden states at marker positions, and scores each marker with a small MLP.

The calibration layer is split between [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_config.json) and `temp_bucket` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py). Temperatures vary by question type and option count, which is a practical concession to the fact that two-label yes/no decisions and many-way choices calibrate differently.

### Inference / data / control flow

`RLAgent.__init__` in [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_api.py) loads [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_config.json), the tokenizer from [tokenizer/tokenizer_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/tokenizer/tokenizer_config.json), the encoder architecture from [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/encoder/config.json), and weights from [model.safetensors](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/model.safetensors).

`system_one` then loops through the requested questions, builds a sequence per question with `build_sequence`, batches them with `collate_items`, runs one encoder/head forward pass, and converts logits to calibrated probabilities. `choice` returns an argmax label plus probability map; `score` returns expected ordinal value; `noul` returns `p[1]`.

The email helper in [email_utils.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/email_utils.py) shows how this is meant to be used in a real app: normalize messy email text before asking a fan-out of typed routing, spam, phishing, urgency, reply, and sentiment questions.

## Key files, configs, cards, and artifacts

- [README.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/README.md): model card, quickstart, router story, architecture, training description, benchmarks, limits, and links.
- [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_api.py): local inference API and response formatting.
- [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py): sequence construction, decision model, proper-scoring reward, calibration helpers, batching, and metrics.
- [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_config.json): root model max lengths, head size, training metadata, and temperatures.
- [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/encoder/config.json): ModernBERT architecture config.
- [tokenizer/tokenizer_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/tokenizer/tokenizer_config.json): tokenizer class and special tokens.
- [multilingual/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/multilingual/rl_agent_config.json): multilingual checkpoint dimensions and training metadata.
- [typed-decisions/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/typed-decisions/rl_agent_config.json): specialized checkpoint config and fine-tuning metadata.
- [email_utils.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/email_utils.py): a concrete preprocessor and default question set.
- [eval/results.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/eval/results.md): measured accuracy, ECE, NLL, and latency tables.

## Important components

`build_sequence` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py) is the core trick. It makes labels dynamic by placing one `[MASK]` marker before each rendered option, then gathers those marker states after encoding.

`DecisionModel` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py) is small and legible. It is not a hidden proprietary router. It is an encoder, type embedding, optional head transformer, marker scorer, and an act/escalate head.

`proper_reward` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py) encodes the RLCD claim: log score plus spherical score, with ranked probability score for ordinal questions. This is where "honest probabilities" becomes an implementation rather than a tagline.

`RLAgent.system_one` in [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_api.py) is the production wrapper. It also exposes a brittle but important failure mode: if markers do not fit in `head_max_len`, the question errors instead of silently truncating the answer space.

## Important knobs / configs / extension points

The length knobs in [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_config.json) matter most: `max_len`, `head_max_len`, and `max_prefixes`. These decide how much budget goes to the question/options versus the state.

The calibration knobs are `temperature` and `temperature_by_options` in [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_config.json). Builders should not treat those as universal truth; they need refitting on local distributions if probabilities drive business decisions.

The checkpoint choice is an operational knob. The [README.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/README.md) recommends a router that chooses English or multilingual, while [typed-decisions/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/typed-decisions/rl_agent_config.json) is a reminder that specialization can dominate the base checkpoint on a known workflow.

## Practical questions and answers

Q: Is this an LLM?
A: No. The root encoder in [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/encoder/config.json) is bidirectional ModernBERT, and [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_api.py) emits no generated tokens.

Q: How are arbitrary labels supported?
A: [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py) renders each option into the prompt and inserts a marker before it. The model scores those markers, so the answer set is defined at request time.

Q: What is the first production gotcha?
A: Label count. The card's [README.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/README.md) explicitly says high-cardinality choice questions can collapse because `head_max_len` is shared across all options.

Q: Can we trust the probabilities out of the box?
A: Not blindly. [eval/results.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/eval/results.md) reports good calibrated ECE in-task, but the [README.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/README.md) says raw calibration needed temperature fitting and advises local calibration.

Q: What would I test before adopting it?
A: My exact label schema, my languages, my maximum state length, and my high-cardinality cases. The model family is promising, but the artifact itself says performance depends heavily on task shape.

## What is smart

The option-marker design is clean. It avoids text generation and makes dynamic labels possible without retraining every time a workflow adds a category.

The release includes more than a card. [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_api.py), [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py), [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_config.json), and [eval/results.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/eval/results.md) make the mechanism auditable.

The card is unusually honest about limits. The [README.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/README.md) calls out zero-shot weakness, high-cardinality trouble, `noul` label bias, overconfidence, and an unusable action head. That is exactly the kind of disclosure builders need.

## What is flawed or weak

The root checkpoint is not a general zero-shot decision oracle. The [README.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/README.md) says base checkpoints are near chance on typed-decisions zero-shot and that the strong typed-decisions score belongs to a fine-tuned checkpoint.

The option budget is a real architectural limit. In [build_sequence](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py), options are squeezed into `head_max_len`; with many labels each option may get only a few tokens.

The shipped [email_utils.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/email_utils.py) is useful but also a clue: good results require domain-specific preprocessing. A raw messy document dumped into 512 tokens is not magic.

## What we can learn / steal

Steal the schema-native output idea. If a workflow needs routing, scoring, moderation, or escalation, a small bidirectional model with marker-scored options can be a better tool than a decoder LLM.

Steal the release shape. A useful model card should include configs, inference code, evaluation artifacts, and failure notes. This artifact's [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_common.py) is a compact reference implementation of the idea.

Steal the calibration posture. The per-type and per-cardinality temperature buckets in [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/rl_agent_config.json) are a reminder that probabilities are a product feature, not an afterthought.

## How we could apply it

For internal automation, use this pattern where today we ask an LLM to classify something and parse JSON. Convert the branch into a typed question, run a bounded scorer, store the probability distribution, and use confidence thresholds to decide when to escalate.

For customer-support triage, copy the structure from [email_utils.py](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/email_utils.py): clean noisy messages before classification, ask several small typed questions in one pass, and calibrate on our own tickets.

For evaluation, copy the skepticism from [README.md](https://huggingface.co/convaiinnovations/laya/blob/5e7b2b1b8ca2ecdd3f2322d94069c9b6ce7e844b/README.md). Test exact label counts, exact languages, exact state lengths, and exact probability thresholds before treating this as infrastructure.

## Bottom line

Laya is a strong builder artifact because it turns "agent decisions" into a concrete, inspectable modeling pattern: dynamic option markers, one encoder forward pass, calibrated probabilities, and no generated text. It is not magic, and it says so. The idea is most compelling where the workflow can be expressed as small typed questions with bounded labels.
