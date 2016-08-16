#!/bin/sh
INPUT=$1
OUTPUT=$2

#insert colorize script here
sleep 4
cp $INPUT $OUTPUT
sips -f horizontal $OUTPUT
rm $INPUT