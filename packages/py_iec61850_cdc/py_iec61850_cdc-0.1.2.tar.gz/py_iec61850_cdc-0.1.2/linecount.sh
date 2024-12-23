#!/bin/bash
#

echo "src/ line count:"
find src/ -name '*.py' | xargs wc -l
echo "tests/ line count:"
find tests/ -name '*.py' | xargs wc -l

