# Optional CPU Turbo — experimental build

This is a local modification of MiSTer-devel/TurboGrafx16_MiSTer at upstream
commit `827d45f45799b8ab3a536510847f2108a92e81bd`. This distribution is hosted by To the Limit. Nothing was pushed upstream. The existing core's identity and game folders
are preserved.

## Use

Open **Hardware → CPU Turbo**. The default is **Off**.

| Selection | High-speed CPU divisor | Ideal CPU rate before memory waits |
| --- | --- | --- |
| Off | 6 | 7.159 MHz |
| +20% | 5 | 8.591 MHz |
| +50% | 4 | 10.739 MHz |

These percentages describe eligible CPU cycles, not measured game speed or
frame-rate gains. Low-speed CPU mode retains divisor 24. All accesses to physical
bank `$FF` (VDC, palette, PSG, controller, timer, interrupt registers and CD I/O)
retain the normal high-speed divisor 6. Reserved selection `11` behaves as Off.
The period is latched after the next address and CSH/CSL speed selection settle,
so changing the menu option cannot shorten a cycle already waiting for memory.

For Ninja Spirit, start with +20%, then compare +50% in the same busy scene.
**Sprites per line → Extra** remains a separate flicker-reduction setting and is enabled by default in the To the Limit revision. Normal is still selectable.
If another game shows timing issues, return CPU Turbo to Off. Existing global
core configuration saves can carry this selection into other games.

## What the inspection found

- `rtl/HUC6280/HUC6280.vhd` explicitly paces the CPU with divisors 6 and 24.
  Optimizing host Linux or FPGA logic placement alone does not give the game
  more emulated CPU cycles. This change deliberately supplies extra CPU cycles.
- PSG synthesis and the hardware timer share an independent divisor-6 `IO_CE`.
  That divider and all video timing/PLL settings are untouched.
- `WAIT_N` and VDC `RDY` stalls remain in force. VDC entry wait handling and
  register side effects are preserved; VDC register traffic is not accelerated.
- ROM reads are launched through the existing memory interface. The SDRAM
  controller runs at twice the master clock and has a fixed command/data
  sequence. Four master clocks is the minimum candidate CPU period here;
  memory readiness can extend it. In the standalone SDRAM simulation, every
  read at divisor 5 required one extra CPU master clock, and every read at
  divisor 4 required two. Consequently, ROM-heavy code will gain less than the
  advertised ideal percentages. This implementation does not bypass that wait.
- A ROM prefetch/cache could improve that bottleneck, but would need a separate
  change with mapper, ROM loading, RAM and cache-invalidation validation. No
  speculative cache or faster SDRAM commands were added.

Ninja Spirit is reported as a useful overclock test case, particularly the first
boss and the area immediately before it:
https://github.com/drhelius/Geargrafx/issues/202 . This is supporting evidence
for where to test, not proof that this FPGA modification fixes that game.

## Validation

The test ROM is synthetic and embedded in the testbench; no commercial ROM is
included or used. GHDL runs the real HuC6280 CPU, wrapper and PSG RTL. Its volume
ROM is modeled with the exact upstream MIF contents and synchronous read timing.
The original CPU wrapper is included as a pinned regression fixture.

CPU tests cover all four two-bit selections plus changing selections every
17 master clocks, each with and without variable memory/VDC stalls (10 runs).
They check:

- Off and reserved-mode bus, CPU speed output, timer, controller and audio
  outputs match the upstream wrapper cycle for cycle.
- All runs produce the same ordered write trace and expected 256-byte RAM
  arithmetic results, including stack accesses and register writes.
- Eligible unstalled cycles use divisors 6/5/4; low-speed and I/O cycles retain
  their original minimum lengths.
- `IO_CE` matches upstream on every clock; successive timer decrements retain
  6,144-master-clock spacing.
- Menu changes during operation and memory waits do not deadlock the CPU.

The separate Icarus test exercises the actual SDRAM controller with a behavioral
CAS-2 memory model: 300 reads at each divisor, covering different rows, banks,
columns and byte lanes. It verifies returned data and wait extensions. The
runner only adapts upstream's procedural bidirectional output into a separate
tri-state driver for Icarus compatibility; it does not change controller timing.
Use strict Verilog expression widths, as the runner does, to match Quartus.

