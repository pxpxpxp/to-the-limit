# To the Limit

Experimental turbo cores for **MiSTer FPGA**, with source, build evidence and a pixel-art download hub.

**Website:** https://pxpxpxp.github.io/to-the-limit/

## Available builds

| Core | Changes | Status |
| --- | --- | --- |
| TurboGrafx-16 / PC Engine | CPU Turbo Off / +20% / +50%; existing Extra sprite mode retained | Experimental RBF; owner reports +50% works; gameplay gains not measured |

The website also links to Corn's community N64 94MHz+ project, based on Robert Peip's core. That is not an original To the Limit build and its binaries are not redistributed here.

## TurboGrafx installation

1. Keep your original RBF as a backup.
2. Copy `docs/downloads/TurboGrafx16_20261029.rbf` to MiSTer's `_Console` directory and launch it.
3. Select **Hardware → CPU Turbo → +20%** or **+50%**. Off remains the default.
4. On the initial build, select **Sprites per line → Extra** manually. An Extra-default revision is being rebuilt and will have its own filename and matching source.
5. Compare the same busy scene at Off and turbo. Check sound, controls, raster effects and stability. Return to Off if needed.

The percentages describe eligible CPU cycle rates before memory waits; they do not promise equivalent gameplay improvements. The video and audio clocks remain unchanged. ROM waits can absorb the extra CPU speed.

## Source and validation

- [Source archive](docs/downloads/TurboGrafx16_CPU_Turbo_source.zip)
- [Build notes](cores/turbografx16/README.md)
- [SHA-256](docs/downloads/TurboGrafx16_20261029.sha256)
- Upstream: https://github.com/MiSTer-devel/TurboGrafx16_MiSTer
- Base commit: `827d45f45799b8ab3a536510847f2108a92e81bd`

The initial RBF passed 10 synthetic CPU scenarios and 900 SDRAM reads, plus reported constrained multi-corner TimeQuest checks. Full mixed-language core simulation, physical DDR3 and broad game/CD compatibility are not established by these tests. The user's +50% hardware report is encouraging but not a measured benchmark.

## Website

GitHub Pages serves `main` → `/docs`. The site is buildless HTML, CSS and JavaScript, with an original locally hosted pixel font and code-drawn artwork. No analytics, external scripts, ROMs or BIOS files.

Add future verified builds with their matching source, hashes, upstream attribution and validation limits. Do not turn proposed or third-party cores into claimed original releases.

## Credits and licenses

Original TurboGrafx and MiSTer framework authors retain their copyrights. The downloadable source preserves upstream license notices and includes the local changes and build reports. See [NOTICE](NOTICE.md). Corn and Robert Peip (FPGAzumSpass) are credited for the separate N64 work.
