import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GLib, Gdk
from pathlib import Path
import getpass,os, inspect,logging,sys, getopt, json
from datetime import datetime
#import stat
#from gi.repository.GdkPixbuf import Pixbuf

import Config.config as Globals
from Soft.Simulacion import Simulacion
from Soft.DB import DB
from Soft.User import User
from FileTransfer.SimFiles import SimFiles
from Soft.PKI import PKI

class xSSDM(Gtk.Application):
    
    def show_message(self,parent, image, msg,title):
#        self.logger.info ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
        self.logger.info (msg)
        self.messageWin.set_title(title)
        self.messageLabel.set_markup("<span foreground='black'><b> " + msg + " </b></span>")
        
        #self.messageIMG.new_from_icon_name(image,Gtk.IconSize.DIALOG) # icon name: GTK_STOCK_OPEN, GTK_STOCK_QUIT. Sample stock sizesare GTK_ICON_SIZE_MENU, GTK_ICON_SIZE_SMALL_TOOLBAR
        self.messageIMG.set_from_icon_name(image,Gtk.IconSize.DIALOG);
        #self.messageWin.set_transient_for(self.LoginWindow)
        self.messageWin.show()

    # Signals para Login Window
    def on_MainCancel_clicked (self, widget, data=None):
        Gtk.main_quit()
        return False
    
    def on_LoginButton_clicked (self, widget, data=None):
        # Autentificacion PKI
        self.error=""
        self.LoginWindow.hide()
        
        # Login con Webseal. Solo comprobamos targeta insertada
        pki=PKI("")
        if pki.error: 
            self.show_message(self.LoginWindow,"dialog-error", pki.msg,"Error Login")
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],pki.msg))
            self.LoginWindow.show()
            return

        # Conexion con DB
        self.DB = DB(self.User)

        if self.DB.Conn.conectado == True:  
            msg="User Connected";
            #self.logger.info ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.logger.info (msg)

            err=self.cargaDatos()
            if not err: self.start_SSDM()
            else: self.LoginWindow.show()
        else:
            self.show_message(self.LoginWindow,"dialog-error", self.DB.Conn.error,"Error Login")
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.Conn.error))
            self.LoginWindow.show()
    
    # Check ver solo Simulaciones propias
    def on_OwnSimsClicked(self,data=None):
        if data.get_active():
            self.seeOwnSims='True'
            #self.project_store.clear()
            #self.userProjectsCombo.set_active(0);
            msg="Own Sims Activated"
            self.logger.info (msg)
        else: 
            self.seeOwnSims='False'
            #self.project_store.clear()
            #self.userProjectsCombo.set_active(0);
            msg="Own Sims Deactivated"
            self.logger.info (msg)
                
    def cargaDatos(self):
        self.DB.cargaDatos(self.User, 'getUserProfile','user')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error Profile")
            return 1
        self.User.cargaProjects()
        self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error Structura")
            return 1
        self.DB.cargaDatos(self.User, 'getUsers','users')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error Projects")
            return 1
        self.DB.cargaDatos(self.User, 'getCompanies','company')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error Companies")
            return 1
        self.DB.cargaDatos(self.User, 'getProjects','project')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error Projects")
            return 1
        self.DB.cargaDatos(self.User, 'getDisciplinas','discipline')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error Disciplinas")
            return 1
        self.DB.cargaDatos(self.User, 'getEstados','estado')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error Estados")
            return 1
        self.DB.cargaDatos(self.User, 'getTipos','tipo')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error Tipos")
            return 1
        self.DB.cargaDatos(self.User, 'getRights','right')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error Rights")
            return 1
        self.DB.cargaDatos(self.User, 'getRoles','role')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error Rights")
            return 1
        self.DB.cargaDatos(self.User, 'getAccessLevels','accesslevel')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error Rights")
            return 1

        return 0
        
    # Signals para Main Window
    def on_New_clicked(self, widget, data=None):
        self.LoginWindow.hide()

    def on_Find_clicked(self, widget, data=None):
        self.LoginWindow.hide()
        # Autentificacion PKI
        #self.soft=NewSimulation(self.glade,self.useridOS,self.logger)
    def cargaRama (self, tipoParent, tipoChild, curretnIter, projectID, estadoID, seeOwnSims):
        for node in self.DB.getRama(tipoParent, tipoChild, "", "", ""):
            numsims= self.DB.getNumSims(self.User,projectID,node[0],"","",estadoID,seeOwnSims,self.User.username.upper())
            if self.DB.error==1:
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
                self.show_message(self.selectDirWindow, 'dialog-error', "Tree not download " + self.DB.errorMsg, "Tree View")
                return 1
            if not numsims=="0": self.project_store.append(curretnIter,[node[0],numsims,tipoChild,""])      
        
    def onProjectSelected(self,project_combo):        
        # Limpiamos carga antigua
        #self.project_store.clear()
        self.selected_project = project_combo.get_active_text()
        
        if not self.selected_project == 'Select Project ...':
            self.EstadosCombo.remove_all()
            self.EstadosCombo.append_text('Select Status ...')
            self.EstadosCombo.set_active(0)
            # Cargar estados para el proyecto seleccionado
            self.DB.getEstatusbyProject(self.User,self.selected_project,self.seeOwnSims)
            # Adding info in the Estado Combo
            for estado_ref in self.DB.Estados:
                cur_estado=self.EstadosCombo.append_text(estado_ref[0])

    def onEstadoSelected(self,estado_combo):
        self.selected_estado = estado_combo.get_active_text()

    def onProjectView_row_expand(self,project_view, path, column):
        currentIter = self.project_store.get_iter(path)
        name = self.project_store.get_value(currentIter, 0)
        nsimsparent = self.project_store.get_value(currentIter, 1)
        tipoParent = self.project_store.get_value(currentIter, 2)
        datos = self.project_store.get_value(currentIter, 3)
        
        disciplina = ""
        subdisciplina = ""
        loadcase = ""
        tipoChild=self.User.getTipoChild(tipoParent)
        
        # Buscar en Server los datos bajo el Projecto
        if ((not self.project_store.iter_has_child(currentIter)) and (nsimsparent!="0")):
#             if tipo == 'Project':
#                 # Buscar disciplinas en DB
#                 self.project_store.append(rama,["Disciplina1","Disciplina"])
            if tipoParent == 'Disciplina':
                disciplina=name
                # Buscar SubDisciplina DB
                #self.cargaRama(tipoParent, tipoChild, self.selected_projectID, disciplina, subdisciplina, loadcase, self.selected_estadoID, self.seeOwnSims)
                childs = self.DB.getSubdisciplinas(name)
                for child in childs:
                    numsims= self.DB.getNumSims(self.User,self.selected_projectID,disciplina,child,loadcase,self.selected_estadoID,self.seeOwnSims,self.User.username.upper())
                    if not numsims=="0": self.project_store.append(currentIter,[child,numsims,tipoChild,""])
            if tipoParent == 'Subdisciplina':
                # Buscar LoadCases DB
                ramaDisciplina=self.getParentIter(self.project_store,path)
                disciplina=self.project_store.get_value(ramaDisciplina, 0)
                childs = self.DB.getLoadCases(disciplina, name)
                for child in childs:
                    numsims = self.DB.getNumSims(self.User,self.selected_projectID,disciplina,name,child,self.selected_estadoID,self.seeOwnSims,self.User.username.upper())
                    if not numsims=="0": self.project_store.append(currentIter,[child,numsims,tipoChild,""])
                    if self.DB.error==1:
                        self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
                        self.show_message(self.selectDirWindow, 'dialog-error', "Tree not download " + numsims, "Tree View")
                        return 1
            if tipoParent == 'LoadCase':
                # Buscar Simulacion DB
                iterSubdisciplina=self.getParentIter(self.project_store,path)
                subdisciplina=self.project_store.get_value(iterSubdisciplina, 0)
                iterDisciplina=self.getParentIter(self.project_store,self.project_store.get_path(iterSubdisciplina))
                disciplina=self.project_store.get_value(iterDisciplina, 0)
                loadcase=name
                
                sims=self.DB.getSims(self.User,self.selected_projectID,disciplina,subdisciplina,loadcase,self.selected_estadoID,self.seeOwnSims)
                for sim_ref in sims:
                    iterChild=self.project_store.append(currentIter,[sims[sim_ref]['name'],"1",tipoChild,""])
                    pathChild=self.project_store.get_path(iterChild)
                    sims[sim_ref]['path']=pathChild.to_string()
                    datos=json.dumps(sims[sim_ref])
                    self.project_store[iterChild][-1]=datos
            if tipoParent == 'Simulacion':
                self.listaSimsStore.clear()  
                self.detailsFrame.set_position(100)      
                self.mostrar_Simulacion(datos)
                          
    def getParentIter(self,store,path):
        indices=path.get_indices()
        parentIndices=[]
        i = 0
        while i <= len(indices)-2:
            parentIndices.append(indices[i])
            i += 1
        parentPath=path.new_from_indices(parentIndices)
        return store.get_iter(parentPath)

    def simulacion_Mostrada(self,item):
        for row in self.listaSimsStore:
            if row[0] == item[0]: # 00: Simid
                return True
        return False
        
        #view.row_activated(tree_path, column_number)
        #view.set_cursor(tree_path, column_number, True)

    def mostrar_Simulacion(self,datos):
        dicti=json.loads(datos)
        listpanelsimulaciones=self.dict2List(dicti)
        if (not self.simulacion_Mostrada(listpanelsimulaciones)):
            self.listaSimsStore.append(listpanelsimulaciones)

    def on_findUserButton_clicked(self,findedUserEntry):
        userid_to_find=findedUserEntry.get_text().upper()
        self.listaUsersStoreAdmin.clear()
        
        for user in self.DB.Users:
            # Compare with userid or user long name
            if ((user[0].find(userid_to_find) != -1) or ((user[2].upper()).find(userid_to_find) != -1)):
                listd=[]
                listd.append(user[0])
                listd.append(user[2])
                self.listaUsersStoreAdmin.append(listd)
    
    def on_rowUser_Activated (self,view,path,column):
        userid_to_find=self.listaUsersStoreAdmin[self.listaUsersStoreAdmin.get_iter(path)][0]
        self.listaRolesStoreAdmin.clear()
        self.DB.getUserProfile(self.User,userid_to_find)
        #self.useridEntry.set_text(self.DB.Datos['id'])
        self.useridEntry.set_text(userid_to_find)
        self.useridvwEntry.set_text(self.DB.Datos['useridvw'])
        self.nameEntry.set_text(self.DB.Datos['longname'])
        self.departmentEntry.set_text(self.DB.Datos['department'])
        self.emailEntry.set_text(self.DB.Datos['correo'])
        self.stoEntry.set_text(self.DB.Datos['sto'])
        self.listaCompanies.set_active_id(self.DB.Datos['company'])
        for role in self.DB.Datos['roles']:
            listd=self.dict2List(self.DB.Datos['roles'][role])
            self.listaRolesStoreAdmin.append(listd)
        self.listaUsers.set_active_id(userid_to_find)
        self.userModified=False
