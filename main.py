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
    valid = []
    if os.path.isfile(path):
        if path.endswith(".crt") or path.endswith(".cer"):
            cert = open(path, 'rb').read()
            certificado = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            chain = resolve(cert)
            for it in chain:
                for confiavel in store:
                    if confiavel.get_serial_number() == it.serial:
                        valid.append(it)
                        break
            if valid:
                showValidChain(valid, certificado)
            else:
                print("Certificado não confiavel")
    else:
        print("Arquivo não encontrado")

def showValidChain(validators, certificate):
    print("Certificado válido, abaixo a cadeia do mesmo até a raiz.")
    print(certificate.get_subject().CN)
    i = 1
    for it in validators:
        print(("\t" * i) + "↳ " + it.common_name)
        i += 1
        if it.is_root:
            break

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



