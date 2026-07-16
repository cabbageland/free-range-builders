# HF Realtime Voice

- Source: Hugging Face
- Artifact: space `smolagents/hf-realtime-voice`
- URL: https://huggingface.co/spaces/smolagents/hf-realtime-voice
- Date: 2026-07-16
- Snapshot studied: space `main` @ `1cfad643d1d9155e1418fd6d01bad4f73c927611`, last modified 2026-07-09T11:21:05Z
- Why picked today: It was one of the current trending Hugging Face Spaces when checked, and it is more instructive than the average voice demo because the code shows a complete product compromise: browser-side real-time audio and tool execution, but server-side secrets, queueing, and usage metering.

## Executive summary
`hf-realtime-voice` is a Docker Space that wraps a Hugging Face speech-to-speech backend with a real product shell rather than a toy static demo. The architecture is explicit in [`README.md`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/README.md): the browser owns microphone capture, WebSocket transport, tool execution, and playback, while [`server.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/server.py) keeps the load-balancer URL, Serper key, Hugging Face OAuth state, queueing, and usage metering server-side.

The best builder move is that the server stays out of the audio path. [`server.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/server.py) proxies `/api/session`, `/api/queue`, `/api/search`, and metering endpoints, but the actual media still flows browser -> per-session compute WebSocket -> browser. [`ws/s2s-ws-client.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/ws/s2s-ws-client.js) then owns the tricky bits the demo surface usually hides: queue wait / join semantics, one-response-at-a-time serialization, `session.update`, tool-call replies, heartbeat-based budget expiry, and audio state transitions.

The second smart move is that the app was deliberately converted from a static Space into a Docker app so it could keep secrets off the client. That rationale is recorded plainly in [`docs/adr/0001-docker-space-with-search-proxy.md`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/docs/adr/0001-docker-space-with-search-proxy.md). This is not glamorous, but it is the difference between a cool front-end and a deployable product.

The caution is that the app inherits the brittleness of a browser-owned media stack. Raw PCM over WebSocket is easier to debug than WebRTC, but less efficient. The limiter is clever, yet approximate by design, and the Space still depends on an external speech backend plus a load balancer that the repo does not fully own.

## What they built / released
They built a layered voice-agent Space with three major surfaces:

- A server shell in [`server.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/server.py) for search proxying, load-balancer session proxying, queue lifecycle, heartbeat metering, and static-file serving.
- A browser app in [`main.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/main.js), [`ui/chat.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/tree/main/ui), and [`index.html`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/index.html) that owns settings, camera, transcript UI, and tool execution.
- A real-time audio and transport layer in [`ws/s2s-ws-client.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/ws/s2s-ws-client.js), [`worklets/mic-capture.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/worklets/mic-capture.js), and [`worklets/audio-playback.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/worklets/audio-playback.js).

## Why it matters
This artifact matters because it shows how to turn a flashy real-time voice demo into something closer to a product.

1. It hides the dangerous secrets and stable infra addresses, but keeps the browser in direct control of the conversation transport.
2. It treats queueing and budget enforcement as explicit systems problems instead of pretending capacity is infinite.
3. It exposes the browser audio pipeline in readable worklet code instead of burying it inside a black-box SDK.

## Artifact shape at a glance
The Space is structurally clean:

- [`README.md`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/README.md) explains the WebSocket variant, backend expectations, limits, tools, and file roles.
- [`server.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/server.py), [`auth.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/auth.py), and [`limiter.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/limiter.py) form the server/infrastructure layer.
- [`main.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/main.js), [`ui/`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/tree/main/ui), and [`style.css`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/style.css) form the browser product shell.
- [`ws/`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/tree/main/ws) and [`worklets/`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/tree/main/worklets) form the actual audio and realtime transport layer.
- [`docs/adr/0001-docker-space-with-search-proxy.md`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/docs/adr/0001-docker-space-with-search-proxy.md) plus [`DESIGN.md`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/DESIGN.md) show that the repo cares about deploy shape and UI language, not only code.

## Layered architecture dissection
### High-level system shape
The runtime loop is simple but disciplined. The browser asks the Space for config via `/api/config`, then either connects directly to a pinned realtime URL or uses `/api/session` as a same-origin proxy to the load balancer in [`server.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/server.py). [`ws/s2s-ws-client.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/ws/s2s-ws-client.js) then opens the realtime WebSocket, sends `session.update`, streams microphone chunks, receives TTS chunks and transcripts, and fires tool-call events back into [`main.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/main.js).

