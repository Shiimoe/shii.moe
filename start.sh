#!/bin/sh

FLASK_APP=server.py flask run --host=0.0.0.0 --port=5000 &
echo "$!" > ./.pid

echo "Shii.moe is online!"