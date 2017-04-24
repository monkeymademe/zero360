#!/bin/bash

: ${HOSTNAME?}

COMMANDS=("scp * pan01.local:."
"scp * pan02.local:."
"scp * pan03.local:."
"scp * pan04.local:."
"scp * pan05.local:."
"scp * pan06.local:."
"scp * pan07.local:."
"scp * pan08.local:.")

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
