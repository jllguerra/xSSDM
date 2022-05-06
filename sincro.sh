#!/bin/bash


if [ "$#" -ne 1 ] ; then
    echo "sindro [DES|CNS|PRD]"
    exit
fi
if [ $1 == "DES" ] ; then
    echo "Sincronizando xSSDM Servidor de DESARROLLO 10.201.160.102 en SCAEDM_import"
    echo ""
    rsync -av * --exclude-from sincro_exclude.txt ssdm@ssdm:/data/ssdm/SCAEDM_import
    echo ""
elif [ $1 == "CNS" ]; then
    echo "Sincronizando xSSDM Servidores de CONSOLIDACION scaedm004.cns.seat.vwg en SCAEDM_import"
    echo ""
    rsync -av * --exclude-from sincro_exclude.txt ssdm@scaedm004.cns.seat.vwg:/data/ssdm/SCAEDM_import
    echo ""
    echo "Sincronizando xSSDM Servidor de CONSOLIDACION scaedm005.cns.seat.vwg en SCAEDM_import"
    echo ""
    rsync -av * --exclude-from sincro_exclude.txt ssdm@scaedm005.cns.seat.vwg:/data/ssdm/SCAEDM_import
    echo ""
elif [ $1 == "PRD" ]; then
    echo "Sincronizando xSSDM Servidores de CONSOLIDACION scaedm030.cns.seat.vwg en SCAEDM_import"
    echo ""
    rsync -av * --exclude-from sincro_exclude.txt ssdm@scaedm030.prd.seat.vwg:/data/ssdm/SCAEDM_import
    echo ""
    echo "Sincronizando xSSDM Servidor de CONSOLIDACION scaedm031.prd.seat.vwg en SCAEDM_import"
    echo ""
    rsync -av * --exclude-from sincro_exclude.txt ssdm@scaedm031.prd.seat.vwg:/data/ssdm/SCAEDM_import
    echo ""
elif [ $1 == "PRD" ]; then
    echo "Sincronizando Servidores de PRODUCCION"
elif [ $1 == "CLI" ]; then
    echo "Sincronizando cliente"
    rsync -av * --exclude-from sincro_exclude.txt caeapps@vic:/usr2/applications/xSCAEDM
elif [ $1 == "CLI.CNS" ]; then
    echo "Sincronizando cliente"
    rsync -av * --exclude-from sincro_exclude.txt caeapps@vic:/usr2/applications/xSCAEDM/cns
elif [ $1 == "CLI.PRD" ]; then
    echo "Sincronizando cliente"
    rsync -av * --exclude-from sincro_exclude.txt caeapps@vic:/usr2/applications/xSCAEDM/prd
else
    echo "sindro [DES|CNS|PRD]"
fi
