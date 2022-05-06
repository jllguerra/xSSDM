import sys, getopt, os, getpass, logging, inspect
from Soft.User import User
from Soft.Simulacion import Simulacion
from FileTransfer.SimFiles import SimFiles
from Soft.DB import DB
from pathlib import Path
import Config.config as Globals
from Config.config import TMP_DIR
import argparse
import shutil
import re

class ssdm_import():
    def upload_simulation(self,file):
        result=""
        # check STO
        if not os.path.exists(self.User.Profile['sto']): return "STO " + self.User.Profile['sto'] + " doesn't exist"
        if not os.path.exists(file): return "The file " + file +" doesn't exist"
        
        # check structure
        self.Sim = Simulacion()
        self.Sim.Filename=file
        self.Sim.soft=self.soft;
        self.Sim.Name=Path(self.Sim.Filename).stem
#        if not self.Sim.isStructureOK(self.logger): return "Error in simulation structure: " + self.Sim.errorMsg
        
        # Open file
        SimFile=SimFiles()
        file = SimFile.openfile(self.Sim.Filename,'r')
        if SimFile.error: return SimFile.errorMSG
        
        # Read HeadFile
        error = self.Sim.readCabecera(file)
        if not error: valid=self.DB.isValidSimulation(self.User, self.Sim)
        else: return "Error en la cabecera de la simulacion: " + self.Sim.errorMsg
        if not valid: 
            if self.DB.errorMsg == 'project': return "Simulation not valid: " + self.DB.errorMsg + " " + self.Sim.Proyecto + " doesn't exist or you don't have rights"
            if self.DB.errorMsg == 'tipo': return "Simulation not valid: " + self.DB.errorMsg + " " + self.Sim.Tipo + " doesn't exist"
            if self.DB.errorMsg == 'estado': return "Simulation not valid: " + self.DB.errorMsg + " " + self.Sim.Estado + " doesn't exist"
            if self.DB.errorMsg == 'disciplina': return "Simulation not valid: " + self.DB.errorMsg + " " + self.Sim.Disciplina + " doesn't exist"
            if self.DB.errorMsg == 'subdisciplina': return "Simulation not valid: " + self.DB.errorMsg + " " + self.Sim.Subdisciplina + " doesn't exist"
            if self.DB.errorMsg == 'loadcase': return "Simulation not valid: " + self.DB.errorMsg + " " + self.Sim.LoadCase + " doesn't exist"
        
        # Check duplicated simulation
        if (self.Sim.Disciplina == 'PedestrianProtection'):
          self.Sim.Name=self.Sim.Name[0:len(self.Sim.Name)-5]
          
          # Buscamos el nombre del Shot con el nombre de sim y dentro del .pc
          shotnameraw=self.Sim.Filename[len(self.Sim.Filename)-8:len(self.Sim.Filename)-3]
          shotincluline=SimFiles.mygrep(self.Sim.Filename,shotnameraw+'.inc')
          
          shotname=re.search(r"\w+009\w+", shotincluline).group(0)
          
          newBaseFileName=self.Sim.Filename[0:len(self.Sim.Filename)-8]
          newBaseFileName+=self.Sim.Filename[len(self.Sim.Filename)-3:]
#          shutil.copyfile(self.Sim.Filename,newBaseFileName)
          self.Sim.Filename=newBaseFileName
          sim = self.DB.getSimbyName(self.User,self.Sim.Name)
          if (len(sim)==1):
            self.currentsim = next(iter(sim.items()))
            self.Sim.ID=self.currentsim[0]
            self.Sim.addShot(self.DB,self.User,shotname,self.logger)
            if (self.Sim.error==1): 
              result=self.Sim.errorMsg
          else:
            shutil.copyfile(self.Sim.Filename,newBaseFileName)
            self.Sim.importSimulation(self.DB,self.User,self.logger)
            if (self.Sim.error==1):  
              result=self.Sim.errorMsg
          
        else:
          sim = self.DB.getSimbyName(self.User,self.Sim.Name)
          if (len(sim)==1): 
            self.simduplicated = next(iter(sim.items()))
            self.DB.deleteSimulation(self.User,self.simduplicated[0])
            if (self.DB.error==1): 
              result=self.DB.errorMsg

          # Import Simulation 
          if ( result==""):           
            self.Sim.importSimulation(self.DB,self.User,self.logger)
            if (self.Sim.error==1):  
              result=self.Sim.errorMsg
        
        return result
  

    def cargaDatos(self):
        self.DB.cargaDatos(self.User, 'getUserProfile','user')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            return 1
        self.User.cargaProjects()
