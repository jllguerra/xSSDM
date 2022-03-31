#!/bin/bash

export APPSHOME=/apps/ssdm-servers/ 

export PYTHONPATH=${APPSHOME}/python
export PATH=${PYTHONPATH}/bin:${PATH}
export LD_LIBRARY_PATH=${PYTHONPATH}/lib:${LD_LIBRARY_PATH}

if [  $# -eq 1 ] 
then
	python3 /data/ssdm/SCAEDM_import/src/ssdm_import.py -i=$1
else
	echo "Invalid parameters"
	echo "$0 <file>"
fi
