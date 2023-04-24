#!/bin/bash

SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
echo $SCRIPTPATH

while [ 1 ]; do
  python3 "$SCRIPTPATH/suspender.py"
done