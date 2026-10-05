# Cloudflare Clef

- Source: Hugging Face
- Artifact: model Cloudflare/clef
- URL: https://huggingface.co/Cloudflare/clef
- Date: 2026-10-05
- Snapshot studied: revision 2f3de3dd85f379784083b0814d997ab627200f0c, last modified 2026-10-01T15:23:46Z
- Why picked today: Hugging Face trending placed it at the top of the model list, and it has unusually inspectable mechanics: a Qwen multimodal backbone, sharded safetensors, custom typed-decision head, config files, processor/tokenizer assets, and release code.

## Executive summary

[Cloudflare/clef](https://huggingface.co/Cloudflare/clef/tree/main) is a 27B multimodal decision model. Instead of generating free text, it takes a state plus a schema of typed questions and returns one probability distribution per question. The interesting engineering move is the extra [joint schema head](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) on top of a [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) backbone: the backbone reads text/images/video, while the head routes evidence to each field and scores all allowed options jointly.

That makes this a strong artifact to study because the release is not only weights plus a model card. It includes [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py), [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/main/joint_head_config.json), [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/main/joint_head.safetensors), standard backbone shards, tokenizer/processor configs, and a compatibility wrapper for the Jev/SystemOne API.

## What they built / released

They released a specialized decision model for typed outputs. The [README card](https://huggingface.co/Cloudflare/clef/blob/main/README.md) describes a model that reads a `state` as text, JSON, image, or video and answers schema fields of type `noul`, `choice`, or `score`. The output is not a parsed string. It is logits over each field's allowed options, converted to probabilities per question.

The released files have two large parts. The first is the Qwen3.8 multimodal backbone stored in [model-00001-of-00012.safetensors](https://huggingface.co/Cloudflare/clef/blob/main/model-00001-of-00012.safetensors) through [model-00012-of-00012.safetensors](https://huggingface.co/Cloudflare/clef/blob/main/model-00012-of-00012.safetensors), indexed by [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/main/model.safetensors.index.json). The second is the custom schema head stored in [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/main/joint_head.safetensors) and configured by [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/main/joint_head_config.json).

## Why it matters

Most structured-output LLM stacks still ask a generative model to produce JSON, then parse, validate, retry, and sometimes repair it. Clef sidesteps that entire class of failures by making the allowed answers the output space. For routing, triage, form filling, eval judging, policy decisions, and workflow branching, probabilities over explicit options are often more useful than a fluent explanation.

It also exposes a useful design pattern: keep a very capable multimodal backbone, but add a task head that understands the schema and scores choices directly. That is a middle road between generic chat-completion prompting and training a separate classifier for every task.

## Artifact shape at a glance

- [README.md](https://huggingface.co/Cloudflare/clef/blob/main/README.md): model card, usage examples, input format, benchmark tables, and release file map.
- [config.json](https://huggingface.co/Cloudflare/clef/blob/main/config.json): Qwen3.8 multimodal configuration, including text and vision configs.
- [generation_config.json](https://huggingface.co/Cloudflare/clef/blob/main/generation_config.json): inherited generation defaults, mostly incidental because Clef's core path does not generate free text.
- [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/main/model.safetensors.index.json): 27,356,728,560-parameter backbone index across twelve shards.
- [model-00001-of-00012.safetensors](https://huggingface.co/Cloudflare/clef/blob/main/model-00001-of-00012.safetensors) through [model-00012-of-00012.safetensors](https://huggingface.co/Cloudflare/clef/blob/main/model-00012-of-00012.safetensors): sharded backbone weights.
- [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/main/joint_head_config.json): compact custom head shape: hidden size 5120, internal width 1024, two routing layers, four decoder layers, 16 heads, and 4096 feedforward width.
- [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/main/joint_head.safetensors): trained weights for the custom decision head.
- [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py): encoding, batching, evidence routing, model wrapper, release loader, and SystemOne-compatible inference helper.
- [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/main/processor_config.json): Qwen3VL image/video processor settings.
- [tokenizer.json](https://huggingface.co/Cloudflare/clef/blob/main/tokenizer.json), [tokenizer_config.json](https://huggingface.co/Cloudflare/clef/blob/main/tokenizer_config.json), and [chat_template.jinja](https://huggingface.co/Cloudflare/clef/blob/main/chat_template.jinja): tokenizer and prompt/chat formatting assets.
- [LICENSE](https://huggingface.co/Cloudflare/clef/blob/main/LICENSE): Apache-2.0 license.

## Layered architecture dissection

### High-level system shape

Clef wraps a multimodal foundation model with a task-specific decision layer. The backbone reads the rendered record and produces hidden states. The custom code in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) records where each question and option appears in the token stream, pools those spans, routes evidence from the full hidden-state memory into option queries, and returns option logits per schema field.

This is best understood as "schema-conditioned classification" rather than text generation. The schema is part of the input, but the answer vocabulary is not open-ended.

### Main layers

The input rendering layer is `encode_record` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py). It serializes arbitrary JSON/string state with deterministic JSON formatting, writes a schema section with field IDs, types, instructions, and allowed options, inserts image/video placeholders when needed, truncates state to fit the token budget, and returns an `EncodedRecord` containing token IDs plus question/option spans.

The batching layer is `collate_records` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py). It pads variable-length records, builds attention masks, and handles media tensors and token-type masks from the processor. This is the bridge that lets text-only and multimodal examples share a batch.

The backbone layer is configured by [config.json](https://huggingface.co/Cloudflare/clef/blob/main/config.json). The text config has 64 layers, hidden size 5120, 24 attention heads, a long 262144-token position setting, and a repeating pattern of linear-attention layers with periodic full-attention layers. The vision config has a 27-layer vision encoder with 16 heads, patch size 16, temporal patch size 2, and output hidden size 5120.

The schema head layer is implemented by `JointSchemaHead` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) and shaped by [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/main/joint_head_config.json). It projects hidden states into a 1024-wide decision space, represents question spans and option spans, adds type embeddings for the three question types, uses evidence-routing attention layers, then uses transformer decoder layers to let fields attend to the full memory.

The API compatibility layer is `systemone` and `systemone_answer` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py). It validates Jev/SystemOne-shaped requests, runs one encoded record, softmaxes per-field logits, and returns typed answers with confidence/probability fields.

### Inference / data / control flow

The user calls `load_release_model` from [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py). That function loads the Qwen3.5/3.8-style conditional-generation backbone from the model directory, disables cache, reads [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/main/joint_head_config.json), loads [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/main/joint_head.safetensors) with safetensors, and returns a `ClefModel` plus `AutoProcessor`.

At inference time, `encode_record` creates the combined system/user/schema sequence. `collate_records` moves it to the target device. `ClefModel.forward` calls the backbone text model or multimodal model depending on whether media is present, then passes `last_hidden_state`, `input_ids`, `attention_mask`, records, and the output embedding matrix into the head.

Inside `JointSchemaHead.forward`, every question gets a question vector by averaging hidden states over its instruction span. Every option gets both a contextual span average and a lexical embedding average from the output embedding table. Option queries attend over the full record memory through `EvidenceRoutingLayer`. The head builds field vectors from question vectors, option summaries, global final-token context, and question-type embeddings, then scores each option with a mix of lexical prior, cosine joint score, and residual MLP score.

## Key files, configs, cards, and artifacts

- [README.md](https://huggingface.co/Cloudflare/clef/blob/main/README.md): the release contract and examples. It is useful, but not sufficient alone.
- [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py): the critical source file. It contains `EncodedQuestion`, `EncodedRecord`, `encode_record`, `collate_records`, `EvidenceRoutingLayer`, `JointSchemaHead`, `ClefModel`, `load_release_model`, and `systemone`.
- [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/main/joint_head_config.json): tells us the custom head is small relative to the backbone but still real: 1024 width, two routing layers, four transformer decoder layers, and 16 heads.
- [config.json](https://huggingface.co/Cloudflare/clef/blob/main/config.json): the backbone and vision geometry. It confirms this is not a text-only classifier.
- [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/main/model.safetensors.index.json): weight map and total parameter count/size.
- [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/main/processor_config.json): image/video preprocessing and frame sampling details, including `Qwen3VLProcessor`, image normalization, video FPS, and frame limits.
- [tokenizer_config.json](https://huggingface.co/Cloudflare/clef/blob/main/tokenizer_config.json): long-context tokenizer settings and special vision/audio tokens.
- [chat_template.jinja](https://huggingface.co/Cloudflare/clef/blob/main/chat_template.jinja): chat formatting inherited from the backbone ecosystem.

## Important components

`question_options` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) is small but important. It normalizes the three output types. `noul` becomes true/false, `choice` sorts named criteria, and `score` enumerates ordered labels. That creates a uniform "options per question" substrate for the rest of the head.

`encode_record` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) is the real input compiler. It decides exactly what the model sees: system prompt, state, schema field text, option semantic JSON, media placeholder tokens, and an assistant prefix ending in `JOINT SCHEMA DECISIONS:`. It also enforces the max-length policy by truncating state rather than schema.

`EvidenceRoutingLayer` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) is the head's retrieval mechanism. Option queries attend over the full sequence memory, then pass through a feedforward block. That lets a candidate answer gather evidence from any part of the state/schema sequence.

`JointSchemaHead` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) is the main architectural payload. The scoring path is especially interesting: it combines a lexical prior between option embeddings and a question/global anchor with a joint routed score and residual scorer. That is a practical way to preserve option semantics while letting the head learn task-specific evidence matching.

`systemone` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) is the product adapter. It turns raw probability vectors into stable API responses: choices with confidence/probabilities, scores with expected value plus legend, and `noul` with true probability.

## Important knobs / configs / extension points

The key inference budget knob is `max_length` in `encode_record` and `systemone` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py), defaulting to 16384. The backbone may support a larger context according to [config.json](https://huggingface.co/Cloudflare/clef/blob/main/config.json) and [tokenizer_config.json](https://huggingface.co/Cloudflare/clef/blob/main/tokenizer_config.json), but the release code defaults to a practical request-size ceiling.

The custom-head shape is controlled by [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/main/joint_head_config.json). The obvious extension points are routing depth, decoder depth, width, and feedforward size. More routing layers could gather richer evidence; more decoder layers could model interactions between fields; both would raise latency and memory.

Media behavior is controlled by [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/main/processor_config.json). Image resize, normalization, merge size, video FPS, min/max frames, and temporal patching are not incidental if the model is used for receipts, screenshots, video review, or UI state inspection.

Question schema is the user-facing extension point. Any task that can be represented as `noul`, `choice`, or ordered `score` can be packed into the same decision call. Anything requiring spans, entities, structured lists, free-form rationales, or generated text does not fit this release directly.

## Practical questions and answers

Q: Is Clef a chat model?  
A: Not in the normal sense. The [README](https://huggingface.co/Cloudflare/clef/blob/main/README.md) is explicit that there is no free-form text generation or output parsing. The core output is option logits per schema field.

Q: What makes it different from JSON-mode prompting?  
A: JSON-mode prompting still asks a generator to emit a syntactically valid object. Clef makes the allowed choices the output classes. The code in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) softmaxes logits per question, so invalid options are not in the output space.

Q: How does it use the schema?  
A: The schema is not merely validated after the fact. `encode_record` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) embeds field IDs, instructions, types, and option descriptions into the prompt, records the token spans, and the head pools those spans as question/option vectors.

Q: Why keep `generation_config.json` if Clef does not generate?  
A: Because the backbone is still a Transformers conditional-generation model. [generation_config.json](https://huggingface.co/Cloudflare/clef/blob/main/generation_config.json) ships with the standard model surface, but the custom inference path in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) uses hidden states and the joint head instead of decoding text.

Q: What would fail in production?  
A: Schemas that are too large can consume the token budget before useful state is included. Ambiguous criteria will produce confident-looking probabilities over poorly designed options. Long video/image inputs can be expensive because [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/main/processor_config.json) allows significant visual input. And a 27B bfloat16 backbone is not a casual deployment target.

## What is smart

The cleverest part is making typed decisions first-class. `noul`, `choice`, and `score` cover a surprising amount of real workflow routing. By returning probabilities, Clef can express uncertainty without asking downstream code to infer it from text.

The span-aware head is also clean. [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) does not simply look at the final token and classify. It keeps question spans, option spans, lexical option embeddings, type embeddings, and global context separate, then lets evidence routing and decoder layers combine them.

The release packaging is good. Publishing [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) beside [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/main/joint_head.safetensors), [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/main/joint_head_config.json), [config.json](https://huggingface.co/Cloudflare/clef/blob/main/config.json), and processor/tokenizer files makes the artifact inspectable and reusable without reverse engineering.

## What is flawed or weak

The artifact is custom-code heavy. Users have to trust and import [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py), and the README's tested stack names Torch 2.11 and Transformers 5.10.2. That is acceptable for an advanced model release, but it is less plug-and-play than a plain `AutoModelFor...` card.

The output types are intentionally narrow. That is a strength for decisions, but a weakness for extraction tasks that need multiple entities, references to source spans, or mixed structured/free-form output. You could wrap Clef around a workflow, but it is not a universal structured-output replacement.

The model card's benchmark tables are broad, but they are still the publisher's internal run. The [README](https://huggingface.co/Cloudflare/clef/blob/main/README.md) gives useful numbers, yet a production adopter should rerun task-specific evals with their own schema wording and thresholds.

The compute footprint is large. [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/main/model.safetensors.index.json) reports roughly 27.36B parameters and about 54.7 GB of weights. That makes the smaller [Cloudflare/clef-flash](https://huggingface.co/Cloudflare/clef-flash) important for many real deployments.

## What we can learn / steal

Steal the "schema as classes, not just output instructions" pattern. If a task can be reduced to explicit options, train or adapt the model to score those options directly instead of generating text and parsing it.

Steal the input compiler shape from [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py): deterministic state rendering, explicit field sections, explicit option semantics, stable span bookkeeping, and state truncation that never chops off the schema.

Steal the probability-returning API. The `systemone` wrapper in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) returns confidence and per-option probabilities, which are more operationally useful than a single opaque answer.

Steal the separation between backbone and task head. The config in [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/main/joint_head_config.json) is small enough to understand independently, while [config.json](https://huggingface.co/Cloudflare/clef/blob/main/config.json) keeps the general multimodal capacity in the base model.

## How we could apply it

For an internal workflow router, Clef's pattern would let us define a schema of actions, urgency, responsible team, required follow-up, and "needs human" flags, then get calibrated probabilities for each field in one pass. The downstream system could threshold or escalate based on uncertainty instead of parsing a generated rationale.

For evals, the same pattern could turn a rubric into typed questions. Instead of asking a judge model for prose, ask for `choice` and `score` fields with criteria. The per-option distributions would make disagreement and borderline cases visible.

For multimodal operations, the image/video path in [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/main/processor_config.json) plus media handling in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/main/joint_schema_model.py) suggests a practical way to classify UI states, receipts, incident screenshots, or short video snippets with the same schema interface as text records.

## Bottom line

Clef is a good builder study because it turns structured output from a parsing problem into a modeling problem. The reusable lesson is simple: when the answer space is known, make the model score that answer space directly, carry probabilities through the API, and keep the schema mechanics inspectable in the release artifact.
