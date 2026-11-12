# To the Limit

Experimental MiSTer FPGA cores, matching source archives, and a pixel-art download hub.

**Website:** https://tothelimit.monster/
**Downloads and source:** [Current download index](docs/downloads/README.md)

## Current releases

| Cartridge | Build | Features and validation |
| --- | --- | --- |
| 004 · latest | [Standard rewind taste test](docs/downloads/TurboGrafx16_20261112_OC_SS_Rewind.md) | Rewind for supported HuCards, four SD-backed manual save slots and CPU Turbo. THE OWNER hardware-tested the preceding MainMenu build. This About-label recompile passed all 40 global timing checks across eight corners and awaits its own hardware test. Save-state and rewind controls are now in the main menu. |
| 003 | [TTL SavePoint](docs/downloads/TTL_SavePoint_TurboGrafx16_20261106.md) | Four manual HuCard save slots, SD persistence through the standard MiSTer interface, and CPU Turbo. THE OWNER has hardware-validated this build on their Sony PVM. The RBF also passed Quartus timing checks. |
| 001 | Extra Sprites and CPU Turbo | CPU Turbo Off / +20% / +50%, with Extra sprites enabled by default. The initial CPU-turbo binary was tested by THE OWNER at +50%; this Extra-default revision still awaits its own hardware testing. |

The latest core is the [Cartridge 004 rewind taste test](docs/downloads/TurboGrafx16_20261112_OC_SS_Rewind.md). [SavePoint](docs/downloads/TTL_SavePoint_TurboGrafx16_20261106.md) remains available for persistent save states, alongside the original CPU overclock core. The [download index](docs/downloads/README.md) pairs each RBF with its source and available checksums.

**Known issue in Cartridge 004:** reloading the core may reopen the previous game with save states and rewind unavailable. Open **Load TurboGrafx** and explicitly reload the HuCard ROM, even if the game is already visible. This is being investigated by THE OWNER.

## Installation and testing

1. Back up your stock RBF and game progress.
2. Copy the selected RBF into MiSTer's `_Console` directory and launch it. Follow that build's setup notes.
3. Start with CPU Turbo **Off**, then compare +20% and +50% in the same scene. Check sound, controls, raster effects and stability; return to Off if issues appear.
4. Keep separate save files for different snapshot formats. Let SD writes finish before resetting or powering off.

Turbo percentages describe eligible CPU cycles before memory waits, not equivalent gameplay improvements. Video and audio clocks remain unchanged. Hardware reports apply to the build and conditions tested, not every game or configuration.

### Cartridge 001 development notes

[CPU Turbo and Extra-default documentation](cores/turbografx16/README.md) covers the original CPU experiment, its focused patches and synthetic validation. The initial CPU implementation passed 10 synthetic scenarios and 900 SDRAM reads. The Extra-default revision passed a fresh build and constrained multi-corner timing checks. These are not full game, CD or physical-memory compatibility guarantees.

The initial CPU Turbo build and other superseded experiments remain available with their source in the [historical downloads snapshot](https://github.com/pxpxpxp/to-the-limit/tree/93312177178b0d95d6a06a96fdcb08fae489f3ab/docs/downloads).

## Repository layout

- `docs/`: buildless GitHub Pages site, served from `main` → `/docs`.
- `docs/downloads/`: current RBFs, source archives, setup notes, checksums and attribution records.
- `cores/turbografx16/`: historical CPU Turbo/Extra-default build documentation and focused patches. Full core source and FPGA test runners are in the matching source ZIPs, not expanded into this checkout.
- `tools/`: repository validation and pixel-font generation. See [tool instructions](tools/README.md).
- `.github/`: gameplay issue template and repository checks.

## Local checks

Python 3.10 or newer is sufficient for the repository checks; they do not access the network or modify files.

```sh
python3 tools/check_repository.py
python3 -m unittest discover -s tools -p 'test_*.py'
```

To preview the site locally:

```sh
python3 -m http.server 8000 --directory docs
```

Then open http://localhost:8000/.

## Adding a release

Publish each verified RBF with its matching source, available hashes, upstream attribution and validation limits. Update the site and download index together, and run the checks before publishing. Preserve historical evidence rather than treating an old test result as validation of a new binary.

Experimental builds use `TTL_TurboGrafx16_<variant>_<YYYYMMDD>_EXPERIMENTAL`; SavePoint uses `TTL_SavePoint_TurboGrafx16_<YYYYMMDD>`. Companion files use the corresponding `_source.zip`, `.sha256` and notes suffixes. Existing source archives retain their original internal filenames and build records.

## Credits and licenses

Original TurboGrafx and MiSTer framework authors retain their copyrights. Source archives preserve upstream notices, local changes and build evidence. See [NOTICE](NOTICE.md) and the [attribution page](docs/attribution.html); no blanket license applies to all core components.

The website credits Corn's community N64 94MHz+ work, based on Robert Peip's core. It is not an original To the Limit release, and its binaries are not redistributed here. No game ROMs or BIOS files are included.
