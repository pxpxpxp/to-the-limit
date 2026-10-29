# To the Limit — Extra-default revision (2026-10-29)

- Upstream: MiSTer-devel/TurboGrafx16_MiSTer at `827d45f45799b8ab3a536510847f2108a92e81bd`.
- CPU Turbo: Off / +20% / +50%; default Off. CPU implementation unchanged from the first tested build.
- Sprites per line: **Extra by default**, Normal remains selectable.
- New sprite status bit 41: zero=Extra, one=Normal. Old bit 11 is reserved and ignored. Older saved options do not get inverted.
- Quartus Prime Lite 23.1std.0 Build 991; Cyclone V 5CSEBA6U23I7; Standard Fit; seed 2; four workers.
- Full synthesis, fitting, final multi-corner timing analysis and RBF assembly completed successfully.
- Minimum reported constrained timing slack: **0.066 ns**. Inherited external I/O constraints remain incomplete.
- Earlier unchanged CPU regression: 10 scenarios passed; SDRAM simulation: 900 reads passed.
- Hardware feedback applies to the initial binary: owner reports +50% is working. This Extra-default revision has not yet been tested on physical hardware.
- No measured game-speed improvement or broad CD/DDR3/game compatibility claim.

RBF: `TurboGrafx16_TTL_20261029.rbf` (4,237,192 bytes).
SHA-256: `37e3e6c4eabff63d87e0f59cd412546f99f09265e2518550687676fc95d1c0e2`.

## Build

```sh
quartus_map TurboGrafx16
quartus_fit TurboGrafx16 -c TurboGrafx16
quartus_sta TurboGrafx16 -c TurboGrafx16 --multicorner=on --do_report_timing
quartus_asm TurboGrafx16 -c TurboGrafx16
```

The hosted build uses the included `tools/quartus_host_compat.c` to address legacy host library/PID namespace behavior. It changes no FPGA clocks, RTL timing constraints or license checks. Synthesis also preloads host libtcmalloc_minimal; fitting, timing and assembly do not. Complete component license notices remain in the source archive.
