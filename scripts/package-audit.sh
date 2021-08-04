#!/bin/sh
cd "$(git rev-parse --show-toplevel)" || exit
[ -d venv ] && . d3fend-venv/bin/activate

safety check -r requirements.txt
