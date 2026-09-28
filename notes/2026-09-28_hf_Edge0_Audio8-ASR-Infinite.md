# Audio8 ASR Infinite

- Source: Hugging Face
- Artifact: model
- URL: https://huggingface.co/Edge0/Audio8-ASR-Infinite
- Date: 2026-09-28
- Snapshot studied: revision `7476824bc222e4ad509d286e8cae8b8d3f371129`, last modified `2026-09-24T03:39:57Z`
- Why picked today: It was a fresh, popular ASR artifact on the Hugging Face trending page with real custom source files, not just a weight upload. The useful angle is streaming ASR mechanics: frame clocks, delay conditioning, rolling cache claims, and semantic VAD heads.

## Executive summary

[Edge0/Audio8-ASR-Infinite](https://huggingface.co/Edge0/Audio8-ASR-Infinite/tree/7476824bc222e4ad509d286e8cae8b8d3f371129) is a bilingual Chinese/English streaming speech-recognition model built as a custom Transformers architecture. The artifact combines a Voxtral-style realtime audio encoder, a Qwen2.5-3B text decoder, a projector that groups acoustic frames into streaming token slots, explicit delay conditioning, optional frame-length conditioning, and separate semantic VAD heads.

The note to remember: this is not a normal Whisper-style batch ASR card. The model shape is designed around the operational problem of low-latency partial transcription: pick an audio clock, pick target delay, keep the audio/text state rolling, and avoid memory growth over long sessions.

## What they built / released

The HF repo ships:

- [README.md](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/README.md) with the release claim, operation points, evaluation table, and usage examples.
- [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json) defining a custom `audio8_asr_infinite` architecture, Voxtral realtime encoder config, Qwen2 text config, supported frame lengths, delay-token map, VAD horizons, and auto-map entries.
- [configuration_audio8_asr_infinite.py](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/configuration_audio8_asr_infinite.py) implementing config validation and delay/frame-length resolution.
- [modeling_audio8_asr_infinite.py](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py) implementing the custom model.
- [preprocessor_config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/preprocessor_config.json) specifying Voxtral realtime feature extraction at 16 kHz with 128 mel bins.
- [model.safetensors](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/model.safetensors), [model.safetensors.index.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/model.safetensors.index.json), and [semantic_vad_heads.safetensors](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/semantic_vad_heads.safetensors) for weights.
- [tokenizer.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/tokenizer.json), [tokenizer_config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/tokenizer_config.json), [chat_template.jinja](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/chat_template.jinja), [generation_config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/generation_config.json), and [Audio8-Asr-Infinite-Demo.mp4](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/Audio8-Asr-Infinite-Demo.mp4).

## Why it matters

Realtime ASR is mostly about managing delay, partial words, cache state, and end-of-turn decisions. This artifact exposes those concerns in the config and model code. [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json) declares supported audio clocks as frame lengths 4, 6, and 8 over a 20 ms audio tower frame, which correspond to 80, 120, and 160 ms streaming frames. It maps those to allowed delay tokens. [modeling_audio8_asr_infinite.py](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py) makes delay an explicit conditioning vector instead of leaving it as a hidden runtime convention.

That makes the artifact useful even before benchmarking it locally: it shows how a streaming ASR release can encode latency/accuracy tradeoffs as first-class model inputs.

## Artifact shape at a glance

The repo is small but dense:

- Model card and examples: [README.md](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/README.md).
- Architecture/config contract: [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json) and [configuration_audio8_asr_infinite.py](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/configuration_audio8_asr_infinite.py).
- Runtime implementation: [modeling_audio8_asr_infinite.py](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py).
- Preprocessing/tokenization: [preprocessor_config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/preprocessor_config.json), [tokenizer.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/tokenizer.json), [tokenizer_config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/tokenizer_config.json), and [chat_template.jinja](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/chat_template.jinja).
- Weights/artifacts: [model.safetensors](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/model.safetensors), [model.safetensors.index.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/model.safetensors.index.json), [semantic_vad_heads.safetensors](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/semantic_vad_heads.safetensors), and [Audio8-Asr-Infinite-Demo.mp4](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/Audio8-Asr-Infinite-Demo.mp4).

## Layered architecture dissection

### High-level system shape

The model is a multimodal causal generator. Audio features enter a Voxtral realtime audio tower. Consecutive audio frames are grouped according to selected `frame_len`. A projector maps those grouped audio features into Qwen hidden size. The Qwen decoder then predicts ASR tokens while receiving a delay-conditioning vector based on the chosen transcription delay.

The semantic VAD heads are parallel classifiers attached to the text backbone's final hidden state. They predict future semantic units at 0.5, 1.0, 2.0, and 3.0 second horizons, with class 0 treated as end-of-turn.

### Main layers

The audio layer is described in [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json): 32 audio layers, hidden size 1280, 128 mel bins, sliding window 750, and `streaming_n_left_pad_tokens` defaults. [preprocessor_config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/preprocessor_config.json) specifies 16 kHz audio, 400-sample FFT/window, 160-sample hop, 128 features, and right padding.

The projection layer is [Audio8ASRInfiniteMaxFrameLenProjector](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py), which flattens grouped audio frames at `max_frame_len * audio_hidden_size`, projects to Qwen hidden size, applies GELU, and projects again.

The decoder layer is Qwen2.5-ish per [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json): 36 text layers, hidden size 2048, 16 query heads, 2 KV heads, vocab size 151936, and tied embeddings. The implementation subclasses Qwen2/Qwen3 model classes in [modeling_audio8_asr_infinite.py](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py) so it can inject Voxtral-style delay modulation.

### Inference / data / control flow

The model enforces exactly one audio input form in [forward](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py): `input_features`, `source_input_features`, or `encoder_inputs_embeds`. Audio hidden states are grouped by [group_audio_hidden_states](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py), where rows with different frame lengths are partitioned, padded, flattened, and projected.

Delay is resolved by [build_t_cond](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py). It converts `num_delay_tokens` into sinusoidal delay embeddings and optionally adds a frame-length embedding. That `t_cond` is passed to modified Qwen decoder layers, which scale post-attention hidden states before the MLP.

The model card's 24/7 claim depends on the serving stack, not just the HF repo. [README.md](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/README.md) says the rolling KV cache lives in an adapted vLLM build and points to the external GitHub project. The HF artifact contains the model code and weights, but not the full docker/vLLM runtime described in the README.

## Key files, configs, cards, and artifacts

- [README.md](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/README.md): claims, operation points, architecture table, eval table, usage.
- [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json): the real contract for frame lengths, delay tokens, audio/text subconfigs, VAD horizons, and auto-map.
- [configuration_audio8_asr_infinite.py](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/configuration_audio8_asr_infinite.py): validation layer that rejects wrong model types and unsupported weight format versions.
- [modeling_audio8_asr_infinite.py](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py): the source worth studying.
- [preprocessor_config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/preprocessor_config.json): audio feature contract.
- [model.safetensors.index.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/model.safetensors.index.json): shows one 8.17 GB weight shard with audio tower, projector, and language-model weights.
- [semantic_vad_heads.safetensors](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/semantic_vad_heads.safetensors): separate future-semantic-unit classifiers.
- [generation_config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/generation_config.json): enables cache for generation while the model config itself defaults `use_cache` false.

## Important components

The cleanest component is [Audio8ASRInfiniteConfig](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/configuration_audio8_asr_infinite.py). It validates the model type, weight-format version, frame lengths, audio tower frame size, semantic VAD horizons, and delay divisibility. This is the right place for operational constraints, because serving systems can inspect it without loading 8 GB of weights.

The most interesting model component is [build_t_cond](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py). Delay is not a magic prompt string; it becomes a sinusoidal conditioning vector that each realtime decoder layer consumes.

The most practical component is [group_audio_hidden_states](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py). It handles mixed frame lengths in one batch by partitioning rows, padding temporal groups, flattening to a fixed projector width, and repacking into a shared padded sequence.

## Important knobs / configs / extension points

- `supported_frame_lens` in [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json): 4, 6, and 8 audio-tower frames, meaning 80, 120, and 160 ms clocks.
- `num_delay_tokens_by_frame_len` in [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json): maps target delays to token delays per clock.
- `streaming_n_left_pad_tokens_by_frame_len` in [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json): keeps left context aligned to frame length.
- `use_frame_len_embedding` in [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json): lets one model learn distinct behavior for different clocks.
- `semantic_vad_horizons_seconds` and `semantic_vad_num_classes` in [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json): defines the VAD auxiliary heads.
- `VoxtralRealtimeFeatureExtractor` settings in [preprocessor_config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/preprocessor_config.json): sample rate, FFT size, hop length, feature count, and log-mel limits.

## Practical questions and answers

Q: Can this be used with ordinary `AutoModelForCausalLM`?
A: Yes, but only with `trust_remote_code=True`, because [config.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/config.json) maps AutoConfig and AutoModelForCausalLM to local files. That is powerful and risky; audit [modeling_audio8_asr_infinite.py](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py) before loading.

Q: What languages are actually in scope?
A: The card and tokenizer helpers support Chinese and English only. [resolve_qwen_language_token_id](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py) rejects anything except `zh` or `en`.

Q: Is the 24/7 claim proven by the HF files alone?
A: No. The HF files expose architecture and weights. The rolling KV cache and vLLM runtime are described in [README.md](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/README.md), but the canonical docker/vLLM serving code is external.

Q: What is the biggest deployment cost?
A: Weight size and custom runtime. [model.safetensors.index.json](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/model.safetensors.index.json) reports 8.17 GB of model weights, plus semantic VAD heads and a serving path that wants bfloat16-capable GPU infrastructure.

## What is smart

The model treats latency as a training/runtime variable. Frame length, left padding, and delay tokens are config-level controls, not incidental server flags. That is the right mental model for realtime ASR.

The [from_pretrained](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py) override is also unusually strict: it forbids `ignore_mismatched_sizes` and raises on missing/unexpected/mismatched keys. For a custom realtime architecture, silent partial loads would be dangerous.

The semantic VAD design is clever because it reuses the same forward pass. [attach_semantic_vad_heads](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py) adds one classifier per future horizon over final hidden states; it does not require a separate acoustic VAD stack.

## What is flawed or weak

The artifact is preview-shaped. [README.md](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/README.md) has strong claims about unlimited 24/7 streaming, but the evidence in this HF repo is mostly config/model code, one demo video, and a card evaluation table. The complete serving implementation is linked externally.

The usage snippet imports package paths like `audio8_asr_infinite.streaming_inference`; those files are not present in the HF repo tree. That means the model artifact is not the whole developer experience. Builders need the external GitHub repo or their own streaming decode loop.

The language coverage is intentionally narrow. For English/Chinese realtime ASR this may be fine, but it should not be mistaken for a multilingual general ASR replacement.

## What we can learn / steal

Steal the latency-as-conditioning pattern. If a model must operate at several realtime points, encode the chosen point into the model interface and train against it.

Steal the strict config validation from [configuration_audio8_asr_infinite.py](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/configuration_audio8_asr_infinite.py). Realtime model formats drift quickly; failing closed is better than producing plausible broken transcripts.

Steal the separation between base transcription and semantic turn-taking. The VAD heads in [modeling_audio8_asr_infinite.py](https://huggingface.co/Edge0/Audio8-ASR-Infinite/blob/7476824bc222e4ad509d286e8cae8b8d3f371129/modeling_audio8_asr_infinite.py) hint at a better voice-agent architecture: the ASR pass can also produce end-of-turn intelligence on the same frame grid.

## How we could apply it

For our own realtime voice systems, expose clock and target delay as product knobs tied directly to model inputs. Do not hide them in buffer code. Then measure each operating point independently.

For local/offline assistant builds, the architecture suggests a path beyond "transcribe then detect silence": use ASR hidden states to predict semantic completion, stutter, and thinking pauses. Even a small auxiliary head can be more useful than pure acoustic silence thresholds.

## Bottom line

Audio8 ASR Infinite is a valuable streaming-ASR source study because its repo shows the mechanisms, not just a leaderboard claim: audio-frame grouping, explicit delay conditioning, strict custom config, and semantic VAD heads. The risk is that the most important production claim, long-running rolling-cache service, lives in the external runtime rather than being fully demonstrated inside this HF artifact.
