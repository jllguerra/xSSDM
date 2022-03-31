import os, stat, time
from pathlib import Path
from FileTransfer.SimFiles import SimFiles
from Soft.XMLFunctions import XMLFunctions
from Config import config

class Simulacion:

    def __init__(self):    
        self.ID=""
        self.soft=""
        self.Filename=""
        self.Name=""
        self.path=""
        self.pathSTO=""
        
        self.Proyecto=""
        self.Tipo=""
        self.Estado=""
        self.Disciplina=""
        self.Subdisciplina=""
        self.LoadCase=""
        self.SubLoadcase=""
        self.Aux1=""
        self.Aux2=""
        self.Aux3=""
        self.Aux4=""
        self.Aux5=""
        self.Aux6=""
        self.Type=""
        self.Label=""
        self.Description=""
        self.Variant=""
        self.Reference=""
        
        self.Subdisciplinas=[]  #Lista de subdisciplinas dada la Disciplina de la Simulacion
        self.LoadCases=[]  #Lista de subdisciplinas dada la Disciplina de la Simulacion
        self.AccessLevel="0"
        self.Owner=""
        self.OwnerLN=""
        self.CreationDate=""
        self.Rights=""
        self.Nfiles=0
        self.Outputs=0
        self.Reports=0
        self.Extern=""
        self.TreePath=0
        self.error=0
        self.errorMsg=""
        #self.structureDir=['input','output']
        self.inputDir=['']
        self.outputsDir=dict(
            default=['output'],
            pc=['output'],
            dat=['output'],
            bdf=['output'],
            inc=['output'],
            sdm=['output.*'])

        
    def isStructureOK(self,logger):
        file=SimFiles()
#         pa=os.path.split(os.path.dirname(self.Filename))
#         msg = "filedir: " + pa[0] + " dir: " + self.outputsDir['default'][0]
#         
#         if not file.isInDirectory(self.Filename,self.structureDir[0]): # is in Input Directory
#             self.msg = "file: " + self.Filename + " is not in " + self.structureDir[0] + " directory"
#             logger.error (": %s" % (self.msg))
#             return False
        
        splitFile=os.path.splitext(self.Filename)
        ext=splitFile[len(splitFile)-1]
        index=ext.lstrip('.')
        self.path=file.getRootDirectory(self.Filename)
        if not index in self.outputsDir:
            index='default'
        if not file.existStructure(self.path, self.outputsDir[index]):
            self.error=file.error
            self.errorMsg=file.errorMSG
            return False

        return True

    
    def downloadFiles(self, sim, User, DB, dirdest,selected_files,logger):
        self.error=0
        self.errorMsg=""
#         STOdir=User.Profile['sto'] + "/" + config.DOWNLOAD_DIR
#         if not os.path.exists(STOdir):
#             file=SimFiles()
#             file.creaDir(STOdir)
#             file.chmodDir(STOdir,stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
#             #file.chmodDir(STOdir,'0o777')
            
        dirdest = dirdest + "/" + sim['id'] + "_" + sim['name']
        file=SimFiles()
        if file.dirExist(dirdest):
            self.error=1
            self.errorMsg="ERROR: Target directory " + dirdest + " already exist"
            logger.error (": %s" % (self.errorMsg))
            return self.error
        msg="Copying files to " + dirdest
        logger.debug(": %s" % (msg))
        dirorig=DB.donwloadFiles(User,sim['id'],dirdest,selected_files)
        msg="Finish copy files"
        logger.debug(msg)
        if DB.error != 0:
#        if DB.error == 0:
#             msg="Copying files from " + dirorig + " to " + dirdest
#             logger.debug(msg)
#             # 1GB -> 10min aprox. MIRAR DE PONER THREADING
#             #file.SlowCopyDir(dirorig, dirdest)
#             file.slowCopyDir(dirorig, dirdest)
#             msg="Finish copy files"
#             logger.debug(": %s" % (msg))
#             if file.error==1:
#                 self.error=file.error
#                 self.errorMsg=file.errorMSG
#                 logger.error (": %s" % (self.error))
#             msg="Deleting temporary files from " + dirorig
#             logger.debug(": %s" % (msg))
#             file.delDir(dirorig)
#             msg="Finish delete temporary files"
#             logger.debug(": %s" % (msg))
#             if file.error==1:
#                 self.error=file.error
#                 self.errorMsg = self.errorMsg + "-" + file.errorMSG
#             logger.error (": %s" % (self.errorMsg))
#        else:
            self.error=DB.error
            self.errorMsg=dirorig
            logger.error (": %s" % (self.errorMsg))
        return self.error

    def changeAccessLevel (self, User, sim, DB):
        simid=sim['id']
        result=DB.changeAccessLevel(User,simid)
        if result==1:
            self.error=DB.error
        else:
            self.error=""
            self.AccessLevel=DB.Datos['accesslevel']
            self.Rights=DB.Datos['rights']
        return result
        
    def modifySimulation (self, User, sim, DB,changes):
        simid=sim['id']
        DB.updateSimulation(User, simid,changes)
        if DB.error==1:
            self.error=DB.error
            self.errorMsg=DB.errorMsg
        else:
            for item in changes:
                if item == 'label':
                    self.Label=DB.Datos[item]
                if item == 'description':
                    self.Description=DB.Datos[item]
        return self.error

    def importSimulation(self,DB,User,logger):
        #print ("import Simulation")
#        self.pathSTO=User.Profile['sto'] + "/" + User.username + "." + self.Name
        file=SimFiles()
        self.msg = "    File to UPLOAD: " + self.Filename
        logger.info (": %s" % (self.msg))