### Main layers
**1. Secret-keeping / infra layer**  
[`server.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/server.py) is where the product boundary lives. It keeps `SERPER_API_KEY` and `LOAD_BALANCER_URL` off the client, proxies queue/session calls, and only enables metering when both `LOAD_BALANCER_URL` and `SPACE_ID` exist.

**2. Identity and budget layer**  
[`auth.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/auth.py) turns HF OAuth into usage identity, distinguishing `anon`, `free`, `org`, and `pro` tiers. [`limiter.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/limiter.py) then meters conversation time with chunked reservations in SQLite instead of trying to sit inline with the media stream.

**3. Realtime protocol layer**  
[`ws/s2s-ws-client.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/ws/s2s-ws-client.js) owns the OpenAI Realtime-style protocol, queue polling, join gating, response serialization, and tool-call handoff.

**4. Browser audio layer**  
[`worklets/mic-capture.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/worklets/mic-capture.js) resamples mic audio to 16 kHz PCM16 and applies a tunable noise gate. [`worklets/audio-playback.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/worklets/audio-playback.js) upsamples received audio back to the device sample rate with queue stats, fade-in/out, and underrun handling.

**5. Tool/UI layer**  
[`main.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/main.js) declares `web_search` and `camera_snapshot`, executes them in the browser, sends tool outputs back through the WebSocket client, and requests the next spoken response only after the tool result is attached.

### Inference / data / control flow
The most instructive end-to-end flow is the limited, queued LB path:

1. The client fetches deployment mode from [`/api/config`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/server.py).
2. On start, [`ws/s2s-ws-client.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/ws/s2s-ws-client.js) POSTs `/api/session`.
3. [`server.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/server.py) resolves the caller's tier through [`auth.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/auth.py), checks remaining budget via [`limiter.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/limiter.py), and either returns a queue ticket or a grant.
4. If queued, the browser polls `/api/queue/{id}` until it reaches the front, then waits for an explicit user join before spending the slot.
5. Once granted, the client acquires the mic, starts the worklets, opens the realtime WebSocket, and sends `session.update`.
6. The mic worklet posts PCM16 chunks, the server pushes audio deltas back, and the playback worklet drains them to speakers.
7. If the model emits `response.function_call_arguments.done`, [`main.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/main.js) runs the tool locally, sends `function_call_output`, and triggers `response.create` again, with image payloads deferred so the camera snapshot travels with the next response.
8. While the session lives, `/api/session/heartbeat` extends reserved time chunk by chunk; `/api/session/end` reconciles and refunds unused time.

## Key files, configs, cards, and artifacts
- [`README.md`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/README.md): the clearest source-level overview.
- [`server.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/server.py): secret proxy, queue lifecycle, metering hooks, and static serving.
- [`auth.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/auth.py): HF OAuth and identity resolution.
- [`limiter.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/limiter.py): chunked reservation and refund logic.
- [`main.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/main.js): state machine, tool execution, connection targeting, and restart flow.
- [`ws/s2s-ws-client.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/ws/s2s-ws-client.js): queue + realtime + tool-call control plane.
- [`worklets/mic-capture.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/worklets/mic-capture.js): capture/resample/noise-gate logic.
- [`worklets/audio-playback.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/worklets/audio-playback.js): playback queue and underrun behavior.
- [`docs/adr/0001-docker-space-with-search-proxy.md`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/docs/adr/0001-docker-space-with-search-proxy.md): the deploy-shape rationale.
- Linked backend route: [`speech_to_speech/api/openai_realtime/websocket_router.py`](https://github.com/huggingface/speech-to-speech/blob/feat/webrtc-transport/src/speech_to_speech/api/openai_realtime/websocket_router.py).

## Important components
**`server.py` is a boundary keeper, not an inference server**  
That is the right instinct. The server keeps secrets, queue state, and budget enforcement, but it does not unnecessarily proxy the audio.

**`ws/s2s-ws-client.js` is the real product engine**  
This file is where the app becomes serious: join windows, queue expiry, one-active-response serialization, toolcall events, and heartbeat awareness all live here.

**The audio worklets are pragmatic and readable**  
[`mic-capture.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/worklets/mic-capture.js) uses a cheap 48 -> 16 kHz fast path plus a fallback linear interpolator. [`audio-playback.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/worklets/audio-playback.js) keeps playback simple and observable instead of hiding it in a third-party media stack.

**The tool loop is intentionally non-magical**  
[`main.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/main.js) runs tools in the browser, sends outputs explicitly, and only then requests the follow-up response. That is easy to reason about and debug.

