#!/bin/bash

: ${HOSTNAME?}

COMMANDS=("ssh pan01.local './haltnode.sh'"
"ssh pan02.local './haltnode.sh'"
"ssh pan03.local './haltnode.sh'"
"ssh pan04.local './haltnode.sh'"
"ssh pan05.local './haltnode.sh'"
"ssh pan06.local './haltnode.sh'"
"ssh pan07.local './haltnode.sh'"
"ssh pan08.local './haltnode.sh'")

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
