# AnyPS5

- Repo: boykopovar/AnyPS5
- URL: https://github.com/boykopovar/AnyPS5
- Date: 2026-10-06
- Repo snapshot studied: main at 5895ea721a43f48547cc996aee0bb65b603622ac
- Why picked today: Daily GitHub trending surfaced it as a hot, fast-moving systems project. It is not AI, but it is unusually deep: a binary relinker, target-specific ELF/PE writers, AMD-to-Intel instruction lowering, shader recompilation, and many PRX compatibility libraries.

## Executive summary

[AnyPS5](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac) is a source-heavy compatibility project that tries to run console executables on Linux or Windows without a separate emulator process. The core idea in the [README](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/README.md) is direct relinking: convert the input executable to the host's native format, provide replacement system PRX libraries, and make the resulting app load against that compatibility layer.

The builder lesson is not "port a console." It is that compatibility systems become maintainable when they split binary transformation, platform stubs, runtime layout, graphics translation, and library surface area into explicit layers. AnyPS5 is rough, legally and operationally specialized, and far from a general consumer product, but the codebase has real engineering bones.

## What they built

They built a C++ toolchain for converting a clean input ELF plus its bundled modules into a Linux ELF or Windows PE output. The user-facing flow in [docs/user/USAGE.md](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/docs/user/USAGE.md) describes a source directory with an input ELF plus `sce_module`, `sce_modules`, or `prx`, then a `relinker` command that writes the target executable and converted guest modules.

Underneath that, [core/relinker](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker) parses and patches ELF metadata, builds replacement dynamic sections, filters unused NID references, optionally lowers AMD-only x86 instructions for Intel hosts, and emits either Linux ELF or Windows PE. The runtime side lives mostly under [core/libs/prx](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx), which contains many small library implementations standing in for system PRX modules.

## Why it matters

Most compatibility stacks are framed as emulation. AnyPS5 is interesting because it instead treats the executable as something to rewrite into a host-native binary and then satisfy through dynamic linking. That gives it different tradeoffs: less runtime indirection, but much more up-front binary surgery and a huge obligation to emulate system libraries accurately.

It also matters as a study in boundaries. The recent commit stream includes low-level kernel API work, but the repo keeps that in named PRX modules such as [core/libs/prx/libkernel](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx/libkernel), while the relinker stays focused on binary and symbol mechanics.

## Repo shape at a glance

- [core/relinker](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker): conversion CLI, ELF reader, relinking pipeline, dynamic-section builder, NID filtering, target patchers, AMD-only instruction conversion, and tests.
- [core/libs/prx](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx): host-side implementations of console PRX libraries, including graphics, kernel, libc, networking, audio, font, video, and web modules.
- [core/shader](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/shader): shader decoder, IR, optimization, resource tracking, and SPIR-V backend machinery.
- [core/Decoder](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/Decoder): media/image decoders with tests.
- [3rdparty](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/3rdparty): bundled dependencies such as SDL2, Vulkan headers, SPIRV-Tools, ffmpeg-core, freetype, jpeg-turbo, and shader tooling.
- [docs/user](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/docs/user) and [docs/dev](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/docs/dev): usage, compatibility, build instructions, conventions, and technical debt.
- [.github/workflows](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/.github/workflows): build, release, labeling, and progress-report automation.

## Layered architecture dissection

### High-level system shape

The system has three main strata. First, the relinker reads a guest executable, validates the supported dynamic-linking shape, rewrites references, and writes a host executable. Second, host-side PRX libraries provide symbols and behavior that the rewritten executable expects. Third, graphics and media subsystems translate console-facing APIs into host-facing APIs such as Vulkan, SDL, and SPIR-V.

The important boundary is that [core/relinker/main.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/main.cpp) does orchestration, not every detail. It parses CLI args, optionally runs instruction conversion, builds a `RelinkerPipeline`, writes registry files, builds guest artifacts, chooses the Linux or Windows patcher, writes output bytes, and prints the runtime layout.

### Main layers

The binary-analysis layer sits in [core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp). It reads program headers, dynamic tags, relocation tables, string tables, needed libraries, syscall presence, and NID references. It then validates relocation types, filters unused NID references, compacts the PLT in strict mode, builds a new dynamic section, and resolves call sites for a registry.

The target-output layer is split by platform. Linux output uses [core/relinker/elfpatcher/include/elfpatcher/linux/LinuxElfPatcher.hpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/elfpatcher/include/elfpatcher/linux/LinuxElfPatcher.hpp) and supporting general builders. Windows output uses the PE-oriented files in [core/relinker/elfpatcher/src/windows](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/elfpatcher/src/windows), including import, relocation, TLS, startup, icon-resource, and trampoline builders.

