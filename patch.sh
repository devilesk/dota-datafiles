#!/bin/bash
# update.sh

if [ -n "$1" ]; then
    cd build
    python3 parser.py --make_dirs --dotabuff --process
    cd ..
    git add dist
    git add source
    git commit -m $1
    npm version minor
    git push
    npm publish
else
    echo "missing patch"
fi