#!/bin/bash

files=$(ls -lSh | head -n 11 | tail -n 10 | grep "M" | awk '{print $9}')

for filename in $files;
do
    echo $filename
    ffmpeg -i $filename -q:v 30 modify-$filename
    mv modify-$filename $filename
done