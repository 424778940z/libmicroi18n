#!/bin/env bash

ORGDIR=$(pwd)

BASEDIR=$(dirname "$0")
cd $BASEDIR
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
cd $ORGDIR