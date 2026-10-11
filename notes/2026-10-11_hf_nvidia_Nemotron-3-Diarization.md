# Nemotron 3 Diarization

- Source: Hugging Face
- Artifact: model nvidia/Nemotron-3-Diarization
- URL: https://huggingface.co/nvidia/Nemotron-3-Diarization
- Date: 2026-10-11
- Snapshot studied: revision f667ed73aee57d40cc39428eb768b4fd87a0a29e, last modified 2026-09-24
- Why picked today: It was still visible in Hugging Face trending and is unusually source-rich for a model card: weights, NeMo and GGUF artifacts, Transformers config, processor config, ASR integration guide, evaluation protocol, safety/privacy/bias cards, and concrete streaming settings.

## Executive summary

[nvidia/Nemotron-3-Diarization](https://huggingface.co/nvidia/Nemotron-3-Diarization/tree/f667ed73aee57d40cc39428eb768b4fd87a0a29e) is a 100M-parameter speaker diarization model: it answers "who spoke when" from mono 16 kHz audio. The model supports offline inference and streaming inference, with up to eight speakers and speaker channels ordered by first arrival in the audio.

The useful builder angle is the artifact's operational detail. The [README.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/README.md) explains the Sortformer-style architecture, streaming speaker cache, FIFO context, latency presets, NeMo usage, Transformers usage, and ASR pairing. [config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/config.json) exposes the actual model geometry: 31 Transformer layers, 512 hidden size, 8 attention heads, 128 mel bins, subsampling factor 8, eight speaker heads, and specific streaming cache thresholds. [processor_config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/processor_config.json) exposes the audio frontend and named streaming modes.

This is a good model-card study because it treats deployment as part of the artifact. The repository includes a NeMo checkpoint, a Transformers safetensors model, a quantized GGUF file, and documentation for diarization alone and speaker-attributed ASR.

## What they built / released

NVIDIA released a general-access diarization checkpoint that can output per-speaker activity probabilities at 10 ms resolution. The core model files are [model.safetensors](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/model.safetensors), [Nemotron-3-Diarization.nemo](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/Nemotron-3-Diarization.nemo), and [Nemotron-3-Diarization.q8_0.gguf](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/Nemotron-3-Diarization.q8_0.gguf). The presence of all three matters: NeMo users, Transformers users, and local/native runtime users get different entry points.

The model predicts a `[T, 8]` activity tensor, where `T` is the number of output frames and the second dimension is the maximum eight speaker channels. The [README](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/README.md) says the speaker channels are ordered by arrival time, following Sortformer. That is a practical convention: a system can label "speaker 0" as the first speaker heard without solving arbitrary output permutation after every chunk.

The artifact also includes deployment docs. [ASR_INTEGRATION_GUIDE.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/ASR_INTEGRATION_GUIDE.md) shows how to pair diarization with NVIDIA streaming ASR models to produce "who said what." [diarization_evaluation.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/diarization_evaluation.md) describes how to score DER, speaker count accuracy, and speaker count error.

## Why it matters

Diarization is easy to demo and hard to deploy. A production system needs stable speaker identities across chunks, overlap handling, streaming latency choices, ASR alignment, evaluation protocol clarity, and privacy posture. This artifact exposes those concerns instead of hiding them behind a single "works on meetings" claim.

The model is also interesting because it bridges model research and systems work. The [README](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/README.md) describes a 31-layer Transformer encoder plus a Conv1D upsampler, but the operational levers live in cache and chunk geometry: speaker cache length, FIFO length, chunk length, right context, and update period.

## Artifact shape at a glance

- [README.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/README.md): model card, usage, streaming presets, Transformers examples, architecture, datasets, evaluation discussion, and limitations.
- [config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/config.json): Transformers model configuration, model dimensions, default offline chunking, head config, and streaming threshold/cache settings.
- [processor_config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/processor_config.json): feature extractor settings, sampling rate, FFT/mel parameters, streaming modes, and processor class.
- [model.safetensors](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/model.safetensors): Transformers-compatible weights.
- [Nemotron-3-Diarization.nemo](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/Nemotron-3-Diarization.nemo): NeMo checkpoint for NVIDIA NeMo Speech workflows.
- [Nemotron-3-Diarization.q8_0.gguf](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/Nemotron-3-Diarization.q8_0.gguf): quantized artifact for local/native use paths.
- [ASR_INTEGRATION_GUIDE.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/ASR_INTEGRATION_GUIDE.md): speaker-attributed ASR recipe with concrete NeMo Speech commands and service-loop guidance.
- [diarization_evaluation.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/diarization_evaluation.md): evaluation command, manifest format, DER metric definition, reporting protocol, and scoring caveats.
- [safety.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/safety.md), [privacy.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/privacy.md), [bias.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/bias.md), and [explainability.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/explainability.md): governance subcards that make deployment assumptions explicit.

## Layered architecture dissection

### High-level system shape

The artifact has three system layers.

The audio frontend layer is the processor. [processor_config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/processor_config.json) specifies `NemotronAsrStreamingFeatureExtractor` at 16 kHz, 128 mel features, 160-sample hop length, 512-point FFT, 400-sample window, preemphasis 0.97, right padding, and attention masks. The model card says those 10 ms mel frames are downsampled by eight, giving an 80 ms encoder frame rate.

The model layer is the diarization network. [config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/config.json) names `Nemotron3DiarizationForAudioFrameClassification`, with audio hidden size 512, 31 hidden layers, 8 attention heads, 2048 intermediate size, RoPE, 128 mel bins, and a head configured for eight speakers.

The streaming/session layer is speaker-cache management. [README.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/README.md) describes the Arrival-Order Speaker Cache and FIFO queue. [config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/config.json) gives the streaming defaults: FIFO length 264, speaker cache length 264, update period 222, prediction score threshold 0.25, and several score-boost settings.

### Main layers

For offline-style inference, the default geometry in [config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/config.json) is `chunk_length=340`, `chunk_right_context=40`, `fifo_length=40`, and `speaker_cache_update_period=300`. Since frames are 80 ms at the encoder, the README calls that a 30.4 s input buffer.

For streaming inference, [processor_config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/processor_config.json) defines named modes: `low_latency` as `[9, 4]`, `very_low_latency` as `[6, 2]`, and `ultra_low_latency` as `[3, 1]`. The README translates these into roughly 1.04 s, 0.64 s, and 0.32 s input-buffer latency.

For ASR integration, [ASR_INTEGRATION_GUIDE.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/ASR_INTEGRATION_GUIDE.md) makes the diarizer one component in a coupled streaming pipeline. The diarizer emits frame-level speaker activity. The ASR layer maintains a transcription stream per detected speaker. Settings such as `parallel_speaker_strategy`, `cache_gating`, `binary_diar_preds`, `fifo_len`, and `spkcache_update_period` become pipeline controls, not just model hyperparameters.

### Inference / data / control flow

For offline Transformers use, [README.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/README.md) loads `AutoProcessor` and `AutoModelForAudioFrameClassification`, resamples audio to the processor's sampling rate, runs one forward pass, and calls `processor.extract_speaker_dict` on logits and the attention mask.

For streaming Transformers use, the processor chunks incoming audio, includes lookahead frames that are attended to but not scored, and passes `speaker_cache` from one model call to the next. The last chunk is marked with `is_last_audio_chunk=True` so no lookahead is held back. The outputs are concatenated along time and then converted to segments.

For NeMo Speech ASR integration, [ASR_INTEGRATION_GUIDE.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/ASR_INTEGRATION_GUIDE.md) describes a persistent service shape: load ASR and diarization checkpoints once per worker, create a session per live client, buffer/resample incoming PCM chunks, process each complete frame, and return the latest speaker-attributed transcript.

## Key files, configs, cards, and artifacts

- [config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/config.json): the most compact source of model dimensions and streaming thresholds.
- [processor_config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/processor_config.json): audio frontend and latency-mode definitions.
- [README.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/README.md): model card and practical code paths for NeMo and Transformers.
- [ASR_INTEGRATION_GUIDE.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/ASR_INTEGRATION_GUIDE.md): best file for understanding deployment as a "who said what" streaming product.
- [diarization_evaluation.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/diarization_evaluation.md): best file for understanding reproducible evaluation.
- [model.safetensors](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/model.safetensors), [Nemotron-3-Diarization.nemo](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/Nemotron-3-Diarization.nemo), and [Nemotron-3-Diarization.q8_0.gguf](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/Nemotron-3-Diarization.q8_0.gguf): three runtime artifacts for different inference ecosystems.

## Important components

The output convention is one of the most important components. The model emits eight speaker channels ordered by speaker arrival. That converts a nasty permutation problem into a stable stream convention.

The streaming state is the second major component. The Arrival-Order Speaker Cache keeps speaker identity across chunks, while the FIFO queue gives the current chunk recent context. Without those pieces, low-latency diarization would tend to relabel speakers across chunks.

The processor is also a real component, not boilerplate. [processor_config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/processor_config.json) encodes audio normalization assumptions and named latency presets. Applications should not casually reimplement that logic.

## Important knobs / configs / extension points

- `chunk_length` and `chunk_right_context` in [config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/config.json) set the offline-style buffer geometry.
- `streaming_modes` in [processor_config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/processor_config.json) exposes the latency presets a product can name in UI or service config.
- `prediction_score_threshold`, `min_positive_scores_rate`, and boost rates in [config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/config.json) shape postprocessed speaker activity.
- `max_num_of_spks`, `parallel_speaker_strategy`, `masked_asr`, `cache_gating`, `att_context_size`, `fifo_len`, and `spkcache_update_period` in [ASR_INTEGRATION_GUIDE.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/ASR_INTEGRATION_GUIDE.md) are the main pipeline knobs for speaker-attributed transcription.
- `collar`, `ignore_overlap`, output resolution, streaming settings, precision, and hardware are required reporting fields in [diarization_evaluation.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/diarization_evaluation.md).

## Practical questions and answers

Q: Is this a transcription model?
A: No. It is a diarization model. It outputs speaker activity and timestamps, not words. To produce speaker-attributed transcripts, [ASR_INTEGRATION_GUIDE.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/ASR_INTEGRATION_GUIDE.md) pairs it with streaming ASR models.

Q: What is the lowest-latency path?
A: The card advertises an ultra-low-latency configuration with roughly 0.32 s input-buffer latency. [processor_config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/processor_config.json) shows that as `[3, 1]` chunks/right-context in 80 ms units.

Q: What should a production service preserve?
A: Preserve the processor and cache semantics. A service should carry `speaker_cache` across chunks, respect lookahead handling, resample to mono 16 kHz, and maintain a session per live client as described in [ASR_INTEGRATION_GUIDE.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/ASR_INTEGRATION_GUIDE.md).

Q: What should be reported with benchmark numbers?
A: Do not report DER alone. [diarization_evaluation.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/diarization_evaluation.md) says to include model revision, evaluation code, dataset, reference annotations, UEM, overlap handling, collar, post-processing, output resolution, streaming settings, precision, hardware, and batch size.

## What is smart

The artifact gives multiple runtime paths instead of forcing one ecosystem. [model.safetensors](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/model.safetensors), [Nemotron-3-Diarization.nemo](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/Nemotron-3-Diarization.nemo), and [Nemotron-3-Diarization.q8_0.gguf](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/Nemotron-3-Diarization.q8_0.gguf) broaden the deployment surface.

The model-card authors expose streaming geometry clearly. Builders can reason about latency, cache size, and context rather than guessing why a diarizer lags.

The evaluation doc is unusually careful about reference labels and protocol. That is exactly where diarization claims often get mushy.

## What is flawed or weak

The artifact is strongest for NVIDIA-oriented stacks. The README lists NVIDIA GPUs and Linux as the preferred path, and the richest integration path is through NeMo Speech.

The eight-speaker ceiling is clear and useful, but it is still a ceiling. Large meetings, broadcasts, or diarization over long multi-session archives need application-level segmentation, session reset, or speaker linking beyond the model output.

The card includes a lot of dataset and benchmark detail, but real product accuracy will depend heavily on microphone conditions, language mix, overlap, background noise, and whether the application needs real identities rather than anonymous speaker slots.

## What we can learn / steal

Steal the artifact shape. A serious model release should include weights, configs, processor settings, examples, integration recipes, evaluation protocol, and governance cards in one repository.

Steal the way streaming presets are named and documented. Users should choose "low latency" or "ultra low latency," while engineers can trace those labels back to concrete chunk and lookahead values in [processor_config.json](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/processor_config.json).

Steal the reporting discipline from [diarization_evaluation.md](https://huggingface.co/nvidia/Nemotron-3-Diarization/blob/f667ed73aee57d40cc39428eb768b4fd87a0a29e/diarization_evaluation.md). Metric values without protocol are not reusable knowledge.

## How we could apply it

For a meeting assistant, use this model as the diarization layer and keep the application session model explicit: one speaker cache per call, one ASR stream per active speaker, and a reset path when the call ends.

For local audio tooling, prefer the published processor and runtime artifacts over hand-rolled mel/chunk logic. The risk is not just wrong tensors; it is speaker identity drift across chunks.

For our own model-release notes, copy the structure: operational examples first, configs linked directly, evaluation caveats spelled out, and safety/privacy/bias files treated as part of the artifact rather than appendix paperwork.

## Bottom line

Nemotron 3 Diarization is valuable because it makes speaker diarization feel like a deployable system instead of a benchmark trick. The model itself is interesting, but the stronger lesson is the release packaging: concrete configs, cache/latency knobs, ASR integration guidance, reproducible evaluation rules, and multiple runtime artifacts.
