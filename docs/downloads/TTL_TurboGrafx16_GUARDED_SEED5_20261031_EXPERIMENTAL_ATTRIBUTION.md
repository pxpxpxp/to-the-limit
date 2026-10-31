# TurboGrafx-16 / PC Engine — attribution and license inventory

Audit: 2026-10-31. This is an independent **To the Limit** experimental derivative, not an official MiSTer release or an endorsement by the contributors below. Existing source copyright and license notices are retained. No game ROM or BIOS is supplied.

## Core lineage and credits

The recorded base is [MiSTer-devel/TurboGrafx16_MiSTer, commit 827d45f45799b8ab3a536510847f2108a92e81bd](https://github.com/MiSTer-devel/TurboGrafx16_MiSTer/tree/827d45f45799b8ab3a536510847f2108a92e81bd), recorded in `docs/CPU_Turbo.md` and `docs/NinjaSpirit_SaveStates_initial.md`. Its [README at that commit](https://github.com/MiSTer-devel/TurboGrafx16_MiSTer/blob/827d45f45799b8ab3a536510847f2108a92e81bd/ReadMe.md) was checked directly. This base identifier is provenance, not a claim that all current files are byte-identical to that revision.

The upstream README credits:

- **Gregory Estrade (Torlus)** — original [FPGAPCE](https://github.com/Torlus/FPGAPCE), from which the MiSTer core was ported.
- **Sorgelig** — MiSTer port, Arcade Card, DDR3, mappers and other changes.
- **srg320** — tweaks and CD support.
- **greyrogue** — additional bug fixes.
- **Kitrinx** — palettes and audio filters; [TG16_Palette](https://github.com/Kitrinx/TG16_Palette).
- **dshadoff** — further refinements and maintenance.
- **furrtek** — VDP reverse engineering used for the original palette; **ArtemioUrbina** — color-output verification.

This is not an exhaustive list of everyone who has contributed upstream; consult upstream history. Local CPU Turbo, sprite-default and experimental save-state changes are documented separately in this package. No upstream contribution is claimed as original To the Limit work.

## Bundled support components

The per-file inventories and preserved-notice indexes accompanying this file cover the delivered interim source and the fuller work-in-progress separately. Header evidence includes:

| Component | Preserved attribution / terms |
| --- | --- |
| Main top level, `rtl/huc6202.vhd`, color/audio filters; portions of `sys/` | Sorgelig / Alexey Melnikov; GPL-2.0-or-later where explicit |
| SDRAM / DDR and HPS support | Sorgelig / Alexey Melnikov; Till Harbaum credited as SDRAM basis; GPL-3.0-or-later where explicit |
| `sys/hps_io.sv`, `sys/scandoubler.v` | Till Harbaum and Alexey Melnikov; GPL-3.0-or-later |
| `sys/sd_card.sv` | Till Harbaum and Sorgelig; **Lesser** GPL version 3 or later in header |
| `sys/hq2x.sv` | Ludvig Strigeus and Sorgelig; GPL, header refers to COPYING without specifying version |
| `sys/video_freak.sv` | Grabulosaure and Alexey Melnikov; GPL, header refers to COPYING |
| `sys/video_mixer.sv`, `sys/video_cleaner.sv` | Alexey Melnikov / Sorgelig; GPL, header refers to COPYING |
| `sys/ascal.vhd` | TEMLIB 2018–2020; custom permission to distribute/use for any purpose, with request to report bugs/enhancements to info@temlib.org; retain complete header |
| `sys/spdif.v` | Ultra-Embedded.com, Copyright 2012; GPL-2.0-or-later |
| `sys/f2sdram_safe_terminator.sv` | bellwood420, Copyright 2021; no explicit license statement located in this file |
| `sys/yc_out.sv` | Mike Simone, Copyright 2022; GPL-2.0-or-later |
| Generated PLL, reconfiguration and CD FIFO HDL | Intel / Altera; vendor-specific notices and restrictions retained in each file. **Not relicensed by this document or COPYING.** |

Files without individual attribution/license headers (including several original CPU/VDC/PSG modules and support utilities) remain identified by path and hash. Absence of a header is **not** a public-domain determination, permission grant, or evidence of authorship by this project. Historical authorship beyond the verified README and file headers is unresolved; do not invent individual ownership assignments.

## Save-state references and host firmware

`docs/NinjaSpirit_SaveStates_initial.md` explicitly identifies SNES, GBA and PSX implementations as **architectural references, not code ports**. Preserve its links to [SNES savestates](https://github.com/MiSTer-devel/SNES_MiSTer/blob/master/rtl/savestates.sv), [SNES top level](https://github.com/MiSTer-devel/SNES_MiSTer/blob/master/rtl/SNES.vhd), [GBA save states](https://github.com/MiSTer-devel/GBA_MiSTer/blob/master/rtl/gba_savestates.vhd), [GBA state registers](https://github.com/MiSTer-devel/GBA_MiSTer/blob/master/rtl/reg_savestates.vhd), and [PSX save states](https://github.com/MiSTer-devel/PSX_MiSTer/blob/main/rtl/savestates.vhd). “SNES-style menu” describes interface inspiration, not SNES code authorship or compatibility.

The interim's `savestate/firmware_persistence_audit/` contains extracted functions from official [Main_MiSTer commit 08271656799ede50358de1248f6ee878dd7ce5c4](https://github.com/MiSTer-devel/Main_MiSTer/tree/08271656799ede50358de1248f6ee878dd7ce5c4), not a newly authored firmware implementation. Its README preserves exact source lines and blob IDs for `process_ss.inc` / `user_io.cpp` and `file_path.inc` / `file_io.cpp`; its full upstream GPL-3.0 LICENSE is retained.

The fuller WIP additionally retains official Main firmware source under `savestate/guarded_cdc_validation/hps_guard/firmware_source/` for protocol inspection. `osd.cpp` preserves **Dennis van Weeren (2005–2007)** and **Jakub Bednarski (2008–2009)** notices. See the adjacent `NO_DISC_STARTUP_AUDIT.md` for the pinned commit. These are evidence/test inputs, not FPGA synthesis inputs.

## License texts, scope and remaining uncertainty

`LICENSES/GPL-2.txt`, `LICENSES/GPL-3.txt`, and `LICENSES/LGPL-3.txt` reproduce the complete GNU license texts from this environment's `/usr/share/common-licenses`. Root `COPYING` indexes both GPL versions and LGPL without choosing a version for ambiguous files; it does not remove any file's stated version choice, change authorship, override custom/vendor terms, or assign a license to files with unresolved terms. LGPL v3 is read together with GPL v3. Preserve all source notices and these texts when redistributing the corresponding source. Distribute an RBF with access to its matching source, not a later unrelated WIP snapshot.

The audit found preserved upstream README credits and embedded notices, but the delivered interim lacked top-level COPYING and complete standalone GPL-2/LGPL-3 texts. These documentation additions close those identified packaging omissions. The GPL3 firmware license already present is retained unchanged. Explicit license/version terms remain unresolved for some no-header or generic-GPL files; this inventory is not a legal clearance or a guarantee that every historical contributor has been identified. Intel/Altera generated IP retains separate terms.

Documentation-only additions do not alter the interim RBF SHA-256:
`a20b06692b6be4c720de500504dfcfc468d7d0ec20532f6bcb7b0db34caa63d9`.
No HDL, build constraints, generated hardware files or active synthesis inputs were edited for attribution.

## Upstream notice cross-check

The first 80 lines of all 75 `rtl/` and `sys/` HDL/header paths in the delivered interim were requested at the recorded upstream commit. 72 existed upstream; 3 were local additions. Every copyright, explicit GPL-label and TEMLIB permission line found in those upstream prefixes was retained in the corresponding complete interim file (zero missing/changed matching notice lines). This bounded cross-check complements the full-text local inventory; it is not a complete authorship-history reconstruction.
