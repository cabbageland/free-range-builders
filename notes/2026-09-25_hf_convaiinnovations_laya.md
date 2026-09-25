# Laya

- Source: Hugging Face
- Artifact: model
- URL: https://huggingface.co/convaiinnovations/laya
- Date: 2026-09-25
- Snapshot studied: 55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851, last modified 2026-09-24T05:39:22Z
- Why picked today: It was near the top of the Hugging Face trending model page when scouted, with 3.5k+ likes and a fresh update. Unlike many trending cards, it exposes actual inference code, shared model code, calibration/eval files, encoder configs, tokenizer configs, and multiple checkpoint variants.

## Executive summary

[convaiinnovations/laya](https://huggingface.co/convaiinnovations/laya/tree/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851) is a typed decision model, not a text generator. The [README.md](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md) calls it a multilingual, non-autoregressive "System 1 decision model": give it a state plus typed questions and it returns typed answers with probabilities in one forward pass.

The source is inspectable enough to study mechanism. [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) builds sequences with option marker masks, defines the encoder-plus-decision-head model, and implements strictly proper scoring rewards. [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) loads the tokenizer, encoder config, safetensors weights, and returns `choice`, `score`, or `noul` answers with calibrated probabilities.

The key builder lesson is sharp: not every AI decision should be an LLM generation. Laya turns "ask the model a question and parse text" into "score a fixed answer space and return probabilities." That is a better shape for routing, triage, moderation, guardrails, and escalation gates.

## What they built / released

They released a Hugging Face model repo containing three related decision checkpoints:

- The root checkpoint in [model.safetensors](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/model.safetensors), configured by [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json), [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/encoder/config.json), and [tokenizer/tokenizer_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/tokenizer/tokenizer_config.json).
- A multilingual variant under [multilingual](https://huggingface.co/convaiinnovations/laya/tree/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual), with [multilingual/model.safetensors](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/model.safetensors), [multilingual/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/rl_agent_config.json), [multilingual/encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/encoder/config.json), and [multilingual/tokenizer/tokenizer_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/tokenizer/tokenizer_config.json).
- A typed-decisions variant under [typed-decisions](https://huggingface.co/convaiinnovations/laya/tree/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/typed-decisions), with [typed-decisions/model.safetensors](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/typed-decisions/model.safetensors), [typed-decisions/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/typed-decisions/rl_agent_config.json), and [typed-decisions/encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/typed-decisions/encoder/config.json).

The repo also includes code files: [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py), [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py), and [email_utils.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/email_utils.py). The [eval](https://huggingface.co/convaiinnovations/laya/tree/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval) folder contains benchmark images plus [eval/results.md](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.md) and [eval/results.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.json).

## Why it matters

Laya is interesting because it is a specialized decision engine. Many production workflows do not need prose. They need "which queue?", "how urgent?", "is this unsafe?", "does this need escalation?", or "which of these labels is most likely?" A text generator can answer those, but the output then needs parsing, validation, and calibration.

The implementation in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) avoids that by representing the answer space directly. A `choice` question becomes options. A `score` question becomes ordered levels. A `noul` question becomes `false` and `true`. The model scores option marker positions and emits probabilities.

The release also matters because it is frank about evaluation. [eval/results.md](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.md) reports overall in-task accuracy 0.753 with ECE 0.030, but zero-shot accuracy drops to 0.651 with ECE 0.204. That is useful evidence: the approach is promising, but calibration and transfer are not magic.

## Artifact shape at a glance

- [README.md](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md) is the model card, quickstart, routing story, long-document note, fine-tuning pointer, benchmark images, and checkpoint-family table.
- [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) is the Jev-compatible inference wrapper with `RLAgent.system_one`.
- [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) holds sequence rendering, model definition, reward functions, metrics, batching, and prediction utilities.
- [email_utils.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/email_utils.py) is a small domain utility for cleaning emails and creating default email-triage questions.
- [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json) declares the root checkpoint's encoder, max lengths, head layers, escalation cost, dtype, calibration temperatures, and training metadata.
- [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/encoder/config.json) declares a ModernBERT-large style encoder: hidden size 1024, 28 layers, 16 heads, local attention 128, mixed full/sliding layers, and 8192 max positions.
- [tokenizer/tokenizer_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/tokenizer/tokenizer_config.json) defines the fast tokenizer and special tokens `[CLS]`, `[MASK]`, `[PAD]`, and `[SEP]`.
- [eval/results.md](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.md) and [eval/results.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.json) provide calibration, accuracy, latency, and task-family metrics.
- [assets](https://huggingface.co/convaiinnovations/laya/tree/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/assets) and [eval](https://huggingface.co/convaiinnovations/laya/tree/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval) contain benchmark and comparison images, which are useful for presentation but less important than the configs and code.

## Layered architecture dissection

### High-level system shape

At the outer layer, Laya is a Hugging Face model repo with custom helper code. The API metadata reports `library_name: transformers` and `pipeline_tag: text-classification`, but the actual shipped inference path is not a normal text-classification label head. It is [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) loading [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json), [tokenizer](https://huggingface.co/convaiinnovations/laya/tree/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/tokenizer), [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/encoder/config.json), and [model.safetensors](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/model.safetensors).

Inside the model, [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) uses an encoder from Transformers, adds a question-type embedding, optionally runs a small Transformer decision head, gathers hidden states at option marker positions, scores each marker, and softmaxes across the option set.

The repo bundles variants instead of splitting each checkpoint into a separate repo only. The root is ModernBERT-large with [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json) at `max_len` 512. The multilingual variant in [multilingual/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/rl_agent_config.json) uses `jhu-clsp/mmBERT-base` with default `max_len` 1024, while [multilingual/encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/encoder/config.json) exposes 8192 maximum positions.

### Main layers

The input-rendering layer is `build_sequence` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py). It serializes a state, renders the typed question and options, creates a sequence shaped like `[CLS] <type> instructions [SEP] [MASK] option0 [MASK] option1 ... [SEP] state [SEP]`, and records the marker positions for answer options.

The encoder layer is configured in [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/encoder/config.json). It uses 28 layers, hidden size 1024, 16 heads, local attention 128, and alternating full/sliding attention. The multilingual [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/encoder/config.json) is smaller: hidden size 768, 22 layers, 12 heads, and vocab size 256000.

The decision-head layer is `DecisionModel` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py). It adds a type embedding, optionally runs Transformer encoder layers over hidden states, gathers marker hidden states, applies a scorer MLP, masks invalid marker positions, and builds an `act_head` from pooled state plus distribution summary features.

The calibration layer is in [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json). It stores per-question-type temperatures and cardinality-specific temperatures such as `choice:3-5`, `choice:6-10`, `choice:11+`, `score:3-5`, and `noul:2`.

The evaluation layer is [eval/results.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.json), which records question counts, per-task-family accuracy/ECE/NLL, calibration temperatures, latency, and an action policy summary.

### Inference / data / control flow

The caller passes `state` and `questions` into `RLAgent.system_one` in [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py). Each question is normalized into internal fields `t`, `ins`, and `crit`.

For each question, `build_sequence` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) constructs token IDs and marker positions. `collate_items` pads them into a batch. The model returns logits for markers plus `act` logits. [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) then applies temperatures, softmaxes probabilities, and formats answers.

For `choice`, [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) returns the winning choice, per-option probabilities, entropy-based confidence, and `act_probability`. For `score`, it returns an expected numeric score and a probability distribution over levels. For `noul`, it returns the probability of `true` as `noul`.

The email path in [email_utils.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/email_utils.py) shows the intended product use: strip quoted replies, signatures, and disclaimers, build an email state, then ask a bundle of typed questions such as category, spam, phishing, urgency, reply-needed, and sentiment.

## Key files, configs, cards, and artifacts

- [README.md](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md): model card, usage, checkpoint-family table, and links to docs/fine-tuning.
- [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py): runtime wrapper and answer formatter.
- [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py): core model, rendering, reward, metrics, batching, and prediction code.
- [email_utils.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/email_utils.py): small but concrete domain adapter for email triage.
- [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json): root checkpoint config and calibration temperatures.
- [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/encoder/config.json): ModernBERT encoder architecture.
- [tokenizer/tokenizer_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/tokenizer/tokenizer_config.json): special-token and model-length contract.
- [model.safetensors](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/model.safetensors): root weights.
- [multilingual/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/rl_agent_config.json): multilingual checkpoint config.
- [typed-decisions/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/typed-decisions/rl_agent_config.json): fine-tuned typed-decisions checkpoint config.
- [eval/results.md](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.md): readable evaluation summary.
- [eval/results.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.json): machine-readable metrics.

## Important components

`build_sequence` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) is the main trick. It turns state plus question plus options into one encoder sequence with explicit `[MASK]` markers for each possible answer.

`DecisionModel` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) is the model shell. The pretrained encoder reads the full sequence. The head scores only marker positions. That makes the output space typed and bounded.

