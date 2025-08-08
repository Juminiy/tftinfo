#!/bin/bash

files=$(ls -lSh | head -n 7 | tail -n 6 | awk '{print $9}')

for filename in $files;
do
    echo $filename
    ffmpeg -i $filename -q:v 30 $filename.png
    rm -rf $filename
done