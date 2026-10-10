# AnyPS5

- Repo: boykopovar/AnyPS5
- URL: https://github.com/boykopovar/AnyPS5
- Date: 2026-10-10
- Repo snapshot studied: main at commit 57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4
- Why picked today: It was high on GitHub daily trending, had fresh activity today, and is a rare source-rich compatibility project: a PS5 executable relinker, native PRX library replacements, a shader recompiler, Vulkan runtime work, binary patching, build tooling, tests, and unusually candid architecture docs.

## Executive summary

[boykopovar/AnyPS5](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4) is not an emulator in the usual "host runtime interprets the guest" sense. The project tries to convert PS5 executables into native Linux, Windows, or macOS x86-64 programs and then satisfy their dynamic imports with native implementations of PlayStation system PRX libraries. The README says this directly: the [relinker](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker) converts executables to a target system's native format and [core/libs/prx](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx) supplies system library implementations for dynamic linking.

The interesting mechanism is the split between conversion and compatibility. [docs/dev/ARCHITECTURE.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/ARCHITECTURE.md) shows the pipeline: ingest a PS5 ELF and bundled `sce_module` files, optionally lower AMD-only instructions, read imports by NID, reject raw syscalls, build a SysV dynamic section, convert bundled modules, patch the output image, and let the host loader bind imports by NID against generated `.prx` libraries.

The builder lesson is that compatibility work is mostly bookkeeping with teeth. The glamorous part is the shader recompiler, but the repo's real value is in the boring-looking invariants: exact binary format writing in [core/relinker/elfpatcher](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/elfpatcher), export-name-to-NID patching in [core/libs/nid](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/nid), native library coverage in [core/libs/prx](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx), and many tests around edge cases that would otherwise fail as mysterious runtime crashes.

## What they built

AnyPS5 builds two big things.

First, it builds a relinker. The entry point and usage surface live under [core/relinker](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker), with user-facing documentation in [docs/user/USAGE.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/user/USAGE.md). The relinker consumes a clean ELF executable plus bundled ELF modules from `sce_module`, `sce_modules`, or `prx`, then emits a Linux ELF, Windows PE, or macOS Mach-O target. Platform-specific patchers live in [core/relinker/elfpatcher/src/linux/LinuxElfPatcher.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/elfpatcher/src/linux/LinuxElfPatcher.cpp), [core/relinker/elfpatcher/src/windows/WindowsPePatcher.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/elfpatcher/src/windows/WindowsPePatcher.cpp), and the macOS patcher files under [core/relinker/elfpatcher/src/macos](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/elfpatcher/src/macos).

Second, it builds a compatibility library set. [core/libs/CMakeLists.txt](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/CMakeLists.txt) turns each library in [core/libs/prx](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx) into a shared `.prx`, then runs `nid_patcher` so exports match the NID names the converted executable imports. Some libraries are stubs or partial implementations, but some are real subsystems, especially [libSceAgc](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgc) and [libSceAgcDriver](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgcDriver), which carry graphics command, shader, queue, memory, synchronization, and Vulkan pipeline work.

## Why it matters

Most compatibility projects hide complexity behind a single "run this game" claim. This repo exposes the conversion architecture. It is a useful case study in turning a closed-platform binary into something the host OS can load without pretending the differences disappear.

The architecture also makes a strong argument for replacing magical emulation language with explicit contracts. [core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp) validates dynamic tags, scans executable segments, identifies imports, and throws when assumptions are violated. [core/relinker/relinker/src/analysis/SyscallScanner.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/analysis/SyscallScanner.cpp) rejects guest syscall instructions instead of letting them leak into a host process. [docs/dev/BUILD.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/BUILD.md) is similarly practical: build modes, target limits, dependency requirements, shader flags, and warnings about stale PRX outputs are spelled out.

## Repo shape at a glance

- [CMakeLists.txt](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/CMakeLists.txt): root build graph, third-party dependency wiring, test registration, relinker-only mode, full build mode, shader and timing flags.
- [core/relinker](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker): executable conversion pipeline, ELF parsing, dynamic-section construction, platform patchers, AMD-only instruction lowering, guest module conversion, CLI, and tests.
- [core/libs](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs): native system library implementations, export NID tooling, decoder helpers, timing/logging support, graphics driver code, libc/kernel/net/video/audio/game-service shims, and PRX build rules.
- [core/shader/recompiler](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/shader/recompiler): RDNA shader decode, control-flow graph building, IR translation, optimization passes, SPIR-V emission, disk caching, and optional SPIRV-Tools validation.
- [core/Decoder](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/Decoder): JPEG and PNG helpers with headers, sources, and tests.
- [3rdparty](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/3rdparty): SDL2, Vulkan headers, Vulkan memory allocator, glslang, SPIRV-Tools, FFmpeg core, FreeType, image codecs, and other host-side building blocks.
- [docs](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs): user docs, build docs, compatibility notes, architecture docs, technical debt, and conventions.
- [.github/workflows](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/.github/workflows): build, release, progress, label, convention, and PR intake automation.

