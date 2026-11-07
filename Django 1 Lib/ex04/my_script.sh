#!/usr/bin/env bash

# Source this script so the environment stays active in the calling shell.
if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    printf 'Usage: source %q\n' "$0" >&2
    exit 1
fi

prepare_django_environment() {
    local exercise_directory python_command environment_directory
    exercise_directory="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)" || return
    python_command="${PYTHON:-python3}"
    environment_directory="$exercise_directory/django_venv"
    "$python_command" -m venv "$environment_directory" || return
    if [[ -f "$environment_directory/bin/activate" ]]; then
        source "$environment_directory/bin/activate" || return
    elif [[ -f "$environment_directory/Scripts/activate" ]]; then
        source "$environment_directory/Scripts/activate" || return
    else
        printf 'Error: virtual environment activation script is missing.\n' >&2
        return 1
    fi
    python -m pip install --requirement "$exercise_directory/requirement.txt" || return
    printf 'Virtual environment active: %s\n' "$VIRTUAL_ENV"
}

prepare_django_environment
