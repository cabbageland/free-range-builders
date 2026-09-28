# AERIS-10 PLFM RADAR

- Repo: NawfalMotii79/PLFM_RADAR
- URL: https://github.com/NawfalMotii79/PLFM_RADAR
- Date: 2026-09-28
- Repo snapshot studied: main at `749bd0f86a07a28a86347d8ce9c141e601057c40`
- Why picked today: It was high on GitHub trending and, unlike another AI app wrapper, it is a rare open hardware plus firmware plus FPGA plus GUI repository. The interesting part is not the headline "open-source radar"; it is how much of the cross-domain stack is actually checked in.

## Executive summary

[PLFM_RADAR](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40) is the AERIS-10 project: a low-cost 10.5 GHz pulse-LFM phased-array radar design with hardware documentation, RF simulations, STM32 firmware, FPGA DSP blocks, Python GUIs, CI, and cross-layer tests. It is not polished like a product SDK, but it is unusually valuable as a builder artifact because it puts schematics, datasheets, signal-processing RTL, embedded control code, and host visualization code in one inspectable tree.

The strongest lesson is architectural: the repo treats radar as a whole system, not as one beautiful algorithm. The useful seams are between the hardware bill of materials, the timed STM32 control plane, the FPGA data plane, and the Python operator surface.

## What they built

The [README](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/README.md) describes AERIS-10 as a 10.5 GHz phased-array radar with a shorter-range patch-array version and an extended slotted-waveguide version. The checked-in material supports that claim structurally:

- Hardware: production outputs, stackup images, schematics, and RF component references under [4_Schematics and Boards Layout](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/4_Schematics%20and%20Boards%20Layout) and datasheets under [7_Components Datasheets and Application notes](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/7_Components%20Datasheets%20and%20Application%20notes).
- Simulation: antenna, waveguide, reconstruction-filter, BPF, via-fencing, MATLAB, and openEMS material under [5_Simulations](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/5_Simulations).
- Firmware: STM32 board control, FPGA RTL, GUI, and tests under [9_Firmware](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware).
- Documentation: generated reports and bring-up pages under [docs](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/docs).

The claimed processing pipeline is DAC chirp generation, RF up/down conversion, ADAR1000 beam steering, ADC capture, digital down-conversion, filtering, pulse compression, Doppler, MTI, CFAR, USB transfer, and host visualization.

## Why it matters

Open radar projects often stop at diagrams, notebooks, or one disconnected HDL demo. This repo is more useful because it exposes failure-prone interfaces: GPIO timing, I2C/SPI peripheral bring-up, FPGA command registers, GUI packet parsers, and testbenches. The most reusable part is the discipline of checking contracts across languages and hardware layers, not any single radar component.

It is also a reminder that "open source hardware" is only helpful when the repo shows manufacturing files, component evidence, simulation assumptions, and test hooks. A block diagram alone is not a buildable system.

## Repo shape at a glance

- [1_Project_Description](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/1_Project_Description) contains the project description document.
- [2_Functional Diagram & Interconnection Matrices](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/2_Functional%20Diagram%20%26%20Interconnection%20Matrices) holds architecture drawings.
- [3_Power Management](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/3_Power%20Management) holds the power-management worksheet.
- [4_Schematics and Boards Layout](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/4_Schematics%20and%20Boards%20Layout) is the PCB/manufacturing area.
- [5_Simulations](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/5_Simulations) is the RF/signal-processing study area.
- [7_Components Datasheets and Application notes](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/7_Components%20Datasheets%20and%20Application%20notes) anchors the component choices in actual vendor documents.
- [9_Firmware](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware) is the live software/RTL stack.
- [.github/workflows/ci-tests.yml](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/.github/workflows/ci-tests.yml) runs Python lint/tests, MCU tests, FPGA regression, and cross-layer contract checks.
- [pyproject.toml](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/pyproject.toml) keeps host/cosim dependencies deliberately small and uses ruff rules that catch common generated-code slop.

## Layered architecture dissection

### High-level system shape

This is a four-plane system:

1. The physical/RF plane: antenna arrays, mixers, clocking, PA/LNA, power rails, and board files.
2. The real-time control plane: STM32 firmware sequences rails, clocks, beamformer state, GPS/IMU/barometer, and PA bias.
3. The data plane: FPGA RTL generates chirps, ingests ADC samples, performs radar DSP, and exposes USB command/data paths.
4. The operator plane: Python GUI modules parse packets, run software-side processing, apply geospatial corrections, and visualize targets.

### Main layers

