#!/usr/bin/env bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 <cube_id1> <cube_id2> ..."
    echo "Example: $0 8 9 10 11"
    exit 1
fi

echo "Starting cubes: $@"

core=0
num_cores=$(nproc)  # Detect number of available CPUs

for i in "$@"; do
    echo "Starting cube $i on CPU core $core..."
    # Pin process to specific core and run in background
    nohup taskset -c $core ./3dsudoku "$i" >out-cube"$i".txt 2>&1 &
    
    # Increment core, wrap around if more processes than cores
    core=$(( (core + 1) % num_cores ))
done

echo "All processes started."
