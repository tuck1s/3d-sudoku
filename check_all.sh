#!/usr/bin/env bash
for i in {8..18}; do
    grep --with-filename "^--- " out-cube$i.txt
done
