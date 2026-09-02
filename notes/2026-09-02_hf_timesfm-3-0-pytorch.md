# TimesFM 3.0 (PyTorch)

- Source: Hugging Face
- Artifact: model `google/timesfm-3.0-pytorch`
- URL: https://huggingface.co/google/timesfm-3.0-pytorch
- Date: 2026-09-02
- Snapshot studied: `main` @ `43046b85ec22d584a13f8098c2ed39c889e129c2` (last modified 2026-09-02T15:44:59Z), cross-checked against upstream implementation repo `google-research/timesfm` @ `45e0a3bc7fc4acef17b7ba7910488be2159bae5f`
- Why picked today: it appeared in the live Hugging Face trending models feed when checked, and the model API showed a same-day update plus 278 likes. More importantly, it is a useful builder artifact because the Hugging Face repo is intentionally thin while the upstream implementation is open, which makes the packaging boundary itself worth dissecting.

## Executive summary
[`google/timesfm-3.0-pytorch`](https://huggingface.co/google/timesfm-3.0-pytorch/tree/main) is not a giant self-contained model repo. The Hugging Face artifact is deliberately small: [`README.md`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/README.md), [`config.json`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/config.json), [`LICENSE`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE), and one big [`model.safetensors`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/model.safetensors). That sounds shallow, but the package is still useful because [`config.json`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/config.json) exposes the real forecasting contract: patch lengths 32 and 64, 20 transformer layers at width 1280, 16 heads, variate attention, linear detrending, stitching, and iterative CPM RevIN refinement.

The real mechanism lives upstream in [`google-research/timesfm`](https://github.com/google-research/timesfm/tree/45e0a3bc7fc4acef17b7ba7910488be2159bae5f). [`src/timesfm3/model.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/model.py) defines `TimesFM3Torch` as a `PyTorchModelHubMixin`-backed model that consumes the same config the Hub repo ships. [`src/timesfm3/timesfm3_forecaster.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/timesfm3_forecaster.py) handles query shaping, left padding, NaN interpolation, and batching. [`src/timesfm3/evaluator.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/evaluator.py) adds the benchmark-facing defaults and a hard 32-variate chunking strategy.

The strongest move is that Google did not hide the inference code behind the Hub card. The weak side is that the artifact boundary is a little too thin: you need the upstream repo to really understand behavior, and the weights are under a non-commercial license even though the source code is Apache-2.0.

## What they built / released
They released the official PyTorch checkpoint package for TimesFM 3.0 plus an open implementation repo that explains how to actually run it. The model card in [`README.md`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/README.md) positions it as a pretrained time-series foundation model for forecasting. The upstream repo expands that into real interfaces:

- [`src/timesfm3/model.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/model.py): the inference-only PyTorch model
- [`src/timesfm3/timesfm3_forecaster.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/timesfm3_forecaster.py): the high-level forecasting API
- [`src/timesfm3/evaluator.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/evaluator.py): benchmark-oriented evaluator wrapper
- [`src/timesfm3/transformer.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/transformer.py): the stacked mixing transformer blocks
- [`src/timesfm3/cpm_revin_refine.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/cpm_revin_refine.py): iterative refinement for CPM-masked patches

The result is a nicer-than-usual split between checkpoint packaging and implementation transparency.

## Why it matters
Most model releases for forecasting are bad builder artifacts in one of two ways: either they are all paper and no runnable package, or they are a checkpoint bucket with no clear inference contract.

TimesFM 3.0 matters because it lands in the middle:

1. The Hub package is small but explicit.
2. The config is rich enough to expose the core architectural bets.
3. The upstream repo gives you actual inference code, examples, and archived older versions.
4. The forecasting API is oriented around practical use cases like multivariate series and covariates, not just offline benchmark plots.

That makes it useful as both a model artifact and a packaging pattern.

## Artifact shape at a glance
The Hugging Face repo has an intentionally minimal "checkpoint plus contract" shape:

- [`README.md`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/README.md): card, architecture summary, training-data summary, and license pointer
- [`config.json`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/config.json): the real inference and architecture knobs
- [`LICENSE`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE): non-commercial weight terms
- [`model.safetensors`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/model.safetensors): monolithic checkpoint payload

The upstream implementation repo carries the structural detail the Hub package omits:

- [`src/timesfm3`](https://github.com/google-research/timesfm/tree/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3): current TimesFM 3.0 Python implementation
- [`timesfm-forecasting/examples`](https://github.com/google-research/timesfm/tree/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/timesfm-forecasting/examples): practical usage examples
- [`timesfm3-usage`](https://github.com/google-research/timesfm/tree/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/timesfm3-usage): demo notebooks and benchmark-oriented materials
- [`v1`](https://github.com/google-research/timesfm/tree/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/v1): archived older model code

That split is the main design fact to understand before touching the model.

## Layered architecture dissection
### High-level system shape
The high-level flow is: callers provide one or more target series plus optional covariates, the forecaster normalizes and pads them into fixed patch windows, the model mixes sequence and variate attention over those patches, the output head emits horizon patches across multiple quantiles, and optional refinement logic updates running stats for CPM-masked regions before returning the final forecast tensors.

### Main layers
**1. Hub packaging layer**  
[`README.md`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/README.md) and [`config.json`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/config.json) are the only pieces most users will see first. That means the config has to carry real explanatory weight, and it mostly does.

**2. Config layer**  
[`config.json`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/config.json) makes the architecture concrete: `input_patch_len: 32`, `output_patch_len: 64`, 9 quantiles, a 20-layer transformer stack, RMS-based norms, `max_variates: 32`, `use_variate_attention: true`, `use_linear_detrending: true`, `use_stitching: true`, and `use_iterative_cpm_revin: true`.

**3. Core model layer**  
[`src/timesfm3/model.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/model.py) shows the actual block ordering. A pre-transformer residual block ingests concatenated values and masks, [`transformer.StackedMixingTransformer`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/transformer.py) does the heavy mixing, and a linear output head projects into `output_patch_len * num_quantiles`.

**4. Forecasting API layer**  
[`src/timesfm3/timesfm3_forecaster.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/timesfm3_forecaster.py) is where the builder-facing surface gets real. It defines `ModelConfig`, caps context length at 15,360, interpolates NaNs, left-pads shorter series, truncates longer ones, and wraps outputs into a structured `ForecastOutput`.

**5. Evaluation and scaling layer**  
[`src/timesfm3/evaluator.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/evaluator.py) is an unusually useful file. It hardcodes benchmark-ish defaults like returning quantiles and symmetric averaging, but the more interesting part is the variate budget: if inputs exceed 32 total variates, it subsamples covariates and chunks target variates across forward passes.

**6. Refinement and example layer**  
[`src/timesfm3/cpm_revin_refine.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/cpm_revin_refine.py) shows how CPM-masked patches get iterative running-stat updates from model-estimated values. [`timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py) demonstrates the practical covariate story with a synthetic retail example rather than a vague "supports XReg" sentence.

### Inference / data / control flow
1. A caller constructs `ModelConfig` and provides target contexts and optional covariates through [`src/timesfm3/timesfm3_forecaster.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/timesfm3_forecaster.py).
2. The forecaster left-pads, truncates, interpolates, and masks inputs into fixed patch-ready arrays.
3. [`src/timesfm3/model.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/model.py) preprocesses with running stats, RevIN, future-covariate rolling, and a pre-transformer residual block.
4. [`src/timesfm3/transformer.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/transformer.py) applies the stacked mixing transformer with rotary embeddings, sequence attention, and variate-aware masking.
5. The output head emits horizon patches for all configured quantiles.
6. If CPM masking is active, [`src/timesfm3/cpm_revin_refine.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/cpm_revin_refine.py) refines running means and sigmas from estimated values.
7. [`src/timesfm3/evaluator.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/evaluator.py) optionally wraps this with multivariate chunking and benchmark defaults before yielding `ForecastOutput` objects.

## Key files, configs, cards, and artifacts
- [`README.md`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/README.md): Hub card and high-level architecture summary
- [`config.json`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/config.json): architecture and inference knobs
- [`LICENSE`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/LICENSE): non-commercial weight terms
- [`model.safetensors`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/model.safetensors): checkpoint payload
- [upstream `README.md`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/README.md): version map, install surface, and usage examples
- [`src/timesfm3/model.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/model.py): core model graph
- [`src/timesfm3/timesfm3_forecaster.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/timesfm3_forecaster.py): forecasting API and batching logic
- [`src/timesfm3/evaluator.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/evaluator.py): variate chunking and benchmark defaults
- [`src/timesfm3/transformer.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/transformer.py): attention stack internals
- [`src/timesfm3/cpm_revin_refine.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/cpm_revin_refine.py): iterative refinement logic
- [`timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py): concrete covariate usage path

## Important components
The most important component is [`config.json`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/config.json), because the Hub package is so small that this file becomes the real artifact contract.

The second is [`src/timesfm3/model.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/model.py), which turns the Hub config into an actual model graph and makes the patch-level design legible.

The third is [`src/timesfm3/timesfm3_forecaster.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/timesfm3_forecaster.py), because most real users do not want a raw decoder; they want a forecasting surface that handles context and covariate wrangling.

The fourth is [`src/timesfm3/evaluator.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/evaluator.py), because it exposes the practical variate-budget tradeoff rather than hiding it.

The fifth is [`src/timesfm3/cpm_revin_refine.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/cpm_revin_refine.py), which shows that the normalization story is an active part of prediction quality, not just an input prepass.

## Important knobs / configs / extension points
- [`config.json`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/config.json): `input_patch_len`, `output_patch_len`, `quantiles`, `use_variate_attention`, `use_stitching`, `use_linear_detrending`, `linear_detrending_threshold`, and `use_iterative_cpm_revin`
- [`src/timesfm3/configs.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/configs.py): framework-agnostic residual and transformer config types
- [`src/timesfm3/timesfm3_forecaster.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/timesfm3_forecaster.py): `per_core_batch_size`, `device`, `revision`, `cache_dir`, `local_files_only`, and context-length handling
- [`src/timesfm3/evaluator.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/evaluator.py): `univariate`, `return_quantiles`, `use_symmetric_averaging`, `make_positive`, and the 32-variate chunking path

## Practical questions and answers
**Is the Hugging Face repo self-contained enough to understand the model?**  
Only partly. The Hub repo tells you what the checkpoint is, but the upstream implementation repo is where you learn how inputs are formatted, batched, normalized, and decoded.

**Where does the multivariate and covariate story become concrete?**  
In the combination of [`config.json`](https://huggingface.co/google/timesfm-3.0-pytorch/blob/main/config.json), [`src/timesfm3/evaluator.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/evaluator.py), and the worked example in [`timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/timesfm-forecasting/examples/covariates-forecasting/demo_covariates.py).

**What is the sharpest implementation idea here?**  
Treating patch-level normalization as a first-class iterative inference step. [`src/timesfm3/cpm_revin_refine.py`](https://github.com/google-research/timesfm/blob/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3/cpm_revin_refine.py) is the file that makes that obvious.

**Where is the biggest practical limit?**  
The 32-variate budget visible in the config and evaluator. The model can still handle larger shapes through chunking, but that is a real implementation constraint, not infinite multivariate magic.

**What is the main operator caveat?**  
The license split. The code is open under Apache-2.0 upstream, but the 3.0 pretrained weights in the Hugging Face package are non-commercial and non-production by default.

## What is smart
- Keeping the Hub artifact small while still shipping enough config to expose the real architecture
- Backing the checkpoint with open upstream inference code instead of a closed serving stack
- Making multivariate and covariate support visible in examples and evaluator code, not just in a benchmark claim
- Exposing practical constraints like `max_variates: 32` instead of pretending the model is unlimited
- Preserving older versions in [`v1`](https://github.com/google-research/timesfm/tree/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/v1) while giving 3.0 its own modern code path in [`src/timesfm3`](https://github.com/google-research/timesfm/tree/45e0a3bc7fc4acef17b7ba7910488be2159bae5f/src/timesfm3)

## What is flawed or weak
- The Hugging Face artifact is so thin that a builder has to leave the Hub page to really understand it
- The monolithic checkpoint package does not ship richer evaluation artifacts, example notebooks, or data adapters alongside the weights
- The non-commercial license on the 3.0 weights sharply limits immediate production reuse
- The card explains the high-level architecture, but many of the most important behavioral details only become clear in upstream Python code

## What we can learn / steal
- A thin checkpoint repo can still be a good artifact if the config is explicit and the upstream implementation is easy to find
- Publish real forecasting examples, not only generic inference snippets
- Make scaling limits visible in code and config instead of hiding them behind marketing language
- Separate current-model code from archived legacy versions cleanly

## How we could apply it
If we shipped our own domain model, I would happily copy this split with one improvement: keep the Hub package minimal, but link the exact upstream implementation files even more aggressively from the card. TimesFM gets most of the way there. The remaining friction is discoverability, not capability.

## Bottom line
`google/timesfm-3.0-pytorch` is worth studying because it shows a credible checkpoint-packaging pattern: a small Hub artifact, a rich config, and an open upstream repo where the real mechanism lives.

The reusable builder lesson is that a model release does not need a giant Hub repo to be useful, but it does need an honest contract and an easy path to the actual implementation.
