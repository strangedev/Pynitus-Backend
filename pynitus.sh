#!/bin/bash

if [ ! -f .pynitus_venv ]
then
    virtualenv .pynitus_venv
fi

source .pynitus_venv/bin/activate
export FLASK_APP=Pynitus
pip install -e .
flask run