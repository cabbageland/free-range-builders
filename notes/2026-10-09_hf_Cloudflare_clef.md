# Cloudflare Clef

- Source: Hugging Face
- Artifact: model Cloudflare/clef
- URL: https://huggingface.co/Cloudflare/clef
- Date: 2026-10-09
- Snapshot studied: revision ed3eed331870db2eff4b0db01237128ede8a00ce, last modified 2026-10-07T15:35:49Z
- Why picked today: It is still high on Hugging Face's trending model list, and the current revision is newer than the earlier Clef notes in this notebook. The artifact remains unusually inspectable: a Qwen multimodal backbone, sharded safetensors, a custom joint schema head, runnable Python release code, processor/tokenizer assets, config files, and benchmark tables.

## Executive summary

[Cloudflare/clef](https://huggingface.co/Cloudflare/clef/tree/ed3eed331870db2eff4b0db01237128ede8a00ce) is a 27B multimodal typed-decision model. It takes a `state` plus a schema of questions and returns a probability distribution over the allowed options for every question in one forward pass. This is not JSON-mode generation with a parser bolted on. The answer space is explicitly the schema's options.

The artifact has a clean two-part shape. The base is a [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) multimodal backbone represented by [config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/config.json), [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/model.safetensors.index.json), and twelve sharded model files. The decision layer is [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_head.safetensors), [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_head_config.json), and [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py).

The key idea is schema-conditioned classification. [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) renders a record, tracks the token spans for every question and allowed option, runs the Qwen backbone, then uses a small transformer head to route evidence from the state to each option and score them. That is a very practical pattern for workflow automation, triage, eval judging, routing, policy checks, and any place where a decision should be a probability distribution rather than prose.

## What they built / released

Cloudflare released a typed-output decision model post-trained from [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B). The [README.md](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/README.md) says Clef reads text, JSON, images, or video and supports three question types: `noul` for true/false, `choice` for named options, and `score` for ordered options.

The release includes the backbone weights in [model-00001-of-00012.safetensors](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/model-00001-of-00012.safetensors) through [model-00012-of-00012.safetensors](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/model-00012-of-00012.safetensors), with [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/model.safetensors.index.json) reporting 27,356,728,560 parameters and about 54.7 GB of indexed weights. The custom head is separate: [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_head_config.json) declares hidden size 5120, internal width 1024, two routing layers, four decoder layers, 16 heads, and 4096 feedforward width.

The runnable mechanism is not hidden in a paper. [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) contains record rendering, media encoding, span tracking, batching, the evidence-routing layer, the joint schema head, the model wrapper, `load_release_model`, `systemone`, and conversion back to Jev/SystemOne-style responses.

## Why it matters

Structured-output work is everywhere in agent systems. A model routes a support ticket, chooses an action, scores urgency, labels an incident, extracts invoice status, checks whether a UI state is acceptable, or judges an eval case. The common implementation asks a chat model for JSON and then layers on schema validation, repair prompts, retries, and confidence guesses.

Clef attacks the problem at the output layer. Because the allowed options are in the model's scoring head, the product can get one probability distribution per field. That makes confidence thresholds, abstention, fallback, telemetry, and downstream state machines simpler.

It also matters because it is a concrete packaging example. The model card in [README.md](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/README.md) gives usage code, but the source artifact gives the real contract: [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) accepts a record, returns logits per field, and exposes a compatibility `systemone` wrapper.

## Artifact shape at a glance

- [README.md](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/README.md): model card, file map, usage examples, Jev/SystemOne API notes, input format, Decision Index benchmarks, workflow evals, and license.
- [config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/config.json): Qwen3.5/Qwen3.8-style multimodal config with 64 text layers, 5120 hidden size, 262144 max positions, linear-attention layers with periodic full attention, and a 27-layer vision config.
- [generation_config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/generation_config.json): inherited generation defaults; mostly incidental because Clef's core path is not free-text generation.
- [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/model.safetensors.index.json): backbone tensor-to-shard map with parameter and size metadata.
- [model-00001-of-00012.safetensors](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/model-00001-of-00012.safetensors) through [model-00012-of-00012.safetensors](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/model-00012-of-00012.safetensors): sharded BF16 backbone weights.
- [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_head_config.json): compact schema-head shape: 5120 input hidden size, 1024 internal width, two routing layers, four decoder layers, 16 heads, and 4096 feedforward width.
- [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_head.safetensors): learned weights for the custom decision head.
- [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py): core release code for encoding, batching, model loading, inference, evidence routing, logits, and response conversion.
- [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/processor_config.json): Qwen3VL processor setup for images and video: normalization, patch size, merge size, frame sampling, and video limits.
- [tokenizer.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/tokenizer.json), [tokenizer_config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/tokenizer_config.json), and [chat_template.jinja](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/chat_template.jinja): tokenizer and multimodal chat formatting assets.

## Layered architecture dissection

### High-level system shape

Clef is a large multimodal backbone plus a small schema-conditioned decision head. The backbone reads the rendered state, media placeholders, and schema. The custom head reads the final hidden states and computes logits for every allowed option of every question.

That gives the model two sources of structure. The first is textual: [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) writes `STATE`, `SCHEMA FIELDS`, field IDs, question types, instructions, and allowed options into the prompt. The second is tensor-level: the same file records spans for questions and options so the head can pool exactly those regions.

### Main layers

The input rendering layer is `encode_record` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py). It renders arbitrary string or JSON state with deterministic JSON formatting, inserts optional image/video token placeholders, writes each schema field, stores `question_span` and `option_spans`, enforces `max_length`, and optionally truncates state with `max_state_tokens`.

