#!/usr/bin/env bash
SOURCE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SOURCE_DIR"
export PYTHONPATH="$SOURCE_DIR/.."
../.venv/bin/python3 tolthawk-login.py