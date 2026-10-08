# autotrust/GEV-26B-Decide

- Source: Hugging Face
- Artifact: model autotrust/GEV-26B-Decide
- URL: https://huggingface.co/autotrust/GEV-26B-Decide
- Date: 2026-10-08
- Snapshot studied: revision 7c89590ead085bf77630b4bf68264ea30b6ddc78, last modified 2026-10-03T11:00:46Z
- Why picked today: It was high on Hugging Face's trending model list and is unusually inspectable: a Gemma-4-based decision model with LoRA adapters, a 24-slot decision head, calibration files, vLLM serving code, a patch, reports, demo traces, and videos.

## Executive summary

[autotrust/GEV-26B-Decide](https://huggingface.co/autotrust/GEV-26B-Decide/tree/7c89590ead085bf77630b4bf68264ea30b6ddc78) is an open-weights typed-decision model built on [google/gemma-4-26B-A4B-it](https://huggingface.co/google/gemma-4-26B-A4B-it). It is not packaged primarily as a chat model. The interesting surface is a decision API: ask a yes/no, 0-5 score, or multiple-choice question, and get calibrated probabilities over options.

The release has two modes. System 1 is a fast decision head over the Gemma hidden state, carried by [adapter/adapter_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter/adapter_config.json), [head.safetensors](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/head.safetensors), [judge_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/judge_config.json), and [calibration.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration.json). System 2 is the unchanged Gemma-4 backbone doing normal reasoning. [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) adds `POST /v1/decide` to vLLM and can escalate from System 1 to System 2 when confidence falls below a threshold.

The practical lesson is strong: product decisions should often be probability distributions, not text completions. This artifact shows how to package that: explicit slot ranges, verbalizer IDs, per-kind temperature calibration, adaptive-thinking thresholds, many-option strategy, reports, and a serving endpoint that keeps the chat API and decision API side by side.

## What they built / released

AutoTrust released a decision model on Gemma-4-26B-A4B-it with text and image input. The model card in [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md) describes System 1 as one forward pass that returns probabilities over typed answers, and adaptive thinking as a fallback that asks the base model to reason when System 1 is uncertain.

The model's visible mechanism is in the files. [config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/config.json) declares `Gemma4ForConditionalGeneration`, bfloat16 weights, Gemma-4 text config, a 262,144-token context, a 27-layer vision config, and no audio config. [adapter/adapter_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter/adapter_config.json) describes a LoRA adapter with rank 32, alpha 64, dropout 0.05, and target modules across attention and MLP projections. [judge_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/judge_config.json) defines 24 decision slots: two for `noul` false/true, six for `score` 0-5, and sixteen for choice labels A-P.

The serving path is first-class. [serve.sh](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve.sh) downloads the artifact, launches vLLM with LoRA enabled, loads [adapter_vllm](https://huggingface.co/autotrust/GEV-26B-Decide/tree/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter_vllm), enables processed logprobs, sets `--max-logprobs 256`, limits images per prompt, and optionally enables a speculative Gemma-4 draft model. [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) implements the endpoint, request schema, single/tournament/permute strategies, image parts, logprob readout, and adaptive thinking mix.

## Why it matters

Many production uses of LLMs are actually decisions: route this ticket, classify this intent, choose the next UI action, score this response, accept or reject an output. Returning prose and then parsing it is a weak contract. GEV-26B-Decide instead exposes a typed decision distribution. That makes confidence gating, abstention, escalation, policy thresholds, and UI loops much cleaner.

The artifact also matters because it shows both speed and caution. The card says System 1 is about 45 ms for a single request on a B200, while adaptive thinking can add seconds or tens of seconds. [reports/adaptive_latency_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_latency_summary.json) shows the Knowledge & Reasoning run thinking on 65.9 percent of requests, with estimated median latency 13.4 seconds without speculative decoding and 7.7 seconds with speculative decoding. That is a useful product boundary: fast decisions are for control loops; thinking is for cases where accuracy beats latency.

## Artifact shape at a glance

- [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md): model card, Decision Index claims, adaptive-thinking explanation, demo descriptions, latency notes, quick start, training disclosure, limitations, and file inventory.
- [config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/config.json): Gemma-4 architecture, text config, vision config, dtype, context length, token IDs, and no audio config.
- [model-00001-of-00002.safetensors](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/model-00001-of-00002.safetensors), [model-00002-of-00002.safetensors](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/model-00002-of-00002.safetensors), and [model.safetensors.index.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/model.safetensors.index.json): backbone checkpoint shards and index.
- [adapter](https://huggingface.co/autotrust/GEV-26B-Decide/tree/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter): PEFT LoRA adapter for the transformers path.
- [adapter_vllm](https://huggingface.co/autotrust/GEV-26B-Decide/tree/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter_vllm): vLLM-specific LoRA packaging, including [adapter_vllm/decision_head.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter_vllm/decision_head.json).
- [head.safetensors](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/head.safetensors): the 24-slot fp32 decision head for the transformers path.
- [judge_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/judge_config.json): slot ranges, verbalizers, token IDs, softcap, readout, LoRA metadata, base model name, and temperature profile.
- [calibration.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration.json) and [calibration_gold.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration_gold.json): per-kind temperature calibration files.
- [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) and [serve.sh](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve.sh): vLLM server extension and launcher.
- [patches/vllm-gemma4-lm-head-lora.patch](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/patches/vllm-gemma4-lm-head-lora.patch): vLLM patch for LoRA on Gemma-4's tied language-model head.
- [reports](https://huggingface.co/autotrust/GEV-26B-Decide/tree/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports): adaptive validation, Decision Index recomputation, latency summary, other-area sample, games, and demos.
- [videos](https://huggingface.co/autotrust/GEV-26B-Decide/tree/7c89590ead085bf77630b4bf68264ea30b6ddc78/videos): demonstration videos for computer use, robot arm, and reasoning games.

## Layered architecture dissection

### High-level system shape

The high-level shape is a base multimodal LLM plus a specialized decision readout. [config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/config.json) supplies the Gemma-4 backbone. [adapter/adapter_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter/adapter_config.json) adapts the backbone for decisions. [head.safetensors](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/head.safetensors) adds a compact output head. [judge_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/judge_config.json) defines how that head maps hidden state to a typed probability distribution.

There are two serving surfaces. The ordinary OpenAI-compatible chat/completions surface exposes System 2, the base model. The custom `POST /v1/decide` surface in [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) exposes System 1 and adaptive thinking. [serve.sh](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve.sh) makes that topology concrete by starting one vLLM engine with the base model and LoRA module.

### Main layers

The backbone layer is Gemma-4. [config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/config.json) shows a 30-layer text config with 2,816 hidden size, 16 attention heads, 128 experts, top-8 experts, a 262,144-token vocabulary, 262,144 max position embeddings, sliding attention with periodic full attention, and bfloat16 dtype. The same config includes a vision encoder with 27 hidden layers, 1,152 hidden size, 16 attention heads, 16-pixel patches, and 280 default soft tokens per image.

The System 1 decision layer is small and explicit. [judge_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/judge_config.json) says the readout uses the last token, a 24-slot head, a 30.0 softcap, and three kinds: `noul`, `choice`, and `score`. The slot layout is simple: `noul` uses slots 0-1, `score` uses 2-7, and `choice` uses 8-23. [adapter_vllm/decision_head.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter_vllm/decision_head.json) repeats the slot structure and stores the verbalizer IDs and bias for vLLM.

The calibration layer is separate from the weights. [calibration.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration.json) has per-kind temperatures: about 1.003 for `noul`, 1.017 for `choice`, and 0.999 for `score`, fitted on 10,954 rows. The model card in [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md) says [calibration_gold.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration_gold.json) should be used when automatic actions are gated on confidence.

The adaptive layer is policy plus serving logic. [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) defaults Gemma to tournament strategy, threshold 0.8, mix 0.5, and thinking off unless requested. In adaptive mode, it gets the System 1 distribution, checks the top probability, runs System 2 reasoning when below threshold, reads an answer-letter distribution, and mixes the two distributions.

The evidence layer is unusually rich. [reports/adaptive_validation_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_validation_summary.json), [reports/adaptive_latency_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_latency_summary.json), [reports/adaptive_other_areas_sample.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_other_areas_sample.json), [reports/thinking_games.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/thinking_games.json), and [reports/demos](https://huggingface.co/autotrust/GEV-26B-Decide/tree/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/demos) give enough raw material to evaluate the claims rather than just trust the card.

### Inference / data / control flow

For a System 1 decision, the caller sends `kind`, `state`, `question`, and optional `options` to `POST /v1/decide`. [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) serializes the request into a bare template with `[kind]`, `[state]`, `[question]`, `[options]`, and `[decision]`. The model reads one token's logprobs over the trained verbalizer IDs, adds tiny bias values, divides by the per-kind temperature from [calibration.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration.json), and softmaxes.

For choices above sixteen options, [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) supports strategies. The default Gemma profile uses `tournament`: groups of at most sixteen options plus a final. The model card's many-options section in [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md) reports better accuracy for tournament than a single pass with labels beyond P.

For adaptive thinking, System 1 runs first. If the leading probability is lower than the threshold, the base model reasons through the ordinary chat path. When reasoning ends, [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) reads the answer-letter distribution and mixes it with System 1. The default mix is 0.5, so the reasoning can improve accuracy without completely discarding System 1 calibration.

For image decisions, [processor_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/processor_config.json) defines a Gemma-4 processor with 280 image sequence tokens, 32 video frames, and an audio feature extractor section. The model card in [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md) is clearer about actual capability: this checkpoint contains the vision encoder and no audio encoder, so image decisions are supported while audio should not be assumed.

## Key files, configs, cards, and artifacts

- [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md): the best map of intended behavior, claims, usage, disclosure, and limitations.
- [config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/config.json): backbone architecture, context length, dtype, vision encoder, and token IDs.
- [adapter/adapter_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter/adapter_config.json): PEFT LoRA setup for the transformers path.
- [adapter_vllm/decision_head.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter_vllm/decision_head.json): vLLM-facing decision head metadata.
- [judge_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/judge_config.json): canonical decision slot and readout config.
- [calibration.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration.json): default per-kind temperature calibration.
- [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py): vLLM endpoint implementation and the best source for actual request semantics.
- [serve.sh](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve.sh): operational launch recipe and required flags.
- [patches/vllm-gemma4-lm-head-lora.patch](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/patches/vllm-gemma4-lm-head-lora.patch): evidence that the vLLM path depends on a specific patch, not only standard vLLM.
- [reports/adaptive_validation_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_validation_summary.json): threshold/mix validation on six outside datasets.
- [reports/adaptive_latency_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_latency_summary.json): estimated cost of thinking over Knowledge & Reasoning benchmarks.
- [reports/demos/cu_results.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/demos/cu_results.json), [reports/demos/arm_direct.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/demos/arm_direct.json), and [reports/demos/arm_servo.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/demos/arm_servo.json): the concrete demo traces behind the computer-use and robot-arm claims.
- [reports/thinking_games.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/thinking_games.json): one-move puzzle and game results showing where adaptive thinking helps and where it does not.

## Important components

The 24-slot decision head is the conceptual core. [judge_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/judge_config.json) says all supported decision kinds share one head, with inactive slots masked. That is a clean product surface: a yes/no, a score, and a choice all become one calibrated distribution API.

The LoRA adapter in [adapter](https://huggingface.co/autotrust/GEV-26B-Decide/tree/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter) is the specialization mechanism. [adapter/adapter_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter/adapter_config.json) targets attention and MLP projections across Gemma layers rather than only bolting on an external classifier.

The vLLM packaging in [adapter_vllm](https://huggingface.co/autotrust/GEV-26B-Decide/tree/7c89590ead085bf77630b4bf68264ea30b6ddc78/adapter_vllm) is important because serving is part of the release, not an exercise left to users. [serve.sh](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve.sh) captures operational assumptions: 80GB or larger GPU, Gemma-4-capable vLLM, the bundled patch, prefix caching, image limits, and optional speculative decoding.

The report files are first-class components. [reports/adaptive_validation_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_validation_summary.json) says adaptive thinking improved the six-dataset validation set from 73.32 percent to 83.35 percent while escalating 47.78 percent of questions. [reports/thinking_games.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/thinking_games.json) shows a more nuanced picture: huge gains on one-move Wordle, Sudoku, Connect Four, and 24-game puzzles, but weak or negative value on Flappy Bird, 2048, and some perception-heavy tasks.

## Important knobs / configs / extension points

The most important knob is `thinking`. [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md) and [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) expose `"off"`, `"auto"`, and `"on"`. Use `"off"` for classification, retrieval, tool routing, and tight control loops. Use `"auto"` when reasoning can justify latency.

The threshold and mix are product knobs. [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) defaults to threshold 0.8 and mix 0.5. [reports/adaptive_validation_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_validation_summary.json) is the grounding for those defaults, but product teams should refit them to their own risk and latency envelope.

The `strategy` knob matters for many-option choices. [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) supports `single`, `tournament`, and `permute`. The card in [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md) argues for tournament when there are more than sixteen options because the trained choice slots are A-P.

Calibration files are operational knobs. [calibration.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration.json) is the default; [calibration_gold.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration_gold.json) is recommended by the card for confidence-gated automatic actions. This is the right shape: confidence policy should be explicit and swappable.

The deployment knobs are in [serve.sh](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve.sh): `MODEL_DIR`, `MTP`, `MAX_MODEL_LEN`, `PORT`, max LoRA rank, `--max-logprobs 256`, prefix caching, and image-per-prompt limits.

## Practical questions and answers

Q: Is this a classifier or a chat model?  
A: It is both, but the interesting product surface is the classifier-like decision API. [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) adds `POST /v1/decide`, while the base model still serves normal OpenAI-compatible endpoints.

Q: What does "System 1" actually mean here?  
A: One forward pass, no generated rationale, and a probability distribution from a fixed decision head. [judge_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/judge_config.json) defines the head and slots; [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) implements the readout.

Q: What does adaptive thinking buy?  
A: It buys accuracy on explicit reasoning tasks, at a steep latency cost. [reports/adaptive_validation_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_validation_summary.json) shows a six-dataset validation jump from 73.32 percent to 83.35 percent. [reports/adaptive_latency_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_latency_summary.json) shows why this is not free: median estimated latency over Knowledge & Reasoning is seconds, not milliseconds.

Q: Can it drive UI and robot loops?  
A: The demos suggest it can be useful, but the limits are visible. [reports/demos/cu_results.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/demos/cu_results.json) reports 95 percent success on 60 browser tasks when numbered marks include text, but only 15 percent with marks alone. [reports/demos/arm_servo.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/demos/arm_servo.json) reports 40 percent robot-arm success and 45 percent grasped.

Q: What would I validate before using it?  
A: Validate calibration on the exact action set. The release already warns in [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md) that System 1 can be confidently wrong, and [calibration.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration.json) was fit on a particular data mix. Any automatic-action product needs its own holdout set and confidence thresholds.

## What is smart

The cleanest idea is returning calibrated probabilities over typed decisions. That changes the integration contract. A downstream system can require 0.95 confidence, abstain, ask a human, switch to System 2, or compare alternative policies without parsing prose.

The adaptive design is pragmatic. [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) does not ask the model to think on every request. It lets System 1 handle high-confidence cases and spends reasoning tokens only when the top option is uncertain.

The slot design is legible. [judge_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/judge_config.json) is small enough to understand at a glance. A builder can see exactly which outputs exist, where they live, and how temperatures apply.

The release is candid about reports and limitations. [reports/adaptive_other_areas_sample.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_other_areas_sample.json) shows that adaptive thinking barely helps ToolRet and hurts BANKING77. [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md) discloses that some public training splits overlap with benchmark families' test suites, while saying test splits were excluded.

## What is flawed or weak

The headline Decision Index score is self-computed, not a board result. The card in [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md) says the score uses adaptive thinking for Knowledge & Reasoning and System 1 for the other areas. That is a reasonable experiment, but not the same thing as an independently posted benchmark entry.

The latency envelope is not broad-production friendly for adaptive mode. [reports/adaptive_latency_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_latency_summary.json) makes clear that hard reasoning often uses the full 8,192-token budget. The model card also says adaptive mode does not meet the Decision Index latency limit on those Knowledge & Reasoning benchmarks.

The serving stack is specialized. [serve.sh](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve.sh) needs a vLLM development build with Gemma-4 support and [patches/vllm-gemma4-lm-head-lora.patch](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/patches/vllm-gemma4-lm-head-lora.patch). That is not a drop-in deployment for a conservative infra team.

The demos need careful reading. [README.md](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/README.md) emphasizes fast computer-use decisions, while [reports/demos/cu_results.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/demos/cu_results.json) shows much slower end-to-end medians in the trace file and a huge dependence on element text. That does not invalidate the demo, but it says the "model step" and "UI loop step" are different products.

## What we can learn / steal

Steal the decision endpoint pattern. [serve_decide.py](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/serve_decide.py) is a good sketch for any product that needs an LLM to pick among known actions: define a request schema, return probabilities, expose debug distributions, and make escalation explicit.

Steal the calibration packaging. [calibration.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration.json), [calibration_gold.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration_gold.json), and [judge_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/judge_config.json) make confidence behavior inspectable instead of folklore.

Steal the "fast first, think only when needed" architecture. [reports/adaptive_validation_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_validation_summary.json) and [reports/adaptive_latency_summary.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports/adaptive_latency_summary.json) together show how to reason about the accuracy/latency trade rather than pretending one setting fits all tasks.

Steal the raw report habit. The demos and benchmark reports under [reports](https://huggingface.co/autotrust/GEV-26B-Decide/tree/7c89590ead085bf77630b4bf68264ea30b6ddc78/reports) make it possible to inspect failures, not just screenshots and percentages.

## How we could apply it

For tool selection, browser control, support routing, and policy checks, I would expose an internal `/decide` style API rather than asking a chat model to explain itself first. The response should include the option list, probability distribution, selected option, calibration profile, threshold decision, and whether escalation was used.

For agent control loops, I would keep System 1 behavior separate from reasoning behavior. UI clicks, router choices, and quick yes/no gates should be measured for sub-second operation. Hard reasoning should be a deliberate fallback with latency shown to the caller.

For any model we ship with confidence values, I would include files like [judge_config.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/judge_config.json), [calibration.json](https://huggingface.co/autotrust/GEV-26B-Decide/blob/7c89590ead085bf77630b4bf68264ea30b6ddc78/calibration.json), and report summaries beside the weights. Confidence without calibration metadata is decoration.

## Bottom line

GEV-26B-Decide is interesting because it turns a generative backbone into a typed decision substrate. The best reusable idea is the contract: fixed decision kinds, probabilities over caller-supplied options, calibrated confidence, and adaptive escalation when uncertainty justifies slower reasoning. The weak point is deployment and evaluation risk, but the artifact gives enough files and reports for a builder to judge that risk instead of trusting the headline.
