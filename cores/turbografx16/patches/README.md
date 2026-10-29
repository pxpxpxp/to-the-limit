# Focused RTL patches

Apply to upstream commit `827d45f45799b8ab3a536510847f2108a92e81bd` in order:

```sh
git apply 0001-cpu-turbo.patch
git apply 0002-extra-default.patch
```

`0001` is the CPU Turbo implementation in the initial binary. `0002` changes the sprite option to use new status bit 41, where 0 means Extra and 1 means Normal. Bit 11 is reserved so saved settings from the earlier encoding are not silently inverted. CPU Turbo still defaults to Off.

The new sprite option is `P1o9` (32+9 = status bit 41). Extra is the first menu option and its hardware signal is `~status[41]`. It remains possible to select and save Normal.

These focused patches cover production RTL only. Use the complete source archive for tests, build settings, Quartus 23 PLL QIP alias, host compatibility tooling and full upstream source/licenses. The initial `TurboGrafx16_20261029.rbf` does not contain patch 0002. The current `TurboGrafx16_TTL_20261029.rbf` includes both patches and passed its fresh build and constrained multi-corner timing checks.
