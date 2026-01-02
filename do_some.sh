#!/usr/bin/env bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <cube_id1> <cube_id2> ..."
    echo "Example: $0 8 9 10 11"
    exit 1
fi

echo "Starting cubes: $@"
for i in "$@"; do
    echo "Starting cube $i..."
    nohup ./3dsudoku $i >out-cube$i.txt &
done
echo "All processes started."
