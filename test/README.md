## Test setup

Create a virtual environment:

```bash
uv venv --python 3.14 .venv
call .venv\Scripts\activate
```

Install the built wheel:

```bash
uv pip install --force-reinstall --no-index --find-links dist oead
```

Install the test dependencies:

```bash
uv pip install pytest
```

## Running tests

Run the functional tests:

```bash
python -m pytest test\aamp\test_aamp_empty_strings.py test\aamp\test_aamp_roundtrip.py test\byml\test_byml_roundtrip.py test\gsheet\test_gsheet_roundtrip.py test\sarc\test_sarc_get_file.py test\sarc\test_sarc_roundtrip.py test\yaz0\test_yaz0.py test/aamp/test_parameter_map.py
```

Run the full test suite, including benchmarks:

```bash
python -m pytest -q test
```
