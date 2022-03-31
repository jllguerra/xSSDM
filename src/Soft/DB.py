from Soft.XMLFunctions import XMLFunctions
from httpdclient.httpdclient import httpdclient
import Config.config as Globals
import json

class DB:

    def __init__(self,User):    
        self.soft=""
        self.Users=[]
        self.Companies=[]
        self.Projects=[]
        self.ProjectStructure={}
        self.Tipos=[]
        self.Estados=[]
        self.AllEstados=[]
        self.Disciplinas=[]
        self.Subdisciplinas=[]
        self.LoadCases=[]
        self.error=""
        self.errorMsg=""
        self.Datos={}
        self.AccessLevel=0
        self.AccessLevels=[]
        
        #self.Conn = httpdclient(User.username, User.passwd, User.Cert_pem, User.PubKey)
        self.Conn = httpdclient(User.username)
        self.error=self.Conn.error
         #self.Conn.execAPIfunction("conectar", dict())


    def isValidSimulation(self,User, sim):
        found=False
        for project in User.Projects:
            if sim.Proyecto==project[0]:
                found=True
                break
        if found==False:
            self.error=1
            self.errorMsg='project'
            return False
        found=False
        for tipo in self.Tipos:
            if sim.Tipo==tipo[0]:
                found=True
                break
        if found==False:
            self.error=1
            self.errorMsg="tipo"
            return False
        found=False
        for estado in self.AllEstados:
            if sim.Estado==estado[0]:
                found=True
                break
        if found==False:
            self.error=1
            self.errorMsg="estado"
            return False
        if not sim.Disciplina in self.ProjectStructure:
            self.error=1
            self.errorMsg="disciplina"
            return False
        if not sim.Subdisciplina in self.ProjectStructure[sim.Disciplina][2]:
            self.error=1
            self.errorMsg="subdisciplina"
            return False
        if not sim.LoadCase in self.ProjectStructure[sim.Disciplina][2][sim.Subdisciplina][2]:
            self.error=1
            self.errorMsg="loadcase"
            return False
        
        sim.cargaDatos(self.ProjectStructure)
        return True
    
    def getSubdisciplinas (self, disciplina):
        return self.ProjectStructure[disciplina][2]

    def getLoadCases (self, disciplina,subdisciplina):
        return self.ProjectStructure[disciplina][2][subdisciplina][2]
 
    def getSims(self,User,projectid,disciplina,subdisciplina,loadcase,estado,owner):
        self.error=0
        dict = {'projectid':projectid,'disciplina':disciplina,'subdisciplina':subdisciplina,'loadcase':loadcase,'estado':estado,'owner':owner}
        DatosXML = self.Conn.execAPIfunction("getSims",User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if resultElem.text=='ERROR': 
            self.error=1
            self.errorMsg=resultElem.text
            return 0
        Datos = XMLFunctions.xml_getSimulaciones(self,resultElem)

        return Datos
    
    def getSimbyName(self,User,name):
        self.error=0
        dict = {'name':name}
        DatosXML = self.Conn.execAPIfunction("getSimbyName", User.username,dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if resultElem.text=='ERROR': 
            self.error=1
            self.errorMsg=resultElem.text
            return 0
        Datos = XMLFunctions.xml_getSimulaciones(self,resultElem)

        return Datos

    def checkMD5(self, User, simid):
        self.error=0
        dict = {'simid': simid} 
        DatosXML = self.Conn.execAPIfunction("checkMD5", User.username,dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if not resultElem.text is None: 
            if resultElem.text[0:5]=='ERROR': 
                self.error=1
                self.errorMsg=resultElem.text
                return False
        return True
        
        
    def getFiles(self, User,simid):
        self.error=0
        dict = {'simid': simid} 
        DatosXML = self.Conn.execAPIfunction("getFiles", User.username,dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if not resultElem.text is None: 
            if resultElem.text[0:5]=='ERROR': 
                self.error=1
                self.errorMsg=resultElem.text
                return 0
        Datos = XMLFunctions.xml_getSimulationFiles(self,resultElem)

        return Datos
       
    def donwloadFiles(self,User, simid,dirname,selected_files):
        self.error=0
        files=""
        for file in selected_files:
            if files=="":
                files=selected_files[file] + "/" + file
            else:
                files=files + ";" + selected_files[file] + "/" + file
        dict = {'simid': simid,'dirname' : dirname,'selected_files' : files} 
        DatosXML = self.Conn.execAPIfunction("downloadFiles", User.username,dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if resultElem.text[0:5]=='ERROR': 
            self.error=1
            self.errorMsg=resultElem.text
        return resultElem.text
    
    def getProjectID(self,User,projectname):
        self.error=0
        dict = {'projectname':projectname}
        DatosXML = self.Conn.execAPIfunction("getProjectID", User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if resultElem.text=='ERROR': 
            self.error=1
            self.errorMsg=resultElem.text
            return 0
        return resultElem.text
                              
    def getNumSims(self,User,project,disciplina,subdisciplina,loadcase,estado,owner,userid):
        self.error=0
        dict = {'project':project,'disciplina':disciplina,'subdisciplina':subdisciplina,'loadcase':loadcase,'estado':estado,'owner':owner,'userid':userid}
        DatosXML = self.Conn.execAPIfunction("getNumSims", User.username,dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if resultElem.text[0:5]=='ERROR': 
            self.error=1
            self.errorMsg=resultElem.text
            return 0
        return resultElem.text
    
    def changeAccessLevel(self, User, simid): 
        self.error=0
        dict = {'simid': simid} 
        DatosXML = self.Conn.execAPIfunction("changeAccessLevel", User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if resultElem.text=='ERROR': 
            self.error=1
            self.error=resultElem.text
            return 1
        self.Datos=XMLFunctions.xml_getSimulationAccessLevel(self, resultElem)
        return 0        

    def updateSimulation(self, User,simid, changes): 
        self.error=0
        dict = {'simid': simid, 'changes': json.dumps(changes)} 
        DatosXML = self.Conn.execAPIfunction("modifySimulation", User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if resultElem.text=='ERROR': 
            self.error=1
            self.errorMsg=resultElem.text
            return 0
        self.Datos = XMLFunctions.xml_getSimulationData(self,resultElem)
        return 0      
                                 
    def getUserProfile(self,User,userid):
        self.error=0
        dict = {'userid': userid}
        DatosXML = self.Conn.execAPIfunction('getUserProfile', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
                return 1
        self.Datos = XMLFunctions.xml_getProfileDict(self,resultElem,'user')
        return 0
    
    def addUser(self, User, userid,useridvw,longname,department,email,company,sto):
        self.error=0
        dict = {'userid': userid,'useridvw': useridvw, 'longname': longname, 'department': department, 'email': email, 'company': company, 'sto': sto}
        DatosXML = self.Conn.execAPIfunction('addUser', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
                
    def modifyUser(self, User, userid,useridvw,longname,department,email,company,sto):
        self.error=0
        dict = {'userid': userid,'useridvw': useridvw, 'longname': longname, 'department': department, 'email': email, 'company': company, 'sto': sto}
        DatosXML = self.Conn.execAPIfunction('modifyUser', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text

    def deleteUser(self, User, userid):
        self.error=0
        dict = {'userid': userid}
        DatosXML = self.Conn.execAPIfunction('deleteUser', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
                
    def deactivateUser(self, User, userid):
        self.error=0
        dict = {'userid': userid}
        DatosXML = self.Conn.execAPIfunction('deactivateUser', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
                
    def addDiscipline(self,User, discipline,responsible):
        self.error=0
        dict = {'discipline': discipline,'responsible': responsible}
        DatosXML = self.Conn.execAPIfunction('addDiscipline', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text

    def modifyDiscipline(self,User,olddiscipline, discipline,responsible):
        self.error=0
        dict = {'olddiscipline': olddiscipline,'discipline': discipline,'responsible': responsible}
        DatosXML = self.Conn.execAPIfunction('modifyDiscipline', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text

    def deleteDiscipline(self,User,discipline):
        self.error=0
        dict = {'discipline': discipline}
        DatosXML = self.Conn.execAPIfunction('deleteDiscipline', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
        
    def addSubdiscipline(self,User,discipline,subdiscipline):
        self.error=0
        dict = {'discipline': discipline,'subdiscipline': subdiscipline}
        DatosXML = self.Conn.execAPIfunction('addSubdiscipline', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text

    def modifySubdiscipline(self,User,oldsubdiscipline,discipline,subdiscipline):
        self.error=0
        dict = {'oldsubdiscipline': oldsubdiscipline,'discipline': discipline,'subdiscipline': subdiscipline}
        DatosXML = self.Conn.execAPIfunction('modifySubdiscipline', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
        
    def deleteSubdiscipline(self,User,discipline,subdiscipline):
        self.error=0
        dict = {'discipline': discipline,'subdiscipline': subdiscipline}
        DatosXML = self.Conn.execAPIfunction('deleteSubdiscipline', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text

    def addLoadcase(self,User, discipline,subdiscipline, loadcase):
        self.error=0
        dict = {'discipline': discipline,'subdiscipline': subdiscipline,'loadcase': loadcase}
        DatosXML = self.Conn.execAPIfunction('addLoadcase', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
        
    def modifyLoadcase(self,User,oldoadcase, discipline,subdiscipline, loadcase):
        self.error=0
        dict = {'oldloadcase': oldoadcase,'discipline': discipline,'subdiscipline': subdiscipline,'loadcase': loadcase}
        DatosXML = self.Conn.execAPIfunction('modifyLoadcase', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text

    def deleteLoadcase(self,User, discipline,subdiscipline, loadcase):
        self.error=0
        dict = {'discipline': discipline,'subdiscipline': subdiscipline,'loadcase': loadcase}
        DatosXML = self.Conn.execAPIfunction('deleteLoadcase', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text

    def cargaDatos(self,User, action,tag):
        self.error=0
        dict = {}
        DatosXML = self.Conn.execAPIfunction(action, User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
                return 1
        if action == 'getProjectStructure':
#            Datos = XMLFunctions.xml_getStructrure(self,DatosXML,tag)
            Datos = XMLFunctions.xml_getStructureDict(self,resultElem,tag)
            self.ProjectStructure = Datos
            return 0
        if action == 'getUserProfile':
            Datos = XMLFunctions.xml_getProfileDict(self,resultElem,tag)
            User.Profile = Datos
            return 0
        if action == 'getRights':
            Datos = XMLFunctions.xml_getDict(self,resultElem,tag)
            self.Rights = Datos
            return 0
        if action == 'getRoles':
            Datos = XMLFunctions.xml_getDict(self,resultElem,tag)
            self.Roles = Datos
            return 0
        if action == 'getAccessLevels':
            Datos = XMLFunctions.xml_getElemsData(self,resultElem,tag)
            self.AccessLevels = Datos
            return 0
        Datos = XMLFunctions.xml_getLista(self,resultElem,tag)
        if tag == 'discipline': self.Disciplinas = Datos[:]
        if tag == 'project': self.Projects = Datos[:]
        if tag == 'users': self.Users = Datos[:]
        if tag == 'company': self.Companies = Datos[:]
        if tag == 'proyecto': User.Projects = Datos[:]
        if tag == 'tipo': self.Tipos = Datos[:]
        if tag == 'estado': self.AllEstados = Datos[:]
        if tag == 'storagews': User.storageWS = Datos[0][0]
        #if tag == 'storagews': User.storageWS = "/data/storage/cae-stg01/stg-ing01/VWGS/scernud/CSBdata"
        return 0
        
    def uploadSimulation (self, User, username,Filename):
#        dict['username']=User.username
        self.error=0
        self.errorMsg=""
        dict = {'filename': Filename,'userid': username,'soft':self.soft}
        xml = self.Conn.execAPIfunction('addsimfromfile', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,xml)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
                return 0
        else:
            Datos = XMLFunctions.xml_getSimulaciones(self,resultElem)
            self.Datos = Datos[list(Datos.keys())[0]]
        return 0                    

    
    def deleteSimulation(self,User, simid):
        self.error=0
        self.errorMsg=""
        dict = {'simid': simid}
        xml = self.Conn.execAPIfunction('deleteSimulation', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,xml)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
                return 0
        return 0                 
        

    def getEstadoID (self,estadoName):
        for status in self.AllEstados:
            if estadoName==status[0]:
                return status[1]
        return ""
    
    def getEstatusbyProject(self, User, projectName,ownsims):
        self.error=0
        dict = {'projectname': projectName, 'ownsims': ownsims}
        DatosXML = self.Conn.execAPIfunction('getStatusbyProject', User.username, dict)
        resultElem = XMLFunctions.xml_getResultado(self,DatosXML)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
                return 1
        Datos = XMLFunctions.xml_getLista(self,resultElem,'estado')
        self.Estados = Datos[:]        
    
    def getRama (self, tipoParent, tipoChild, disciplina, subdisciplina,loadcase):
        if tipoParent == "root":
            if tipoChild == "Disciplina":
                return self.Disciplinas
            if tipoChild == "Subdisciplina":
                return self.Subdisciplinas
            if tipoChild == "LoadCase":
                return self.LoadCases
        if tipoParent == "Disciplina":
            if tipoChild == "Subdisciplina":
                return self.Subdisciplinas
            if tipoChild == "LoadCase":
                return self.LoadCases
        if tipoParent == "Subdisciplina":
            if tipoChild == "Disciplina":
                return self.Disciplinas
            if tipoChild == "LoadCase":
                return self.getLoadCases(disciplina, subdisciplina)
        
    def addRoleUser (self,User, username,requester,daterequest,project, discipline,role):
        self.error=0
        self.errorMsg=""
        params = {'userid': username,'requester': requester, 'daterequest': daterequest,'project': project,'discipline': discipline,'role': role}
        xml = self.Conn.execAPIfunction('addroleuser', User.username,params)
        resultElem = XMLFunctions.xml_getResultado(self,xml)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
                return 0
        return 0     

    def deleteRoleUser (self,User, username,project,discipline,role):
        self.error=0
        self.errorMsg=""
        params = {'userid': username,'project': project,'discipline': discipline,'role': role}
        xml = self.Conn.execAPIfunction('deleteroleuser', User.username,params)
        resultElem = XMLFunctions.xml_getResultado(self,xml)
        if (resultElem.text!=None):
            if resultElem.text[0:5]=='ERROR': 
                self.error = 1
                self.errorMsg=resultElem.text
                return 0
        return 0     
