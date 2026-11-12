# Cartridge 004: Standard rewind taste test

**A sneaky taste test for the Turbo Club.**

This is the latest Standard build in testing, dated 261111. It adds rewind for supported TurboGrafx-16 / PC Engine HuCards, alongside four SD-backed manual save slots and CPU Turbo.

## Status

THE OWNER reports this exact test binary working well. Final verification and updated OSD menus following MiSTer’s template are coming. This is an experimental preview, not a fully qualified release or a guarantee of compatibility with every game, display or configuration. Keep Cartridge 003 SavePoint available if you prefer its established track.

- [Test RBF](TurboGrafx16_ToTheLimit_261111_Standard_TEST.rbf)
- [Matching source archive](TurboGrafx16_ToTheLimit_261111_Standard_TEST_source.zip)
- [SHA-256 checksums](TurboGrafx16_ToTheLimit_261111_Standard_TEST.sha256)
- RBF size: 4,494,748 bytes.
- RBF SHA-256: `7fba6e8920f3f2424da8dd2e7bc073da1329ffeffa3f1dd2b745a7a1a86db869`.

The archive accompanies this exact test RBF. Source correspondence does not establish final timing, CDC, hardware or full-system qualification. It is not a later root-menu revision or a quarter-second capture build. The archive includes source, project files and test code, but not a complete runnable regression harness.

## Known issue: core reload

Reloading the core may reopen the previous game with save states and rewind unavailable. **Workaround: open Load TurboGrafx and explicitly reload your HuCard ROM**, even if the game is already visible. This is being investigated by THE OWNER.

This workaround applies to the current test binary; it is not a claim that the issue is fixed. Final verification and the OSD menu update are still forthcoming.

## Try rewind

1. Back up your usual RBF, battery saves and save states. Keep separate test progress and retain your known-good core.
2. Copy this RBF to MiSTer's `_Console` folder and launch it. Load a supported HuCard using SDRAM. After reloading the core, select the ROM again through **Load TurboGrafx** before using save states, even if the previous game is still visible.
3. Open **Save States (HuCard) → Rewind → On**, then close the OSD and play to build some history.
4. Hold **Backspace** or your mapped **Rewind** controller button to step backward through snapshots. Release it to continue playing from that point.
5. **Rewind History** offers 128, 64, 32 or 16 snapshots. **Capture Pace** offers approximately 1, 0.5, 2 or 4 seconds. This is snapshot rewind; capture spacing and available history determine how far back you can go.

Loading or rewinding an older state can restore older battery RAM. A later backup-RAM save or autosave can write it to SD and replace newer progress. Test with backup copies, never your only important save.

Rewind history is temporary. Changing the rewind settings clears it. Do not rely on history as a permanent save or your only copy of progress. Analog video may flash during restoration.

## Manual saves and CPU Turbo

- Select one of four slots in **Save States (HuCard)**. **F5** saves; **F8** loads. Let SD writes finish before resetting, changing cores or powering off.
- Keep saves from different builds and snapshot formats separate. Do not assume older snapshots are compatible.
- **Hardware → CPU Turbo** offers Off, +20% and +50%. Begin with Off and compare the same scene when experimenting. The percentages describe eligible CPU cycles, not guaranteed gameplay speedups.

## Scope and feedback

Save states and rewind require a supported HuCard configuration and SDRAM. **Rewind is available on supported HuCards. Save states and rewind are not supported for CD or SuperGrafx.** Other device, cheat and configuration guards can disable the feature; this is not an all-HuCard compatibility claim. Normal CD operation is a separate matter.

Report the exact build, game, display/output, SDRAM setup, capture pace and steps to reproduce any issue in the [issue tracker](https://github.com/pxpxpxp/to-the-limit/issues). Stop testing if restoration causes corruption, instability or a lock-up; return to your known-good core and backup saves.

## Ninja Spirit preview

The [Ninja Spirit GIF](../assets/ninja-spirit-real-gameplay-rewind.gif) is real gameplay footage edited to illustrate rewind. **It is not a recording of this core or evidence of its hardware behavior.** Footage credit: Shootergott / [World of Longplays](https://longplays.org/). Original game rights remain with their owners. No game ROMs or BIOS files are included.
