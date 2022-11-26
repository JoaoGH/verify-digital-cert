import os
import OpenSSL
import shutil
from cert_chain_resolver.resolver import resolve

store = []

def loadTrusted():
    certificados = os.listdir("./trusted/")
    for it in certificados:
        certficate = open("./trusted/" + it, "rb").read()
        confiavel = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certficate)
        store.append(confiavel)

def addTrustedCertificate():
    path = input("Insira o caminho do certificado raiz")
    if os.path.isfile(path):
        if path.endswith(".crt") or path.endswith(".cer"):
            ca = open(path, 'rb').read()
            confiavel = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, ca)
            store.append(confiavel)
            shutil.copy(path, "./trusted/")
    else:
        print("Arquivo não encontrado")

def validateCertificate():
    path = input("Insira o caminho do arquivo")
    valid = False
    if os.path.isfile(path):
        if path.endswith(".crt") or path.endswith(".cer"):
            cert = open(path, 'rb').read()
            chain = resolve(cert)
            for it in chain:
                if valid:
                    break
                for confiavel in store:
                    if confiavel.get_serial_number() == it.serial:
                        print("O certificado informado é valido pela: " + it.common_name)
                        valid = True
                        break
            if not valid:
                print("Certificado não confiavel")
    else:
        print("Arquivo não encontrado")

loadTrusted()
opc = 0
while opc != 4:
    print()
    print("--------- Validar confiança de certificados ---------")
    print("1 - Adicionar ACR")
    print("2 - Validar confiança de certificado")
    print("3 - Sair")
    opc = int(input())
    print()
    if opc == 1:
        addTrustedCertificate()
    elif opc == 2:
        validateCertificate()



