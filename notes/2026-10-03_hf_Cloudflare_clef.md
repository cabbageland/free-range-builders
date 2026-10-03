# Clef

- Source: Hugging Face
- Artifact: model Cloudflare/clef
- URL: https://huggingface.co/Cloudflare/clef
- Date: 2026-10-03
- Snapshot studied: Hugging Face revision 2f3de3dd85f379784083b0814d997ab627200f0c, last modified 2026-10-01T15:23:46Z
- Why picked today: It was high in Hugging Face trending, close to the top after a previously covered Laya item. It is useful because it is not just another chat checkpoint: Cloudflare exposes a 27B multimodal decision model with a custom joint schema head, runnable adapter code, configs, tokenizer/processor files, and sharded weights.

## Executive summary

Clef is a multimodal typed-decision model. Instead of generating free-form text and hoping downstream code can parse it, it takes a state plus a schema of questions and returns option probabilities for each question in one forward pass. The [model card](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/README.md) describes it as a 27B post-train of [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), with text, JSON, image, and video inputs.

The source artifact is unusually inspectable for a hosted model. It includes the backbone config in [config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/config.json), generation defaults in [generation_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/generation_config.json), multimodal processing in [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/processor_config.json), the schema-head shape in [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_head_config.json), the implementation in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py), and the sharded-weight map in [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/model.safetensors.index.json).

## What they built / released

They released a Qwen-based multimodal classifier/decision model with a custom head. The base model is `Qwen3_5ForConditionalGeneration` according to [config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/config.json), but inference does not use text generation for the final answer. The custom code in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py) encodes a record, marks spans for each question and allowed option, runs the backbone to get hidden states, then applies `JointSchemaHead` to score every allowed option.

The release includes roughly 27.36B BF16 parameters according to the Hugging Face API metadata, with the backbone in [model-00001-of-00012.safetensors](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/model-00001-of-00012.safetensors) through [model-00012-of-00012.safetensors](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/model-00012-of-00012.safetensors), a separate [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_head.safetensors), and a [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/model.safetensors.index.json) map.

## Why it matters

This is a clean example of moving a common agent problem out of brittle prompt parsing. Many workflows need decisions: route this ticket, classify this invoice, choose the next tool, score urgency, decide whether an image is legible. A normal chat model can answer those, but production systems then need output-format prompts, retry loops, JSON repair, and confidence heuristics. Clef's design says: give the model the schema, let it score allowed options directly, and return calibrated-ish probabilities.

It also points at a practical middle ground between "LLM as universal text generator" and "tiny task-specific classifier." Clef keeps the multimodal and reasoning capacity of a large Qwen backbone, but the final interface is typed. That is attractive for business workflows where the answer must join a state machine, not entertain a human.

## Artifact shape at a glance

- [README.md](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/README.md): model card, usage examples, input format, file map, benchmark tables, and Jev/SystemOne API notes.
- [config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/config.json): the Qwen3.5/Qwen3.8-style text and vision backbone configuration, including 64 text layers, 5120 hidden size, 262144 max position embeddings, and a 27-layer vision stack.
- [chat_template.jinja](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/chat_template.jinja): a Qwen-style multimodal chat template with image/video placeholders, tool-call formatting, and reasoning-effort instructions.
- [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/processor_config.json): Qwen3VL processor setup for image and video resizing, normalization, frame sampling, patch size, merge size, and video limits.
- [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_head_config.json): custom head dimensions: hidden size 5120, width 1024, 2 evidence-routing layers, 4 decoder layers, 16 heads, and 4096 feedforward width.
- [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py): the real mechanism: record rendering, media encoding, span tracking, batching, evidence routing, logits, model loading, and SystemOne response conversion.
- [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_head.safetensors): learned weights for the schema head.
- [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/model.safetensors.index.json): maps backbone tensors to the 12 model shards.
- [tokenizer.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/tokenizer.json) and [tokenizer_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/tokenizer_config.json): tokenizer and template metadata.

## Layered architecture dissection

### High-level system shape

Clef has three conceptual layers.

The first layer is the Qwen multimodal backbone. [config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/config.json) shows a 64-layer text model with alternating `linear_attention` and periodic `full_attention`, a 5120 hidden size, 24 attention heads, 4 key/value heads, and a Qwen vision configuration with patch size 16 and out hidden size 5120. The model can ingest text, images, and videos through the Qwen3VL-style processor in [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/processor_config.json).

The second layer is schema encoding. [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py) converts each request into a prompt-like token sequence: a system prompt, the rendered state, `SCHEMA FIELDS`, each question's ID/type/instruction, and every allowed option. Crucially, it records token spans for the question text and option descriptions, so the head can later pull hidden-state summaries for each semantic slot.