The STM32 layer starts in [main.cpp](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_1_Microcontroller/9_1_3_C_Cpp_Code/main.cpp), where the system declares I2C, SPI, timers, UARTs, UM982 GPS state, GY-85 IMU state, radar chirp parameters, DAC5578 handles, ADS7830 readings, and watchdog state. The beamformer/control specifics sit in [ADAR1000_Manager.cpp](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_1_Microcontroller/9_1_1_C_Cpp_Libraries/ADAR1000_Manager.cpp), which has explicit power-up, power-down, RX/TX switching, and ADAR1000 vector-modulator lookup tables.

The FPGA top is [radar_system_top.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/radar_system_top.v). It declares the system clocks, DAC outputs, mixer enables, ADAR level-shifter paths, ADC LVDS inputs, STM32 control toggles, FT601/FT2232H USB modes, host command registers, AGC GPIOs, and debug outputs. The receiver path is in [radar_receiver_final.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/radar_receiver_final.v), which ties the ADC interface to DDC, gain control, matched filtering, range-bin decimation, MTI, Doppler, and CFAR integration.

The host layer lives in [9_Firmware/9_3_GUI](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_3_GUI). [test_v7.py](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_3_GUI/test_v7.py) shows the unit-testable model: radar targets, settings, GPS data, processing config, MTI, CFAR, windowing, DC notch, clustering, and USB packet parsing.

### Request / data / control flow

A useful mental model is "timed pulses down, detections up." The STM32 and/or host command registers trigger chirp/elevation/azimuth events. [radar_system_top.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/radar_system_top.v) turns those into transmitter and receiver control state. [radar_receiver_final.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/radar_receiver_final.v) processes ADC samples into range/Doppler products. [doppler_processor.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/doppler_processor.v) explicitly splits the 32-chirp staggered PRI frame into two 16-point FFTs, avoiding the invalid shortcut of one uniform 32-point FFT over non-uniform timing. [cfar_ca.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/cfar_ca.v) buffers Doppler magnitude per range/Doppler bin and runs configurable CA/GO/SO CFAR after a frame-complete pulse.

The GUI and tests are the receiving end of that contract. [test_cross_layer_contract.py](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/tests/cross_layer/test_cross_layer_contract.py) treats opcode maps, widths, packet layouts, Verilog cosim output, and C stub parsing as one compatibility surface.

## Key directories and files

- [README.md](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/README.md): product-level architecture, components, specifications, build guidance, and license split.
- [radar_system_top.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/radar_system_top.v): the integration point for clocks, transmitter, receiver, USB, host commands, and AGC status.
- [radar_receiver_final.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/radar_receiver_final.v): the ADC-to-DSP chain.
- [doppler_processor.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/doppler_processor.v): corrected staggered-PRF Doppler logic.
- [cfar_ca.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/cfar_ca.v): adaptive threshold detector with guard/train/alpha/mode controls.
- [main.cpp](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_1_Microcontroller/9_1_3_C_Cpp_Code/main.cpp): MCU hardware ownership and radar constants.
- [ADAR1000_Manager.cpp](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_1_Microcontroller/9_1_1_C_Cpp_Libraries/ADAR1000_Manager.cpp): beamformer mode switching and per-device state.
- [test_cross_layer_contract.py](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/tests/cross_layer/test_cross_layer_contract.py): the best testing idea in the repo.
- [array_pattern_Kaiser25dB_like.py](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/5_Simulations/array_pattern_Kaiser25dB_like.py): antenna pattern and taper study.
- [Generate_ChirpcsvFile.py](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/5_Simulations/DAC_ReconstructionFilter/Generate_ChirpcsvFile.py): chirp-ramp CSV generator for reconstruction-filter work.

## Important components

The most important component is the contract between [radar_system_top.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/radar_system_top.v) and the host/STM32 layers. Host opcodes configure radar mode, chirp timing, detection threshold, stream control, gain shift, CFAR parameters, MTI, DC notch, AGC, self-test, and status. That makes the FPGA configurable enough to test without reflashing.

The second key component is the ADAR1000 layer. [ADAR1000_Manager.cpp](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_1_Microcontroller/9_1_1_C_Cpp_Libraries/ADAR1000_Manager.cpp) does not hide the scary physical details: it sequences bias rails, switches RX/TX modes, and documents the vector-modulator table provenance.

The third component is verification. [.github/workflows/ci-tests.yml](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/.github/workflows/ci-tests.yml) runs Python tests, MCU tests, FPGA regression, and cross-layer tests. For a mixed hardware/software repo, that is the difference between a museum archive and a living build.

## Important knobs / configs / extension points

