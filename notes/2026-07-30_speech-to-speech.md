# Speech To Speech

- Repo: `huggingface/speech-to-speech`
- URL: https://github.com/huggingface/speech-to-speech
- Date: 2026-07-30
- Repo snapshot studied: `main` @ `e927901542db1618e08579442f5c759fed333ff6`
- Why picked today: It was the top repo on GitHub's trending page when checked, showing 8,487 stars, 1,058 forks, and 627 stars today there. The current repo API was already up to 8,491 stars and 1,060 forks. More importantly, it is one of the clearest open attempts to package a real-time voice agent as a protocol-compatible systems stack instead of a single fixed demo.

## Executive summary
`speech-to-speech` is not just "VAD -> STT -> LLM -> TTS" as a README slogan. The real product is a control plane around that pipeline: a large CLI/orchestration entrypoint in [`src/speech_to_speech/s2s_pipeline.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/s2s_pipeline.py), an OpenAI Realtime-compatible session layer in [`src/speech_to_speech/api/openai_realtime`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime), transport adapters in [`src/speech_to_speech/connections`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/connections), and backend modules for VAD, STT, LLM, and TTS.

The most interesting system idea is not the component list. It is the speculative-turn machinery in [`pipeline/speculative_turns.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/pipeline/speculative_turns.py), [`VAD/vad_handler.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/VAD/vad_handler.py), [`api/openai_realtime/service.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime/service.py), and [`LLM/lm_output_processor.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/LLM/lm_output_processor.py). The repo explicitly tracks turn revisions so reopened speech segments can invalidate stale transcriptions, text deltas, token usage, and TTS output before they leak to the client. That is a real systems answer to barge-in and interruption, not a prompt-level hack.

The second strong move is protocol decoupling. The client-facing edge speaks OpenAI Realtime, while the inside stays modular and mostly open-source-model-first. [`responses_api_language_model.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/LLM/responses_api_language_model.py) lets the LLM slot talk to any OpenAI-compatible `/v1/responses` server, and [`pyproject.toml`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/pyproject.toml) exposes extras for alternative STT/TTS paths rather than freezing the stack to one provider.

## What they built
They built a Python package and server for low-latency voice agents with several operating surfaces:

- [`src/speech_to_speech/s2s_pipeline.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/s2s_pipeline.py) is the giant orchestration entrypoint and CLI.
- [`src/speech_to_speech/api/openai_realtime`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime) turns the pipeline into an OpenAI Realtime-compatible service.
- [`src/speech_to_speech/VAD`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/VAD), [`STT`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/STT), [`LLM`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/LLM), and [`TTS`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech) provide interchangeable model backends.
- [`src/speech_to_speech/connections`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/connections) exposes local, socket, and WebSocket edge adapters.
- [`demo/server.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/demo/server.py) adds a Space-style front-end proxy with search, session brokering, and rate limiting.

## Why it matters
This repo matters because voice-agent demos usually hide the hard part inside a managed black box. This repo does the opposite.

1. It keeps the wire protocol stable while making the internals swappable.
2. It treats interruption and reopened speech as first-class concurrency problems.
3. It packages production-ish concerns like session draining, queue cleanup, platform-specific backend selection, and a deployable demo server alongside the core pipeline.

## Repo shape at a glance
The repository shape is wide, but not random:

