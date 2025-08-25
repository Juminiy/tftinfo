# tftinfo
tft info details, txt and json, process.py

## CreateENV (Must RUN)
```bash
uv venv
source .venv/bin/activate
uv sync
```

## RUN metatftapi
```bash
cd metatftapi
./run.sh

# redownload metatftapi data
uv run req_raw.py
# refresh parsed data
./run.sh
```

## RUN tftapi
```bash
# refresh parsed data
cd tftapi
./run.sh

# redownload tftapi data
uv run req_raw.py
# redownload tftapi icon
uv run req_icon.py
# refresh parsed data
./run.sh
```