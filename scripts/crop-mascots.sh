#!/usr/bin/bash

shopt -s extglob

DIR="$1"
[ -z "$DIR" ] && DIR='./public/mascots'

for file in "$DIR"/+([0-9]).png; do
	echo "$file -> ${file:0:-4}-square.png"
	convert "$file" -gravity Northwest -crop 1:1 "${file:0:-4}-square.png"
done

echo -e "\nDone."