The batching layer is `collate_records` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py). It pads records, builds attention masks, and carries media tensors plus token-type masks. This is what lets text-only and multimodal records mix in one batch.

The backbone layer is configured by [config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/config.json). The text config has 64 layers, hidden size 5120, 24 attention heads, four key/value heads, 262144 max position embeddings, and a layer pattern of linear attention with periodic full attention. The vision config has 27 layers, hidden size 1152, 16 heads, patch size 16, temporal patch size 2, and output hidden size 5120.

The decision head is `JointSchemaHead` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py). It normalizes hidden states, projects full memory, projects question spans, projects option spans, adds a type embedding for `noul`, `choice`, or `score`, runs evidence-routing attention layers, then runs transformer decoder layers so fields can attend to memory.

The scoring layer combines lexical and contextual evidence. In [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py), each option gets a prior from output-embedding lexical similarity and a joint score from field/option cosine similarity plus a residual scorer over `[field, option, field * option, abs(field - option)]`. A learned gate blends the joint score into the prior.

The API layer is `systemone` and `systemone_answer` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py). It validates a Jev/SystemOne-shaped request, runs a single encoded record, applies softmax per question, and returns typed answers: true probability for `noul`, top choice plus probabilities for `choice`, and expected score plus legend/probabilities for `score`.

### Inference / data / control flow

The caller supplies a record with `state`, optional `images` and `videos`, and a `questions` mapping. [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) renders the state and schema into one input sequence. If images or video are present, `_encode_media` uses the processor to create media tensors and inserts Qwen vision placeholders.

The batch enters `ClefModel.forward` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py). If there is no media, it can use the text-only `language_model` submodule; if media is present, it routes through the full multimodal model. The backbone produces `last_hidden_state`.

The head loops record by record. It mean-pools the question spans and option spans, projects the whole hidden-state sequence into memory, routes option queries over the memory, summarizes options back into field vectors, and decodes field representations against the same memory. Finally, it emits one vector of logits per question, whose length equals that question's option count.

`systemone` then converts logits into product-ready answers. For `choice`, it returns the selected option, confidence, and per-option probabilities. For `score`, it returns an expected score rather than only the argmax. For `noul`, it returns the probability of true.

## Key files, configs, cards, and artifacts

- [README.md](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/README.md): best high-level map of model intent, file roles, usage, and benchmarks.
- [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py): the most important source file because it exposes the real inference protocol and head logic.
- [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_head_config.json): head topology and dimensions.
- [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_head.safetensors): the learned custom head.
- [config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/config.json): backbone text and vision configuration.
- [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/processor_config.json): image/video preprocessing and sampling constraints.
- [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/model.safetensors.index.json): weight-map proof that this is a 12-shard 27B backbone plus external head, not a tiny classifier.
- [chat_template.jinja](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/chat_template.jinja): relevant for tokenizer/model compatibility, even though the typed decision path does not rely on free-form generation.

## Important components

- `encode_record` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py): converts product-shaped state and schema into model tokens while recording spans.
- `_encode_media` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py): bridges optional images/videos into Qwen processor outputs and token offsets.
- `EvidenceRoutingLayer` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py): multi-head attention from option queries into full sequence memory.
- `JointSchemaHead` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py): the custom architecture that makes Clef more than a prompted Qwen checkpoint.
- `load_release_model` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py): release loader for the merged backbone, head weights, and processor.
- `systemone` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py): compatibility wrapper for the typed decision API.

