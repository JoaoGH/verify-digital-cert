import os
import OpenSSL
import shutil

store = OpenSSL.crypto.X509Store()

def loadTrusted():
    certificados = os.listdir("./trusted/")
    for it in certificados:
        certficate = open("./trusted/" + it, "rb").read()
        confiavel = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certficate)
        store.add_cert(confiavel)

def addTrustedCertificate():
    path = input("Insira o caminho do certificado raiz")
    if os.path.isfile(path):
        if path.endswith(".crt") or path.endswith(".cer"):
            ca = open(path, 'rb').read()
            confiavel = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, ca)
            store.add_cert(confiavel)
            shutil.copy(path, "./trusted/")
    else:
        print("Arquivo não encontrado")

def validateCertificate():
    path = input("Insira o caminho do arquivo")
    if os.path.isfile(path):
        if path.endswith(".crt") or path.endswith(".cer"):
            ca = open(path, 'rb').read()
            certificado = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, ca)
            try:
                context = OpenSSL.crypto.X509StoreContext(store, certificado)
                context.verify_certificate()
                print("Certificado confiavel")
            except OpenSSL.crypto.X509StoreContextError as e:
                print("Certificado não confiavel")
                print(e)
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



