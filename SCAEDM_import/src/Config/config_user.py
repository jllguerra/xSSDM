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
    
    SSDM_SERVER_CNS = "https://scaedm004.cns.seat.vwg" 
    SSDM_PORT_CNS = "8444" 
#     SSDM_SERVER_CNS = "http://scaedm004.cns.seat.vwg" 
#     SSDM_SERVER_CNS = "http://scaedm005.cns.seat.vwg" 
#     SSDM_PORT_CNS = "8080" 
#     SSDM_PORT_CNS = "80" 
    SSDM_ENV_CNS = "Consolidation Environment"
    
    SSDM_SERVER_PRD = "https://scaedm.prd.seat.vwg" 
    SSDM_PORT_PRD = "8444" 
    SSDM_ENV_PRD = "Producion Environment"

    SSDM_SERVER = SSDM_SERVER_CNS 
    SSDM_PORT = SSDM_PORT_CNS
    SSDM_ENV = SSDM_ENV_CNS
    #SSDM_SERVER = "https://10.201.160.102:8444/SSDM" 
    #SSDM_SERVER_URL="https://ssdm.des.seat.vwg:8445/secure/index.php"
    SSDM_SERVER_URL = SSDM_SERVER+":"+SSDM_PORT+"/SSDM/HttpsServer/httpdsserver.php"
    SSDM_AUTO=0


       