#         else:
#             msg="Role User Error: " + self.DB.errorMsg
#             self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
#             self.show_message(self.selectDirWindow, 'dialog-error', msg, "Get Roles User")                    


    def on_modifyItemButton_clicked (self, data=None):
        selected = data.get_selected()
        self.disciplineModEntry.set_text('')
        self.responsibleModEntry.set_text('')
        self.subdisciplineModEntry.set_text('')
        self.loadcaseModEntry.set_text('')
            
        if selected[1]!=None:
            # Get type selecction
            rowSelected=self.disciplineStoreAdmin[selected[1]]
            rowIterSelected = self.disciplineStoreAdmin.get_iter(rowSelected.path)
            itemNameSelected=self.rowSelected[0]
            self.respNameSelected=self.rowSelected[1]
            self.typeSelected=self.rowSelected[2]
            self.respidSelected=self.rowSelected[3]
            if self.typeSelected=='discipline':
                # Modify new Discipline
                self.disciplineSelected=itemNameSelected
                self.action='modifyDiscipline'
                self.disciplineModEntry.set_text(self.disciplineSelected)
                self.responsibleModEntry.set_text(self.respidSelected)
                self.disciplineModEntry.set_editable(True)
                self.disciplineModEntry.set_sensitive(True)
                self.responsibleModEntry.set_editable(True)
                self.responsibleModEntry.set_sensitive(True)
                self.subdisciplineModEntry.set_editable(False)
                self.subdisciplineModEntry.set_sensitive(False)
                self.loadcaseModEntry.set_editable(False)
                self.loadcaseModEntry.set_sensitive(False)
            if self.typeSelected=='subdiscipline':
                # Modify subdiscipline
                self.subdisciplineSelected=itemNameSelected
                parentIter=self.getParentIter(self.disciplineStoreAdmin, rowSelected.path)
                self.disciplineParent=self.disciplineStoreAdmin.get_value(parentIter, 0)
                self.responsibleParent=self.disciplineStoreAdmin.get_value(parentIter, 1)
                self.action='modifySubdiscipline'     
                self.disciplineModEntry.set_editable(False)
                self.disciplineModEntry.set_sensitive(False)
                self.disciplineModEntry.set_text(self.disciplineParent)
                self.responsibleModEntry.set_editable(False)
                self.responsibleModEntry.set_sensitive(False)
                self.responsibleModEntry.set_text(self.responsibleParent)
                self.subdisciplineModEntry.set_editable(True)
                self.subdisciplineModEntry.set_sensitive(True)
                self.subdisciplineModEntry.set_text(self.subdisciplineSelected)
                self.loadcaseModEntry.set_editable(False)
                self.loadcaseModEntry.set_sensitive(False)
            if self.typeSelected=='loadcase':
                # Modify loadcase
                self.loadcaseSelected=itemNameSelected
                parentIter=self.getParentIter(self.disciplineStoreAdmin, rowSelected.path)
                self.subdisciplineParent=self.disciplineStoreAdmin.get_value(parentIter, 0)
                parentIter=self.getParentIter(self.disciplineStoreAdmin, self.disciplineStoreAdmin.get_path(parentIter))
                self.disciplineParent=self.disciplineStoreAdmin.get_value(parentIter, 0)
                self.responsibleParent=self.disciplineStoreAdmin.get_value(parentIter, 1)
                self.action='modifyLoadcase'
                self.disciplineModEntry.set_editable(False)
                self.disciplineModEntry.set_sensitive(False)
                self.disciplineModEntry.set_text(self.disciplineParent)
                self.responsibleModEntry.set_editable(False)
                self.responsibleModEntry.set_sensitive(False)
                self.responsibleModEntry.set_text(self.responsibleParent)
                self.subdisciplineModEntry.set_editable(False)
                self.subdisciplineModEntry.set_sensitive(False)
                self.subdisciplineModEntry.set_text(self.subdisciplineParent)
                self.loadcaseModEntry.set_editable(True)
                self.loadcaseModEntry.set_sensitive(True)
                self.loadcaseModEntry.set_text(self.loadcaseSelected)
        self.modifyItemDialog.show()   

    def on_modifyItem_clicked (self,data=None):
        if self.action=='modifyDiscipline':
            discipline=self.disciplineModEntry.get_text()
            if discipline=='':
                msg="Discipline is empty!"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Modify Discipline")
                return
            responsible=self.responsibleModEntry.get_text()        
            if responsible=='':
                msg="Responsible is empty!"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Modify Discipline")
                return
            if (discipline==self.disciplineSelected) and (responsible==self.respNameSelected): return
            if not any(responsible in x for x in self.DB.Users):
            #if not responsible in self.DB.Users:
                msg="Responsible " + responsible + " is not in the system!"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Modify Discipline")
                return                
            self.DB.modifyDiscipline(self.User,self.disciplineSelected,discipline,responsible)
            if self.DB.error==0:
                msg="Discipline " + discipline + " modify successfuly!"
                self.logger.info (msg)
                #self.disciplineStoreAdmin.delete(None,[self.itemNameSelected,self.respNameSelected,'discipline'])
                self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
                if self.DB.error==1: 
                    self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
                    self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Modify Discipline")
                    return 1
                self.rowSelected[0]=discipline
                self.rowSelected[1]=self.DB.ProjectStructure[discipline][0]
                self.rowSelected[3]=self.DB.ProjectStructure[discipline][1]
                #self.disciplineStoreAdmin.append(None,[discipline,responsible,'discipline',self.DB.ProjectStructure[discipline][1]])
                self.modifyItemDialog.hide()
            else:
                msg=self.DB.errorMsg
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Modify Discipline")
        if self.action=='modifySubdiscipline':
            subdiscipline=self.subdisciplineModEntry.get_text()
            if subdiscipline=='':
                msg="Subdiscipline is empty!"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Modify Subdiscipline")
                return
            if subdiscipline==self.subdisciplineSelected: return
            self.DB.modifySubdiscipline(self.User,self.subdisciplineSelected,self.disciplineParent,subdiscipline)
            if self.DB.error==0:
                msg="Subdiscipline " + subdiscipline + " added successfuly!"
                self.logger.info (msg)
#                self.disciplineStoreAdmin.delete(currentDiscipline,[self.itemNameSelected,'','subdiscipline'])
                self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
                if self.DB.error==1: 
                    self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
                    self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Modify Discipline")
                    return 1
                self.rowSelected[0]=subdiscipline
                self.modifyItemDialog.hide()
            else:
                msg=self.DB.errorMsg
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Modify Subdiscipline")
        if self.action=='modifyLoadcase':
            loadcase=self.loadcaseModEntry.get_text()
            if loadcase=='':
                msg="Loadcase is empty!"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Modify Loadcase")
                return
            if loadcase==self.loadcaseSelected: return
            self.DB.modifyLoadcase(self.User,self.loadcaseSelected,self.disciplineParent,self.subdisciplineParent,loadcase)
            if self.DB.error==0:
                msg="Loadcase " + loadcase + " added successfuly!"
                self.logger.info (msg)
#                self.disciplineStoreAdmin.delete(currentSubdiscipline,[self.itemNameSelected,'','loadcase'])
                self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
                if self.DB.error==1: 
                    self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
                    self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Modify Discipline")
                    return 1
                self.rowSelected[0]=loadcase
                self.modifyItemDialog.hide()
            else:
                msg=self.DB.errorMsg
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Modify Loadcase")

    def on_useridEntry_changed (self,data=None):    
        self.userModified=True
        
    def on_useridvwEntry_changed (self,data=None):    
        self.userModified=True
        
    def on_nameEntry_changed (self,data=None):    
        self.userModified=True
        
    def on_departmentEntry_changed (self,data=None):    
        self.userModified=True
        
    def on_emailEntry_changed (self,data=None):    
        self.userModified=True
        
    def on_listaCompanies_changed(self,data=None):
        self.userModified=True

    def on_stoEntry_changed(self,data=None):
        self.userModified=True
        
    def on_modifyUserButton_clicked (self, data=None):
        userid=self.useridEntry.get_text()
        useridvw=self.useridvwEntry.get_text()
        longname=self.nameEntry.get_text()
        department=self.departmentEntry.get_text()
        email=self.emailEntry.get_text()
        sto=self.stoEntry.get_text()
        company=self.listaCompanies.get_active_text()
        
        if self.userModified==False: return 
        
        found=0
        for user in self.DB.Users:
            if (user[0]==userid.upper()):
                found=1
        if (found==0):
                msg="This user doesn't exist in the system"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Modify User")
                return 1