## Important knobs / configs / extension points

- `max_length` in `encode_record` and `systemone` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) defaults to 16384 tokens. That is a real product budget: large schemas can crowd out state, and long states can be truncated.
- `max_state_tokens` in `encode_record` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) lets callers bound state length separately from schema length.
- `media_kwargs` in the record are passed into the processor by [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py), so image/video processing can be tuned by callers.
- [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/processor_config.json) sets video sampling to 2 fps with `min_frames` 4 and `max_frames` 768, and defines image/video resizing and normalization.
- [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_head_config.json) is the obvious head-size extension point: width, routing layers, decoder layers, heads, and feedforward width.

## Practical questions and answers

Q: Is Clef just a JSON-output prompt?  
A: No. [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) returns logits per allowed option. The schema is rendered into the input, but the final output is not generated text.

Q: What makes the head "joint"?  
A: The head scores all fields in one pass over the same state and memory. It builds field vectors, routes option queries over the full hidden-state sequence, and lets field representations attend to memory through decoder layers in [JointSchemaHead](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py).

Q: What are the production limits?  
A: The model is huge: [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/model.safetensors.index.json) reports a 27B backbone. The [README.md](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/README.md) says it was tested on a single H200. This is not a cheap edge classifier.

Q: Where should builders be skeptical?  
A: The benchmark table in [README.md](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/README.md) is useful but mostly an internal Decision Index run. Treat it as directional until reproduced on your schemas and traffic.

Q: What is most reusable?  
A: The schema-head idea. Even without training a 27B model, the pattern of rendering schema, tracking spans, scoring allowed options, returning probabilities, and preserving expected-score semantics is worth copying.

## What is smart

The biggest smart move is removing parsing from the critical path. Clef does not ask a model to produce valid JSON and then repair it. It scores the actual allowed options. That is cleaner for state machines and automation.

The second smart move is preserving option semantics in two ways. [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) uses both the hidden states from rendered option descriptions and the output embedding weights for the option tokens. That gives the head lexical priors plus contextual evidence routing.

The third smart move is making the release runnable. Many model cards describe custom behavior but ship only weights. Clef ships [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py), [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_head_config.json), [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_head.safetensors), and usage code in [README.md](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/README.md).

## What is flawed or weak

The dependency footprint is heavy. [README.md](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/README.md) says the release was tested with Torch 2.11 and Transformers 5.10.2 on a single H200. That is fine for serious inference, but it narrows who can evaluate it casually.

The schema rendering is clear but brittle in ordinary ways. If a schema is enormous, [encode_record](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) can spend the token budget before much state fits. If option descriptions are sloppy, the model scores sloppy semantics. The system improves structured output, but it does not remove schema design from the product.

The safety and calibration story is not very visible in the files I inspected. We get probabilities, but probability is not the same as calibrated confidence under distribution shift. A builder still needs offline calibration, abstention policies, and monitoring.

## What we can learn / steal

Steal the product contract: decisions should often be probabilities over explicit options, not strings. That alone simplifies retries, audit logs, thresholds, and downstream automation.

Steal the encoding pattern from [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py): deterministic state rendering, explicit field IDs, explicit option descriptions, span tracking, and a bounded token budget.

Steal the score semantics. For `score`, [systemone_answer](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) returns an expected score and the full probability distribution, not just an argmax. That is a better interface for risk scoring and thresholds.

Steal the compatibility wrapper idea. `systemone` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/ed3eed331870db2eff4b0db01237128ede8a00ce/joint_schema_model.py) lets a custom model present a stable API contract. That is how you let clients benefit from new model mechanics without rewriting their workflow layer.

## How we could apply it

For internal tools, Clef suggests a different architecture for agent decisions. Instead of asking an LLM to "return JSON with action and confidence," define the action schema first, render the state plus schema, and return probabilities over legal actions. For high-volume routes, a specialized head or smaller classifier could do the same thing cheaply.

For eval systems, Clef's design maps naturally to judge tasks. Evals often ask a model to choose among labels, score a rubric, or mark true/false. A schema-conditioned scorer would produce better telemetry than a judge that emits prose and needs parsing.

For product workflows, the strongest application is a typed decision gateway: invoice state in, schema of possible actions in, probability distributions out. The rest of the system can decide thresholds, fallbacks, and human review separately.

## Bottom line

Clef is worth studying because it turns structured output into a model architecture choice. The release is large and hardware-hungry, but the mechanism is concrete: render state and schema, track spans, route evidence, score options, and return probabilities. That pattern is broadly useful even when the deployed model is much smaller.