- FPGA command registers in [radar_system_top.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/radar_system_top.v): chirp/listen/guard cycles, chirps per elevation, gain shift, range mode, CFAR, MTI, AGC, and status.
- CFAR knobs in [cfar_ca.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/cfar_ca.v): guard cells, train cells, Q4.4 alpha, mode, enable, and simple-threshold fallback.
- GUI-side processing knobs in [test_v7.py](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_3_GUI/test_v7.py): MTI order, CFAR guard/train/threshold, windowing, DC notch, clustering, and pitch correction.
- Simulation parameters in [array_pattern_Kaiser25dB_like.py](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/5_Simulations/array_pattern_Kaiser25dB_like.py): array dimensions, element spacing, taper, steering angles, and beamwidth.
- Chirp-generation parameters in [Generate_ChirpcsvFile.py](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/5_Simulations/DAC_ReconstructionFilter/Generate_ChirpcsvFile.py): sample rate, burst length, repetition period, min/max frequency, duration, and DAC hold.

## Practical questions and answers

Q: Is this buildable from the repo alone?
A: Not safely by a casual builder. The source has a lot of manufacturing and firmware material, but high-power RF, phased arrays, and radar regulation demand review, equipment, and local legal compliance. Treat it as an engineering reference first.

Q: What is the most reusable software pattern?
A: The cross-layer contract test in [test_cross_layer_contract.py](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/tests/cross_layer/test_cross_layer_contract.py). Any hardware project with Python tooling, RTL, and embedded C should steal that idea.

Q: What part looks production-minded?
A: The FPGA receiver chain has comments about prior bugs, CDC removal, host-configurable timings, staggered-PRF correctness, and CFAR resource/timing estimates. That kind of explanation in [radar_receiver_final.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/radar_receiver_final.v) and [cfar_ca.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/cfar_ca.v) is a strong signal.

Q: What part looks weakest?
A: The repo is large and uneven. Some critical design knowledge is in binary docs, PDFs, spreadsheets, and images, not machine-checkable specs. That is normal for hardware, but it makes review and reuse slower.

## What is smart

The smartest piece is not a single radar algorithm; it is the use of independent ground truth at boundaries. [test_cross_layer_contract.py](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/tests/cross_layer/test_cross_layer_contract.py) explicitly says the goal is to find unknown bugs, not merely prove that two wrong layers agree. That is exactly the right posture for hardware/software systems.

The Doppler correction in [doppler_processor.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/doppler_processor.v) is also smart. It calls out why a single 32-point FFT over staggered PRI samples is invalid and splits the work into two 16-point FFTs.

## What is flawed or weak

The repo carries a lot of heavy artifacts and historical material. That is useful for provenance, but it makes the signal-to-noise ratio rough. Some important build knowledge is embedded in docs or images rather than versioned text with tests. The README still makes large capability claims that require hardware validation; source inspection can confirm structure, not range or RF performance.

The documentation shape is also mixed: [docs](https://github.com/NawfalMotii79/PLFM_RADAR/tree/749bd0f86a07a28a86347d8ce9c141e601057c40/docs) has reports and pages, while core design details also live in spreadsheets, docx files, comments, and simulation outputs. A new contributor will need a guide that orders the bring-up path.

## What we can learn / steal

Steal the idea of cross-layer tests before hardware is "done." If GUI constants, FPGA opcodes, and C packet parsers are one contract, test them as one contract.

Steal the explicit register-map style in [radar_system_top.v](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_2_FPGA/radar_system_top.v): hardware behavior is easier to operate when runtime knobs have named opcodes, reset defaults, and tests.

Steal the comments that name the physical reason for a design choice. [ADAR1000_Manager.cpp](https://github.com/NawfalMotii79/PLFM_RADAR/blob/749bd0f86a07a28a86347d8ce9c141e601057c40/9_Firmware/9_1_Microcontroller/9_1_1_C_Cpp_Libraries/ADAR1000_Manager.cpp) is valuable because it explains power/bias sequencing, not just because it writes registers.

## How we could apply it

For any robotics, embedded, lab-instrument, or edge-AI device, mirror this repo shape: a top-level architecture doc, a manufacturing/hardware folder, firmware split by controller and programmable logic, simulation notebooks/scripts, a host UI, and CI that checks cross-language contracts.

For our own builder notes, the repo is a good reminder to evaluate projects by boundary quality. A fancy algorithm is less impressive than the ability to trace a real signal from physical input, through device timing, through processing, through transport, into a UI and tests.

## Bottom line

PLFM_RADAR is messy in the way real hardware projects are messy, but it is a serious source study. The keeper idea is the system-level contract: radar is not "the FFT"; it is board files, timing, firmware, RTL, host parsing, and verification all negotiating one physical machine.