#         self.DB.getUserProfile(self.User,userid.upper())
#         if (self.DB.error):
#             self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
#             self.show_message(self.selectDirWindow, 'dialog-error', self.DB.errorMsg, "Modify User")
#             return 1

        simfile=SimFiles()
        exists=simfile.dirExist(sto)
        if (not exists):
            msg="This storage " + sto + " doesn't exists"
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.selectDirWindow, 'dialog-error', msg, "Modify User")
            return 1
        modifUser=User(userid.upper())
        modifUser.modifyUser(self.User,self.DB,useridvw,longname,department,email,company,sto)
        if modifUser.error:
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],modifUser.errorMsg))
            self.show_message(self.selectDirWindow, 'dialog-error', modifUser.errorMsg, "Modify User")
        else:
            self.DB.cargaDatos(self.User, 'getUsers','users')
            if self.DB.error==1: 
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
                self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Modify User")
                return
            self.useridEntry.set_text(userid.upper())
            self.on_findUserButton_clicked(self.useridEntry)
            if self.DB.error==1: 
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
                self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Modify User")
                return 1
            msg="User " + userid + " modified successfully"
            self.logger.info (msg)
            self.show_message(self.selectDirWindow, 'dialog-information', msg, "Modify User")

    def on_deleteUserButton_clicked (self,data=None): 
        userid=self.useridEntry.get_text()
        useridvw=self.useridvwEntry.get_text()
        longname=self.nameEntry.get_text()
        department=self.departmentEntry.get_text()
        email=self.emailEntry.get_text()
        sto=self.stoEntry.get_text()
        company=self.listaCompanies.get_active_text()
        for user in self.DB.Users:
            if (user[0]==userid.upper()):
                found=True
                break
        if found==False:
            msg="This user doesn't exist in the system"
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.selectDirWindow, 'dialog-error', msg, "Delete User")
            return

        userToDelete=User(userid)
        # Find simulations 
        numsims=self.DB.getNumSims(self.User,"","","","","",'False',userToDelete.username.upper())
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Delete User")
            return 1
        
        # show message
        self.questionLabel1.set_markup("<span foreground='black'> THE USER " + userid + " IS OWNER OF " + numsims + " SIMULATIONS </span>")
        deleteRoles=False
        deleteUser=False
        if int(numsims)>0:
            self.questionLabel2.set_markup("<span foreground='black'> The USER " + userid + " will be DEACTIVATED. Do you want to continue? </span>")
            self.questionLabel3.set_markup("<span foreground='black'><b> (NOTE: The existing roles will be deleted) </b></span>")
            #self.YesCancelWindow.show()
            if not self.questionWindow.is_active(): 
                response = self.questionWindow.run()
                self.questionWindow.hide()
                if not response == Gtk.ResponseType.YES:
                    return 
            # Delete roles
            deleteRoles=True
            # Deactivate User
            deleteUser=False
        else:
            self.questionLabel2.set_markup("<span foreground='black'> The USER " + userid + " will be DELETED. Do you want to continue? </span>")
            self.questionLabel3.set_markup("<span foreground='black'><b> </b></span>")
            self.questionWindow.show()
            if not self.questionWindow.is_active(): 
                response = self.questionWindow.run()
                self.questionWindow.hide()
                if not response == Gtk.ResponseType.YES:
                    return 
            # Delete Roles
            deleteRoles=True
            # Delete User
            deleteUser=True

        if deleteRoles==True: 
            userToDelete.deleteRoles(self.User,self.DB)
            if userToDelete.error:
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],newUser.errorMsg))
                self.show_message(self.selectDirWindow, 'dialog-error', newUser.errorMsg, "Delete User")
                return
        userToDelete.deleteUser(self.User,self.DB,deleteUser)
        if userToDelete.error:
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],newUser.errorMsg))
            self.show_message(self.selectDirWindow, 'dialog-error', newUser.errorMsg, "Delete User")
        else:
    #         self.listaUsers.append(userid,userid)
    #         self.listaRequest.append(userid,userid)
    #         self.listaUsers.set_active_id(userid)
            self.DB.cargaDatos(self.User, 'getUsers','users')
            if self.DB.error==1: 
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
                self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Delete/deactivate User")
                return
            self.useridEntry.set_text("")
            self.on_findUserButton_clicked(self.useridEntry)
            if self.DB.error==1: 
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
                self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Delete/deactivate User")
                return 1
            msg="User " + userid + " deleted/deactivated successfully"
            self.logger.info (msg)
            self.show_message(self.selectDirWindow, 'dialog-information', msg, "Delete/deactivate User")
            
        
    def on_newUserButton_clicked (self,data=None):
        userid=self.useridEntry.get_text().upper()
        useridvw=self.useridvwEntry.get_text().upper()
        longname=self.nameEntry.get_text()
        department=self.departmentEntry.get_text()
        email=self.emailEntry.get_text()
        sto=self.stoEntry.get_text()
        company=self.listaCompanies.get_active_text()
        for user in self.DB.Users:
            if (user[0]==userid):
                msg="This user already exist in the system"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add User")
                return
        newUser=User(userid)
        newUser.addUser(self.User,self.DB,useridvw,longname,department,email,company,sto)
        if newUser.error:
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],newUser.errorMsg))
            self.show_message(self.selectDirWindow, 'dialog-error', newUser.errorMsg, "Add User")
        else:
            self.listaUsers.append(userid,userid)
            self.listaRequest.append(userid,userid)
            self.listaUsers.set_active_id(userid)
            self.DB.cargaDatos(self.User, 'getUsers','users')
            if self.DB.error==1: 
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
                self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Add User")
                return 1
            self.useridEntry.set_text(userid)
            self.on_findUserButton_clicked(self.useridEntry)
            if self.DB.error==1: 
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
                self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Modify User")
                return 1
            self.listaRolesStoreAdmin.clear()
            msg="User " + userid + " created successfully"
            self.logger.info (msg)
            self.show_message(self.selectDirWindow, 'dialog-information', msg, "Add User")


    def on_addItemButton_clicked(self,data=None): 
        selected = data.get_selected()
        self.disciplineEntry.set_text('')
        self.responsibleEntry.set_text('')
        self.subdisciplineEntry.set_text('')
        self.loadcaseEntry.set_text('')
            
        if selected[1]==None:
            # Add new Discipline
            self.action='addDiscipline'
            self.disciplineEntry.set_editable(True)
            self.disciplineEntry.set_sensitive(True)
            self.responsibleEntry.set_editable(True)
            self.responsibleEntry.set_sensitive(True)
            self.subdisciplineEntry.set_editable(False)
            self.subdisciplineEntry.set_sensitive(False)
            self.loadcaseEntry.set_editable(False)
            self.loadcaseEntry.set_sensitive(False)
        else:
            # Get type selecction
            self.rowSelected=self.disciplineStoreAdmin[selected[1]]
            self.rowIterSelected = self.disciplineStoreAdmin.get_iter(self.rowSelected.path)
            self.itemNameSelected=self.rowSelected[0]
            self.respNameSelected=self.rowSelected[1]
            self.typeSelected=self.rowSelected[2]
            if self.typeSelected=='discipline':
                # Add subdiscipline
                self.action='addSubdiscipline'     
                self.disciplineEntry.set_text(self.itemNameSelected)
                self.disciplineEntry.set_editable(False)
                self.disciplineEntry.set_sensitive(False)
                self.responsibleEntry.set_text(self.respNameSelected)
                self.responsibleEntry.set_editable(False)
                self.responsibleEntry.set_sensitive(False)
                self.subdisciplineEntry.set_editable(True)
                self.subdisciplineEntry.set_sensitive(True)
                self.loadcaseEntry.set_editable(False)
                self.loadcaseEntry.set_sensitive(False)
            if self.typeSelected=='subdiscipline':
                # Add loadcase
                self.action='addLoadcase'
                self.disciplineEntry.set_text(self.disciplineParentSelected)
                self.disciplineEntry.set_editable(False)
                self.disciplineEntry.set_sensitive(False)
                self.responsibleEntry.set_text(self.responsibleParentSelected)
                self.responsibleEntry.set_editable(False)
                self.responsibleEntry.set_sensitive(False)
                self.subdisciplineEntry.set_text(self.itemNameSelected)
                self.subdisciplineEntry.set_editable(False)
                self.subdisciplineEntry.set_sensitive(False)
                self.loadcaseEntry.set_editable(True)
                self.loadcaseEntry.set_sensitive(True)
        self.addItemDialog.show()   
    
    def on_addItem_clicked (self,data=None):
        if self.action=='addDiscipline':
            discipline=self.disciplineEntry.get_text()
            if discipline=='':
                msg="Discipline is empty!"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add Discipline")
                return
            responsible=self.responsibleEntry.get_text()        
            if responsible=='':
                msg="Responsible is empty!"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add Discipline")
                return
            if not any(responsible in x for x in self.DB.Users):
            #if not responsible in self.DB.Users:
                msg="Responsible " + responsible + " is not in the system!"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add Discipline")
                return                
            self.DB.addDiscipline(self.User,discipline,responsible)
            if self.DB.error==0:
                msg="Discipline " + discipline + " added successfuly!"
                self.logger.info (msg)
                self.disciplineStoreAdmin.append(None,[discipline,responsible,'discipline',responsible])
                self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
                self.addItemDialog.hide()
            else:
                msg=self.DB.errorMsg
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add Discipline")
        if self.action=='addSubdiscipline':
            discipline=self.itemNameSelected
            currentDiscipline=self.rowIterSelected
            subdiscipline=self.subdisciplineEntry.get_text()
            if subdiscipline=='':
                msg="Subdiscipline is empty!"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add Subdiscipline")
                return
            self.DB.addSubdiscipline(self.User,discipline,subdiscipline)
            if self.DB.error==0:
                msg="Subdiscipline " + subdiscipline + " added successfuly!"
                self.logger.info (msg)
                self.disciplineStoreAdmin.append(currentDiscipline,[subdiscipline,'','subdiscipline',''])
                self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
                self.addItemDialog.hide()
            else:
                msg=self.DB.errorMsg
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add Subdiscipline")
        if self.action=='addLoadcase':
            discipline=self.disciplineParentSelected
            subdiscipline=self.itemNameSelected
            currentSubdiscipline=self.rowIterSelected
            loadcase=self.loadcaseEntry.get_text()
            if loadcase=='':
                msg="Loadcase is empty!"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add Loadcase")
                return
            self.DB.addLoadcase(self.User,discipline,subdiscipline,loadcase)
            if self.DB.error==0:
                msg="Loadcase " + loadcase + " added successfuly!"
                self.logger.info (msg)
                self.disciplineStoreAdmin.append(currentSubdiscipline,[loadcase,'','loadcase',''])
                self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
                self.addItemDialog.hide()
            else:
                msg=self.DB.errorMsg
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add Loadcase")
        
    def on_deleteItemButton_clicked (self,data=None):
        selected = data.get_selected()
            
        if selected[1]!=None:
            # Get type selecction
            rowSelected=self.disciplineStoreAdmin[selected[1]]
            rowIterSelected = self.disciplineStoreAdmin.get_iter(rowSelected.path)
            itemNameSelected=self.rowSelected[0]
            self.respNameSelected=self.rowSelected[1]
            self.typeSelected=self.rowSelected[2]
            self.respidSelected=self.rowSelected[3]
            if self.typeSelected=='discipline':
                # Modify new Discipline
                self.disciplineSelected=itemNameSelected
                if (len(self.DB.ProjectStructure[self.disciplineSelected][2])!=0):
                    msg="You can't delete this discipline. Delete first its subdisciplines"
                    self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                    self.show_message(self.selectDirWindow, 'dialog-error', msg, "Delete Discipline")
                else:
                    self.DB.deleteDiscipline(self.User,self.disciplineSelected)
                    if self.DB.error==0:
                        msg="Discipline " + self.disciplineSelected + " deleted successfuly!"
                        self.logger.info (msg)
                        self.disciplineStoreAdmin.remove(rowIterSelected)
                        self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
                    else:
                        msg=self.DB.errorMsg
                        self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                        self.show_message(self.selectDirWindow, 'dialog-error', msg, "Delete Discipline")
            if self.typeSelected=='subdiscipline':
                # Modify subdiscipline
                self.subdisciplineSelected=itemNameSelected
                parentIter=self.getParentIter(self.disciplineStoreAdmin, rowSelected.path)
                self.disciplineParent=self.disciplineStoreAdmin.get_value(parentIter, 0)
                self.responsibleParent=self.disciplineStoreAdmin.get_value(parentIter, 1)
                subdisciplines=self.DB.ProjectStructure[self.disciplineParent][2]
                if (len(subdisciplines[self.subdisciplineSelected][2])!=0):
                    msg="You can't delete this Subdiscipline. Delete first its loadcases"
                    self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                    self.show_message(self.selectDirWindow, 'dialog-error', msg, "Delete Subdiscipline")
                else:
                    self.DB.deleteSubdiscipline(self.User,self.disciplineParent,self.subdisciplineSelected)
                    if self.DB.error==0:
                        msg="Subdiscipline " + self.subdisciplineSelected + " deleted successfuly!"
                        self.logger.info (msg)
                        self.disciplineStoreAdmin.remove(rowIterSelected)
                        self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
                    else:
                        msg=self.DB.errorMsg
                        self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                        self.show_message(self.selectDirWindow, 'dialog-error', msg, "Delete Subdiscipline")
            if self.typeSelected=='loadcase':
                # Modify loadcase
                self.loadcaseSelected=itemNameSelected
                parentIter=self.getParentIter(self.disciplineStoreAdmin, rowSelected.path)
                self.subdisciplineParent=self.disciplineStoreAdmin.get_value(parentIter, 0)
                parentIter=self.getParentIter(self.disciplineStoreAdmin, self.disciplineStoreAdmin.get_path(parentIter))
                self.disciplineParent=self.disciplineStoreAdmin.get_value(parentIter, 0)
                self.responsibleParent=self.disciplineStoreAdmin.get_value(parentIter, 1)
                self.DB.deleteLoadcase(self.User,self.disciplineParent,self.subdisciplineParent,self.loadcaseSelected)
                if self.DB.error==0:
                    msg="Loadcase " + self.loadcaseSelected + " deleted successfuly!"
                    self.logger.info (msg)
                    self.disciplineStoreAdmin.remove(rowIterSelected)
                    self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
                else:
                    msg=self.DB.errorMsg
                    self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                    self.show_message(self.selectDirWindow, 'dialog-error', msg, "Delete Loadcase")
        
    def on_ItemRow_selected(self,data,column=None,path=None):
        self.addItemButton.set_sensitive(True)
        self.deleteItemButton.set_sensitive(True)
        selected = data.get_selected()
        if selected[1]!=None:
            # Get type selecction
            self.rowSelected=self.disciplineStoreAdmin[selected[1]]
            self.rowIterSelected = self.disciplineStoreAdmin.get_iter(self.rowSelected.path)
            self.itemNameSelected=self.rowSelected[0]
            self.respNameSelected=self.rowSelected[1]
            self.typeSelected=self.rowSelected[2]
            if self.typeSelected=='subdiscipline':
                # Get discipline
                parentIter=self.getParentIter(self.disciplineStoreAdmin,self.rowSelected.path)                
                self.disciplineParentSelected=self.disciplineStoreAdmin.get_value(parentIter, 0)
                self.responsibleParentSelected=self.disciplineStoreAdmin.get_value(parentIter, 1)
            if self.typeSelected=='loadcase':
                self.addItemButton.set_sensitive(False)
        
    def on_unselectItemButton_clicked(self, data=None):
        self.disciplineView.get_selection().unselect_all()
        self.addItemButton.set_sensitive(True)
        self.deleteItemButton.set_sensitive(False)
        
        
    def on_adminStructure_activated(self,menu, data=None):
        self.msg = "Discipline Tree Admin Window"
        self.logger.debug ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.msg))
           
        # Roles
        self.disciplineStoreAdmin.clear()
        self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error getProjectStructure")
            return 1
        for discipline in self.DB.ProjectStructure:
            dis=self.DB.ProjectStructure[discipline]
            resp=dis[0]
            respid=dis[1]
            disstruct=dis[2]
            currentDiscipline=self.disciplineStoreAdmin.append(None,[discipline,resp,'discipline',respid])
            for subdiscipline in disstruct:
                subdis=disstruct[subdiscipline]
                resp=subdis[0]
                respid=subdis[1]
                subdisstruct=subdis[2]
                currentSubdiscipline=self.disciplineStoreAdmin.append(currentDiscipline,[subdiscipline,'','subdiscipline',respid])
                for loadcase in subdisstruct:
                    loadc=subdisstruct[loadcase]
                    resp=loadc[0]
                    respid=loadc[1]
                    loadcstruct=loadc[2]
                    self.disciplineStoreAdmin.append(currentSubdiscipline,[loadcase,'','loadcase',respid])

        self.disciplineAdminWin.show()

    def on_adminUser_activated(self,menu, data=None):
        self.usernameFinded.set_text("")

        self.listaUsersStoreAdmin.clear()
        self.listaRolesStoreAdmin.clear()
        
        #Get Users
        self.listaUsers.remove_all()
        for user in self.DB.Users:
            self.listaUsers.append(user[0],user[0])
        self.listaUsers.set_active(0)
        
        #Get Empresas
        if len(self.listaCompanies.get_model())==0:
            for company in self.DB.Companies:
                self.listaCompanies.append(company[0],company[0])
        self.listaCompanies.set_active(0)

        #Get Requested By
        self.listaRequest.remove_all()
        for user in self.DB.Users:
            self.listaRequest.append(user[0],user[0])
        self.listaRequest.set_active(0)
        
        #Get Projects
        if len(self.listaProjects.get_model())==0:
            for project in self.DB.Projects:
                self.listaProjects.append(project[0],project[0])
        self.listaProjects.set_active(0)
            
        #Get Disciplines
        if len(self.listaDisciplinas.get_model())==0:
            for disciplina in self.DB.Disciplinas:
                self.listaDisciplinas.append(disciplina[0],disciplina[0])
        self.listaDisciplinas.set_active(0)

        #Get Roles
        self.listaRoles.remove_all()
        for role in self.DB.Roles:
                self.listaRoles.append(self.DB.Roles[role],self.DB.Roles[role])
        self.listaRoles.set_active(0)
        
        self.useridEntry.set_text(self.User.username)
        self.useridvwEntry.set_text(self.User.Profile['useridvw'])
        self.nameEntry.set_text(self.User.Profile['longname'])
        self.departmentEntry.set_text(self.User.Profile['department'])
        self.emailEntry.set_text(self.User.Profile['correo'])
        self.dateEntry.set_text("")
        self.stoEntry.set_text(self.User.Profile['sto'])
        self.listaCompanies.set_active_id(self.User.Profile['company'])