The third layer is the joint schema head. `JointSchemaHead` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py) projects the backbone hidden states down to a 1024-wide decision space, routes option queries over the full sequence memory through `EvidenceRoutingLayer`, builds field vectors using question vectors, option summaries, a global vector, and question-type embeddings, then scores each option. The result is one set of logits per question.

### Main layers

The input layer is `encode_record` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py). It supports a `state` string or JSON value, optional `images` and `videos`, optional `media_kwargs`, and a `questions` mapping. Question types are `noul`, `choice`, and `score`. `choice` criteria are sorted by key, `score` levels are indexed, and `noul` defaults to true/false descriptions.

The batching layer is `collate_records` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py). It pads input IDs, builds attention masks, concatenates image/video tensors, and aligns media token type IDs at the right offset. That is the glue that lets text-only and multimodal records share one batch.

The backbone layer is `ClefModel.forward` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py). It pulls the underlying text or multimodal model, disables cache, forwards input IDs, attention mask, and media tensors, then hands `last_hidden_state` plus the output-embedding matrix to the custom head.

The response layer is `systemone` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py). It validates the request, calls `encode_record`, runs the model, applies softmax per question, and formats `noul`, `choice`, or `score` answers with confidence/probabilities and token usage.

### Inference / data / control flow

A caller constructs a record with `state` and `questions`, following the examples in [README.md](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/README.md). `encode_record` renders the state with stable JSON settings, injects image/video placeholder tokens when present, tokenizes the schema, tracks spans, and enforces `max_length` and optional `max_state_tokens`.

`collate_records` creates tensors and media payloads. The Qwen backbone runs once. `JointSchemaHead.forward` then does the important work: mean-pools hidden states over question spans and option spans, uses the output embeddings to build lexical option anchors, routes options through attention over the full sequence memory, constructs field vectors, runs decoder layers against memory, and combines a lexical prior with a joint cosine/residual score.

Finally, the code softmaxes logits per question. For `choice`, the highest-probability criterion becomes the answer; for `score`, it computes the expected score over ordinal levels; for `noul`, it returns the true probability. The [README](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/README.md) emphasizes the production implication: no free-form text generation and no output parsing.

## Key files, configs, cards, and artifacts

- [README.md](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/README.md): the card is good because it includes not just benchmarks but an explicit file-purpose table and runnable Python usage.
- [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py): the core implementation; read this before trusting the card.
- [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_head_config.json): the smallest file with the clearest architectural fingerprint of the custom head.
- [joint_head.safetensors](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_head.safetensors): the learned decision head, separate from the Qwen backbone.
- [config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/config.json): confirms this is a multimodal Qwen-family backbone, not a tiny classifier dressed up with a card.
- [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/processor_config.json): the practical limits and transforms for images and video, including 2 FPS sampling and up to 768 frames.
- [chat_template.jinja](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/chat_template.jinja): standard chat/tool/reasoning formatting still ships with the model, even though Clef's special path avoids free-form answer parsing.
- [model.safetensors.index.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/model.safetensors.index.json): proves the backbone is sharded and maps many Qwen tensor names, including linear-attention and self-attention layers.
- [generation_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/generation_config.json): mostly legacy/default generation settings; less central to Clef than the custom head path.

## Important components

`question_options` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py) is small but important. It normalizes the schema into allowed options: true/false for `noul`, sorted criteria for `choice`, and indexed criteria for `score`. This makes the final output bounded.

`encode_record` is the contract boundary. It decides how state, media, and schema become model-visible tokens. Its `max_length` default is 16384, and it can cap `max_state_tokens`, which is a useful escape hatch when the state is large but the schema must be preserved.

`EvidenceRoutingLayer` is the retrieval-like piece inside the head. It uses multi-head attention from option queries to the sequence memory, then a feed-forward residual. That gives each option a chance to gather evidence from the whole state/schema sequence instead of scoring only local option tokens.

`JointSchemaHead` is the main architectural idea. It combines question spans, option spans, lexical option embeddings, global hidden state, question-type embeddings, evidence routing, decoder layers, lexical prior scaling, joint logit scaling, and a residual gate. The head is compact relative to the 27B backbone but expressive enough to model dependencies between fields.

`systemone_answer` and `systemone` are the product wrapper. They turn tensors into a business API shape: `answers` keyed by question ID with `choice`, `score`, or `noul` values and probabilities. That makes the artifact feel deployable, not just researchy.

## Important knobs / configs / extension points

The most important user-facing knobs are in the request schema described by [README.md](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/README.md): question `type`, optional `instructions`, `criteria`, optional `images`, optional `videos`, and `media_kwargs`.

