#!/bin/bash

if [ $1 -eq 0 ]
then
    echo 'start encoding'
    python3 lab03/main.py $1
    echo 'start decoding'
    python3 lab03/main_decode.py 0 $1
else
    echo 'start encoding'
    python3 lab03/main.py $1 >> lab03/logs/encode.txt
    echo 'start decoding'
    python3 lab03/main_decode.py 0 $1 >> lab03/logs/decode.txt
fi

python3 lab03/check_bits.py