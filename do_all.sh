#!/usr/bin/env bash
for i in {8..18}; do
    nohup ./3dsudoku $i >out-cube$i.txt &
done
