#!/bin/sh

cp .env.example .env

for dir in "tfttraits" "tfttraits/grid" "tfttraits/table" "tftitems" "tftitems/craft-vs-radiant" "tftitems/grid" "tftaugs"
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

for sfile in "parse_traits_grid" "parse_traits_table" "parse_items" "parse_augments"
do
    $cmdof $sfile.py
done