The main inference knobs inside [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py) are `max_length` and `max_state_tokens` on `encode_record` and `systemone`. These decide how much state survives once the fixed prompt and schema are accounted for.

The architecture knobs live in [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_head_config.json): width, routing layers, decoder layers, heads, and feedforward size. That file is effectively the custom-head spec.

The media knobs live in [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/processor_config.json): image normalization, patch size, resize bounds, video FPS, min/max frames, and video processor type.

## Practical questions and answers

Q: Is Clef a chat model?  
A: It has a Qwen chat template in [chat_template.jinja](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/chat_template.jinja), but Clef's core interface is not chat completion. The key path in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py) scores schema options directly.

Q: What is the difference from asking a normal LLM for JSON?  
A: JSON prompting still generates tokens and then requires parsing and validation. Clef creates one logit per allowed option per question and softmaxes those logits. That moves validity into the model head and request schema.

Q: Can it handle multiple fields jointly?  
A: Yes, that is the point of `JointSchemaHead`. It builds field vectors, summarizes options, routes evidence, and runs transformer decoder layers over all fields before scoring options.

Q: What should make a production builder cautious?  
A: Confidence is still model confidence, not ground truth. The [README benchmark table](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/README.md) is broad but internal-run reported; for a real workflow, you would need calibration, abstention policy, drift monitoring, and a human review path for high-cost decisions.

Q: What makes the release unusually useful to inspect?  
A: The custom code is shipped. Many model cards describe architecture vaguely; here [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py) exposes the actual record encoding, custom modules, and response conversion.

## What is smart

The smartest design choice is direct option scoring. It attacks a real systems problem: reliable structured output. By making each answer one of the allowed options, Clef reduces the amount of glue code and retry logic around LLM decisions.

The second smart choice is span-aware schema encoding. `encode_record` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py) does not merely dump a schema into a prompt; it records where questions and options sit in the token sequence. That gives the head stable handles into the hidden states.

The third smart choice is preserving multimodality. The processor setup in [processor_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/processor_config.json) and the media batching in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py) make typed decisions possible over receipts, screenshots, video frames, and JSON state with the same schema mechanism.

## What is flawed or weak

The release is heavy. A 27B BF16 model with 12 safetensor shards plus a custom head is not a casual deployment, and the [README](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/README.md) says the example was tested on a single H200. The smaller [Cloudflare/clef-flash](https://huggingface.co/Cloudflare/clef-flash) exists for a reason.

The API is elegant but opinionated. `noul`, `choice`, and `score` cover many workflows, but they do not cover every structured output. If the user needs hierarchical extraction, sets, spans, or generated rationales, Clef's bounded-decision interface may need to sit beside another model rather than replace it.

The card's benchmark story is broad but not enough by itself. The [README](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/README.md) includes many results, but the artifact does not include the full eval harness in the model repo. Treat the numbers as a pointer, then run your own decision set.

## What we can learn / steal

Steal the pattern: use a large multimodal backbone for understanding, then add a small task-shaped head for the actual production interface. The combination is visible in [config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/config.json), [joint_head_config.json](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_head_config.json), and [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py).

Steal the span bookkeeping. If you are building custom heads over LLM hidden states, record semantic spans during tokenization. Do not force the head to rediscover where the schema pieces are.

Steal the response wrapper. `systemone` in [joint_schema_model.py](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/joint_schema_model.py) is short, but it turns a research module into an API-shaped object with validation, probabilities, and usage metadata.

Steal the file-table style from the [README](https://huggingface.co/Cloudflare/clef/blob/2f3de3dd85f379784083b0814d997ab627200f0c/README.md). For model releases, a table mapping each artifact to its purpose dramatically lowers the cost of serious inspection.

## How we could apply it

For internal agent workflows, Clef's pattern suggests a safer router: state comes from the current task, questions define allowed next actions, and the model returns probabilities instead of prose. That could help with triage, escalation, tool choice, or "does this need human review?" gates.

For evaluation, the typed-decision shape is a good fit for business-process regression suites. Instead of scoring generated text with fuzzy matchers, define the workflow state and expected option labels, then measure exact action, primary action, confidence calibration, and abstention.

For product design, the lesson is to resist making every intelligent feature a chat box. Many valuable AI surfaces are better as decision APIs. Clef is a strong example of a model interface shaped around the downstream system, not the other way around.

## Bottom line

Clef is a serious builder artifact because the mechanism is visible: Qwen multimodal backbone, schema-token span tracking, evidence routing, a compact joint head, and SystemOne-shaped responses. The model is expensive and specialized, but the architecture is a useful antidote to brittle "LLM returns JSON" workflows.
