#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
python_command="${PYTHON:-python3}"
"$python_command" -m pip --version
"$python_command" -m pip install --upgrade --target "$PWD/local_lib" \
    --log "$PWD/install.log" 'git+https://github.com/jaraco/path.git'
PYTHONPATH="$PWD/local_lib${PYTHONPATH:+:$PYTHONPATH}" \
    "$python_command" my_program.py
