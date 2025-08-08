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

# reload metatftapi data
uv run req_raw.py
# refresh parsing data
./run.sh
```

## RUN tftapi
```bash
cd tftapi
./run.sh

# reload tftapi data
uv run req_raw.py
# reload tftapi icon
# refresh parsing data
./run.sh
```