## Layered architecture dissection

### High-level system shape

The top-level architecture has three cooperating products:

1. A relinker turns guest ELF material into host-native loadable images.
2. A library build turns PRX replacements into host shared objects with PS5-style NID exports.
3. A graphics/runtime layer implements enough system behavior for selected titles to run.

[docs/dev/ARCHITECTURE.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/ARCHITECTURE.md) is unusually useful because it draws both the executable conversion path and the graphics path. The conversion path is `input.elf` plus modules into [RelinkerPipeline.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp), [GuestModuleBuilder.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/guest/GuestModuleBuilder.cpp), and a platform patcher. The graphics path is guest command buffers into [libSceAgcDriver](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgcDriver), then PM4 state/draw/dispatch decode, then [core/shader/recompiler](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/shader/recompiler), then Vulkan.

### Main layers

The input and validation layer lives in [core/relinker/relinker](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker). [RelinkerPipeline.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp) reads program headers, locates executable segments, requires a dynamic segment, validates OS-vs-SysV dynamic tags, and delegates import construction. [SyscallScanner.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/analysis/SyscallScanner.cpp) scans instructions and throws on `syscall`, `int 0x80`, `sysenter`, or `sysret`; that is the right kind of hard failure for a project that wants host-native output.

The code-rewriting layer is [core/relinker/codegen](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/codegen). [Amd64OnlyConverter.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/codegen/src/Amd64OnlyConverter.cpp) scans code segments, matches AMD-only instructions, collects branch targets, and creates trampoline sites. [LinuxElfPatcher.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/elfpatcher/src/linux/LinuxElfPatcher.cpp) then appends trampoline bodies and patches original bytes with rel32 jumps while checking range and byte-stability assumptions.

The output-image layer is [core/relinker/elfpatcher](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/elfpatcher). Linux output mutates ELF headers and builds dynamic tables. Windows output in [WindowsPePatcher.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/elfpatcher/src/windows/WindowsPePatcher.cpp) constructs PE sections, relocations, TLS metadata, imports, startup stubs, lazy import GOT stubs, base relocations, and icon resources. That is a lot of mundane binary writing, and it is exactly where compatibility projects usually become fragile.

The PRX-export layer is [core/libs/nid](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/nid). [NidResolver.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/nid/src/NidResolver.cpp) checks duplicate exports, honors explicit no-patch markers and exclusions, strips postfixes, and computes NIDs. [BinaryPatcherFactory.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/nid/src/BinaryPatcherFactory.cpp) chooses ELF, PE, or Mach-O patchers from magic bytes.

The graphics layer is split between [core/libs/prx/libSceAgc](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgc), [core/libs/prx/libSceAgcDriver](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgcDriver), and [core/shader/recompiler](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/shader/recompiler). [ShaderUtils.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgc/Shader/src/ShaderUtils.cpp) shows low-level register patching and semantic packing. [Driver.hpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgcDriver/Execution/include/Driver/Driver.hpp) shows the driver object carrying queue submission, shader registration, draw/dispatch caches, packet history, timing, synchronization, memory writes, and presentation.

### Request / data / control flow

For executable conversion, a user runs `relinker input.elf output` as documented in [docs/user/USAGE.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/user/USAGE.md). The CLI reads options such as `--windows`, `--macos`, `--to-intel`, `--rpath`, `--lazy-binding`, and module path settings. [GuestModuleBuilder.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/guest/GuestModuleBuilder.cpp) validates module directories, rejects SELF containers, folds names on Windows, matches required modules, and processes only direct ELF module files.

The relinker reads dynamic imports, builds a rewritten dynamic section through [SysVDynamicSectionBuilder.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/output/SysVDynamicSectionBuilder.cpp), optionally converts AMD-only instructions through [Amd64OnlyConverter.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/codegen/src/Amd64OnlyConverter.cpp), and then calls a platform patcher. Runtime binding is deliberately delegated to the OS loader: the converted program imports NID-named symbols from PRX shared libraries.