The CPU-compatibility layer is [core/relinker/codegen](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/codegen). [core/relinker/codegen/src/Amd64OnlyConverter.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/codegen/src/Amd64OnlyConverter.cpp) scans executable segments, matches AMD-only instructions, rewrites some in place, and emits trampoline sites when a longer lowering has to live out of line.

The library-compatibility layer is [core/libs/prx](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx). The most revealing example is [core/libs/prx/libkernel/DirectMemory/DirectMemory.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx/libkernel/DirectMemory/DirectMemory.cpp), which maps guest memory semantics onto Linux `mmap` and Windows virtual-memory behavior while preserving a guest arena abstraction.

The shader layer is [core/shader/recompiler/Recompiler.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/shader/recompiler/Recompiler.cpp). It decodes RDNA shader code, builds and structures a control-flow graph, translates to an IR, runs SSA/resource/dead-code passes, builds resource plans, emits SPIR-V, and memoizes results to avoid repeating expensive front-end work.

### Request / data / control flow

A typical conversion begins with [docs/user/USAGE.md](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/docs/user/USAGE.md): an input ELF sits beside bundled modules, and the operator chooses Linux or Windows output plus options such as `--to-intel`, `unused-filter`, `--registry`, or `--rpath`.

[core/relinker/main.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/main.cpp) reads the input bytes, optionally calls the AMD-only converter, constructs a `RelinkerPipeline`, applies returned byte patches, asks `GuestModuleBuilder` to convert bundled modules, and sends the rewritten executable bytes into either the Linux ELF patcher or the Windows PE patcher.

At runtime, the rewritten executable expects the output layout documented in [docs/user/USAGE.md](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/docs/user/USAGE.md): host executable, `libs/*.prx`, and `app0` resources plus converted guest modules. The host PRX implementations then become the compatibility contract.

## Key directories and files

- [README.md](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/README.md): concise statement of the direct-relinking model and project status.
- [docs/user/USAGE.md](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/docs/user/USAGE.md): conversion options, runtime layout, system-font expectations, and exit codes.
- [core/relinker/main.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/main.cpp): top-level orchestration path.
- [core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp): dynamic-linking analysis and patch plan construction.
- [core/relinker/codegen/src/Amd64OnlyConverter.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/codegen/src/Amd64OnlyConverter.cpp): Intel-host instruction lowering machinery.
- [core/relinker/elfpatcher/src/windows](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/elfpatcher/src/windows): PE writer, imports, relocations, TLS, startup, and trampoline builders.
- [core/libs/prx/libkernel](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx/libkernel): kernel API compatibility surface.
- [core/libs/prx/libkernel/DirectMemory/DirectMemory.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx/libkernel/DirectMemory/DirectMemory.cpp): guest direct-memory implementation across Linux and Windows.
- [core/shader/recompiler/Recompiler.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/shader/recompiler/Recompiler.cpp): shader front end, optimization pipeline, cache, and SPIR-V handoff.

## Important components

`RelinkerPipeline` is the heart of the converter. Its job is to turn "this ELF imports these opaque NID symbols" into a host-linkable dynamic section and a registry of what the executable will call. The careful part is not just finding symbols; it validates table bounds, string termination, relocation entry sizes, syscall absence, and unsupported relocation types before emitting output.

`Amd64OnlyConverter` is a pragmatic portability feature. [Amd64OnlyConverter.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/codegen/src/Amd64OnlyConverter.cpp) handles short instruction sites by gathering neighboring movable instructions until there is room for a jump, while rejecting sequences with branch targets or RIP-relative dependencies that cannot safely move.

`libkernel` is the compatibility pressure cooker. Files such as [DirectMemory.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx/libkernel/DirectMemory/DirectMemory.cpp) show the kind of detail every serious compatibility layer must absorb: page sizes, protection bits, fixed mappings, guest address-space ownership, Windows commit semantics, and tracing flags.

The shader recompiler is the other major subsystem. [Recompiler.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/shader/recompiler/Recompiler.cpp) exposes a classic compiler pipeline: decode, CFG, structurize, translate, SSA, fold, remove dead code, materialize resources, emit SPIR-V, and cache/memoize expensive intermediate work.

## Important knobs / configs / extension points

The operator-facing knobs are in [docs/user/USAGE.md](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/docs/user/USAGE.md): `--windows`, `--to-intel`, `unused-filter=0|1|2`, `--registry`, `--rpath`, `--autorun`, and a set of deprecated debugging flags. These knobs are not cosmetic; they select output format, CPU instruction compatibility, import pruning aggressiveness, and runtime library lookup.

For developers, the extension points are mostly module-shaped. New system behavior lands under [core/libs/prx](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx). New executable conversion behavior lands under [core/relinker](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker). New graphics/compiler behavior lands under [core/shader](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/shader).

