#!/bin/bash

: ${HOSTNAME?}

COMMANDS=("ssh pan01.local './rebootnode.sh'"
"ssh pan02.local './rebootnode.sh'"
"ssh pan03.local './rebootnode.sh'"
"ssh pan04.local './rebootnode.sh'"
"ssh pan05.local './rebootnode.sh'"
"ssh pan06.local './rebootnode.sh'"
"ssh pan07.local './rebootnode.sh'"
"ssh pan08.local './rebootnode.sh'")

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
