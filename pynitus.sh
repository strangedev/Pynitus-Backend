#!/bin/bash

if [ ! -f .pynitus_venv ]
then
    virtualenv .pynitus_venv
fi

source .pynitus_venv/bin/activate
export FLASK_APP=Pynitus
pip install -e .

memcached -d -m 512 -l 127.0.0.1 -p 11211
(
    sleep 1
    echo "flush_all"
    sleep 1
    echo "quit"
) | telnet localhost 11211

flask run