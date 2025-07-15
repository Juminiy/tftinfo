#!/bin/sh

for dir in "tfttraits" "tfttraits/grid" "tfttraits/grid/table" "tfttraits/table" "tftitems" "tftitems/craft-vs-radiant" "tftitems/grid"
do
    rm -rf $dir
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