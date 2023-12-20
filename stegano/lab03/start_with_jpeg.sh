#!/bin/bash

if [ $1 -eq 0 ]
then
    python3 lab03/main.py $1
    python3 lab03/bmp_to_jpg.py
    python3 lab03/main_decode.py 1 $1
else
    python3 lab03/main.py $1 >> lab03/logs/encode.txt
    python3 lab03/bmp_to_jpg.py
    python3 lab03/main_decode.py 1 $1 >> lab03/logs/decode.txt
fi