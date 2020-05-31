#!/usr/bin/env bash

if [ $# -ne 1 ]; then
  echo "You must provide the version number."
  exit 1
fi

rm -rf dist/ build/ *.egg-info/

RELEASE_VERSION=$1 python3 setup.py sdist bdist_wheel

python3 -m twine upload --repository testpypi dist/apc-ipmi-monitor-ericbo-$1*