`proper_reward` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) is the training philosophy in code. It combines log score and spherical score for all question types, plus ranked probability score for ordinal `score` questions. The comment says all three are strictly proper, so honest probabilities maximize reward.

`RLAgent.system_one` in [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) is the production shape: no generation, no parsing, no output tokens, just typed answers and probability tables.

The calibration tables in [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json) are not decorative. [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) divides logits by either per-cardinality temperatures or per-type temperatures before softmax.

## Important knobs / configs / extension points

The main task-shape knobs are in caller-supplied question definitions consumed by [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py): `type`, `instructions`, and `criteria`. That is where an app defines the answer space.

The model capacity and context knobs are in [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json): `encoder`, `head_layers`, `max_len`, `head_max_len`, `max_prefixes`, `act_costs`, `cost_wrong_act`, `amp_dtype`, and calibration temperatures.

The encoder architecture knobs are in [encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/encoder/config.json): hidden size, layer count, attention heads, local attention, full/sliding layer schedule, and RoPE parameters.

The multilingual extension point is [multilingual](https://huggingface.co/convaiinnovations/laya/tree/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual). Its [multilingual/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/rl_agent_config.json) switches the encoder to `jhu-clsp/mmBERT-base`, sets `max_len` 1024, and uses a smaller hidden size through [multilingual/encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/encoder/config.json).

The domain-adaptation extension point is demonstrated by [typed-decisions/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/typed-decisions/rl_agent_config.json), which marks `fine_tuned: true`, enables gradient checkpointing, and uses a 1024-token max length.

## Practical questions and answers

Q: Is this a generative LLM?
A: No. [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) wraps an encoder plus decision head, and [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) reports `output_tokens: 0`.

Q: What is the main mechanism?
A: Option marker scoring. `build_sequence` in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) puts `[MASK]` before each option, and `DecisionModel` scores those marker states.

