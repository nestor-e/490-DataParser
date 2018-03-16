#!/bin/bash

SNER_PATH=${1:-../sner}
MODEL=${2:-rdf}
ATF=ur3_20110805_public.atf
DATA_PATH=${PWD}/


rm *.RT *.KEY *.sparseX 2>/dev/null

pushd $SNER_PATH

python3 -m sner  -r export -p $DATA_PATH
python3 -m sner  -r export-atf -p $DATA_PATH -c $ATF
python3 -m sner -r $MODEL -atf True -p $DATA_PATH

popd
