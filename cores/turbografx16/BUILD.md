# CPU Turbo build — 2026-10-29

Upstream: MiSTer-devel/TurboGrafx16_MiSTer, commit `827d45f45799b8ab3a536510847f2108a92e81bd`.
Local modifications distributed by To the Limit; no upstream push.

- Quartus Prime Lite 23.1std.0 Build 991, Cyclone V `5CSEBA6U23I7`.
- CPU Turbo: Off / +20% / +50%, default Off; status bits 40:39.
- Four workers, Balanced optimization, Standard Fit, seed 2, Advanced Physical Optimization Off.
- Full synthesis, fitting, assembly and final multi-corner TimeQuest analysis completed.
- Minimum slack across the final timing summary: **0.015 ns**.
- All reported constrained setup, hold, recovery, removal and minimum-pulse-width checks pass.
- The inherited MiSTer constraints leave 26 input ports and 87 output ports unconstrained; this is not a claim that every external interface is timing constrained.
- Clock frequencies, PLL RTL and SDC timing constraints are unchanged.
- Ten CPU regression scenarios passed, including Off/reserved lockstep with upstream, live changes, waits, arithmetic/write traces and I/O/timer cadence. Actual SDRAM controller simulation passed 900 reads.
- Hardware, DDR3 behavior, Ninja Spirit gameplay, audio compatibility and actual slowdown reduction remain untested.

RBF: `TurboGrafx16_20261029.rbf`, 4,210,616 bytes.
SHA-256: `e189f326af48bb58bae52bd03f9fbf57ec36ae7de53ba7ffcfc0e79e7756dbd8`.

Earlier candidates had HDMI-scaler setup violations (-0.061 ns in Fast Fit and -0.280 ns at the cold corner in Auto Fit). The delivered binary uses Standard Fit, seed 2, and passed multi-corner analysis.

## Reproduce

The source includes `sys/pll_q23.qip`, an alias to the existing Quartus-17 PLL QIP selections, for the project's major-version selector. No PLL was redesigned.

```sh
quartus_sh --flow compile TurboGrafx16
quartus_sta TurboGrafx16 -c TurboGrafx16 --multicorner=on --do_report_timing
```

The hosted build ran `quartus_fit`, `quartus_sta`, and `quartus_asm` directly after successful synthesis. `effective_settings.qsf` records the fitted settings; `build_id.v` records the generated date macro.

On this host only, synthesis used the compatibility shim, host libstdc++ and libtcmalloc_minimal. Successful fitting, timing and assembly used the compatibility shim plus host libstdc++, without libtcmalloc_minimal. Normal supported Quartus hosts may not need the shim. See `tools/quartus_host_compat.c`.
