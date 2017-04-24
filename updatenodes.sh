#!/bin/bash

: ${HOSTNAME?}

FILE="node.py"

COMMANDS=("scp ${FILE} pan01.local:."
"scp ${FILE} pan02.local:."
"scp ${FILE} pan03.local:."
"scp ${FILE} pan04.local:."
"scp ${FILE} pan05.local:."
"scp ${FILE} pan06.local:."
"scp ${FILE} pan07.local:."
"scp ${FILE} pan08.local:.")

for cmd in "${COMMANDS[@]}"; do {
  echo "Process \"$cmd\" started";
  $cmd & pid=$!
  PID_LIST+=" $pid";
} done

trap "kill $PID_LIST" SIGINT

echo "Parallel processes have started";

wait $PID_LIST

echo
echo "$HOSTNAME is done";