#         for role in self.User.Profile['roles']:
#             listd=self.dict2List(self.User.Profile['roles'][role])
#             self.listaRolesStoreAdmin.append(listd)
            
        self.listaUsers.set_active_id(self.User.username)
        self.userModified=False
        
        self.adminUserWindow.show()
        return
    
    def isValidDate(self, dateinput):
        # initializing format
        format = "%d/%m/%Y"
         
        # checking if format matches the date
        res = True
         
        # using try-except to check for truth value
        try:
            res = bool(datetime.strptime(dateinput, format))
            if datetime.strptime(dateinput, format) > datetime.now(): 
                res=False
        except ValueError:
            res = False
        return res
 
    def on_selectDateButton_clicked(self,win):
        date=self.calendar.get_date()
        date_str=str(date.day) + "/" + str(date.month+1) + "/" + str(date.year)
        self.dateEntry.set_text(date_str)
        win.hide()

    def on_deleteRoleButton_clicked(self,button,data=None):
        user=self.listaUsers.get_active_text()
        request=self.listaRequest.get_active_text()
        dateReq=self.dateEntry.get_text()
        project=self.listaProjects.get_active_text()
        discipline=self.listaDisciplinas.get_active_text()
        role=self.listaRoles.get_active_text()
        
        self.DB.deleteRoleUser(self.User,user,project,discipline,role)
        if self.DB.error==0:
            self.DB.getUserProfile(self.User,user)
            if self.DB.error==0:
                self.listaRolesStoreAdmin.clear()
                for role in self.DB.Datos['roles']:
                    listd=self.dict2List(self.DB.Datos['roles'][role])
                    self.listaRolesStoreAdmin.append(listd)
                self.listaUsers.set_active_id(user)
            #self.usernameFinded.set_text("")
            msg="Role User Deleted: " + user + " - " + project + " - " + discipline + " - " + self.DB.Datos['roles'][role]['rolename']
            self.logger.info (msg)
            self.show_message(self.selectDirWindow, 'dialog-information', msg, "Delete Role User")
        else:
            msg="Role User Error: " + self.DB.errorMsg
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.selectDirWindow, 'dialog-error', msg, "Delete Role User")                    
        
    def on_rowRole_activated(self,selection,path=None,column=None):
        treestore, path = selection.get_selected_rows()
        if (len(path)>0):
            for item in path:
                user=self.user2Dict(treestore[item])
                #self.listaUsers.set_active(user['userid'])
                self.listaRequest.set_active_id(user['requester'])
                self.dateEntry.set_text(user['fechapeticion'])
                self.listaProjects.set_active_id(user['projectname'])
                self.listaDisciplinas.set_active_id(user['discipline'])
                self.listaRoles.set_active_id(user['rolename'])

    
    def on_AddRole_clicked(self,button,data=None):
        user=self.listaUsers.get_active_text()
        request=self.listaRequest.get_active_text()
        dateReq=self.dateEntry.get_text()
        project=self.listaProjects.get_active_text()
        discipline=self.listaDisciplinas.get_active_text()
        role=self.listaRoles.get_active_text()
        
        item = self.listaRolesStoreAdmin.get_iter_first ()
        if item==None: 
            self.DB.getUserProfile(self.User,user)
            if self.DB.error==0:
                self.listaRolesStoreAdmin.clear()
                for roleDB in self.DB.Datos['roles']:
                    listd=self.dict2List(self.DB.Datos['roles'][roleDB])
                    self.listaRolesStoreAdmin.append(listd)
                self.usernameFinded.set_text(user)
        while ( item != None ):
            project_done=self.listaRolesStoreAdmin.get_value (item, 0)
            discipline_done=self.listaRolesStoreAdmin.get_value (item, 1)
            role_done=self.listaRolesStoreAdmin.get_value (item, 2)
            if (project_done==project and discipline_done==discipline and role_done==role):
                msg="The Role is already asigned to this user"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add Role User")
                return
            else:
                item = self.listaRolesStoreAdmin.iter_next(item)
            
        if self.isValidDate(dateReq)==True:
            self.DB.addRoleUser(self.User,user,request,dateReq,project,discipline,role)
            if self.DB.error==0:
                self.DB.getUserProfile(self.User,user)
                if self.DB.error==0:
                    self.listaRolesStoreAdmin.clear()
                    for role in self.DB.Datos['roles']:
                        listd=self.dict2List(self.DB.Datos['roles'][role])
                        self.listaRolesStoreAdmin.append(listd)
                    self.listaUsers.set_active_id(user)
                #self.usernameFinded.set_text("")
                msg="Role User Added: " + user + " - " + project + " - " + discipline + " - " + self.DB.Datos['roles'][role]['rolename']
                self.logger.info (msg)
                self.show_message(self.selectDirWindow, 'dialog-information', msg, "Add Role User")
            else:
                msg="Role User Error: " + self.DB.errorMsg
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add Role User")                    
        else:
            msg="Date Request is not valid"
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.selectDirWindow, 'dialog-error', msg, "Add Role User")

            

    def on_sendButton_clicked(self,button,data=None):
        if len(self.items_seleccionados)>0:
            self.listaSimsStore.clear()     
            self.on_sendPlusButton_clicked(button,data)   
        self.detailsFrame.set_position(400)

            
    def on_sendPlusButton_clicked(self,button,data=None):
        if len(self.items_seleccionados)>0:
            #self.listaSimsStore.clear()    
            for item_seleccionado in self.items_seleccionados:    
                item=item_seleccionado['name']
                #nsims=item_seleccionado['nsims']
                tipo=item_seleccionado['tipo']
                datos=item_seleccionado['datos']
                sims={}
                if tipo=="Disciplina": 
                    sims=self.DB.getSims(self.User,self.selected_project,item,"","")
                if tipo=="Subdisciplina":
                    ramaDisciplina=self.getParentIter(self.project_store,item_seleccionado['path'])
                    disciplina=self.project_store.get_value(ramaDisciplina, 0)
                    sims=self.DB.getSims(self.User,self.selected_project,disciplina,item,"")
                if tipo=="LoadCase":
                    iterSubdisciplina=self.getParentIter(self.project_store,item_seleccionado['path'])
                    subdisciplina=self.project_store.get_value(iterSubdisciplina, 0)
                    iterDisciplina=self.getParentIter(self.project_store,self.project_store.get_path(iterSubdisciplina))
                    disciplina=self.project_store.get_value(iterDisciplina, 0)
                    sims=self.DB.getSims(self.User,self.selected_project,disciplina,subdisciplina,item)
                if tipo=="Simulacion":
                    sims[item]=json.loads(datos)
                    
                for sim_ref in sims:
                    datos=json.dumps(sims[sim_ref])
                    self.mostrar_Simulacion(datos)
        self.detailsFrame.set_position(400)

    def hasRights(self,access, sim):
        rights=sim['rights']  # 'RWDA'
        if access=='READ':
            if rights[0]=='R': return True
        if access=='WRITE':
            if rights[1]=='W': return True
        if access=='DELETE':
            if rights[2]=='D': return True
        if access=='CHG_ACCESSLEVEL':
            if rights[3]=='A': return True
        return False
        
    # Show Simulation Details
    def on_treesims_row_activated(self,view,path,column):
        self.id.set_text(self.sim_seleccionada['id'])
        self.name.set_text(self.sim_seleccionada['name'])
        self.project.set_text(self.sim_seleccionada['project'])
        self.disciplina.set_text(self.sim_seleccionada['disciplina'])
        self.subdisciplina.set_text(self.sim_seleccionada['subdisciplina'])
        self.loadcase.set_text(self.sim_seleccionada['loadcase'])
        self.reference.set_text(self.sim_seleccionada['reference'])
        self.variant.set_text(self.sim_seleccionada['variant'])
        self.date.set_text(self.sim_seleccionada['date'])
        self.autor.set_text(self.sim_seleccionada['autor'])
        self.autor.set_text(self.sim_seleccionada['ownerLN'] + " (" + self.sim_seleccionada['autor'] + ")")
        self.status.set_text(self.sim_seleccionada['status'])
        self.inputs.set_text(self.sim_seleccionada['inputs'])
        self.outputs.set_text(self.sim_seleccionada['outputs'])
        self.reports.set_text(self.sim_seleccionada['reports'])
        self.subloadcase.set_text(self.sim_seleccionada['subloadcase'])
        self.aux1.set_text(self.sim_seleccionada['aux1'])
        self.aux2.set_text(self.sim_seleccionada['aux2'])
        self.aux3.set_text(self.sim_seleccionada['aux3'])
        self.aux4.set_text(self.sim_seleccionada['aux4'])
        self.aux5.set_text(self.sim_seleccionada['aux5'])
        self.aux6.set_text(self.sim_seleccionada['aux6'])
        self.type.set_text(self.sim_seleccionada['type'])
        self.label.set_text(self.sim_seleccionada['label'])
        descriptionBuff = self.description.get_buffer()
        if self.sim_seleccionada['description']==None: self.sim_seleccionada['description']=""
        descriptionBuff.set_text(self.sim_seleccionada['description'])
        self.extern.set_text(self.sim_seleccionada['extern'])
        access=self.DB.AccessLevels[self.sim_seleccionada['access']]
        self.access.set_text(self.sim_seleccionada['access'] +" (" + access['value'] + ")")
        
        #simID=self.sim_seleccionada['id']
        # Simulacion=self.DB.getDetails(simID)
        self.detailsFrame.set_position(100)
        i=1
        while i<=self.SimulacionTabs.get_n_pages()-1:
            self.SimulacionTabs.remove_page(i)
        self.SimulacionTabs.show()
        self.sim_activada=self.sim_seleccionada
        self.iterMostrada_activada=self.listaSimsStore.get_iter(path)
        if (self.sim_activada['path']!=''):
            self.iter_activada=self.project_store.get_iter_from_string(self.sim_activada['path'])
        else:
            self.iter_activada=None

        # Si tiene permisos de (A)ccess level, se muestra el botton
        if self.hasRights('CHG_ACCESSLEVEL',self.sim_activada):
            self.publishButton.set_visible(True)
        else:
            self.publishButton.set_visible(False)
        if self.hasRights('WRITE',self.sim_activada):
            self.editButton.set_visible(True)
        else:
            self.editButton.set_visible(False)
        self.saveButton.set_visible(False)

        
    def on_itemSeleccionado_changed(self,selection):
        treestore, path = selection.get_selected_rows()
        if (len(path)>0):
            self.items_seleccionados.clear()
            for item in path:
                self.items_seleccionados.append(self.treesim2Dict(treestore[item]))
        
    def on_simSeleccionada_changed(self,selection):
        treestore, path = selection.get_selected_rows()
        if (len(path)>0):
            self.sim_seleccionada=self.sim2Dict(treestore[path])
        
    def user2Dict(self,row):
        # Valor text en Gtk.CellRendererText dentro de Gtk.TreViewColumn (Arbol)
        # Los que no estan, siguen los ultimos en el orden del TreeStore (projectTree) 
        treedict={}
        treedict["projectname"]=row[0]
        treedict["discipline"]=row[1]
        treedict["rolename"]=row[2]
        treedict["projectid"]=row[3]
        treedict["roleid"]=row[4]
        treedict["disciplineid"]=row[5]
        treedict["requester"]=row[6]
        treedict["requesterid"]=row[7]
        treedict["fechapeticion"]=row[8]
        treedict["fechaactivacion"]=row[9]

        return treedict

    def treesim2Dict(self,row):
        # Valor text en Gtk.CellRendererText dentro de Gtk.TreViewColumn (Arbol)
        # Los que no estan, siguen los ultimos en el orden del TreeStore (projectTree) 
        treedict={}
        treedict["name"]=row[0]
        treedict["nsims"]=row[1]
        treedict["tipo"]=row[2]
        treedict["datos"]=row[3]
        treedict["path"]=row.path
        return treedict

    def sim2Dict(self,row):
        # Valor text en Gtk.CellRendererText dentro de Gtk.TreViewColumn (treesims)
        # Los que no estan, siguen los ultimos en el orden del TreeStore (listasims) 
        simdict={}
        simdict["id"]=row[0]
        simdict["name"]=row[1]
        simdict["project"]=row[2]
        simdict["disciplina"]=row[3]
        simdict["subdisciplina"]=row[4]
        simdict["loadcase"]=row[5]
        simdict["reference"]=row[6]
        simdict["variant"]=row[7]
        simdict["autor"]=row[8]
        simdict["date"]=row[9]
        simdict["status"]=row[10]
        simdict["inputs"]=row[11]
        simdict["outputs"]=row[12]
        simdict["reports"]=row[13]
        simdict["ownerLN"]=row[14]
        simdict["extern"]=row[15]
        simdict["access"]=row[16]
        simdict["subloadcase"]=row[17]
        simdict["aux1"]=row[18]
        simdict["aux2"]=row[19]
        simdict["aux3"]=row[20]
        simdict["aux4"]=row[21]
        simdict["aux5"]=row[22]
        simdict["aux6"]=row[23]
        simdict["label"]=row[24]
        simdict["description"]=row[25]
        simdict["type"]=row[26]
        simdict["rights"]=row[27]
        simdict["path"]=row[28]
        return simdict

    def updateIterListStore(self,row,col,value):
        # Valor text en Gtk.CellRendererText dentro de Gtk.TreViewColumn (treesims)
        # Los que no estan, siguen los ultimos en el orden del TreeStore (listasims) 
        if col=="id": row[0]=value
        if col=="name": row[1]=value
        if col=="project": row[2]=value
        if col=="disciplina": row[3]=value
        if col=="subdisciplina": row[4]=value
        if col=="loadcase": row[5]=value
        if col=="reference": row[6]=value
        if col=="variant": row[7]=value
        if col=="autor": row[8]=value
        if col=="date": row[9]=value
        if col=="status": row[10]=value
        if col=="inputs": row[11]=value
        if col=="outputs": row[12]=value
        if col=="reports": row[13]=value
        if col=="ownerLN": row[14]=value
        if col=="extern": row[15]=value
        if col=="access": row[16]=value
        if col=="subloadcase": row[17]=value
        if col=="aux1": row[18]=value
        if col=="aux2": row[19]=value
        if col=="aux3": row[20]=value
        if col=="aux4": row[21]=value
        if col=="aux5": row[22]=value
        if col=="aux6": row[23]=value
        if col=="label": row[24]=value
        if col=="description": row[25]=value
        if col=="rights": row[26]=value
        if col=="path": row[27]=value
        return row

    def dict2List(self,dictorig):
        newlist=[]
        for elem in dictorig:
            newlist.append(dictorig[elem])
        return newlist

    def populateFileSystemTreeStore(self,treeStore, files, parent=None):
        itemCounter = 0
        # iterate over the items in the path
        for item in files:
            # Get the absolute path of the item
            itemPath = files[item]['path']
            # Determine if the item is a folder
            itemIsFolder = files[item]['isFolder']
            # Get size
            itemSize = files[item]['size']
            # Generate an icon from the default icon theme
            folder=int(itemIsFolder)
            #https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
            if folder:
                itemIcon = Gtk.IconTheme.get_default().load_icon("folder", 22, 0)
            else:    
                itemIcon = Gtk.IconTheme.get_default().load_icon("text-x-generic", 22, 0)
            # add dummy if current item was a folder
            if folder:
                # Append the item to the TreeStore
                currentIter = treeStore.append(parent,[item, itemIcon, itemPath,folder,False,True,itemSize])
           
                #filesfolder=self.DB.getFiles(self.sim_seleccionada['id'], itemFullname)
                #self.populateFileSystemTreeStore(treeStore, filesfolder, currentIter)
                self.populateFileSystemTreeStore(treeStore, files[item]['folder'], currentIter)
                    #currentIter = treeStore.append(currentIter, [None, None, None])
            else:
                currentIter = treeStore.append(parent,[item, itemIcon, itemPath,folder,False,False,itemSize])

            #increment the item counter
            itemCounter += 1
        # add the dummy node back if nothing was inserted before
        #if itemCounter < 1: treeStore.append(parent, [None, None, None,None,None])

    def selectSubTree (self, row):
        activation=row[4]
        treepath=row.path
        treeiter=self.fileSystemTreeStore.get_iter(treepath)
        if self.fileSystemTreeStore.iter_has_child(treeiter)==True:
            treepath.down()
            nextItem=1
            while nextItem != None:
                subtreeiter=self.fileSystemTreeStore.get_iter(treepath)
                subrow=self.fileSystemTreeStore[subtreeiter]
                filename=subrow[0]
                if subrow[3]==True: # is folder
                    if self.selected_files.get(filename) != None:
                        del self.selected_files[filename]
                        msg="folder: " + filename + " deleted from selection"
                        self.logger.debug(": %s" % (msg))
                    subrow[4]=activation
                    self.selectSubTree(subrow)
                nextItem=subrow.next
                if next != None:
                    treepath.next()

    def unselectBrothers (self, row):
        treepath=row.path
        nextItem=row.next
        # Next Brothers
        while nextItem != None:
            treepath.next()
            brotheriter=self.fileSystemTreeStore.get_iter(treepath)
            brotherrow=self.fileSystemTreeStore[brotheriter]
            self.unselectTree(brotherrow)
            nextItem=brotherrow.next
        # Previous Brothers
        prev=row.previous
        while prev != None:
            treepath.prev()
            brotheriter=self.fileSystemTreeStore.get_iter(treepath)
            brotherrow=self.fileSystemTreeStore[brotheriter]
            self.unselectTree(brotherrow)
            prev=brotherrow.previous

    def selectBrothers (self, row):
        treepath=row.path
        nextItem=row.next
        # Next Brothers
        while nextItem != None:
            treepath.next()
            brotheriter=self.fileSystemTreeStore.get_iter(treepath)
            brotherrow=self.fileSystemTreeStore[brotheriter]
            filename=brotherrow[0]
            activation=brotherrow[4]
            path=brotherrow[2]
            if brotherrow[3]==True: # is folder
                if activation == True:
                    self.selected_files[filename]=path
                    msg="folder: " + filename + " added to selection"
                    self.logger.debug(": %s" % (msg))
            nextItem=brotherrow.next
        # Previous Brothers
        prev=row.previous
        while prev != None:
            treepath.prev()
            brotheriter=self.fileSystemTreeStore.get_iter(treepath)
            brotherrow=self.fileSystemTreeStore[brotheriter]
            filename=brotherrow[0]
            activation=brotherrow[4]
            path=brotherrow[2]
            if brotherrow[3]==True: # is folder
                if activation == True:
                    self.selected_files[filename]=path
                    msg="folder: " + filename + " added to selection"
                    self.logger.debug(": %s" % (msg))
            prev=brotherrow.previous

    def unselectFather (self, row):
        # get father
        activation=row[4]
        # if is selected -> unselect father
        if activation==True:
            row[4]=False
            filename=row[0]
            # delete row
            del self.selected_files[filename]
            msg="folder: " + filename + " deleted from selection"
            self.logger.debug(": %s" % (msg))
            if row.parent != None:
                self.unselectFather(row.parent)

    def unselectTree (self, row):
        # get father
        activation=row[4]
        # if is selected -> unselect father
        if activation==True:
            row[4]=False
            filename=row[0]
            # delete row
            if self.selected_files.get(filename) != None:
                del self.selected_files[filename]
                msg="folder: " + filename + " deleted from selection"
                self.logger.debug(": %s" % (msg))
        treepath=row.path
        treeiter=self.fileSystemTreeStore.get_iter(treepath)
        if self.fileSystemTreeStore.iter_has_child(treeiter)==True:
            treepath.down()
            treeiter=self.fileSystemTreeStore.get_iter(treepath)
            childrow=self.fileSystemTreeStore[treeiter]
            self.unselectTree(childrow)
            self.unselectBrothers(childrow)

                   
    def on_selected_folder(self,cell,treepath): 
        filename = self.fileSystemTreeStore[treepath][0]
        path = self.fileSystemTreeStore[treepath][2]
        isfolder = self.fileSystemTreeStore[treepath][3]
        activated = self.fileSystemTreeStore[treepath][4]
        self.fileSystemTreeStore[treepath][4] = not activated
        if not activated == True:
            self.selected_files[filename]=path
            msg="folder: " + filename + " added to selection"
            self.logger.debug(": %s" % (msg))
        else:
            if self.selected_files.get(filename) != None:
                del self.selected_files[filename]  
                msg="folder: " + filename + " deleted from selection"
                self.logger.debug(": %s" % (msg))
            else: 
                # Habia sido seleccionado el padre
                # borrar padre de la lista e insertar hijos sueltos
                treeiter=self.fileSystemTreeStore.get_iter_from_string(treepath)
                row=self.fileSystemTreeStore[treeiter]
                if row.parent != None:
                    self.unselectFather(row.parent)
                    # add all selected brothers to selected_files
                    self.selectBrothers(row)
        if isfolder == True:
            treeiter=self.fileSystemTreeStore.get_iter_from_string(treepath)
            row=self.fileSystemTreeStore[treeiter]
            self.selectSubTree(row)   
        if len(self.selected_files) >0:
            self.downloadButton.set_visible(True)
        else:
            self.downloadButton.set_visible(False)
        
    def on_publishButton_clicked (self,button,data=None): 
        self.Sim = Simulacion()
        result=self.Sim.changeAccessLevel(self.User,self.sim_activada, self.DB)
        if result==0:
            msg="Access Level Changed"
            self.logger.info (msg)
            self.show_message(self.selectDirWindow, 'dialog-information', "Access Level Changed", "Change Access Level")
            access=self.DB.AccessLevels[self.Sim.AccessLevel]

            # Actualizacion de datos en las selecciones y arbol
            if (self.iter_activada!=None): # los datos se han carcado del arbol, sino, es nueva simulacion y no existe en el arbol
                datos_actuales=self.project_store[self.iter_activada][-1]
                datosDict=json.loads(datos_actuales)
                datosDict['access']=self.Sim.AccessLevel
                datosDict['rights']=self.Sim.Rights                
                datos_modif=json.dumps(datosDict)
                self.project_store[self.iter_activada][-1]=datos_modif
            self.access.set_text(self.Sim.AccessLevel + " (" + access['value'] + ")")
            self.sim_activada['access']=self.Sim.AccessLevel
            self.sim_seleccionada['access']=self.Sim.AccessLevel
            self.sim_activada['rights']=self.Sim.Rights
            self.sim_seleccionada['rights']=self.Sim.Rights 
            
            if self.hasRights('CHG_ACCESSLEVEL',self.sim_activada):
                self.publishButton.set_visible(True)
            else:
                self.publishButton.set_visible(False)     
            if self.hasRights('WRITE',self.sim_activada):
                self.editButton.set_visible(True)
            else:
                self.editButton.set_visible(False)     
                self.saveButton.set_visible(False)     
        else:
            msg=self.Sim.error
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.selectDirWindow, 'dialog-error', "Access Level not Changed: " + self.Sim.error, "Change Access Level")
            
    def on_refreshButton_clicked (self,button,data=None): 
        if not self.selected_project == 'Select Project ...':
            # Limpiamos carga antigua
            self.project_store.clear()
            # Identificamos proyecto
            self.selected_projectID=self.User.getProjectID(self.selected_project)
            # Identificamos estado
            if self.selected_estado == 'Select Status ...':
                self.selected_estadoID=""
            else:
                self.selected_estadoID=self.DB.getEstadoID(self.selected_estado)

            tipoParent="root"
            tipoChild=self.User.getTipoChild(tipoParent)
                 
            # Cargamos Rama in the TreeStore model
            self.cargaRama(tipoParent, tipoChild, None, self.selected_projectID,self.selected_estadoID,self.seeOwnSims)


    def on_editButton_clicked (self,button,data=None): 
        self.editButton.set_sensitive(False)    
        self.saveButton.set_visible(True)     
        self.publishButton.set_sensitive(False)    
        self.Sim = Simulacion()
        self.label.set_editable(True)
        self.description.set_editable(True) 
        
        context_label = self.label.get_style_context()
        context_label.add_class("editLabel")
