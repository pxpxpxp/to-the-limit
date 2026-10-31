# To the Limit

Experimental turbo cores for **MiSTer FPGA**, with source, build evidence and a pixel-art download hub.

**Website:** https://tothelimit.monster/

## Available builds

| Core | Changes | Status |
| --- | --- | --- |
| TurboGrafx-16 / PC Engine | CPU Turbo Off / +20% / +50%; Extra sprites enabled by default | Experimental RBF; owner reports +50% works; gameplay gains not measured |

The website also links to Corn's community N64 94MHz+ project, based on Robert Peip's core. That is not an original To the Limit build and its binaries are not redistributed here.

## TurboGrafx installation

1. Keep your original RBF as a backup.
2. Copy `docs/downloads/TTL_TurboGrafx16_ExtraSprites_20261029_EXPERIMENTAL.rbf` to MiSTer's `_Console` directory and launch it.
3. Select **Hardware → CPU Turbo → +20%** or **+50%**. Off remains the default.
4. **Extra sprites are on by default.** Normal remains selectable and can be saved. The new sprite option uses status bit 41; legacy bit 11 is reserved, so older saved options are not silently inverted.
5. Compare the same busy scene at Off and turbo. Check sound, controls, raster effects and stability. Return to Off if needed.

The percentages describe eligible CPU cycle rates before memory waits; they do not promise equivalent gameplay improvements. The video and audio clocks remain unchanged. ROM waits can absorb the extra CPU speed.

## Source and validation

- [Source archive](docs/downloads/TTL_TurboGrafx16_ExtraSprites_20261029_EXPERIMENTAL_source.zip)
- [Build notes](cores/turbografx16/README.md)
- [SHA-256](docs/downloads/TTL_TurboGrafx16_ExtraSprites_20261029_EXPERIMENTAL.sha256)
- Upstream: https://github.com/MiSTer-devel/TurboGrafx16_MiSTer
- Base commit: `827d45f45799b8ab3a536510847f2108a92e81bd`

The initial RBF passed 10 synthetic CPU scenarios and 900 SDRAM reads, plus reported constrained multi-corner TimeQuest checks. The Extra-default revision leaves the CPU implementation unchanged and passed a fresh full synthesis, fit, multi-corner timing check and RBF assembly. See [the new build report](cores/turbografx16/BUILD_EXTRA.md). Full mixed-language core simulation, physical DDR3 and broad game/CD compatibility are not established by these tests. The user's +50% hardware report applies to the initial binary and is not a measured benchmark. The Extra-default revision still needs hardware testing.

## Website

GitHub Pages serves `main` → `/docs`. The site is buildless HTML, CSS and JavaScript, with an original locally hosted pixel font and code-drawn artwork. No analytics, external scripts, ROMs or BIOS files.

Add future verified builds with their matching source, hashes, upstream attribution and validation limits. Do not turn proposed or third-party cores into claimed original releases.

## Credits and licenses

Original TurboGrafx and MiSTer framework authors retain their copyrights. The downloadable source preserves upstream license notices and includes the local changes and build reports. See [NOTICE](NOTICE.md). Corn and Robert Peip (FPGAzumSpass) are credited for the separate N64 work.


## Earlier build

The initial `TTL_TurboGrafx16_CPU_Turbo_20261029_EXPERIMENTAL.rbf` and `TTL_TurboGrafx16_CPU_Turbo_20261029_EXPERIMENTAL_source.zip` remain available in `docs/downloads` for comparison. They require selecting Extra sprites manually.

## Download naming

Published downloads use `TTL_TurboGrafx16_<variant>_<YYYYMMDD>_EXPERIMENTAL.rbf` and the matching `_source.zip`, `.sha256` or `_TEST_NOTES.txt` suffix. The date identifies the build. Source archives preserve their original internal filenames and build records; only the published download filenames have changed.
