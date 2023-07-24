#!/usr/bin/env bash

set -x

# Check python tests
cd python
python3 -m unittest discover
cd ..

# Build cpp code
git submodule update --init
mkdir build
cd build
cmake ..
make -j4
cp cpp/*.so ../python/tests
cd ..

# Test pybind module against python tests
cd python/tests
python3 -m unittest discover
rm *.so

