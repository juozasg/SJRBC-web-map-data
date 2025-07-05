#!/usr/bin/env bash
SOURCE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SOURCE_DIR"
export PYTHONPATH="$SOURCE_DIR/.."
../.venv/bin/python3 update-db.py

# ping webservice to reload data
curl localhost:5003/reload-database