#!/bin/bash

files=$(ls -lSh | head -n 11 | tail -n 10 | awk '{print $9}')

for filename in $files;
do
    echo $filename
    ffmpeg -i $filename -q:v 30 $filename
    rm -rf $filename
done