#         context_desc = self.description.get_style_context()
#         state = Gtk.StateFlags.NORMAL
#         color = context_desc.get_property("background-color", Gtk.StateFlags.NORMAL)
#         color = context_desc.get_background_color(state)
#         context_desc.set_property("background-color:", Gtk.StateFlags.NORMAL)
#         context_desc.add_class("editLabel")
        
        self.labeltext=self.label.get_text();
        descriptionbuff=self.description.get_buffer();
        self.descriptiontext=descriptionbuff.get_text(descriptionbuff.get_start_iter(),descriptionbuff.get_end_iter(),False);

    def on_saveButton_clicked (self,button,data=None): 
        button_context = self.label.get_style_context()
        button_context.remove_class("editLabel")
        self.label.set_editable(False)
        self.description.set_editable(False) 
        
        labeltextmofified=self.label.get_text()
        descriptionbuff=self.description.get_buffer()
        descriptiontextmodified=descriptionbuff.get_text(descriptionbuff.get_start_iter(),descriptionbuff.get_end_iter(),False)
        
        if (self.labeltext!=labeltextmofified) | (self.descriptiontext!=descriptiontextmodified):
            changes=dict();
            if self.labeltext!=labeltextmofified:
                changes['label']=labeltextmofified
            if self.descriptiontext!=descriptiontextmodified:
                changes['description']=descriptiontextmodified
                
            error=self.Sim.modifySimulation(self.User,self.sim_activada, self.DB,changes)

            if error==1:
                if self.labeltext!=labeltextmofified:
                    self.label.set_text(self.labeltext)
                if self.descriptiontext!=descriptiontextmodified:
                    self.descriptionbuff.set_text(self.descriptiontext,len(self.descriptiontext))
                msg=self.DB.errorMsg
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.selectDirWindow, 'dialog-error', self.DB.errorMsg, "Modify Simulation")
            else:
                rowLista=self.listaSimsStore[self.iterMostrada_activada]
                if (self.iter_activada!=None):
                    datos_actuales=self.project_store[self.iter_activada][-1]
                    datosDict=json.loads(datos_actuales)
                    
                if self.labeltext!=labeltextmofified:
                    self.sim_activada['label']=self.Sim.Label
                    self.updateIterListStore(rowLista,'label',self.Sim.Label)
                    #self.sim_seleccionada['label']=self.Sim.Label
                    if (self.iter_activada!=None):
                        datosDict['label']=self.Sim.Label
                if self.descriptiontext!=descriptiontextmodified:
                    self.sim_activada['description']=self.Sim.Description
                    self.updateIterListStore(rowLista,'description',self.Sim.Description)
                    #self.sim_seleccionada['description']=self.Sim.Description
                    if (self.iter_activada!=None):
                        datosDict['description']=self.Sim.Description
                    
                #self.listaSimsStore[self.iterMostrada_activada]=rowLista
                if (self.iter_activada!=None):
                    datos_modif=json.dumps(datosDict)
                    self.project_store[self.iter_activada][-1]=datos_modif
        
        self.saveButton.set_visible(False)     
        self.editButton.set_sensitive(True)     
        self.publishButton.set_sensitive(True)     
            
           
    def on_download_clicked(self,button,data=None): 
        self.selectDirWindow.set_current_folder(self.User.Profile['sto'])
        if not self.selectDirWindow.is_active(): 
            response = self.selectDirWindow.run()
            if not response == Gtk.ResponseType.ACCEPT:
                self.selectDirWindow.hide()
                return
        userdir = self.selectDirWindow.get_file()
        dirdest=userdir.get_path()

        self.selectDirWindow.hide()
        self.Sim = Simulacion()
        
        self.logger.info("Checking MD5 Files")
        self.DB.checkMD5(self.User,self.sim_activada['id'])
        if (self.DB.error):
            msg="Simulation not consistent. Someone change the files in server"
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.selectDirWindow, 'dialog-warning', msg, "Checking Simulation")
            
        self.logger.info("Downloading Files")
        #self.main_window.show_now()
        #https://pythonhosted.org/pyglet/programming_guide/changing_the_mouse_cursor.html
#         import pyglet
#         window = pyglet.window.Window()
#         cursor = window.get_system_mouse_cursor(win.CURSOR_WAIT)
#         window.set_mouse_cursor(cursor)
        self.Sim.downloadFiles(self.sim_activada,self.User, self.DB, dirdest,self.selected_files,self.logger)