For shader execution, [docs/dev/ARCHITECTURE.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/ARCHITECTURE.md) says guest command buffers enter `libSceAgcDriver/Submit`, PM4 state decodes draw and dispatch work, a compiled variant is reused from memory or disk if possible, and otherwise [Recompiler.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/shader/recompiler/Recompiler.cpp) runs RDNA decode, control-flow graph construction, IR translation, optimization, and SPIR-V emission. [ShaderDiskCache.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/shader/recompiler/ShaderDiskCache.cpp) shows the practical side: cache directory selection, versioned binary artifacts, hashes, and struct-size assertions for stable encoding.

## Key directories and files

- [docs/dev/ARCHITECTURE.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/ARCHITECTURE.md): the best high-level map of conversion, PRX linking, shader recompilation, and driver behavior.
- [docs/dev/BUILD.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/BUILD.md): build modes, flags, host constraints, shader settings, and test expectations.
- [docs/user/USAGE.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/user/USAGE.md): input layout, conversion commands, output format selection, and operational options.
- [core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/pipeline/RelinkerPipeline.cpp): central executable analysis and conversion pipeline.
- [core/relinker/relinker/src/guest/GuestModuleBuilder.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/guest/GuestModuleBuilder.cpp): bundled module discovery, validation, conversion, and alias matching.
- [core/relinker/codegen/src/Amd64OnlyConverter.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/codegen/src/Amd64OnlyConverter.cpp): host-instruction compatibility path for `--to-intel`.
- [core/relinker/elfpatcher/src/linux/LinuxElfPatcher.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/elfpatcher/src/linux/LinuxElfPatcher.cpp) and [core/relinker/elfpatcher/src/windows/WindowsPePatcher.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/elfpatcher/src/windows/WindowsPePatcher.cpp): concrete host image writers.
- [core/libs/CMakeLists.txt](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/CMakeLists.txt): PRX build and NID patching rules.
- [core/libs/nid/src/NidResolver.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/nid/src/NidResolver.cpp): export-name-to-NID policy.
- [core/shader/recompiler/Recompiler.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/shader/recompiler/Recompiler.cpp): shader decode, graph, translation, optimization, and SPIR-V control flow.
- [core/libs/prx/libSceAgcDriver/Execution/include/Driver/Driver.hpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgcDriver/Execution/include/Driver/Driver.hpp): driver state and execution surface.

## Important components

- The relinker pipeline is the main conversion coordinator. It is not just a file copier; it reads ELF state, rejects unsupported dynamic structure, filters imports, and hands exact data structures to output writers.
- The NID patcher is the glue between generated libraries and converted executables. Without [core/libs/nid](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/nid), native shared libraries would expose normal C++ names rather than the PS5 import identifiers the guest expects.
- The PRX library tree is the compatibility surface. Simple libraries can be one [Export.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAcm/Export.cpp); complex ones like [libSceAgc](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgc) become whole subsystems.
- The shader recompiler is a staged compiler, not an ad hoc translator. [Recompiler.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/shader/recompiler/Recompiler.cpp) pulls in RDNA decode, graph building, structurization, IR, optimization, resource materialization, binding allocation, and SPIR-V emission.
- The driver object in [Driver.hpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgcDriver/Execution/include/Driver/Driver.hpp) is a warning sign and a necessity: it centralizes too much state, but graphics compatibility probably needs that central arbitration until the model is better understood.

## Important knobs / configs / extension points

- `-DANYPS5_RELINKER_ONLY=ON` in [CMakeLists.txt](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/CMakeLists.txt) builds only the relinker and tests, avoiding full third-party and runtime setup.
- `-DANYPS5_ENABLE_SPIRV_TOOLS=ON` enables SPIR-V validation and optimization for the shader recompiler, as documented in [docs/dev/BUILD.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/BUILD.md).
- `-DAPS5_ENABLE_TIMING_LOG=ON`, `APS5_PIPELINE_STATS=1`, and shader/driver environment switches documented in [docs/dev/BUILD.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/BUILD.md) expose runtime performance diagnostics.
- Relinker options in [docs/user/USAGE.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/user/USAGE.md) choose Windows/macOS output, AMD-to-Intel instruction lowering, lazy binding, RPATH, guest module paths, and module skipping.
- Export patch policy is extendable through [core/libs/nid/include/nid](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/nid/include/nid) and implementations in [core/libs/nid/src](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/nid/src).

## Practical questions and answers

Q: Is this an emulator?
A: Not in the usual runtime-interpreter sense. The README and [docs/dev/ARCHITECTURE.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/ARCHITECTURE.md) describe native relinking plus native PRX implementations. That avoids a separate runtime process but moves complexity into binary patching and API compatibility.

