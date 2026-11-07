# TTL SavePoint

Cartridge 003 for TurboGrafx-16 and PC Engine HuCards on MiSTer. Build `261106SP1` is the stable save-state track. It offers four manual slots, F5/F8 and optional CPU Turbo (+20% and +50%). Rewind has been removed.

## Install and save

1. Back up the stock RBF and your `saves` and `savestates` folders. Start with a test card and a separate copy of your game progress.
2. Copy `TTL_SavePoint_TurboGrafx16_20261106.rbf` to `_Console` and launch it. Start with a HuCard such as Ninja Spirit, SDRAM ROM storage, and the default settings.
3. Keep your existing MiSTer Main. The core uses MiSTer’s standard four-slot SD save-state interface.
4. Select a slot under **Save States (HuCard)**. Press **F5** to save and **F8** to load with the menu closed. The menu provides the same actions.
5. Give MiSTer time to finish writing the save state before resetting, reloading the core, switching games or powering off. Restore with the same ROM, slot and configuration.

This build uses protocol 3. Earlier experimental formats use separate files. Save states are for supported HuCard configurations. Change CPU Turbo before creating a snapshot and use the same setting when restoring it.

## Validation

THE OWNER has hardware-validated this build on their Sony PVM. The RBF also passed Quartus timing checks. This report does not establish broad game compatibility or confirm a separate SD power-cycle test.

The [source ZIP](TTL_SavePoint_TurboGrafx16_20261106_source.zip) includes the corresponding core source, licenses, and build evidence. Verify the downloads with the [SHA-256 list](TTL_SavePoint_TurboGrafx16_20261106.sha256).