Run with GHDL 4.1 and Icarus Verilog 12, or compatible versions:

```sh
python3 tests/run_cpu_turbo.py
python3 tests/run_sdram_turbo.py
```

The runners accept explicit tool paths (`--help`). Results are recorded in
`tests/validation.txt`.

Quartus Lite 23.1 completed synthesis, fitting and RBF assembly. Final multi-corner
TimeQuest results pass the reported constrained checks; inherited external I/O
constraints remain incomplete. See [build results](BUILD.md) and
the included full timing summary.

**Not yet validated:** a complete mixed-language core simulation; physical MiSTer
behavior; DDR3 hardware; Ninja Spirit gameplay, sound compatibility or measured
slowdown reduction. The synthetic results do not establish game compatibility.

## Build and installation

Use Quartus Lite 23.1 with Cyclone V device support, as used for this build.
From the complete source directory:

```sh
quartus_sh --flow compile TurboGrafx16
quartus_sta TurboGrafx16 -c TurboGrafx16 --multicorner=on --do_report_timing
```

The existing pre-flow script generates `build_id.v`. Review compilation and
TimeQuest timing results before installing `output_files/TurboGrafx16.rbf`.
Back up the current TurboGrafx core, then replace its RBF in MiSTer's `_Console`
folder with the compiled file, keeping only the intended version active. Existing
ROM, BIOS and save folders do not need to change. Keep the stock RBF for rollback.

The RBF has been compiled and timing checked. Physical installation and gameplay
validation have not been performed.

## Ninja Spirit acceptance test still required

Use the same ROM revision, difficulty, weapon, shadow companions, position and
input sequence for stock, Off, +20% and +50%. Test a busy section immediately
before the first boss and the boss itself, plus later stages with many enemies.
Keep the sprite-limit setting identical across comparisons.

Record game-logic updates or repeated animation frames over the same fixed
interval, along with sound, controls, raster effects and any hangs. Display refresh
stays constant even when the game's logic slows down, so a nominal 60 Hz output
alone cannot demonstrate improvement. Test both cold boot and a long play session.

## Hosted Linux build compatibility

The hosted build uses Quartus Lite 23.1std.0 Build 991 with four compilation workers,
Standard Fit, Balanced optimization and Advanced Physical Optimization disabled.
The FPGA RTL, PLL frequencies and timing constraints do not depend on the host
compatibility helpers.

On the hosted Ubuntu environment, legacy Quartus encountered a host allocator
mismatch while loading libudev and could not resolve its own namespace PID through
`/proc/<pid>/exe`. `tools/quartus_host_compat.c` provides narrowly scoped runtime
compatibility: it removes `RTLD_DEEPBIND` when loading host libraries and resolves
this process's own executable through `/proc/self/exe`. It does not change license
checks or FPGA source. The allocator issue is described at:
https://community.altera.com/discussions/quartus-prime/quartus-map-crash-possibly-due-to-shared-library-shenanigans/332593

This helper was compiled with `gcc -shared -fPIC -O2 -Wall -Wextra` and preloaded
alongside host libstdc++. Synthesis also used libtcmalloc_minimal; the successful
fitter, timing and assembler runs did not. The helper also makes runtime messages
available line by line. Normal
Quartus installations may not need it. The finished build report records the
actual tool version and results.


## Hardware feedback and next default

On 2026-10-29 the owner reported the +50% setting is working. The amount of gameplay improvement has not been measured. The new revision enables Extra sprites by default using new status bit 41 (0=Extra, 1=Normal). See [its build report](BUILD_EXTRA.md). Legacy status bit 11 is reserved and ignored, so old saved settings are not silently inverted. CPU Turbo remains default Off.


## Current download

Use `TurboGrafx16_TTL_20261029.rbf` and matching `TurboGrafx16_TTL_20261029_source.zip` from the website downloads directory. Both full build/timing results and SHA-256 checksums are published. The new Extra-default binary has not yet been hardware tested.
