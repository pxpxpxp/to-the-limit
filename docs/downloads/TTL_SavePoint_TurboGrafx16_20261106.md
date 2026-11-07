# TTL SavePoint

Cartridge 004 for TurboGrafx-16 and PC Engine HuCards on MiSTer. Build `261106SP1` is the stable save-state track. It offers four manual slots, F5/F8 and optional CPU Turbo (+20% and +50%). Rewind has been removed.

## Install and save

1. Back up the stock RBF and your `saves` and `savestates` folders. Start with a test card and a separate copy of your game progress.
2. Copy `TTL_SavePoint_TurboGrafx16_20261106.rbf` to `_Console` and launch it. Start with a HuCard such as Ninja Spirit, SDRAM ROM storage, and the default settings.
3. Keep your existing MiSTer Main. The core uses MiSTer’s standard four-slot SD save-state interface.
4. Select a slot under **Save States (HuCard)**. Press **F5** to save and **F8** to load with the menu closed. The menu provides the same actions.
5. Give MiSTer time to finish writing the save state before resetting, reloading the core, switching games or powering off. Restore with the same ROM, slot and configuration.

This build uses protocol 3. Earlier experimental formats use separate files. Save states are for supported HuCard configurations. Change CPU Turbo before creating a snapshot and use the same setting when restoring it.

## Validation

The preceding full-image build ran on the owner’s MiSTer and Sony CRT. The owner reported stable sync through manual save/load and confirmed that CPU Turbo works. SavePoint derives from that source and retains its manual snapshot format and video alignment. This RBF awaits its own physical MiSTer and SD power-cycle tests.

The [source ZIP](TTL_SavePoint_TurboGrafx16_20261106_source.zip) includes the corresponding core source, licenses, and build evidence. Verify the downloads with the [SHA-256 list](TTL_SavePoint_TurboGrafx16_20261106.sha256).
