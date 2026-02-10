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

# Set Update
1. update raw data and icon data
```bash
# redownload tftapi data
uv run req_raw.py
# redownload tftapi icon
uv run req_icon.py
# refresh parsed data
./run.sh
```

2. tftapi/meta_data.py:setname,setopentime
3. tftapi/meta_func.py:select_traits_legal