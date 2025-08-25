#!/bin/sh

if [ ! -f ".env" ]; then
    cp .env.example .env
fi

for dir in "tftaugs" "tftitems" "tftitems/craft-vs-radiant" "tfttraits" "tfttraits/comp" "tftspecs" "tftmd"
do
    # rm -rf $dir
    mkdir -p $dir
done

cmdof="uv run"
uv version
if [ $? -ne 0 ]; then
    echo "error: uv cmd NOTFOUND"
    exit 1
fi

for sfile in "parse_augments" "parse_champions" "parse_items" "parse_traits_grid" "parse_traits_table" "parse_special" "meta_tft"
do
    $cmdof $sfile.py
done