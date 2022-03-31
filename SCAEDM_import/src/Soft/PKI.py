import pkcs11
# Para lectura certificados
# from pkcs11 import Attribute, ObjectClass
# from asn1crypto import x509, pem, keys
# from pkcs11.util.rsa import encode_rsa_public_key

class PKI():

    def __init__(self,pin):    
        self.error=0
        self.msg=""
        self.PubKey=""
        self.error=self.readCard(pin)

    def readCard(self,pin):
        # Initialise our PKCS#11 library
        lib = pkcs11.lib('/opt/itp11/libitp11.so')
        
        try:
            token = lib.get_token()     
        except pkcs11.exceptions.NoSuchToken:
            self.msg="Tarjeta no insertada/detectada o error de lectura"
            return 3
        
        # Para lectura certificados
        # Open a session on our token
#         try:
#             with token.open(user_pin=pin) as session:
#                 for pub_key in session.get_objects({Attribute.CLASS: ObjectClass.PUBLIC_KEY}):
#                     public_key = keys.RSAPublicKey.load(encode_rsa_public_key(pub_key))
#                     if (self.PubKey==""): self.PubKey = pem.armor('PUBLIC_KEY', encode_rsa_public_key(pub_key))                    
#                     
#                 for cert in session.get_objects({Attribute.CLASS: ObjectClass.CERTIFICATE,}):
#                     #crt=cert[Attribute.VALUE]
#                     print (cert)
#                     der_bytes = cert[Attribute.VALUE]
#                     # Load a certificate object from the DER-encoded value
#                     x509_cert=x509.Certificate.load(der_bytes)
#                     
#                     issuer=x509_cert.issuer
#                     subject=x509_cert.subject
#                     CN_issuer=issuer.native['common_name']
#                     CN_subject=subject.native['common_name']
#                     print (CN_issuer + " " + CN_subject)
#                     if CN_issuer == 'VW-CA-ENCN-01':
#                         self.Cert=x509_cert
#                         self.Cert_pem = pem.armor('CERTIFICATE', der_bytes)                        
#                         return 0
#                     print (x509_cert.native['tbs_certificate'])
#                     # Write out a PEM encoded valu.

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
      
      