- [`src/speech_to_speech`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech): the real package root.
- [`src/speech_to_speech/api/openai_realtime`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime): session state, service logic, response handlers, transports, and protocol mapping.
- [`src/speech_to_speech/pipeline`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/pipeline): queue item types, control messages, logging context, and speculative turn tracking.
- [`src/speech_to_speech/VAD`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/VAD), [`STT`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/STT), [`LLM`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/LLM), [`TTS`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech): backend families.
- [`demo`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/demo): browser UI plus FastAPI proxy/server glue.
- [`tests`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/tests): lifecycle, backend, and protocol behavior checks.
- [`archive`](https://github.com/huggingface/speech-to-speech/tree/e927901542db1618e08579442f5c759fed333ff6/archive): deprecated implementations kept out of the active CLI surface.

## Layered architecture dissection
### High-level system shape
The live path is: transport receives microphone audio -> VAD chunks it into turns with turn metadata -> STT emits partial/final transcripts -> the realtime service appends transcript state to chat and queues a generation request -> the LLM emits text/tool chunks -> the LM output processor mirrors those chunks to the text side-channel and forwards speakable text into TTS -> transport streams audio back out.

The hidden but crucial side path is control-state propagation. `SESSION_END`, queue drains, speculative turn revisions, and stale-event suppression are carried across the same pipeline so a reopened or disconnected session cannot keep talking after it is obsolete.

### Main layers
**1. Orchestration and packaging layer**  
[`pyproject.toml`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/pyproject.toml) defines the install surface, optional extras, and the `speech-to-speech` CLI entrypoint into [`s2s_pipeline.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/s2s_pipeline.py). That file pre-parses the chosen LLM backend, wires argument dataclasses, and builds the handler chain.

**2. Realtime protocol and session layer**  
[`api/openai_realtime/pipeline_unit.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime/pipeline_unit.py) is the cleanest "one unit of work" abstraction in the repo: one pipeline owns its queues, events, handlers, and per-session state. [`api/openai_realtime/service.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime/service.py) bridges STT and LM, appends chat items, and filters stale turn output before it becomes protocol events. [`api/openai_realtime/handlers/response.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime/handlers/response.py) only commits assistant text after the reopen-grace check succeeds.

**3. Pipeline control layer**  
[`pipeline/speculative_turns.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/pipeline/speculative_turns.py) is the control jewel. It tracks latest revisions, pending reopen candidates, grace windows, and commit state. [`pipeline/control.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/pipeline/control.py) defines the queue-borne control messages that let transports and handlers coordinate resets.

**4. Model backend layer**  
[`STT/parakeet_tdt_handler.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/STT/parakeet_tdt_handler.py) shows the repo's style: one semantic backend with platform-specific implementations underneath. [`LLM/responses_api_language_model.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/LLM/responses_api_language_model.py) translates chat state into OpenAI-compatible responses requests. [`TTS/qwen3_tts_handler.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/TTS/qwen3_tts_handler.py) does the same for Qwen3-TTS, with GGML or MLX paths depending on platform.

### Request / data / control flow
1. A client sends PCM frames through [`connections/websocket_streamer.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/connections/websocket_streamer.py), which rechunks bytes into 512-sample blocks and drains stale edge queues when a new first client arrives.
2. [`VAD/vad_handler.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/VAD/vad_handler.py) decides whether new speech should reopen the current turn or allocate a fresh one, using speculative-turn state.
3. [`STT/parakeet_tdt_handler.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/STT/parakeet_tdt_handler.py) transcribes audio and can emit live partials through its progressive streaming helper.
4. [`api/openai_realtime/service.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime/service.py) converts the final transcript into chat state and pushes a generation request into `text_prompt_queue`.
5. [`LLM/responses_api_language_model.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/LLM/responses_api_language_model.py) streams text deltas, assistant messages, and tool calls back.
6. [`LLM/lm_output_processor.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/LLM/lm_output_processor.py) duplicates the LLM output into two lanes: protocol/text events for the client and TTS inputs for speech synthesis.
7. [`TTS/qwen3_tts_handler.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/TTS/qwen3_tts_handler.py) synthesizes audio and commits the turn once it is still current after reopen grace.
8. [`connections/websocket_streamer.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/connections/websocket_streamer.py) buffers outgoing audio, re-enables listening after `AUDIO_RESPONSE_DONE`, and swallows `SESSION_END` cleanly.

## Key directories and files
- [`pyproject.toml`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/pyproject.toml): install surface, extras, and CLI entrypoint.
- [`src/speech_to_speech/s2s_pipeline.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/s2s_pipeline.py): top-level assembly and backend selection.
- [`src/speech_to_speech/pipeline/speculative_turns.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/pipeline/speculative_turns.py): revision and reopen state machine.
- [`src/speech_to_speech/VAD/vad_handler.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/VAD/vad_handler.py): turn opening, reopen, and audio segmentation logic.
- [`src/speech_to_speech/api/openai_realtime/service.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime/service.py): STT-to-LM bridge and stale-event filtering.
- [`src/speech_to_speech/api/openai_realtime/handlers/response.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime/handlers/response.py): response commit and event emission.
- [`src/speech_to_speech/LLM/lm_output_processor.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/LLM/lm_output_processor.py): side-channel split between text events and TTS.
- [`src/speech_to_speech/connections/websocket_streamer.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/connections/websocket_streamer.py): byte-level transport behavior.
- [`demo/server.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/demo/server.py): Space/deploy proxy with search, queue, and session brokering.

## Important components
The most important component is [`SpeculativeTurnTracker`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/pipeline/speculative_turns.py). This is where the repo becomes more than a modular tutorial. The tracker keeps the latest turn revision, handles pending reopen candidates, and decides when output is still legally attached to the live user turn.

The second is [`VADHandler`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/VAD/vad_handler.py). The VAD is not just endpoint detection. It is where reopened turns are minted and confirmed.

The third is [`RealtimeService`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime/service.py). It acts like the stateful bridge between transcript land, chat state, and protocol event land.

The fourth is [`LMOutputProcessor`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/LLM/lm_output_processor.py). It is easy to underrate, but that split between speakable text and protocol/tool output is what keeps one LLM stream usable for both audio playback and client-side UI.

## Important knobs / configs / extension points
- Backend choice lives in the CLI/dataclass surface wired by [`s2s_pipeline.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/s2s_pipeline.py): `--stt`, `--llm_backend`, `--tts`, and many backend-specific argument classes.
- Packaging extension points live in [`pyproject.toml`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/pyproject.toml): extras such as `faster-whisper`, `paraformer`, `pocket`, `kokoro`, `webrtc`, and `whisper-mlx`.
- LLM portability depends on [`responses_api_language_model.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/LLM/responses_api_language_model.py), which accepts any OpenAI-compatible `/v1/responses` endpoint rather than one vendor.
- Qwen3-TTS has real runtime knobs in [`qwen3_tts_handler.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/TTS/qwen3_tts_handler.py): backend choice, quantization suffix, speaker, reference audio, language normalization, and streaming chunk size.
- Session lifecycle isolation is explicit in [`pipeline_unit.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime/pipeline_unit.py), especially the `drained` session marker.

## Practical questions and answers
**Is this mostly a thin wrapper around OpenAI voice APIs?**  
No. The protocol edge is OpenAI-compatible, but the STT and TTS defaults are local open models and the LLM slot can target any OpenAI-compatible server.

**Where should a builder start reading?**  
Start with [`s2s_pipeline.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/s2s_pipeline.py), then [`pipeline/speculative_turns.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/pipeline/speculative_turns.py), [`VAD/vad_handler.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/VAD/vad_handler.py), [`api/openai_realtime/service.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime/service.py), and [`LLM/lm_output_processor.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/LLM/lm_output_processor.py).

**What is the most reusable engineering move here?**  
Revision-tag every turn-like artifact and make every downstream stage prove that its output still belongs to the latest revision before speaking or emitting it.

**Is the transport layer serious enough to study?**  
Yes. [`connections/websocket_streamer.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/connections/websocket_streamer.py) does boring but necessary work: chunk normalization, queue draining between sessions, and synchronized re-listening.

## What is smart
- Making the outside protocol standard while keeping the inside swappable.
- Treating reopened speech as a real concurrency/control problem with turn revisions.
- Splitting LLM output into a text event lane and a TTS lane.
- Packaging platform-specific backend differences behind one semantic interface.
- Isolating per-client ephemeral state in [`PipelineUnit`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/api/openai_realtime/pipeline_unit.py) so stale session fields do not outlive the connection.

## What is flawed or weak
- [`s2s_pipeline.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/s2s_pipeline.py) is doing too much. It is orchestrator, CLI parser, backend factory, runtime defaults holder, and environment setup script in one place.
- The repo downloads NLTK resources at import time in [`s2s_pipeline.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/src/speech_to_speech/s2s_pipeline.py). That is convenient for demos and slightly ugly for deterministic production startup.
- The control path is powerful but complicated. Shared queues carrying both payloads and control messages make debugging race conditions harder than a more explicit async state machine would.
- [`demo/server.py`](https://github.com/huggingface/speech-to-speech/blob/e927901542db1618e08579442f5c759fed333ff6/demo/server.py) is pragmatic, but it mixes search proxying, load-balancer brokering, auth, limiter logic, and static serving in one file.

## What we can learn / steal
- Put protocol compatibility at the edge, not in the core.
- Use turn revisioning plus grace windows to tame interruption races.
- Keep text/tool and audio output as separate lanes even when they come from one model stream.
- Expose backend choice through packaging and argument surfaces, not branches hidden in app code.

## How we could apply it
If we built our own voice agent stack, I would copy the turn-revision contract almost verbatim. I would also copy the idea of a protocol adapter at the edge and open model backends inside. I would not copy the gigantic top-level orchestrator file as-is; I would split it into a small bootloader plus clearer backend registries.

## Bottom line
`huggingface/speech-to-speech` is worth studying because it shows what happens when a voice-agent repo stops being a toy and starts caring about session lifecycle, interruption, protocol compatibility, and backend portability.

The builder lesson is that the clever part of real-time voice systems is often not the model choice. It is the turn bookkeeping that decides whether the right words and the right audio are still allowed to exist.