Q: What makes it more production-shaped than "ask an LLM for JSON"?
A: Bounded typed output. [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) returns probabilities over a known option set, expected scores, and `noul` probabilities.

Q: How well does it transfer?
A: Mixed. [eval/results.md](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.md) reports 0.753 in-task accuracy and 0.030 ECE, but zero-shot falls to 0.651 accuracy and 0.204 ECE.

Q: Where would I be cautious?
A: Calibration claims outside the tested task mix. [eval/results.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.json) shows weak spots such as zero-shot emotion/tone ECE 0.3178 and sentiment/rating in-task ECE 0.4384.

## What is smart

The output grammar is the product. By forcing every decision through `choice`, `score`, or `noul`, [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) removes most parser and schema-repair work.

The marker-position trick in [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) is simple and reusable. It lets one forward pass answer many heterogeneous questions because each option is just another scored marker.

The reward function is aligned with the promise. [proper_reward](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py) explicitly optimizes proper scoring rules, which is the right direction if the product sells probabilities rather than labels.

The repo ships its own evaluation artifacts in [eval/results.md](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.md) and [eval/results.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.json), which makes the hype easier to interrogate.

## What is flawed or weak

The Hugging Face `pipeline_tag` is `text-classification`, but the useful runtime is really the custom [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) plus [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py). Builders expecting a normal `pipeline()` experience may miss the actual interface.

The calibration story is uneven. [eval/results.md](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.md) is honest enough to show zero-shot ECE 0.204, which is not "trust these probabilities everywhere."

The long-context story needs care. [README.md](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/README.md) says to pass `max_len=8192` for multilingual long documents, but [multilingual/rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/rl_agent_config.json) defaults to 1024 while [multilingual/encoder/config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/multilingual/encoder/config.json) exposes 8192 positions. That is not necessarily wrong, but it means runtime configuration matters.

The eval set is useful but not a reproduction package. [eval/results.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/eval/results.json) gives outputs, not the full dataset and scripts needed to independently rerun every claim from scratch.

## What we can learn / steal

Steal the typed decision interface. For routing, triage, moderation, guardrails, and escalation, a bounded answer space is often better than free-form generation.

Steal the option-marker sequence pattern from [rl_common.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_common.py). It is a clean way to turn heterogeneous app decisions into one encoder scoring problem.

Steal the explicit calibration tables from [rl_agent_config.json](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_config.json). Probability products need temperature and cardinality handling, not just argmax labels.

Steal the email adapter pattern from [email_utils.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/email_utils.py): clean the state before asking the model, and ship default question bundles for common workflows.

## How we could apply it

In an agent platform, use a Laya-shaped model as a fast gate before expensive agents wake up. For example: route inbound support, score urgency, detect whether a request needs a human, and decide which specialist agent should receive the issue.

For guardrails, replace "LLM, please classify this and return JSON" with a typed `noul` or `choice` question set. The app can then threshold probabilities from [rl_agent_api.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/rl_agent_api.py) and log calibration over time.

For internal operations, build small domain adapters like [email_utils.py](https://huggingface.co/convaiinnovations/laya/blob/55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851/email_utils.py): normalize noisy state, define typed questions, and keep the model's job narrow.

## Bottom line

Laya is a useful artifact because it shows a concrete alternative to generative decision-making: encode the state, mark the options, score the options, calibrate the probabilities, and return typed answers. The approach is not universally calibrated, especially zero-shot, but the interface and implementation are worth stealing for production triage and routing systems.