There are also debug-oriented environment variables embedded in source. [Recompiler.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/shader/recompiler/Recompiler.cpp) checks flags such as `APS5_SINGLE_LANE` and `APS5_DUMP_IR`, while [DirectMemory.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx/libkernel/DirectMemory/DirectMemory.cpp) includes memory tracing through `APS5_TRACE_MEMORY`.

## Practical questions and answers

Q: Is this an emulator?  
A: Not in the usual separate-runtime sense. The [README](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/README.md) explicitly frames the approach as relinking to native host formats plus PRX implementations, not an emulator process.

Q: Where would a builder start reading?  
A: Start with [docs/user/USAGE.md](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/docs/user/USAGE.md), then [core/relinker/main.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/main.cpp), then [RelinkerPipeline.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp). That path reveals the product contract before the implementation depth.

Q: What looks production-hard here?  
A: The dynamic-linking validator is serious about failing closed. [RelinkerPipeline.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp) repeatedly rejects unsupported or inconsistent binary structures rather than trying to guess.

Q: What is the biggest correctness risk?  
A: The surface area. Every guest library function, shader behavior, memory-map edge case, and binary relocation corner can become an app-specific failure. The breadth of [core/libs/prx](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx) is evidence of the problem.

Q: Is the shader system a toy?  
A: No. [core/shader/recompiler/Recompiler.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/shader/recompiler/Recompiler.cpp) has a multi-pass compiler shape and explicit memoization of failures and results, which is what you expect in a real compatibility layer.

## What is smart

The smartest move is the hard separation between conversion and compatibility libraries. [core/relinker](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker) handles "make the binary load and call the right things." [core/libs/prx](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx) handles "make those things behave." That split keeps a giant problem somewhat navigable.

The Intel-conversion logic is also thoughtfully constrained. [Amd64OnlyConverter.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/codegen/src/Amd64OnlyConverter.cpp) does not pretend every instruction can be moved or expanded. It checks branch targets, RIP-relative dependencies, replacement lengths, and optional substitutions.

The shader pipeline shows another good habit: cache and memoize the expensive parts. [Recompiler.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/shader/recompiler/Recompiler.cpp) remembers source entries, plans, variants, and even failures because the same shader can be hit every frame.

## What is flawed or weak

The whole system is inherently brittle. The [README](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/README.md) says unexpected states throw `std::runtime_error` and terminate. That is honest, but it also tells you this is a research and compatibility project, not a polished runtime.

The legal and operational context is narrow. The [README disclaimer](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/README.md) says the project does not include proprietary software, firmware, keys, or libraries, and users are responsible for lawful inputs. That disclaimer is necessary because the useful path depends on material the repo intentionally does not provide.

The repo is also hard to onboard into. A contributor needs binary formats, platform ABI knowledge, CMake, PRX semantics, shader compilation, Vulkan/SPIR-V, host memory management, and game-runtime expectations. The modular layout helps, but this is not casual code.

## What we can learn / steal

Steal the layer boundaries: binary rewriting, target output, runtime library shims, shader translation, and documentation should be separate enough that each can fail with useful diagnostics. The shape of [core/relinker/main.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/main.cpp) is a good orchestration example.

Steal the "fail on unknown binary reality" posture from [RelinkerPipeline.cpp](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp). For compatibility tooling, guessing around malformed tables or unsupported relocations creates worse bugs than rejecting input.

Steal the source-tree honesty. [docs/user/USAGE.md](https://github.com/boykopovar/AnyPS5/blob/5895ea721a43f48547cc996aee0bb65b603622ac/docs/user/USAGE.md) explains options, deprecated flags, runtime layout, fonts, memory constraints, and exit codes. It does not hide the awkward bits.

## How we could apply it

For our own compatibility or migration tools, copy the pipeline shape: parse and validate input, build an explicit intermediate registry, generate target-specific output through a narrow patcher interface, and keep runtime compatibility modules out of the converter. That pattern works for binary migrations, data format migrations, legacy API shims, and compiler-like asset transforms.

For agent-built systems, the lesson is also useful: when a problem is huge, make the boundaries visible in the repo. AnyPS5's [core/relinker](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/relinker), [core/libs/prx](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/libs/prx), and [core/shader](https://github.com/boykopovar/AnyPS5/tree/5895ea721a43f48547cc996aee0bb65b603622ac/core/shader) split gives an agent a fighting chance to work locally instead of smearing changes across the whole system.

## Bottom line

AnyPS5 is a specialized, sharp-edged compatibility project with enough real architecture to reward study. The reusable lesson is that direct compatibility work is less about one clever trick and more about disciplined boundaries: binary transformation here, platform output there, runtime libraries over there, shader translation in its own compiler-shaped subsystem, and no pretending unsupported cases are fine.
