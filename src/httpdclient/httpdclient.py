'''
Created on Jun 10, 2021

@author: scernud
'''
import Config.config as Globals
import urllib3
from urllib3.exceptions import InsecureRequestWarning             
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
import re
import sys, os.path

class httpdclient(object):
    '''
    classdocs
    '''
#    def __init__(self, username, passw, cert,pubkey):
    def __init__(self, username):
        self.server=Globals.SSDM_SERVER
        self.port=Globals.SSDM_PORT
        self.username=username
        self.conectado=False
        self.url=Globals.SSDM_SERVER_URL
        self.error=""
        self.urlib=""
        
        if Globals.SSDM_AUTO==1:
            result=self.conectar_auto()
            if (result=='<resultado>CONNECTED</resultado>'):
                self.conectado=True  
            else:
                self.conectado=False
                #self.error="ERROR CONEXION CON BASE DE DATOS"
        else:
            result=self.conectar()
            if ((result[(len(result)-46):len(result)])=='<resultado>CONNECTED</resultado></body></html>'):
                self.conectado=True  
            else:
                if ((result[(len(result)-26):len(result)])=='UNAUTHORIZED</body></html>'):
                    self.conectado=False  
                    self.error="UNAUTHORIZED: THE USER IS NOT IN THE SYSTEM"
                else:
                    self.conectado=False
                    self.error="CONNECTION ERROR"

    def stringify(self,obj: dict) -> dict:
        """turn every value in the dictionary to a string"""
        for k, v in obj.items():
            if isinstance(v, dict):
                # if value is a dictionary, stringifiy recursively
                self.stringify(v)
                continue
            if not isinstance(v, str):
                if isinstance(v, bool):
                    # False/True -> false/true
                    obj[k] = str(v).lower()
                else:
                    obj[k] = str(v)
        return obj
    
    def conectar(self):    
        try:
            #postdata={"accion":"conectar"}
            capabilities = DesiredCapabilities.FIREFOX
            capabilities['marionette'] = False
            
            src_path=os.path.dirname(os.path.realpath(sys.argv[0]))
            # Prefil firefox original: ~/.mozilla/firefox/d8nfhel3.default-1637923288256
            # Definirlo y  copiar los ficheros en /../etc/profile_firefox
#            fp_dir = src_path + "/../etc/profile_firefox"

#            mozilla_config_dir=os.getenv("HOME") + "/.mozilla/firefox/"
#            profile_dir="ssdm.default"
            
#            for line in open(mozilla_config_dir + "installs.ini", 'r'):
#              esta=re.split("Default=", line.rstrip())
#              if re.search("Default=", line):
#                print(line)
#                profile_dir=esta[1]
#              if line == None:
#                print('no matches found')
                          
#            fp_dir = mozilla_config_dir + profile_dir + "/"
          
##############################################
            fp_dir = src_path + "/../etc/profile_firefox"
#############################################
            fp = webdriver.FirefoxProfile(fp_dir)
            binary = FirefoxBinary('/usr/bin/firefox')
            #fp.set_timeout(28800) # seconds -> 8h
            self.driver = webdriver.Firefox(firefox_binary=binary,firefox_profile=fp,capabilities=capabilities,timeout=28800)
#            self.driver = webdriver.Firefox(firefox_binary=binary,capabilities=capabilities,timeout=28800)
            
            self.driver.set_window_position(0, 0)
            self.driver.set_window_size(800, 170)
            self.driver.get(self.url)
#             print(self.driver.current_url)
#             print(self.driver.page_source)
        
            #pos=self.driver.get_window_position()
            #size=self.driver.get_window_size()
            
            #Click on the "Login" button
            button = self.driver.find_element_by_xpath("//body/div/div/div[4]/div[3]/form[1]/button[1]")
            button.click()
            
            #Click on the "Continue" button
            button = self.driver.find_element_by_xpath("//button[1]")
            button.click()
                        #              
            # Save selenium session
            #headers = { "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36" } 
            # Firefox
            headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/47.0" } 
            #headers = { "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0" } 
            #headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0" } 
            # Chrome
            #headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
            # Opera 
            #headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41"}
            # Safari
            #headers = { "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"}
            # IE
            #headers = { "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)"}
            
            self.session = requests.session() 
            self.session.headers.update(headers) 
            for cookie in self.driver.get_cookies(): 
                c = {cookie['name']: cookie['value']} 
            self.session.cookies.update(c)
            result=self.driver.page_source
            self.driver.close()
            return result
                   
        except NoSuchElementException:
            self.error="ERROR AUTHENTICATION"
            #print(e.msg)
            self.conectado=False    
            self.driver.close()
            return "<resultado>ERROR</resultado>"
        except urllib3.exceptions.MaxRetryError:
            self.error="ERROR Connection"
            self.conectado=False    
            #self.driver.close()
            return "<resultado>ERROR</resultado>"
                    
    def conectar_auto(self):      
        # Making a get request
        self.session=requests.session()
        self.session.auth=requests.auth.HTTPBasicAuth(self.username, self.username)
        self.session.verify=False
        urllib3.disable_warnings(InsecureRequestWarning)
        response = self.session.request('POST', self.url)
        if (response.status_code==200):
            self.conectado=True 
            return response.text 
        if (response.status_code==401):
            self.error="ERROR Authentication: Unauthorized Access"
            self.conectado=False   
            return "<resultado>ERROR</resultado>" 
        self.error="ERROR Connection"
        self.conectado=False    
        return "<resultado>ERROR</resultado>"
  
        # print request object
        print(response)

    def execAPIfunction(self,accion,username,params):
        result=""
        if not self.conectado:
            if Globals.SSDM_AUTO==1:
                self.conectar_auto()
            else:
                self.conectar()
        if self.conectado:
            try:
                postdata={'accion':accion,'username':username}
                for (n,v) in params.items():
                    postdata[n] = v
                    
                urllib3.disable_warnings(InsecureRequestWarning)
                result = self.session.post(self.url, data=postdata,verify=False)
                result.encoding = 'UTF-8'
                
                if result.text[0:11]!="<resultado>":
                    if result.text[247:275]=="SEAT - Authentication Portal":
                        # Timeout 1h definido por SEAT en Webseal
                        if Globals.SSDM_AUTO==1:
                            self.conectar_auto()
                        else:
                            self.conectar()
                            self.execAPIfunction(accion,params)
                    else:
                        return "<resultado>ERROR internal Server. Consulte con su Administrador</resultado>"
                    
                return result.text
            
            except urllib3.exceptions.HTTPError as e:
                self.error="ERROR"
                if e.code == 401:
                    self.error = "ERROR Authentication: Wrong User or password"
                if e.code == 500:
                    self.error = "ERROR: Internal Error"
                print(Exception)
                return self.error
   
