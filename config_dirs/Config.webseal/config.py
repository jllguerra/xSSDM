#!/usr/bin/env python
# encoding: utf-8
import Config.config_auto as Globals_auto;
import Config.config_user as Globals_user;
from pathlib import Path


DOWNLOAD_DIR="SCAEDM_downloads"
TMP_DIR= str(Path.home())


def initialize(auto): 
    global DOWNLOAD_DIR
    global TMP_DIR
    global SSDM_SERVER 
    global SSDM_PORT 
    global SSDM_SERVER_URL 
    global SSDM_AUTO
    global SSDM_ENV
    if (auto):
        Globals_auto.initialize();
        SSDM_SERVER=Globals_auto.SSDM_SERVER;
        SSDM_PORT=Globals_auto.SSDM_PORT;
        SSDM_SERVER_URL=Globals_auto.SSDM_SERVER_URL;
        SSDM_AUTO=Globals_auto.SSDM_AUTO;
    else:
        Globals_user.initialize();
        SSDM_SERVER=Globals_user.SSDM_SERVER;
        SSDM_PORT=Globals_user.SSDM_PORT;
        SSDM_SERVER_URL=Globals_user.SSDM_SERVER_URL;
        SSDM_AUTO=Globals_user.SSDM_AUTO;
        SSDM_ENV=Globals_user.SSDM_ENV;
      