## Important knobs / configs / extension points
- `SERPER_API_KEY`, `LOAD_BALANCER_URL`, `SPEECH_TO_SPEECH_URL`, and `SPACE_ID` in [`server.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/server.py).
- `LIMIT_ANON_SEC`, `LIMIT_FREE_SEC`, `RESERVE_CHUNK_SEC`, `HEARTBEAT_SEC`, and `USAGE_HASH_SECRET` in [`limiter.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/limiter.py).
- `UNLIMITED_ORGS` and OAuth behavior in [`auth.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/auth.py).
- Tool declarations and local-storage-backed user settings in [`main.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/main.js).
- Noise-gate threshold and worklet behavior in [`worklets/mic-capture.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/worklets/mic-capture.js).

## Practical questions and answers
**Why not keep this as a static Space?**  
Because the search tool and LB address need secrets. The ADR in [`docs/adr/0001-docker-space-with-search-proxy.md`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/docs/adr/0001-docker-space-with-search-proxy.md) explains the conversion clearly.

**Why not proxy the audio through the FastAPI server too?**  
Because that would make the Space server an unnecessary bottleneck. This repo uses it for control traffic and policy, not media forwarding.

**What is the most reusable engineering here?**  
The chunked reservation limiter in [`limiter.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/limiter.py), the queue/join flow in [`ws/s2s-ws-client.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/ws/s2s-ws-client.js), and the split between server-side secrets and browser-side realtime transport.

**What should a builder read first?**  
Read [`README.md`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/README.md), then [`server.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/server.py), [`ws/s2s-ws-client.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/ws/s2s-ws-client.js), [`limiter.py`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/limiter.py), and [`main.js`](https://huggingface.co/spaces/smolagents/hf-realtime-voice/blob/main/main.js).

## What is smart
- Converting to Docker only when secret-holding became necessary, not before.
- Keeping audio off the Space server while still keeping the LB address secret.
- Metering with chunked reservations and refunds instead of pretending browser-close events are reliable.
- Serializing `response.create` so tool follow-ups do not collide with active responses.
- Deferring camera images to the exact response that should speak about them.

## What is flawed or weak
- Raw PCM over WebSocket is easier to reason about than WebRTC, but it is less network-efficient.
- The limiter is intentionally approximate; a crash can still forfeit up to one chunk.
- The architecture depends on a separate speech backend and LB path that this repo only partially represents.
- The browser now owns a lot of complexity: queue state, mic lifecycle, tool loop, playback buffering, and visual state all live client-side.

## What we can learn / steal
- Use the server for policy and secrets, not necessarily for the realtime media path.
- Queueing and budget limits should be explicit user-facing states, not hidden infra failures.
- Tool execution in voice apps gets more robust when the loop is explicit: call tool, send output, request new response.
- Small ADRs are worth writing when a deploy-shape change has architectural meaning.

## How we could apply it
If we were building our own realtime voice agent, I would copy this split:

1. browser-owned mic and playback,
2. same-origin control proxy for secrets and session grants,
3. explicit queue/join semantics,
4. chunk-based usage metering with reconciliation,
5. local tool execution with explicit response replay.

That gives you most of the product discipline without forcing a giant media backend into your app server.

## Bottom line
`hf-realtime-voice` is worth studying because it solves the unglamorous product problems that most realtime demos skip.

The builder lesson is that a good voice app is not just low latency. It is clean separation between secrets and media, explicit capacity handling, and a browser client that treats audio, tools, and usage policy as real state machines. This Space gets those tradeoffs mostly right.