#         cursor = window.get_system_mouse_cursor(win.CURSOR_DEFAULT)
#         window.set_mouse_cursor(cursor)

        if self.Sim.error == 0:
            msg="Simulation downloaded OK"
            self.logger.info (msg)
            self.show_message(self.selectDirWindow, 'dialog-information', "Simulation downloaded OK", "Download Simulation")
        else:
            msg="Simulation not downloaded: " + self.Sim.errorMsg
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.selectDirWindow, 'dialog-error', "Simulation not downloaded: " + self.Sim.errorMsg, "Download Simulation")
        
        
        
    def on_files_clicked(self,button,data=None): 
        if self.SimulacionTabs.get_n_pages()>1:
            i=1
            while i<=self.SimulacionTabs.get_n_pages()-1:
                page=self.SimulacionTabs.get_nth_page(i)
                if self.SimulacionTabs.get_tab_label_text(page)=='Files':
                    self.SimulacionTabs.set_current_page(i)
                    return
                i+=1
        
        files=self.DB.getFiles(self.User,self.sim_activada['id'])
        self.selected_files={}
        if self.DB.error==1:
            msg=self.DB.errorMsg
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.selectFileWindow,"dialog-error",self.DB.errorMsg,"Error View Files")
            self.selectFileWindow.hide()
            return

        # initialize the filesystem treestore
        self.fileSystemTreeStore = self.MainGlade.get_object("fileSystemTreeStore")
        # populate the tree store
        self.fileSystemTreeStore.clear();
        # Get the absolute path of the item
        itemFullname = ""
        # Determine if the item is a folder
        itemIsFolder = True
        # Generate an icon from the default icon theme
        itemIcon = Gtk.IconTheme.get_default().load_icon("folder", 22, 0)
        # Append the item to the TreeStore
        name=self.sim_activada['name']
#         currentIter = self.fileSystemTreeStore.append(None,[name, itemIcon, itemFullname,int(itemIsFolder),False,True,"-"])
#         self.populateFileSystemTreeStore(self.fileSystemTreeStore, files, currentIter)
        self.populateFileSystemTreeStore(self.fileSystemTreeStore, files, None)

       
        page=self.MainGlade.get_object("pageTreeView") 
        tab_label = Gtk.Label()
        tab_label.set_text('Files')
        page.show()
        self.SimulacionTabs.append_page(page,tab_label)
        self.SimulacionTabs.set_current_page(-1)

    def on_switch_current_page(self,Notebook,Scrolled,page): 
        self.msg = ""
        self.logger.debug ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.msg))
        if page==1: # Files Page
            self.publishButton.set_visible(False)
            self.editButton.set_visible(False)
            self.saveButton.set_visible(False)
            if len(self.selected_files) >0:
                self.downloadButton.set_visible(True)
            else:
                self.downloadButton.set_visible(False)
        else:
            self.publishButton.set_visible(False)
            self.editButton.set_visible(False)
            self.saveButton.set_visible(False)
            if self.hasRights('CHG_ACCESSLEVEL',self.sim_activada):
                self.publishButton.set_visible(True)
            if self.hasRights('WRITE',self.sim_activada):
                self.editButton.set_visible(True)
            self.downloadButton.set_visible(False)
                      
    # Signals comunes
    def gtk_main_quit(self, widget, data=None):
        self.msg = ""
        self.logger.debug ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.msg))
        Gtk.main_quit()
        return False
    
    def gtk_DisciplineTree_show (self,DisciplineWin):
        self.msg = "Discipline Tree Show Window"
        self.logger.debug ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.msg))
           
        # Roles
        self.disciplineStore.clear()
        self.DB.cargaDatos(self.User, 'getProjectStructure','discipline')
        if self.DB.error==1: 
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.DB.errorMsg))
            self.show_message(self.LoginWindow,"dialog-error",self.DB.errorMsg,"Error getProjectStructure")
            return 1
        for discipline in self.DB.ProjectStructure:
            dis=self.DB.ProjectStructure[discipline]
            resp=dis[0]
            disstruct=dis[2]
            currentDiscipline=self.disciplineStore.append(None,[discipline,resp])
            for subdiscipline in disstruct:
                subdis=disstruct[subdiscipline]
                resp=subdis[0]
                subdisstruct=subdis[2]
                currentSubdiscipline=self.disciplineStore.append(currentDiscipline,[subdiscipline,resp])
                for loadcase in subdisstruct:
                    loadc=subdisstruct[loadcase]
                    resp=loadc[0]
                    self.disciplineStore.append(currentSubdiscipline,[loadcase,resp])
        DisciplineWin.show_all()

    def gtk_UserProfile_show (self,UserProfileWin):
        self.msg = "User Profile Show Window"
        self.logger.debug ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.msg))
        self.vwiduserLabel = self.MainGlade.get_object("vwiduserProfile")
        if (self.vwiduserLabel.get_text()==''):
            self.useridLabel = self.MainGlade.get_object("useridProfile")
            self.useridLabel.set_text(self.User.username.upper())
            self.vwiduserLabel.set_text(self.User.Profile['useridvw'])
            self.nameLabel = self.MainGlade.get_object("nameProfile")
            self.nameLabel.set_text(self.User.Profile['longname'])
            self.departmentLabel = self.MainGlade.get_object("departmentProfile")
            self.departmentLabel.set_text(self.User.Profile['department'])
            self.correoLabel = self.MainGlade.get_object("emailProfile")
            self.correoLabel.set_text(self.User.Profile['correo'])
            self.stoLabel = self.MainGlade.get_object("stoProfile")
            self.stoLabel.set_text(self.User.Profile['sto'])
            
            # Roles
            self.listaRolesStore.clear()
            for role in self.User.Profile['roles']:
                listd=self.dict2List(self.User.Profile['roles'][role])
                self.listaRolesStore.append(listd)
        UserProfileWin.show_all()
        
    def gtk_RightsWindow_show (self,RightsWindow):
        self.msg = ""
        self.logger.debug ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.msg))
        self.e0r1_own = self.MainGlade.get_object('e0r1-own')
        if (self.e0r1_own.get_text()==''):
            # Etiquetas Roles
            self.role1_own = self.MainGlade.get_object('role1-own')
            self.role2_own = self.MainGlade.get_object('role2-own')
            self.role3_own = self.MainGlade.get_object('role3-own')
            self.role4_own = self.MainGlade.get_object('role4-own')
            self.role1_own.set_text(self.DB.Roles.get('1'))
            self.role2_own.set_text(self.DB.Roles.get('2'))
            self.role3_own.set_text(self.DB.Roles.get('3'))
            self.role4_own.set_text(self.DB.Roles.get('4'))
             
            self.role1 = self.MainGlade.get_object('role1')
            self.role2 = self.MainGlade.get_object('role2')
            self.role3 = self.MainGlade.get_object('role3')
            self.role4 = self.MainGlade.get_object('role4')
            self.role1.set_text(self.DB.Roles.get('1'))
            self.role2.set_text(self.DB.Roles.get('2'))
            self.role3.set_text(self.DB.Roles.get('3'))
            self.role4.set_text(self.DB.Roles.get('4'))
             
            # Etiquetas Access Levels
            self.estado0_own = self.MainGlade.get_object('estado0-own')
            self.estado1_own = self.MainGlade.get_object('estado1-own')
            self.estado2_own = self.MainGlade.get_object('estado2-own')
            self.estado0_own.set_text('0')
            self.estado1_own.set_text('1')
            self.estado2_own.set_text('2')
 
            self.estado0 = self.MainGlade.get_object('estado0')
            self.estado1 = self.MainGlade.get_object('estado1')
            self.estado2 = self.MainGlade.get_object('estado2')
            self.estado0.set_text('0')
            self.estado1.set_text('1')
            self.estado2.set_text('2')
                        
            # Permisos
            self.e0r1_own = self.MainGlade.get_object('e0r1-own')
            self.e1r1_own = self.MainGlade.get_object('e1r1-own')
            self.e2r1_own = self.MainGlade.get_object('e2r1-own')
            self.e0r2_own = self.MainGlade.get_object('e0r2-own')
            self.e1r2_own = self.MainGlade.get_object('e1r2-own')
            self.e2r2_own = self.MainGlade.get_object('e2r2-own')
            self.e0r3_own = self.MainGlade.get_object('e0r3-own')
            self.e1r3_own = self.MainGlade.get_object('e1r3-own')
            self.e2r3_own = self.MainGlade.get_object('e2r3-own')
            self.e0r4_own = self.MainGlade.get_object('e0r4-own')
            self.e1r4_own = self.MainGlade.get_object('e1r4-own')
            self.e2r4_own = self.MainGlade.get_object('e2r4-own')
            
            self.e0r1_own.set_text(self.DB.Rights.get('e0r1_T'))
            self.e1r1_own.set_text(self.DB.Rights.get('e1r1_T'))
            self.e2r1_own.set_text(self.DB.Rights.get('e2r1_T'))
            self.e0r2_own.set_text(self.DB.Rights.get('e0r2_T'))
            self.e1r2_own.set_text(self.DB.Rights.get('e1r2_T'))
            self.e2r2_own.set_text(self.DB.Rights.get('e2r2_T'))
            self.e0r3_own.set_text(self.DB.Rights.get('e0r3_T'))
            self.e1r3_own.set_text(self.DB.Rights.get('e1r3_T'))
            self.e2r3_own.set_text(self.DB.Rights.get('e2r3_T'))
            self.e0r4_own.set_text(self.DB.Rights.get('e0r4_T'))
            self.e1r4_own.set_text(self.DB.Rights.get('e1r4_T'))
            self.e2r4_own.set_text(self.DB.Rights.get('e2r4_T'))

            self.e0r1 = self.MainGlade.get_object('e0r1')
            self.e1r1 = self.MainGlade.get_object('e1r1')
            self.e2r1 = self.MainGlade.get_object('e2r1')
            self.e0r2 = self.MainGlade.get_object('e0r2')
            self.e1r2 = self.MainGlade.get_object('e1r2')
            self.e2r2 = self.MainGlade.get_object('e2r2')
            self.e0r3 = self.MainGlade.get_object('e0r3')
            self.e1r3 = self.MainGlade.get_object('e1r3')
            self.e2r3 = self.MainGlade.get_object('e2r3')
            self.e0r4 = self.MainGlade.get_object('e0r4')
            self.e1r4 = self.MainGlade.get_object('e1r4')
            self.e2r4 = self.MainGlade.get_object('e2r4')
            
            self.e0r1.set_text(self.DB.Rights.get('e0r1_F'))
            self.e1r1.set_text(self.DB.Rights.get('e1r1_F'))
            self.e2r1.set_text(self.DB.Rights.get('e2r1_F'))
            self.e0r2.set_text(self.DB.Rights.get('e0r2_F'))
            self.e1r2.set_text(self.DB.Rights.get('e1r2_F'))
            self.e2r2.set_text(self.DB.Rights.get('e2r2_F'))
            self.e0r3.set_text(self.DB.Rights.get('e0r3_F'))
            self.e1r3.set_text(self.DB.Rights.get('e1r3_F'))
            self.e2r3.set_text(self.DB.Rights.get('e2r3_F'))
            self.e0r4.set_text(self.DB.Rights.get('e0r4_F'))
            self.e1r4.set_text(self.DB.Rights.get('e1r4_F'))
            self.e2r4.set_text(self.DB.Rights.get('e2r4_F'))
            
            # Legend
            self.estado0_Legend = self.MainGlade.get_object('estado0_Legend')
            self.estado1_Legend = self.MainGlade.get_object('estado1_Legend')
            self.estado2_Legend = self.MainGlade.get_object('estado2_Legend')
            self.estado0_Legend.set_text('0')
            self.estado1_Legend.set_text('1')
            self.estado2_Legend.set_text('2')

            self.estado0_Description = self.MainGlade.get_object('estado0_Description')
            self.estado1_Description = self.MainGlade.get_object('estado1_Description')
            self.estado2_Description = self.MainGlade.get_object('estado2_Description')
            self.estado0_Description.set_text(self.DB.AccessLevels['0']['value'] + " (" + self.DB.AccessLevels['0']['desc'] + ")")
            self.estado1_Description.set_text(self.DB.AccessLevels['1']['value'] + " (" + self.DB.AccessLevels['1']['desc'] + ")")
            self.estado2_Description.set_text(self.DB.AccessLevels['2']['value'] + " (" + self.DB.AccessLevels['2']['desc'] + ")")

        RightsWindow.show_all()
                    
    def gtk_widget_show(self, widget, data=None):
        self.msg = ""
        self.logger.debug ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.msg))
        widget.show_all()

    def gtk_widget_hide(self, widget, data=None):
        self.msg = ""
        self.logger.debug ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.msg))
        widget.hide()
        
    def gtk_NewSimFolderChanged(self,filechooser, data=None):
        folder=os.path.realpath(filechooser.get_current_folder())
        STO=os.path.realpath(self.User.Profile['sto'])
        if (STO != folder[:len(STO)]):
            msg="Change Folder Forbidden. Only in STO folder"
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(filechooser,"dialog-error",msg,"Error new Simulation")
            filechooser.set_current_folder(self.User.Profile['sto'])

        
    def gtk_NewSimulation(self,widget,data=None):
        # Llamada a nueva simulacion con parametros
        # 
#        response=Gtk.ResponseType.REJECT
        if not os.path.exists(self.User.Profile['sto']):
            self.show_message(self.selectFileWindow,"dialog-error","STO " + self.User.Profile['sto'] +" is no accesible","Error new Simulation")
            return
        
        self.selectFileWindow.set_current_folder(self.User.Profile['sto'])

        if not self.selectFileWindow.is_active(): 
            response = self.selectFileWindow.run()
            if not response == Gtk.ResponseType.ACCEPT:
                self.selectFileWindow.hide()
                return
        
        file = self.selectFileWindow.get_file()
        self.Sim = Simulacion()
