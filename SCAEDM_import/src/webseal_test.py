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
      url="https://ssdm.des.seat.vwg:8445/secure/index.php"
      context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

#      context = ssl._create_unverified_context()

      lib = pkcs11.lib('/opt/itp11/libitp11.so')
      token = lib.get_token()
      
      pin="796083"
      PubKey=""
      PrivKey=""
      
      try:
        with token.open(user_pin=pin) as session:
          for pub_key in session.get_objects({Attribute.CLASS: ObjectClass.PUBLIC_KEY}):
            if (PubKey==""):
              public_key = keys.RSAPublicKey.load(encode_rsa_public_key(pub_key))
              print(public_key)
              PubKey = pem.armor('PUBLIC_KEY', encode_rsa_public_key(pub_key))
              print(PubKey)                    
          
          for priv_key in session.get_objects({Attribute.CLASS: ObjectClass.PRIVATE_KEY}):
            if (PrivKey==""):
              private_key = keys.RSAPrivateKey.load(encode_rsa_public_key(priv_key))
              print(private_key)
              PrivKey = pem.armor('PRIVATE_KEY', encode_rsa_public_key(priv_key))                    
              print(PrivKey)
                                  
          Cert_pem=""      
          for cert in session.get_objects({Attribute.CLASS: ObjectClass.CERTIFICATE,}):
            #crt=cert[Attribute.VALUE]
            print (cert)
            if (Cert_pem == ""):
              der_bytes = cert[Attribute.VALUE]
              # Load a certificate object from the DER-encoded value
              x509_cert=x509.Certificate.load(der_bytes)
                     
              issuer=x509_cert.issuer
              subject=x509_cert.subject
              CN_issuer=issuer.native['common_name']
              CN_subject=subject.native['common_name']
              print (CN_issuer + " " + CN_subject)
              if CN_issuer == 'VW-CA-ENCN-01':
                Cert=x509_cert
                print(Cert)
                Cert_pem = pem.armor('CERTIFICATE', der_bytes) 
                print(Cert_pem)       
                
#                Cert_pem = pem.armor('PRIVATE KEY', der_bytes)
#                print(Cert_pem)       
              print (x509_cert.native['tbs_certificate'])
                     # Write out a PEM encoded valu.
      except pkcs11.exceptions.PinIncorrect:
        self.msg="Pin incorrecto"
        return 1
      except pkcs11.exceptions.ArgumentsBad:
        #pin vacio
        self.msg="Pin vacio"
        return 2
      except pkcs11.exceptions.NoSuchToken:
        #no detecta tarjeta
        self.msg="Tarjeta no detectada"
        return 3

      context.load_cert_chain("/home/manchf/tmp/cert","/home/manchf/tmp/key" , pin)
#      context.load_cert_chain(token, token, pin)
      httpsHandler = urllib.request.HTTPSHandler(context = context)
      manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
#      manager.add_password(None,self.server , self.username, self.clave)
      authHandler = urllib.request.HTTPBasicAuthHandler(manager)
#      authHandler = urllib.request.HTTPAuthHandler(manager)
      opener = urllib.request.build_opener(httpsHandler)
      opener = urllib.request.build_opener()
      urllib.request.install_opener(opener)
      postdata={"accion":"conectar"}
            #print(postdata)
      postdataencode=urllib.parse.urlencode(postdata).encode('utf-8')
      urlpostmethod = urllib.request.Request(url,data=postdataencode )
      urlreturn=urllib.request.urlopen(urlpostmethod)
      result=urlreturn.read().decode('utf-8');
      
      print(result)
      postdata={"login-form-type":"cert","token":"e0cf0b68-b4bc-11eb-a444-005056a15061"}
      postdataencode=urllib.parse.urlencode(postdata).encode('utf-8')
      urlpostmethod = urllib.request.Request("https://am.seat.vwgroup.com:444/pkmslogin.form",data=postdataencode)
      urlreturn=urllib.request.urlopen(urlpostmethod)
      result=urlreturn.read().decode('utf-8');
      print(result)

   # Arguments
#      httpdclientI.conectar()
#      httpdclientI.execAPIfunction("conectar", dict())
#      result=httpdclientI.execAPIfunction("getuserprojects", dict())
#      print(result)
#      result=httpdclientI.execAPIfunction("getdisciplinas", dict())
#      print(result)
#      result=httpdclientI.execAPIfunction("getsubdisciplinas", dict())
#      print(result)
#      result=httpdclientI.execAPIfunction("getloadcases", dict())
#      print(result)
#      httpdclientI.execAPIfunction("gettipos", dict())
#      result=httpdclientI.execAPIfunction("AddSimFromFile", "")
      print(result)

      
      
        

# Inicio Aplicacion  
if __name__=='__main__':
    app = (xAPITest)
    app.main(sys.argv[1:])
    
