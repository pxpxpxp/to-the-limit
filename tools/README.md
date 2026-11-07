# Repository tools

## Check the repository

Run from any directory with Python 3.10 or newer:

```sh
python3 tools/check_repository.py
python3 -m unittest discover -s tools -p 'test_*.py'
```

Use the script's full path if your working directory is elsewhere. The checker reads local links and assets, release/source pairs, SHA-256 manifests and ZIP integrity. It does not check external websites, modify release files, compile FPGA source or establish hardware compatibility.

## Regenerate the pixel font

`make_pixel_font.py` generates the original 5×7-grid website font at `docs/assets/limit-pixel-mono.woff`. It requires the optional `fonttools` package; repository checks do not.

```sh
python3 -m pip install -r tools/requirements-font.txt
python3 tools/make_pixel_font.py
```

Review the generated font before committing it. The website loads this single canonical font file from `docs/style.css`.
