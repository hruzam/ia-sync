#!/usr/bin/env zsh
# Lazy runner: the dispatcher executes this file only on explicit invocation.
exec python3 -B "${0:A:h}/source-reader.py" "$@"
