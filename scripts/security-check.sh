#!/bin/sh
cd "$(git rev-parse --show-toplevel)" || exit
[ -d venv ] && . d3fend-venv/bin/activate

bandit  -r ./d3fend.py
