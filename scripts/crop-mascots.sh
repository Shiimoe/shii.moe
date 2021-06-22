#!/bin/bash

shopt -s extglob

for file in mascots/+([0-9]).png; do
	echo "$file -> ${file:0:-4}-square.png"
	convert "$file" -gravity Northwest -crop 1:1 "${file:0:-4}-square.png"
done

echo -e "\nDone."
