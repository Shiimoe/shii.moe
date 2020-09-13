#!/bin/sh

FLASK_APP=server.py flask run
echo "$!" > ./.pid

echo "Shii.moe is online!"