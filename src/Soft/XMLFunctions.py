from xml.etree import ElementTree

class XMLFunctions:

    def __init__(self,stringXML):
        self.error=0
        self.errorMsg=""
        self.root=None
        self.xmltext=stringXML
        if stringXML!="":    
            try:
                self.root = ElementTree.fromstring(stringXML)
                if self.root.tag != "Import": 
                        self.error=1
                        self.errorMsg="Bad Head XML (Import)"
            except Exception as e:
                self.error=1
                xml_arr=stringXML.split('\n')
                line=xml_arr[e.position[1]-1]
                tag=line[e.position[0]:]
                tag_arr=tag.split('<')
                if len(tag_arr)>1: tag_arr=tag_arr[1].split('>')
                tag=tag_arr[0]
                self.errorMsg="XML Bad Formed: " + type(e).__name__ + " - " + e.msg + " (" + tag + ")" 

    def xml_getLista( self , root, tag):
#         <resultado>
#             <tag name ='xxxx'/>
#             <tag name ='xxxx'/>
#             <tag name ='xxxx'/>
#         </resultado>
        lista=[]
        #root = ElementTree.fromstring(xml)
        for elem in root.findall(tag):
            lista2=[]
            for var in elem.keys():
                lista2.append(elem.attrib[var])
            lista.append(lista2)
        return lista
    
    def xml_getResultado(self,xml):
        root = ElementTree.fromstring(xml)
        if root.tag == "resultado":
            return root
        return None
    
    def xml_getSimulaciones( self , root):
        simulaciones={}
        #root = ElementTree.fromstring(xml)
        for sim in root.findall('simulacion'):
            input=sim.find('input')
            id=input.get('id')
            name=input.get('name')
            project=input.get('carproject')
            discipline=input.get('discipline')
            subdiscipline=input.get('subdiscipline')
            loadcase=input.get('loadcase')
            owner=input.get('owner')
            ownerLN=input.get('ownerLN')
            extern=input.get('extern')
            access=input.get('access')
            date=input.get('creation')
            reference=input.get('reference')
            variant=input.get('variant')
            status=input.get('status')
            nfiles=input.get('nfiles')
            outputs=input.get('outputs')
            reports=input.get('reports')
            subloadcase=input.get('subloadcase')
            label=input.get('label')
            #description=input.get('description')
            rights=input.get('rights')
            aux1=input.get('aux1')
            aux2=input.get('aux2')
            aux3=input.get('aux3')
            aux4=input.get('aux4')
            aux5=input.get('aux5')
            aux6=input.get('aux6')
            type=input.get('type')
            description=input.find('description').text
            
            # Orden de columnas en visualizacion
            simulaciones[id]={'id' : id,'name' : name, 'project' : project,'discipline' : discipline,'subdiscipline' : subdiscipline,'loadcase' : loadcase,'reference' : reference,'variant' : variant,'owner' : owner,'creation' : date,'status' : status,'nfiles' : nfiles,'outputs' : outputs,'reports' : reports, 'ownerLN' : ownerLN,'extern' : extern,'access' : access, 'subloadcase' : subloadcase, 'aux1' : aux1, 'aux2': aux2, 'aux3' : aux3, 'aux4' : aux4, 'aux5' : aux5, 'aux6' : aux6, 'label' : label, 'description' : description, 'type': type, 'rights' : rights}
        return simulaciones

    def xml_getFiles(self, root, simid):
        files={}
        for file in root.findall('file'):
            filename=file.get('filename')
            path=file.get('path')
            size=file.get('size')
            isfolder=0
            files[filename]={'filename' : filename,'path' : path, 'isFolder' : isfolder, 'simid' : simid, 'size' : size}
        for folder in root.findall('folder'):
            folders={}
            foldername=folder.get('filename')
            path=folder.get('path')
            size=folder.get('size')
            filesf={}
            filesf=XMLFunctions.xml_getFiles(self,folder, simid)
            isfolder=1
            files[foldername]={'filename' : foldername,'path' : path, 'isFolder' : isfolder, 'simid' : simid, 'folder' : filesf , 'size' : size}
        return files

    def xml_getSimulationFiles(self, root):
        sim=root.find('simulacion')
        simid=sim.get('id')
        files={}
        files=XMLFunctions.xml_getFiles(self,sim,simid)
        return files
    
    def xml_getSimulationAccessLevel(self, root):
        sim=root.find('simulacion')
        accesslevel=sim.get('accesslevel')
        rights=sim.get('rights')
        
        Datos={}
        Datos['accesslevel']=accesslevel
        Datos['rights']=rights

        return Datos

    def xml_getSimulationData(self, root):
        sim=root.find('simulacion')
        Datos={}
        attribs=sim.attrib
        for attrib in attribs:
            Datos[attrib]=attribs[attrib]
        return Datos
       
    def xml_getElemsData(self, root,findname):
        Datos={}
        elems=root.findall(findname)
        for elem in elems:
            atribs={}
            atribs['value']=elem.get('value')
            atribs['desc']=elem.get('desc')
            Datos[elem.get('name')]=atribs
            
        return Datos
            
    def xml_getProfileDict(self,root,find):
        #dict = {'disciplina1': {'subd1':[loadcase1,loadcas,'subd2':dict2,'subd3':dict3}, 'Disciplina2': {'subd1':dict1}, 'disciplina3': {'subd1':dict3}}
        dict={}
        #self.root = ElementTree.fromstring(xml)
        for elem in root.findall(find):
            dict[elem[0].tag]=elem[0].get('name')
            dict[elem[1].tag]=elem[1].get('name')
            dict[elem[2].tag]=elem[2].get('name')
            dict[elem[3].tag]=elem[3].get('name')
            dict[elem[4].tag]=elem[4].get('name')
            dict[elem[5].tag]=elem[5].get('name')
            dict[elem[6].tag]=elem[6].get('name')
            dict[elem[7].tag]={}
            i=0
            for role in elem[7].findall('role'):
                dict_roles={}
                for rolekey in role.keys():
                    dict_roles[rolekey]=role.get(rolekey)
                dict[elem[7].tag][i]=dict_roles
                i=i+1

        return dict
    
    def xml_getDict (self,root,find):
        #dict = {'disciplina1': {'subd1':[loadcase1,loadcas,'subd2':dict2,'subd3':dict3}, 'Disciplina2': {'subd1':dict1}, 'disciplina3': {'subd1':dict3}}
        dict={}
        #self.root = ElementTree.fromstring(xml)
        for elem in root.findall(find):
            dict[elem.get('name')]=elem.get('value')

        return dict
        

    def xml_getStructureDict(self,root,find):
        #dict = {'disciplina1': {'subd1':[loadcase1,loadcas,'subd2':dict2,'subd3':dict3}, 'Disciplina2': {'subd1':dict1}, 'disciplina3': {'subd1':dict3}}
        dict={}
        #self.root = ElementTree.fromstring(xml)
        for elem in root.findall(find):
            if len(elem):                
                subdict = XMLFunctions.xml_getStructureDict(self,elem,elem[0].tag)
                dict[elem.get('name')]=[elem.get('responsible'),elem.get('responsibleid'),subdict]
            else: dict[elem.get('name')]=[elem.get('responsible'),elem.get('responsibleid'),'']

        return dict
    
    def readHead(self):
        dict={}
        dict['Proyecto']=""
        dict['Tipo']=""
        dict['Estado']=""
        dict['Disciplina']=""
        dict['Subdisciplina']=""
        dict['LoadCase']=""
        dict['SubLoadcase']=""
        dict['Aux1']=""
        dict['Aux2']=""
        dict['Aux3']=""
        dict['Aux4']=""
        dict['Aux5']=""
        dict['Aux6']=""
        dict['Type']=""
        dict['Label']=""
        dict['Description']=""
        dict['Variant']=""
        dict['Reference']=""
        
        if self.root!=None:
          elem=self.root.find('Input')
          if elem==None: 
            self.error=1
            self.errorMsg="ERROR: Bad Head XML (Input)"
          else:
            if (elem.find('Project') != None) and (elem.find('Project').text != None): dict['Proyecto']=elem.find('Project').text
            #if (elem.find('SourceType') != None) and (elem.find('SourceType').text != None): dict['Tipo']=elem.find('SourceType').text
            if (elem.find('ModelPhase') != None) and (elem.find('ModelPhase').text != None): dict['Estado']=elem.find('ModelPhase').text
            if (elem.find('Discipline') != None) and (elem.find('Discipline').text != None): dict['Disciplina']=elem.find('Discipline').text
            if (elem.find('SubDiscipline') != None) and (elem.find('SubDiscipline').text != None): dict['Subdisciplina']=elem.find('SubDiscipline').text
            if (elem.find('LoadCase') != None) and (elem.find('LoadCase').text != None): dict['LoadCase']=elem.find('LoadCase').text
            if (elem.find('Setup') != None) and (elem.find('Setup').text != None): dict['SubLoadcase']=elem.find('Setup').text
            if (elem.find('Configuration') != None) and (elem.find('Configuration').text != None): dict['SubLoadcase']=elem.find('Configuration').text
            if (elem.find('Impactor') != None) and (elem.find('Impactor').text != None): dict['SubLoadcase']=elem.find('Impactor').text
            if (elem.find('Aux1') != None) and (elem.find('Aux1').text != None): dict['Aux1']=elem.find('Aux1').text
            if (elem.find('Aux2') != None) and (elem.find('Aux2').text != None): dict['Aux2']=elem.find('Aux2').text
            if (elem.find('Aux3') != None) and (elem.find('Aux3').text != None): dict['Aux3']=elem.find('Aux3').text
            if (elem.find('Aux4') != None) and (elem.find('Aux4').text != None): dict['Aux4']=elem.find('Aux4').text
            if (elem.find('Aux5') != None) and (elem.find('Aux5').text != None): dict['Aux5']=elem.find('Aux5').text
            if (elem.find('Aux6') != None) and (elem.find('Aux6').text != None): dict['Aux6']=elem.find('Aux6').text
            if (elem.find('Type') != None) and (elem.find('Type').text != None): dict['Type']=elem.find('Type').text
            if (elem.find('Label') != None) and (elem.find('Label').text != None): dict['Label']=elem.find('Label').text
            if (elem.find('Description') != None) and (elem.find('Description').text != None): dict['Description']=elem.find('Description').text
            if (elem.find('Variant') != None) and (elem.find('Variant').text != None): dict['Variant']=elem.find('Variant').text
            if (elem.find('Reference') != None) and (elem.find('Reference').text != None): dict['Reference']=elem.find('Reference').text             
        else:
          self.error=1
          self.errorMsg="ERROR: NO Head (Input)"
            
        
        return dict
         
        
        
        
        
        