Q: What is the riskiest technical assumption?
A: That enough PS5 system behavior can be reproduced as host-native libraries with stable NID-bound imports. [core/libs/prx](https://github.com/boykopovar/AnyPS5/tree/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx) has many declared libraries, but correctness is per-function and per-title.

Q: Why does the project patch export names to NIDs?
A: The converted executable imports PS5-style identifiers. [core/libs/CMakeLists.txt](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/CMakeLists.txt) builds the PRX libraries and runs `nid_patcher`; [NidResolver.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/nid/src/NidResolver.cpp) encodes the symbol policy.

Q: What should a builder copy?
A: Copy the separation of conversion, output writing, host libraries, and tests. The use of a relinker-only build mode in [docs/dev/BUILD.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/BUILD.md) is especially good: it gives contributors a tractable part of the system to work on without compiling the world.

Q: What should a builder avoid?
A: Avoid treating the progress badges as evidence of broad compatibility. The README explains that library progress is percentage of functions known to the project so far, not all PS5 system functions. For a user-facing claim, [docs/user/COMPATIBILITY.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/user/COMPATIBILITY.md) matters more than raw declared-function counts.

## What is smart

The project makes native loading the center of gravity. That is bold but coherent: if the host loader can bind NID-named imports to native libraries, the project can reuse OS process behavior rather than simulate it all.

The docs are better than the average compatibility repo. [docs/dev/ARCHITECTURE.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/ARCHITECTURE.md) gives real system diagrams and cites concrete files. [docs/dev/BUILD.md](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/docs/dev/BUILD.md) says what is relinker-only, what needs third-party dependencies, and why the `libs` target matters.

The failure policy is honest. The README says unsupported or unexpected states throw `std::runtime_error` and terminate. That is not user-friendly yet, but for this phase it is much better than corrupted execution.

The shader path is architectural, not merely tactical. The combination of [Recompiler.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/shader/recompiler/Recompiler.cpp), [ShaderDiskCache.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/shader/recompiler/ShaderDiskCache.cpp), and [Driver.hpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgcDriver/Execution/include/Driver/Driver.hpp) shows a path toward repeatable compilation, caching, and runtime integration.

## What is flawed or weak

The blast radius is huge. The project has to get binary conversion, host image writing, PRX export naming, system APIs, GPU command interpretation, shader translation, input, audio/video, file behavior, and per-title quirks all right. A single missing semantic can look like "the game crashes."

The source tree has some central objects with enormous responsibility, especially [Driver.hpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/prx/libSceAgcDriver/Execution/include/Driver/Driver.hpp). That may be unavoidable while the behavior is still being mapped, but long-term it will be hard to reason about.

Compatibility claims need careful reading. The README's progress badges are coverage over known functions in the project, not proof of platform completeness. The project is impressive, but it is not a general "run every PS5 title" solution.

The legal and distribution boundary is necessarily delicate. The README states that AnyPS5 does not include proprietary software, firmware, keys, or libraries. Builders adopting a similar model need equally explicit boundaries and should avoid normalizing risky input acquisition.

## What we can learn / steal

Steal the architecture doc style: pair a diagram with concrete file links and state the operational contract in plain language.

Steal the relinker-only development mode. Large systems need a narrow path where contributors can build and test one core subsystem without third-party setup.

Steal the hard validation posture. [SyscallScanner.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/analysis/SyscallScanner.cpp) rejecting forbidden instructions and [GuestModuleBuilder.cpp](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/relinker/relinker/src/guest/GuestModuleBuilder.cpp) rejecting ambiguous module layouts are examples of failing before runtime ambiguity spreads.

Steal the idea that compatibility data should be generated from the source of truth. [core/libs/CMakeLists.txt](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/core/libs/CMakeLists.txt) builds libraries and then patches exports, rather than asking humans to maintain a parallel list.

## How we could apply it

For any project that adapts one ecosystem into another, separate the pipeline into: input validation, semantic translation, output packaging, runtime compatibility libraries, and conformance tests. Do not let a single "adapter" layer do all five.

For binary or model conversion tools, expose a "core only" build like [ANYPS5_RELINKER_ONLY](https://github.com/boykopovar/AnyPS5/blob/57f96fd2b36563e8380c603a92b1ef0d9d3a6aa4/CMakeLists.txt). That gives maintainers a smaller CI target and gives contributors a faster feedback loop.

For agent tools that need to inspect alien artifacts, copy the source-study habit here: represent every assumption as a checked condition and every translated artifact as an explicit output format. Mystery conversion is not debuggable.

## Bottom line

AnyPS5 is interesting because it treats console compatibility as native binary engineering: rewrite the executable, generate host-loadable images, build NID-compatible libraries, translate GPU work, and fail loudly when the model of the guest is incomplete. It is early and high-risk, but the structure is unusually teachable.
