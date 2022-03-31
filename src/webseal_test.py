from httpdclient import httpdclient
import os
from pathlib import Path
import inspect
import logging
import sys, getopt
import urllib.request
import requests
import ssl
import pkcs11
from pkcs11 import Attribute, ObjectClass
from asn1crypto import x509, pem, keys
from pkcs11.util.rsa import encode_rsa_public_key
import tempfile
from Cython.Shadow import array
import base64
from M2Crypto import m2urllib2 as urllib2
from M2Crypto import m2, SSL, Engine

class xAPITest():
    
  # Inicializacion
  def __init__(self):
    self.url="https://ssdm.des.seat.vwg:8445/secure/index.php"
    self.server="https://ssdm.des.seat.vwg:8445/secure"
    self.yo="yo"
    self.username="manchf"
    self.clave="cae12345"
      
    self.error=0
    self.msg=""
    self.PubKey=""
#      self.error=self.readCard(pin)
    # Programa principal
  def main(self):
#e = Engine.load_dynamic_engine("pkcs11", "/usr/lib/x86_64-linux-gnu/engines-1.1/libpkcs11.so")
#    e = Engine.load_dynamic_engine("pkcs11", "/usr/lib64/security/pam_pkcs11.so")
    e = Engine.load_dynamic_engine("pkcs11", "/home/manchf/pkcs11/libp11-master/lib/libpkcs11.so")
    pk = Engine.Engine("pkcs11")
#    pk.ctrl_cmd_string("MODULE_PATH", "/usr/lib/libeTPkcs11.so")
    pk.ctrl_cmd_string("MODULE_PATH", "/opt/itp11/libitp11_1.0.3.0.so.1")

    m2.engine_init(m2.engine_by_id("pkcs11"))
    pk.ctrl_cmd_string("PIN", '447161')
    name='pkcs11:id=323439323638373430363132353932333430'
    cert=pk.load_certificate(name)
#    cert = pk.load_certificate('pkcs11:model=;manufacturer=;serial=;'
#                        'token=;id=;'
#                        'object=')
#    key = pk.load_private_key('pkcs11:model=XXX;manufacturer=YYYYY;serial=ZZZZ;'
#                        'token=AAAAA;id=BBBBBBBBB;'
#                        'object=CCCCCC', pin='447161')
    
    name='pkcs11:object='+CKO_PRIVATE_KEY
    key = pk.load_private_key(name,pin='447161')

    ssl_context = SSL.Context('tls')
    ssl_context.set_cipher_list('EECDH+AESGCM:EECDH+aECDSA:EECDH+aRSA:EDH+AESGCM:EDH+aECDSA:EDH+aRSA:!SHA1:!SHA256:!SHA384:!MEDIUM:!LOW:!EXP:!aNULL:!eNULL:!PSK:!SRP:@STRENGTH')
    ssl_context.set_default_verify_paths()
    ssl_context.set_allow_unknown_ca(True)

    SSL.Connection.postConnectionCheck = None

    m2.ssl_ctx_use_x509(ssl_context.ctx, cert.x509)
    m2.ssl_ctx_use_pkey_privkey(ssl_context.ctx, key.pkey)

    opener = urllib2.build_opener(ssl_context)
    urllib2.install_opener(opener)

    url = 'https://yourserver/endpoint'

    content = urllib2.urlopen(url=url).read()
# content = opener.open(url)
    print(content)
      
      
        

# Inicio Aplicacion  
if __name__=='__main__':
    app = (xAPITest)
    app.main(sys.argv[1:])
    
