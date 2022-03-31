'''
Created on 

@author: vwgs
'''
import os,sys
from random import random
import threading
import time
#import hashlib
#from DBserver.usuarios import usuarios
#from shutil import copy2

#from Soft.Nastran import Nastran
# from numpy import void
# from pasta.base.codegen import to_str
#from DBserver.jobs import jobs

class SimFiles:
    
    def __init__( self):
        self.md5=""
        self.error=0
        self.errorMSG=""
        self.progress = 0
        self.result = None
        self.result_available = threading.Event()

    def isInDirectory(self,filename,dirname):
        pa = os.path.split(os.path.dirname(filename))
        if pa[1]==dirname:
            return True
        return False
    
    def getRootDirectory(self,filename):
        #rootDir = os.path.split(os.path.dirname(filename))
        rootDir = os.path.dirname(os.path.realpath(filename))
        return rootDir

    def existStructure(self,source,structDir):
        for dir in structDir:
            if not os.path.exists(source + "/" + dir):
                self.error=1
                self.errorMSG=source + "/" + dir + " doesnt exist"
                return False
        return True

    def dirExist(self,dir):
        if os.path.exists(dir):
            return True
        return False
        
    def copyDir(self,orig,dest):
        self.error=0
        if not os.path.exists(orig):
            self.error=1
            self.errorMSG="ERROR: Directory " + orig + " doesn't exists"
            return "ERROR: Directory " + orig + " doesn't exists"
        self.creaDir(dest)
        if self.error == 0:
            #print ("cp -r " + orig + '/* ' + dest)
            try:
                os.system("cp -r " + orig + '/* ' + dest)
#                os.system("tar -czf " + dest + ".tar.gz --totals " + orig)
#                 md5_hash = hashlib.md5()
#                 with open(dest + ".tar.gz","rb") as f:
#                     # Read and update hash in chunks of 4K
#                     for byte_block in iter(lambda: f.read(4096),b""):
#                         md5_hash.update(byte_block)
#                     self.md5hash=md5_hash.hexdigest()
                return 0
            except:
                self.error=sys.exc_info()[1].strerror
                self.errorMSG="ERROR: Copy simulation failed " + self.error            
                self.delDir(dest)
                return "ERROR: Copy simulation failed " + self.error
        else:
            return 

    def slowCopyDir(self,orig,dest):
        thread = threading.Thread(target=self.background_CopyDir, args=(orig,dest,))
        thread.start()
    
        # wait here for the result to be available before continuing
        while not self.result_available.wait(timeout=5):
            #print('\r{}% done...'.format(self.progress), end='', flush=True)
            self.progress = self.progress +1
    
        #print('Fin slowcopydir')
        
    def background_CopyDir(self,orig,dest):
        self.error=0
        if not os.path.exists(orig):
            self.error=1
            self.errorMSG="ERROR: Directory " + orig + " doesn't exists"
            return "ERROR: Directory " + orig + " doesn't exists"
        self.creaDir(dest)
        if self.error == 0:
            try:
                os.system("cp -r " + orig + '/* ' + dest)
                self.result_available.set()
                return 0
            except:
                self.error=sys.exc_info()[1].strerror
                self.errorMSG="ERROR: Copy simulation failed " + self.error            
                self.delDir(dest)
                self.result_available.set()
                return "ERROR: Copy simulation failed " + self.error
        else:
            self.result_available.set()
            return 

    def delDir(self,dirname):
        self.error=0
        self.errorMSG=""
        try:
            #descomentar en mas pruebas
            os.system("rm -rf " + dirname)
            return 0
        except:
            self.error=1
            error=sys.exc_info()[1].strerror
            self.errorMSG="ERROR: Delete Simulation failed " + dirname + " " + error
            return "ERROR: Delete Simulation failed " + dirname + " " + self.errorMSG

        
    def creaDir(self,dirname):
#     
#     idjob=self.dbjob.getidjob();
#     
#     storageWS=self.storageWS+"/"+self.username+"."+str(idjob)+"."+os.path.basename(mainfile)[:-4];
#     
        self.error=0
        self.errorMSG=""
        try:
            os.mkdir(dirname,0o755);
        except:
            self.error=1
            error=sys.exc_info()[1].strerror
            self.errorMSG=dirname + ": " + sys.exc_info()[1].strerror
                ##self.parent.show_error("Fallo al crear el directorio" + format(error));
#       
#     if not os.path.exists(storageWS) or not os.access(storageWS,os.W_OK) is True:
#       storageWS=None;

        return
    
    def chmodDir(self,dirname,mode):
        try:
            os.chmod(dirname, mode)
            error="OK"
        except:
            error=sys.exc_info()[1].strerror
            
        return error
            
     
    def openfile(self,filename,mode):
        fileh=None
        self.error=0
        try:
            fileh=open(filename,mode);
        except:
            self.error=1
            self.errorMSG=sys.exc_info()[1].strerror;
    
        return fileh