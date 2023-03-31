#!/bin/env bash

ORGDIR=$(pwd)

if $(command -v deactivate); then
    deactivate
fi

BASEDIR=$(dirname "$0")
cd $BASEDIR
rm -rf .venv
cd $ORGDIR

rm -rf gen
rm -rf build
rm -rf .vscode
rm -rf usage_demo/.vscode
rm -rf usage_demo/build
rm -rf usage_demo/CMakeLists.txt.user