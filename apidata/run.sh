#!/bin/sh

for dir in "tftgrid" "tfttraits" "tftitems"
do
    mkdir -p $dir
done

cmdof="uv run"
uv version
if [ $? -ne 0 ]; then
    echo "error: uv cmd NOTFOUND"
    exit 1
fi

for sfile in "parse_grid" "parse_traits" "parse_items"
do
    $cmdof $sfile.py
done