#!/bin/bash
# fix.sh

if [ -n "$1" ] && [ -n "$2" ]; then
    cd build
    python3 parser.py --make_dirs --dotabuff --process --dotabuff_branch $2
    cd ..
    git add dist
    git add source
    git commit -m $1
    npm version minor
else
    echo "missing args"
fi