#!/bin/bash

export XCSBHOME=/usr2/applications/caesubmit3/X

export PATH=${XCSBHOME}/tools/Python-3.7.2/bin:${PATH}
export PYTHONPATH=${XCSBHOME}/tools/Python-3.7.2/lib/python3.7
export LD_LIBRARY_PATH=${XCSBHOME}/tools/Python-3.7.2/lib:${LD_LIBRARY_PATH}

if [  $# -eq 1 ] 
then
	python3 ./src/ssdm_import.py -i='$1'
else
	echo "Invalid parameters"
	echo "$0 <file>"
fi
