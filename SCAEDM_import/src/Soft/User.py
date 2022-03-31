class User:

    def __init__(self,userid):    
        self.username=userid
        self.Projects=[]
 #       self.Roles=[]
        self.Profile=[]
        self.error=0
        self.errorMsg=""
#        self.storageWS=""


    def getProjectID (self,projectname):
        for proj in self.Projects:
            if projectname==proj[0]:
                return proj[1]
        return ""
    
    def getTipoChild (self,tipoParent):
        dict={}
        dict["root"]="Disciplina"
        dict["Disciplina"]="Subdisciplina"
        dict["Subdisciplina"]="LoadCase"
        dict["LoadCase"]="Simulacion"
        dict["Simulacion"]=""
        return dict[tipoParent]
    
    def cargaProjects (self):
        for role in self.Profile['roles'].values():
            proj=[]
            proj.append(role['projectname'])
            proj.append(role['projectid'])
            if proj not in self.Projects:
                self.Projects.append(proj)
    
    def addUser(self,User, DB,usernamevw,longname,department,email,company,sto):
        self.error=0
        DB.addUser(User,self.username,usernamevw,longname,department,email,company,sto)
        self.error=DB.error
        self.errorMsg=DB.errorMsg
        
    def modifyUser(self,User, DB,usernamevw,longname,department,email,company,sto):
        self.error=0
        DB.modifyUser(User,self.username,usernamevw,longname,department,email,company,sto)
        self.error=DB.error
        self.errorMsg=DB.errorMsg

    def deleteUser(self,User, DB, delete):
        self.error=0
        if delete==True:
            DB.deleteUser(User,self.username)
        else:
            DB.deactivateUser(User,self.username)
        self.error=DB.error
        self.errorMsg=DB.errorMsg

    def deleteRoles(self,User, DB):
        self.error=0
        DB.getUserProfile(User,self.username)
        for role in DB.Datos['roles'].values():
            DB.deleteRoleUser(User,self.username,role['projectname'],role['discipline'],role['rolename'])
            if DB.error==1: break
        self.error=DB.error
        self.errorMsg=DB.errorMsg
        
