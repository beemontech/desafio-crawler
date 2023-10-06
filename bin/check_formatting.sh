#!/bin/sh
SRC=crawler/
LINE_LENGTH=109

# Check for black formatting errors
black --line-length $LINE_LENGTH --check $SRC
if [ $? -ne 0 ]; then
    exit 1
fi

# Auto-check for pep8 so I don't check in bad code
if [ -n "$SRC" ]; then
    flake8 --max-line-length $LINE_LENGTH $SRC
fi
