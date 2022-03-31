#!/usr/bin/env python
# encoding: utf-8
def initialize(): 
    global SSDM_SERVER 
    global SSDM_PORT 
    global SSDM_SERVER_URL 
    global SSDM_AUTO 
    SSDM_SERVER_DES = "https://ssdm.des.seat.vwg" 
    SSDM_PORT_DES = "8445" 
    
    SSDM_SERVER_CNS = "https://scaedm004.cns.seat.vwg" 
    SSDM_SERVER_CNS = "https://scaedm005.cns.seat.vwg" 
    SSDM_PORT_CNS = "443" 
    
    SSDM_SERVER_PRD = "https://scaedm.prd.seat.vwg" 
    SSDM_PORT_PRD = "443" 

    SSDM_SERVER = SSDM_SERVER_DES 
    SSDM_PORT=SSDM_PORT_DES
    SSDM_SERVER_URL = SSDM_SERVER+":"+SSDM_PORT+"/SCAEDM_AUTO/HttpsServer/httpdsserver.php"
    SSDM_AUTO=1

       