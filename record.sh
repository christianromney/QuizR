#!/usr/bin/env bash
set -e
say -v Samantha -r 30 -o $1 $2
lame -m m $1.aiff $1.mp3
rm -f $1.aiff
