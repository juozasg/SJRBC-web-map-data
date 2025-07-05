#!/usr/bin/env bash
SOURCE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SOURCE_DIR"

python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt