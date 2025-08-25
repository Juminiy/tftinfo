#!/bin/bash

if [ ! -f ".env" ]; then
    cp .env.example .env
fi

dirs=(
"tftaugs" "tftaugs/icon" "tftaugs/md"
"tftchampions" "tftchampions/icon" "tftchampions/md"
"tftitems" "tftitems/craft-vs-radiant" "tftitems/icon" "tftitems/md"
"tfttraits" "tfttraits/comp" "tfttraits/icon"
"tftspecs" "tftspecs/icon"
"tftmd" "tftmd/rewards"
)
for dir in ${dirs[@]}
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

pyfiles=(
"parse_augments"
"parse_champions"
"parse_items"
"parse_traits_grid"
"parse_traits_table"
"parse_special"
"meta_tft"
)
for sfile in ${pyfiles[@]}
do
    $cmdof $sfile.py
done