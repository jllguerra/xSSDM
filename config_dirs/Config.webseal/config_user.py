#!/usr/bin/env python
# encoding: utf-8
def initialize(): 
    global SSDM_SERVER 
    global SSDM_PORT 
    global SSDM_SERVER_URL 
    global SSDM_AUTO 
    global SSDM_ENV
    SSDM_SERVER_DES = "https://ssdm.des.seat.vwg" 
    SSDM_PORT_DES = "8445" 
    SSDM_ENV_DES = "Development Environment"
    
    SSDM_SERVER_CNS = "https://scaedm.cns.seat.vwg" 
    SSDM_PORT_CNS = "443" 
    SSDM_ENV_CNS = "Consolidation Environment"
    
    SSDM_SERVER_PRD = "https://scaedm.prd.seat.vwg" 
    SSDM_PORT_PRD = "443" 
    SSDM_ENV_PRD = "Producion Environment"

    SSDM_SERVER = SSDM_SERVER_DES 
    SSDM_PORT = SSDM_PORT_DES
    SSDM_ENV = SSDM_ENV_DES

    SSDM_SERVER_URL = SSDM_SERVER+":"+SSDM_PORT+"/SSDM/HttpsServer/httpdsserver.php"
    SSDM_AUTO=0


       