import pkcs11
import asn1crypto.pem
import urllib.request
import tempfile
import ssl
import os

# this is OpenSC's implementation of PKCS#11
# other security sticks may come with another implementation.
# choose the most appropriate one
lib = pkcs11.lib('/usr/lib/pkcs11/opensc-pkcs11.so')
# tokens may be identified with various names, ids...
# it's probably rare that more than one at a time would be plugged in
token = lib.get_token(token_serial='<token_serial_value>')

pem = None
with token.open() as sess:
    pkcs11_certificates = sess.get_objects(
        {
            pkcs11.Attribute.CLASS: pkcs11.ObjectClass.CERTIFICATE,
            pkcs11.Attribute.LABEL: "Cardholder certificate"
        })

    # hopefully the selector above is sufficient
    assert len(pkcs11_certificates) == 1

    pkcs11_cert = pkcs11_certificates[0]
    der_encoded_certificate = pkcs11_cert.__getitem__(pkcs11.Attribute.VALUE)
    # the ssl library expects to be given PEM armored certificates
    pem_armored_certificate = asn1crypto.pem.armor("CERTIFICATE",
        der_encoded_certificate)

# this is the ugly part: persisting the certificate on disk
# i deliberately did not go with a sophisticated solution here since it's
#   such a big caveat to have to do this...
certfile = tempfile.mkstemp()
with open(certfile[1], 'w') as certfile_handle:
    certfile_handle.write(pem_armored_certificate.decode("utf-8"))

# this will instruct the ssl library to provide the certificate
# if asked by the server.
sslctx = ssl.create_default_context()
sslctx.load_cert_chain(certfile=certfile[1])
# if your certificate does not contain the private key, find it elsewhere
# sslctx.load_cert_chain(certfile=certfile[1],
#     keyfile="/path/to/privatekey.pem",
#     password="<private_key_password_if_applicable>")

response = urllib.request.urlopen("https://ssl_website", context=sslctx)

# Cleanup and delete the "temporary" certificate from disk
os.remove(certfile[1])