#             if self.DB.cargaDatos(self.User, 'getUserProjects','proyecto'): 
#                 self.show_message(self.LoginWindow,"dialog-error","Error Proyectos","Error cargando Datos")
#                 return 1
        self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            return 1
        self.DB.cargaDatos(self.User, 'getDisciplinas','discipline')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            return 1
        self.DB.cargaDatos(self.User, 'getEstados','estado')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            return 1
        self.DB.cargaDatos(self.User, 'getTipos','tipo')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            return 1
#         if self.DB.cargaDatos(self.User, 'getStorageWS','storagews'):
#             self.logger.info (": Error loading Storage Data" . self.DB.Conn.error)
#             return 1
        self.DB.cargaDatos(self.User, 'getRights','right')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            return 1
        self.DB.cargaDatos(self.User, 'getRoles','role')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            return 1
        self.DB.cargaDatos(self.User, 'getAccessLevels','accesslevel')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            return 1

        return 0
            
     
    def main(self,argv):
      # Config
      Globals.initialize(1)
      # Arguments
        
      parser=argparse.ArgumentParser(description='Usage[-d] -i=simfile -s=soft ')
        
      parser.add_argument('-d', action="store_true", dest='debug',default=False,help='Modo debug')
      parser.add_argument('-i', action="store",dest='simulacion', nargs=1,help='-n no borra .DSY .THP .lis')
      parser.add_argument('-s', action="store",dest='software', nargs=1,help='-n no borra .DSY .THP .lis')
      file=""
      
      try:
        results = parser.parse_args()
    
        if results.debug:
          self.logger.setLevel(logging.DEBUG)
        file=results.simulacion[0]
        self.soft=results.software[0]
      except:
        parser.print_help()
         
  
      self.logger.info (": ******************************** NEW UPLOAD ***************************************")
      self.logger.info ("FILE TO UPLOAD: " + os.path.realpath(file))
      self.DB = DB(self.User)
      self.DB.soft=self.soft
      
      if self.DB.Conn.error == "":  
        err=self.cargaDatos()
        if not err: 
          result=self.upload_simulation(os.path.realpath(file))
          if result=="": 
            self.logger.info ("Simulation %s imported successfuly" % (self.Sim.ID))
          else: 
            self.logger.error (": %s" % (result))
        else: 
          
          self.logger.error ("Error loading Data: %s" % self.DB.Conn.error)
      else:
        self.logger.error ("Login Error: %s" % self.DB.Conn.error)
      return

    # Inicializacion
    def __init__(self):
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.User = User(getpass.getuser())
        #self.logFilename = Globals.TMP_DIR + Path(os.path.realpath(__file__)).stem + ".log"
        #file_handler = logging.FileHandler(filename=self.logFilename)
        stdout_handler = logging.StreamHandler(sys.stdout)
        #handlers = [file_handler, stdout_handler]
        handlers = [stdout_handler]
        #formatter = '%(asctime)s %(levelname)s %(message)s'
        formatter = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
        #formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
        
        logging.basicConfig(
            level=logging.INFO, 
            format=formatter,
            handlers=handlers
        )

        #self.logger = logging.getLogger('LOGGER_NAME') 
        self.logger = logging.getLogger()
        self.soft=""
        # EJEMPLO LOGGER
        #self.msg = "Se ha creado el directorio: %s " % self.tmpDir
        #self.logger.debug ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.msg))
 
# Inicio Aplicacion  
if __name__=='__main__':
    app = ssdm_import()
    app.main(sys.argv[1:])
    
