#!/bin/sh

rm -rf dist
rm -rf build
python3 -m build
twine check dist/*
python3 -m twine upload --repository testpypi dist/*