#        Sim.NewSimulation(self,file)
        self.Sim.Filename=file.get_path()
        self.Sim.Name=Path(self.Sim.Filename).stem
        if not self.Sim.isStructureOK(self.logger):
            msg="Simulation Folder Structure error"
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.selectFileWindow,"dialog-error",msg,"Read error")
            self.selectFileWindow.hide()
            return
        SimFile=SimFiles()
        file = SimFile.openfile(self.Sim.Filename,'r')
        if SimFile.error:
            msg=SimFile.errorMsg
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.selectFileWindow,"dialog-error",SimFile.errorMsg,"Read error")           
        self.Sim.readCabecera(file)
        self.selectFileWindow.hide()
        if not self.Sim.error:
            self.showCabecera()
        else:
            msg="Error reading HeadFile. HeadFile error: " + self.Sim.errorMsg
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.selectFileWindow,"dialog-error",msg,"Error reading HeadFile")

    def showCabecera(self):
        self.buttonImport.set_sensitive(True)
        valid=self.DB.isValidSimulation(self.User, self.Sim)
        filename = self.SimGlade.get_object("filename") 
        filename.set_text(self.Sim.Filename)
        name = self.SimGlade.get_object("name") 
        name.set_text(self.Sim.Name)
#         for project_ref in self.User.Projects:
#             self.listaProyectos.append_text(project_ref[0])
#         self.listaProyectos.insert_text(0,self.Sim.Proyecto)
#         self.listaProyectos.set_active(0)
        proyecto = self.SimGlade.get_object("proyecto") 
        proyecto.set_text(self.Sim.Proyecto)
#         for tipo_ref in self.DB.Tipos:
#             self.listaTipos.append_text(tipo_ref[0])
        self.listaTipos.insert_text(0,self.Sim.Tipo)
        self.listaTipos.set_active(0)
#         for estado_ref in self.DB.Estados:
#             self.listaEstados.append_text(estado_ref[0])
        self.listaEstados.insert_text(0,self.Sim.Estado)
        self.listaEstados.set_active(0) 
#         for disciplina_ref in self.DB.Disciplinas:
#             self.listaDisciplina.append_text(disciplina_ref[0])
        self.listaDisciplina.insert_text(0,self.Sim.Disciplina)
        self.listaDisciplina.set_active(0)
#         # Dada la Disciplina activa, carga las subdisciplinas necesarias
#         for subdisciplina_ref in self.Sim.Subdisciplinas:
#             self.listaSubdisciplina.append_text(subdisciplina_ref)
        self.listaSubdisciplina.insert_text(0,self.Sim.Subdisciplina)
        self.listaSubdisciplina.set_active(0)
#         # Dada la SubDisciplina activa, carga los LoadCases necesarias
#         for loadcase_ref in self.Sim.LoadCases:
#             self.listaLoadCase.append_text(loadcase_ref[0])
        self.listaLoadCase.insert_text(0,self.Sim.LoadCase)
        self.listaLoadCase.set_active(0)
        subloadcase = self.SimGlade.get_object("subloadcase") 
        subloadcase.set_text(self.Sim.SubLoadcase)
        aux1 = self.SimGlade.get_object("aux1") 
        aux1.set_text(self.Sim.Aux1)
        aux2 = self.SimGlade.get_object("aux2") 
        aux2.set_text(self.Sim.Aux1)
        aux3 = self.SimGlade.get_object("aux3") 
        aux3.set_text(self.Sim.Aux1)
        aux4 = self.SimGlade.get_object("aux4") 
        aux4.set_text(self.Sim.Aux1)
        aux5 = self.SimGlade.get_object("aux5") 
        aux5.set_text(self.Sim.Aux1)
        aux6 = self.SimGlade.get_object("aux6") 
        aux6.set_text(self.Sim.Aux1)
        variant = self.SimGlade.get_object("variant") 
        variant.set_text(self.Sim.Variant)
        reference = self.SimGlade.get_object("reference") 
        reference.set_text(self.Sim.Reference)
        label = self.SimGlade.get_object("label") 
        label.set_text(self.Sim.Label)
        description = self.SimGlade.get_object("description") 
        descriptionBuff = description.get_buffer()
        descriptionBuff.set_text(self.Sim.Description)


        self.labelProject.set_text("")
        self.labelTipo.set_text("")
        self.labelEstado.set_text("")
        self.labelDisciplina.set_text("")
        self.labelSubdisciplina.set_text("")
        self.labelLoadCase.set_text("")
        if not valid:
            self.buttonImport.set_sensitive(False)
            if self.DB.errorMsg=='project':
                msg="Project not Valid"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                label=self.labelProject.get_text()
                self.labelProject.set_markup("<span foreground='red'><b>#ERROR#</b></span>")
            if self.DB.errorMsg=='tipo':
                msg="Type not Valid"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                label=self.labelTipo.get_text()
                self.labelTipo.set_markup("<span foreground='red'><b>#ERROR#</b></span>")
            if self.DB.errorMsg=='estado':
                msg="Status not Valid"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                label=self.labelEstado.get_text()
                self.labelEstado.set_markup("<span foreground='red'><b>#ERROR#</b></span>")
            if self.DB.errorMsg=='disciplina':
                msg="Discipline not Valid"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                label=self.labelDisciplina.get_text()
                self.labelDisciplina.set_markup("<span foreground='red'><b>#ERROR#</b></span>")
            if self.DB.errorMsg=='subdisciplina':
                msg="Subdiscipline not Valid"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                label=self.labelSubdisciplina.get_text()
                self.labelSubdisciplina.set_markup("<span foreground='red'><b>#ERROR#</b></span>")
            if self.DB.errorMsg=='loadcase':
                msg="Loadcase not Valid"
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                label=self.labelLoadCase.get_text()
                self.labelLoadCase.set_markup("<span foreground='red'><b>#ERROR#</b></span>")

        self.NewSimWindow.show()
    
    def gtk_overwrite_simulation(self,widget):
        self.YesCancelWindow.hide()
        
        # Delete simulation
        self.DB.deleteSimulation(self.User,self.simduplicated[0])
        if (self.DB.error==0):  
            # Import simulation
            self.Sim.importSimulation(self.DB,self.User,self.logger)
            if (self.Sim.error==0): 
    #            self.show_message(self.NewSimWindow, 'dialog-information', result[3:], "Importacion Simulacion")
                msg="SIMULATION "+ self.Sim.ID + " IMPORTED SUCCESSFULY"
                self.logger.info (msg)
                self.show_message(self.NewSimWindow, 'dialog-information', msg, "Importing Simulation")
                # Añadimos a la seleccion
                datosSim={'id' : self.Sim.ID,'name' : self.Sim.Name, 'project' : self.Sim.Proyecto,'discipline' : self.Sim.Disciplina,'subdiscipline' : self.Sim.Subdisciplina,'loadcase' : self.Sim.LoadCase,'reference' : self.Sim.Reference,'variant' : self.Sim.Variant,'owner' : self.Sim.Owner,'creation' : self.Sim.CreationDate,'status' : self.Sim.Estado,'nfiles' : self.Sim.Nfiles,'outputs' : self.Sim.Outputs,'reports' : self.Sim.Reports, 'ownerLN' : self.Sim.OwnerLN,'extern' : self.Sim.Extern,'access' : self.Sim.AccessLevel, 'subloadcase' : self.Sim.SubLoadcase, 'aux1' : self.Sim.Aux1, 'aux2' : self.Sim.Aux2, 'aux3' : self.Sim.Aux3, 'aux4' : self.Sim.Aux4, 'aux5' : self.Sim.Aux5, 'aux6' : self.Sim.Aux6, 'label' : self.Sim.Label, 'description' : self.Sim.Description, 'type' : self.Sim.Type, 'rights' : self.Sim.Rights, 'path': ''}
                datos=json.dumps(datosSim)
                self.mostrar_Simulacion(datos)
            else:
                msg="SIMULATION not imported: " + self.Sim.errorMsg
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.NewSimWindow, 'dialog-information', msg, "Importing Simulation")
        else:
            msg="SIMULATION DUPLICATED not deleted: " + self.DB.errorMsg
            self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
            self.show_message(self.NewSimWindow, 'dialog-information', msg, "Importing Simulation")

        #self.importMessage.set_markup("<span foreground='red'><b></b></span>")
        self.NewSimWindow.hide()
    
    def gtk_nooverwrite_simulation (self,widget):
        self.YesCancelWindow.hide()
#         self.importMessage.set_markup("<span foreground='red'><b></b></span>")
        self.NewSimWindow.hide()
                                    
    def gtk_importSimulation(self,widget):
#         self.importMessage.set_justify(Gtk.Justification.CENTER)
#         self.importMessage.set_markup("<span foreground='red'><b>Importando simulacion </b></span>")
#         GLib.timeout_add(1000, self.blink_label, self.importMessage)
#         self.blink_label(self.importMessage)
#         self.importMessage.show()
        sim = self.DB.getSimbyName(self.User,self.Sim.Name)
        if (len(sim)==1): 
            # pregunta si sobreescribir
            self.simduplicated = next(iter(sim.items()))
            self.questionLabel.set_markup("<span foreground='black'> ALREALDY EXIST A SIMULATION WITH THIS NAME (" + self.simduplicated[0] + ") </span>")
            self.noteLabel1.set_markup("<span foreground='black'> Do you want to overwrite? </span>")
            self.noteLabel2.set_markup("<span foreground='black'><b> (NOTE: The existing simulation will be deleted) </b></span>")
            self.YesCancelWindow.show()
        else:
            result = self.Sim.importSimulation(self.DB,self.User,self.logger)
            if (self.Sim.error==0): 
                self.importMessage.set_markup("")
                self.show_message(self.NewSimWindow, 'dialog-information', "SIMULACION "+ self.Sim.ID + " IMPORTADA CON EXITO", "Importacion Simulacion")
                # A��adimos a la seleccion
                datosSim={'id' : self.Sim.ID,'name' : self.Sim.Name, 'project' : self.Sim.Proyecto,'discipline' : self.Sim.Disciplina,'subdiscipline' : self.Sim.Subdisciplina,'loadcase' : self.Sim.LoadCase,'reference' : self.Sim.Reference,'variant' : self.Sim.Variant,'owner' : self.Sim.Owner,'creation' : self.Sim.CreationDate,'status' : self.Sim.Estado,'nfiles' : self.Sim.Nfiles,'outputs' : self.Sim.Outputs,'reports' : self.Sim.Reports, 'ownerLN' : self.Sim.OwnerLN,'extern' : self.Sim.Extern,'access' : self.Sim.AccessLevel, 'subloadcase' : self.Sim.SubLoadcase, 'aux1' : self.Sim.Aux1, 'aux2' : self.Sim.Aux2, 'aux3' : self.Sim.Aux3, 'aux4' : self.Sim.Aux4, 'aux5' : self.Sim.Aux5, 'aux6' : self.Sim.Aux6, 'label' : self.Sim.Label, 'description' : self.Sim.Description, 'type' : self.Sim.Type, 'rights' : self.Sim.Rights, 'path': ''}
                datos=json.dumps(datosSim)
                self.mostrar_Simulacion(datos)
            else: 
                msg=result
                self.logger.error ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],msg))
                self.show_message(self.NewSimWindow, 'dialog-error', result, "Importacion Simulacion")
        self.NewSimWindow.hide()
        
        
    def blink_label(self, label):
        if label.get_text()=="": label.set_markup("<span foreground='red'><b>Importando simulacion </b></span>")
        else: label.set_markup("")
        
    def week(self, i):
        switcher={
                'JAN':'01',
                'FEB':'02',
                'MAR':'03',
                'APR':'04',
                'MAY':'05',
                'JUN':'06',
                'JUL':'07',
                'AUG':'08',
                'SEP':'09',
                'OCT':'10',
                'NOV':'11',
                'DEC':'12'
        }
        return switcher.get(i,'00')
    
    def compareNumbers (self,model,row1,row2, user_data):
        sort_column, _ = model.get_sort_column_id()
        string1 = model.get_value(row1, sort_column)
        string2 = model.get_value(row2, sort_column)
        
        number1=int(string1)
        number2=int(string2)
        
        if number1 < number2:
            return 1
        elif number1 > number2:
            return -1
        else:
            return 0
       
        
    def compareDates(self,model, row1, row2, user_data):
        # dd-MON-yy
        sort_column, _ = model.get_sort_column_id()
        date1 = model.get_value(row1, sort_column)
        date2 = model.get_value(row2, sort_column)
        
        date1arr = date1.split("-") # date1arr[0]=dd date1arr[1]=MON date1arr[2]=yy
        date2arr = date2.split("-")
        
        #change month format
        date1arr[1]=self.week(date1arr[1])
        date2arr[1]=self.week(date2arr[1])
    
        if date1arr[2] < date2arr[2]: # year comparison
            return 1
        elif date1arr[2] > date2arr[2]:
            return -1
        else:  # same year
            if date1arr[1] < date2arr[1]: # month comparison
                return 1
            elif date1arr[1] > date2arr[1]:
                return -1
            else:  # same month
                if date1arr[0] < date2arr[0]: # day comparison
                    return 1
                elif date1arr[0] > date2arr[0]:
                    return -1
                else:  # same day
                    return 0

       
    def start_SSDM(self):
        # set environment
        self.entorno.set_text(Globals.SSDM_ENV)
        
        # set username in Window
        self.username.set_text("Welcome: " + self.User.username)
        
        # Add logfile
        with open(self.logFilename, 'r') as f:
                data = f.read()
                self.log_buffer.set_text(data)  
                
        # Activate Admin Module
        self.AdminMenu.set_visible(False)
        for role in self.User.Profile['roles']:
            if (self.User.Profile['roles'][role]['rolename'] == "ADMIN"):
                self.AdminMenu.set_visible(True)
                break
                     
        # Cargar Proyectos Usuario
        # Adding info in the Project Combo
        for project_ref in self.User.Projects:
            cur_project=self.userProjectsCombo.append_text(project_ref[0])
        
        self.userProjectsCombo.set_active(0)
        self.EstadosCombo.set_active(0)
        self.selected_project=self.userProjectsCombo.get_active_text()
        self.selected_estado=self.EstadosCombo.get_active_text()
                        
        # Cargar Estados
        # Adding info in the Estado Combo