#         self.msg = "    STODIR to UPLOAD: " + self.pathSTO
#         logger.info (": %s" % (self.msg))
        
#         borrar=False
#         copyerror=0
#         self.error=0
#         self.errorMsg=""
#         sto_len=len(User.Profile['sto'])
#         root_path=file.getRootDirectory(self.path)
#         if (os.path.realpath(User.Profile['sto']) != root_path[:sto_len]):
#         #if (self.pathSTO != self.path):
#             self.msg = "    COPIA de Simulacion a STODIR "
#             logger.info (": %s" % (self.msg))
#             copyerror = file.copyDir(self.path, self.pathSTO) # Copia al STO del user
#             if copyerror == 0: borrar=True
#         else: self.pathSTO=self.path
#         
#         if copyerror == 0:
        DB.soft=self.soft;
        DB.uploadSimulation(User, User.username,self.Filename)
        if DB.error==1:
            self.error=1
            self.errorMsg=DB.errorMsg
        else:
            self.ID=DB.Datos['id']
            self.Name=DB.Datos['name']
            self.Proyecto=DB.Datos['project']
            self.Disciplina=DB.Datos['discipline']
            self.Subdisciplina=DB.Datos['subdiscipline']
            self.Aux1=DB.Datos['aux1']
            self.Aux2=DB.Datos['aux2']
            self.Aux3=DB.Datos['aux3']
            self.Aux4=DB.Datos['aux4']
            self.Aux5=DB.Datos['aux5']
            self.Aux6=DB.Datos['aux6']
            self.Type=DB.Datos['type']
            self.LoadCase=DB.Datos['loadcase']
            self.Reference=DB.Datos['reference']
            self.Variant=DB.Datos['variant']
            self.Owner=DB.Datos['owner']
            self.CreationDate=DB.Datos['creation']
            self.Estado=DB.Datos['status']
            self.Nfiles=DB.Datos['nfiles']
            self.Outputs=DB.Datos['outputs']
            self.Reports=DB.Datos['reports']
            self.OwnerLN=DB.Datos['ownerLN']
            self.Label=DB.Datos['label']
            self.Description=DB.Datos['description']
            self.Rights=DB.Datos['rights']
            self.Extern=DB.Datos['extern']
#         else:
#             self.error=1
#             self.errorMsg=copyerror
#                 
#         if borrar==True:
#             error = file.delDir(self.pathSTO)
#             if error!=0:
#                 logger.error (": %s" % (error))
#                 self.error=1
#                 self.errorMsg += error 
        return self.errorMsg


    def cargaDatos(self, dict):
        for subdisciplina in dict[self.Disciplina][1]:
            self.Subdisciplinas.append(subdisciplina)
        for loadcase in dict[self.Disciplina][2][self.Subdisciplina][2]:
            self.LoadCases.append(loadcase)
    
    def readCabecera(self,file):
        start=0
        self.error=0
        input=0
        headExist=0
        self.errorMsg=""
        string_Head=""
        
        #print("Funcion readCabecera")
        for line in file:
#            print (line.strip())
            if line[0]!="$": continue
            else: 
                if "<Import>" in line and not start: 
                    start=1
                    string_Head+=line.lstrip('$')
                    continue
                if "</Import>" in line and start: 
                    start=0
                    string_Head+=line.lstrip('$')
                    break
                if start==1: string_Head+=line.lstrip('$')
        file.close()
        xmlHead=XMLFunctions(string_Head)
        if xmlHead.error==1: 
            self.error=xmlHead.error
            self.errorMsg=xmlHead.errorMsg
            return self.error
        dictHead=xmlHead.readHead()
        if xmlHead.error==1: 
            self.error=xmlHead.error
            self.errorMsg=xmlHead.errorMsg
            return self.error
        self.Proyecto=dictHead['Proyecto']
        #self.Tipo=dictHead['Tipo']
        self.Tipo="CAE"
        self.Estado=dictHead['Estado']
        self.Disciplina=dictHead['Disciplina']
        self.Subdisciplina=dictHead['Subdisciplina']
        self.LoadCase=dictHead['LoadCase']
        self.SubLoadcase=dictHead['SubLoadcase']
        self.Aux1=dictHead['Aux1']
        self.Aux2=dictHead['Aux2']
        self.Aux3=dictHead['Aux3']
        self.Aux4=dictHead['Aux4']
        self.Aux5=dictHead['Aux5']
        self.Aux6=dictHead['Aux6']
        self.Label=dictHead['Label']
        self.Description=dictHead['Description']
        self.Variant=dictHead['Variant']
        self.Reference=dictHead['Reference']
        
        # Needed Data
        if self.Proyecto == "":
            self.error=1
            self.errorMsg="Missing Project"
            return self.error
        if self.Subdisciplina == "":
            self.error=1
            self.errorMsg="Missing Subdiscipline"
            return self.error
        if self.Disciplina == "": 
            self.error=1
            self.errorMsg="Missing Discipline"
            return self.error
        if self.LoadCase == "":
            self.error=1
            self.errorMsg="Missing Loadcase"
            return self.error
        if self.Estado == "":
            self.error=1
            self.errorMsg="Missing ModelPhase"
            return self.error
        return self.error 
                    


        

#===============================================================================
#     tree = ElementTree.fromstring(response.content)
# 
# #  or, if the response is particularly large, use an incremental approach:
# 
#     response = requests.get(url, stream=True)
# # if the server sent a Gzip or Deflate compressed response, decompress
# # as we read the raw stream:
#     response.raw.decode_content = True
# 
#     events = ElementTree.iterparse(response.raw)
#     for event, elem in events:
#        # do something with `elem`
