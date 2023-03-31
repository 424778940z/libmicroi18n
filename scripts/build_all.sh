#!/bin/env bash

ORGDIR=$(pwd)

./scripts/cleanup.sh
./scripts/bootstrap.sh

source ./scripts/.venv/bin/activate
./scripts/generate.py
deactivate

cd ./gen
# host native library
cmake -S ./library -B build
cmake --build build
# arm-none library
cmake -S ./library -B build_arm-none -DCMAKE_EXE_LINKER_FLAGS_INIT=--specs=nosys.specs -DCMAKE_C_COMPILER=arm-none-eabi-gcc
cmake --build build_arm-none
cd $ORGDIR

cd ./usage_demo
# host native only
cmake -S . -B build
cmake --build build
cd $ORGDIR