#         for estado_ref in self.DB.Estados:
#             cur_estado=self.EstadosCombo.append_text(estado_ref[0])

        #self.Paned.set_position(250)
        #self.Principal.set_position(300)
        self.main_window.show()
        self.SimulacionTabs.hide()
                
   # Inicializacion
    def __init__(self):
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        #self.tmpDir = self.scriptDir + "/../tmp/"
        self.gladeDir = self.scriptDir + "/../etc/"
        self.User = User(getpass.getuser())
        self.logFilename = Globals.TMP_DIR + "/" + Path(os.path.realpath(__file__)).stem + ".log"
        self.MainGlade = Gtk.Builder()
        self.SimGlade = Gtk.Builder()
        self.DownSimGlade = Gtk.Builder()
        self.AdminGlade = Gtk.Builder()
        
        # Log file        
#         simfile = SimFiles()
#         if (not simfile.dirExist(Globals.TMP_DIR)):
#             simfile.creaDir(Globals.TMP_DIR)

        file_handler = logging.FileHandler(filename=self.logFilename)
        #stdout_handler = logging.StreamHandler(sys.stdout)
        #handlers = [file_handler, stdout_handler]
        handlers = [file_handler]
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
        
        # Anadimos ficheros Glade
        self.MainGlade.add_from_file(self.gladeDir + "xSDM.glade")
        self.SimGlade.add_from_file(self.gladeDir + "InputSim.glade")
        self.DownSimGlade.add_from_file(self.gladeDir + "DownloadSim.glade")
        self.AdminGlade.add_from_file(self.gladeDir + "Admin.glade")
        
        # Definimos ventanas
        self.LoginWindow = self.MainGlade.get_object("LoginWindow")
        self.messageWin = self.MainGlade.get_object("Message")
        self.YesCancelWindow = self.MainGlade.get_object("YesCancelWin")
        self.questionWindow = self.MainGlade.get_object("questionWin")
        self.main_window = self.MainGlade.get_object( "SSDM" )
        self.detailsFrame=self.MainGlade.get_object("detailsFrame")
        self.selectFileWindow=self.SimGlade.get_object("selectFileWin")
        self.NewSimWindow = self.SimGlade.get_object("NewSimWin")
        self.selectDirWindow=self.DownSimGlade.get_object("selectDirWindow")
        self.adminUserWindow=self.AdminGlade.get_object("adminUserWindow")
        self.disciplineAdminWin = self.AdminGlade.get_object("disciplineAdminWindow")

        self.username = self.MainGlade.get_object("userid") 
        self.entorno = self.MainGlade.get_object("entorno") 
        self.lastProcess = self.MainGlade.get_object("lastProcess") 
        self.log_buffer = self.MainGlade.get_object( "Log" )
        self.messageIMG = self.MainGlade.get_object("messageIMG")
        self.messageLabel = self.MainGlade.get_object("messageLabel")
        self.questionLabel = self.MainGlade.get_object("questionLabel")
        self.noteLabel1 = self.MainGlade.get_object("noteLabel1")
        self.noteLabel2 = self.MainGlade.get_object("noteLabel2")
        self.questionLabel1 = self.MainGlade.get_object("questionLabel1")
        self.questionLabel2 = self.MainGlade.get_object("questionLabel2")
        self.questionLabel3 = self.MainGlade.get_object("questionLabel3")
        #self.errorIMG = self.MainGlade.get_object("ErrorIMG")
        #self.OKIMG = self.MainGlade.get_object("OKIMG")
        self.importMessage = self.SimGlade.get_object("importMessage")
        
        # Proyectos
        self.project_store = self.MainGlade.get_object("projectTree") # Datos simulaciones arbol
        self.disciplineStore = self.MainGlade.get_object("disciplineTree") # Datos arbol disciplinas
        self.disciplineView = self.AdminGlade.get_object("disciplineView")
        self.addItemDialog = self.AdminGlade.get_object("addItemDialog")
        self.addItemButton = self.AdminGlade.get_object("addItemButton")
        self.disciplineEntry = self.AdminGlade.get_object("disciplineEntry")
        self.responsibleEntry = self.AdminGlade.get_object("responsibleEntry")
        self.subdisciplineEntry = self.AdminGlade.get_object("subdisciplineEntry")
        self.loadcaseEntry = self.AdminGlade.get_object("loadcaseEntry")
        self.modifyItemDialog = self.AdminGlade.get_object("modifyItemDialog")
        self.modifyItemButton = self.AdminGlade.get_object("modifyItemButton")
        self.disciplineModEntry = self.AdminGlade.get_object("disciplineModEntry")
        self.responsibleModEntry = self.AdminGlade.get_object("responsibleModEntry")
        self.subdisciplineModEntry = self.AdminGlade.get_object("subdisciplineModEntry")
        self.loadcaseModEntry = self.AdminGlade.get_object("loadcaseModEntry")
        self.deleteItemButton = self.AdminGlade.get_object("deleteItemButton")
        self.userProjectsCombo = self.MainGlade.get_object("UserProjects")
        self.EstadosCombo = self.MainGlade.get_object("Estados")
        self.project_tree = self.MainGlade.get_object("Arbol") # Vista proyectos
        self.Paned = self.MainGlade.get_object("Paned")
        self.Principal = self.MainGlade.get_object("Principal")
        self.AdminMenu = self.MainGlade.get_object("AdminMenu")
        self.items_seleccionados=[]
        self.sim_seleccionada=None
        self.sim_activada=None
        self.selected_project=""
        self.selected_estadoID=""
        self.seeOwnSims='False'
        self.listaRolesStore=self.MainGlade.get_object("userRolesstore")
        
        # Admin Structure
        self.disciplineStoreAdmin = self.AdminGlade.get_object("disciplineAdminTree") # Datos arbol disciplinas Admin
        
        # Admin Roles
        self.listaProjects = self.AdminGlade.get_object("listaProjects")
        self.listaDisciplinas = self.AdminGlade.get_object("listaDisciplinas")
        self.listaUsers = self.AdminGlade.get_object("listaUsers")
        self.listaRequest = self.AdminGlade.get_object("listaRequest")
        self.listaRoles = self.AdminGlade.get_object("listaRoles")
        self.dateEntry = self.AdminGlade.get_object("dateEntry")
        self.calendar = self.AdminGlade.get_object("calendar")
        self.listaRolesStoreAdmin=self.AdminGlade.get_object("userRolesstore")
        self.listaUsersStoreAdmin=self.AdminGlade.get_object("usersStore")
        self.usernameFinded=self.AdminGlade.get_object("usernameFinded")
        self.useridEntry = self.AdminGlade.get_object("useridEntry")
        self.useridvwEntry = self.AdminGlade.get_object("useridvwEntry")
        self.nameEntry = self.AdminGlade.get_object("nameEntry")
        self.departmentEntry = self.AdminGlade.get_object("departmentEntry")
        self.emailEntry = self.AdminGlade.get_object("emailEntry")
        self.stoEntry = self.AdminGlade.get_object("stoEntry")
        self.listaCompanies = self.AdminGlade.get_object("listaCompanies")
        
        
        # ComboBoxText Simulacion nueva
        self.listaProyectos = self.SimGlade.get_object("proyecto")
        self.listaTipos = self.SimGlade.get_object("tipo")
        self.labelProject = self.SimGlade.get_object("errorProjectLabel")
        self.labelTipo = self.SimGlade.get_object("errorTypeLabel")
        self.labelEstado = self.SimGlade.get_object("errorStatusLabel")
        self.listaEstados = self.SimGlade.get_object("estado")
        self.listaDisciplina = self.SimGlade.get_object("disciplina")
        self.labelDisciplina = self.SimGlade.get_object("errorDisciplineLabel")
        self.listaSubdisciplina = self.SimGlade.get_object("subdisciplina")
        self.labelSubdisciplina = self.SimGlade.get_object("errorSubdisciplineLabel")
        self.listaLoadCase = self.SimGlade.get_object("loadcase")
        self.labelLoadCase = self.SimGlade.get_object("errorLoadcaseLabel")
        self.buttonImport = self.SimGlade.get_object("importButton")
        
        # Lista simulaciones
        self.listaSims=self.MainGlade.get_object("Simulaciones")
        self.listaSimsStore=self.MainGlade.get_object("listasims")
        self.listaSimsStore.set_sort_func(9, self.compareDates, None) # Date compare function SortColumnID
        self.listaSimsStore.set_sort_func(0, self.compareNumbers, None) # ID compare function SortColumnID

        # Datos mostrar Simulacion
        self.SimulacionTabs = self.MainGlade.get_object("Simulacion")
        self.project = self.MainGlade.get_object("proyecto")
        self.disciplina = self.MainGlade.get_object("disciplina")
        self.subdisciplina = self.MainGlade.get_object("subdisciplina")
        self.loadcase = self.MainGlade.get_object("loadcase")
        self.id = self.MainGlade.get_object("id")
        self.name = self.MainGlade.get_object("nameID")
        self.autor = self.MainGlade.get_object("autor")
        self.extern = self.MainGlade.get_object("extern")
        self.access = self.MainGlade.get_object("access")
        self.date = self.MainGlade.get_object("dateCreation")
        self.reference = self.MainGlade.get_object("reference")
        self.variant = self.MainGlade.get_object("variant")
        self.status = self.MainGlade.get_object("status")
        self.inputs = self.MainGlade.get_object("inputs")
        self.outputs = self.MainGlade.get_object("outputs")
        self.reports = self.MainGlade.get_object("reports")
        self.subloadcase = self.MainGlade.get_object("subloadcase")
        self.aux1 = self.MainGlade.get_object("aux1")
        self.aux2 = self.MainGlade.get_object("aux2")
        self.aux3 = self.MainGlade.get_object("aux3")
        self.aux4 = self.MainGlade.get_object("aux4")
        self.aux5 = self.MainGlade.get_object("aux5")
        self.aux6 = self.MainGlade.get_object("aux6")
        self.type = self.MainGlade.get_object("type")
        self.label = self.MainGlade.get_object("label")
        self.description = self.MainGlade.get_object("description")
        self.description_view = self.MainGlade.get_object("description_view")
        self.description_scroll = self.MainGlade.get_object("description_scroll")
        self.downloadButton = self.MainGlade.get_object("downloadButton")
        self.publishButton = self.MainGlade.get_object("publishButton")
        self.editButton = self.MainGlade.get_object("editButton")
        self.saveButton = self.MainGlade.get_object("saveButton")
        
        self.contextFrame = self.MainGlade.get_object("contextFrame")
        self.detailFrame = self.MainGlade.get_object("detailFrame")
        self.filesFrame = self.MainGlade.get_object("filesFrame")
        self.otherFrame = self.MainGlade.get_object("otherFrame")
        self.useridProfile = self.MainGlade.get_object("useridProfile")
        
        style_provider = Gtk.CssProvider()
        css = open(self.gladeDir + "style.css", 'rb')  # rb needed for python 3 support
        css_data = css.read()
        css.close()
        style_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        # Actions files
        self.selected_files={}

               
        # Conectamos signals
        self.MainGlade.connect_signals(self)
        self.SimGlade.connect_signals(self)
        self.DownSimGlade.connect_signals(self)
        self.AdminGlade.connect_signals(self)
        #self.LoginWindow.set_title("SEAT SDM Login")
        #self.LoginWindow.set_default_size(200, 400)
        #self.msg = "Inicio aplicacion"
        #self.logger.info ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.msg))
        #Gtk.Application.__init__(self)


    # Programa principal
    def main(self,argv):
        # Config
        Globals.initialize(0)
        # Arguments
        try:
            #opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
            opts, args = getopt.getopt(argv,"-h-d")
            #print (opts)
            #print (args)
        except getopt.GetoptError:
            print ("xSDM.py [-d]")
            sys.exit(2)
        for opt,arg in opts:
            if opt == '-h':
                print ("xSDM.py [-d]")
                sys.exit()
            #elif opt in ("-l", "--log"):
            elif opt in ("-d"):
                self.msg = "DEBUG activated"
                self.logger.info (self.msg)
                self.logger.setLevel(logging.DEBUG)
                self.msg = "DEBUG activated"
                self.logger.debug ("File %s, in %s, line %s: %s" % (inspect.stack()[0][1],inspect.stack()[0][3],inspect.stack()[0][2],self.msg))
        
        # Inicio        
#         hdlr = logging.FileHandler(self.logFilename)
#         formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#         hdlr.setFormatter(formatter)
#         self.logger.addHandler(hdlr) 
        
        self.msg = "Starting aplication"
        self.logger.info (self.msg)

        self.LoginWindow.show()
        #result=self.Login()
        Gtk.main()


# Inicio Aplicacion  
if __name__=='__main__':
    app = xSSDM()
    app.main(sys.argv[1:])
    
