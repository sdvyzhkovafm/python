#!/bin/bash
virtualenv venv
source ./venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install ipykernel