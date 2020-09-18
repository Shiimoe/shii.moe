#!/bin/sh

uwsgi --ini shiimoe.ini &
echo "$!" > ./.pid

echo "Shii.moe is online!"
