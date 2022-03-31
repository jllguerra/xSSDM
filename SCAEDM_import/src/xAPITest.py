from httpdclient import httpdclient
import os
from pathlib import Path
import inspect
import logging
import sys, getopt

class xAPITest():
    
   # Inicializacion
    def __init__(self):
      self.yo="yo"
    # Programa principal
    def main(self):
        # Arguments
      httpdclientI=httpdclient.httpdclient("manchf","cae12345")
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
      result=httpdclientI.execAPIfunction("AddSimFromFile", "")
      print(result)

      
      
        

# Inicio Aplicacion  
if __name__=='__main__':
    app = (xAPITest)
    app.main(sys.argv[1:])
    
