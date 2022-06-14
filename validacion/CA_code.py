# Citlalli Selene Avalos Montiel
# Junio-2022
# Autoridad Certificadora
# Creacion de Certificados
# Autenticacion de Certificados

import subprocess
import os
import time

from django.conf import settings


def crear_clave(nombre,contrasena):
    print(contrasena)
    keyname = ".key.pem"
    name = nombre + keyname
    path = os.path.join(settings.BASE_DIR, 'raiz/CA/intermedio/privado/')
    # En path se guarda la firma privada del usuario
    path = path + name

    permisos = ['chmod', '400', path]
    cmd = 'openssl genrsa -aes256 -out '+path+' -passout pass:'+contrasena+' 2048'
    os.system(cmd)

    #subprocess.run(cmd)
    subprocess.run(permisos)


# print (cmd)

# Crea la peticion de firma de certificado de un usuario
def crear_csr(nombre, c, st, l, o, ou, cn,contrasena):
    keyname = ".key.pem"
    csr = ".csr.pem"
    name = nombre + keyname
    name2 = nombre + csr
    path = os.path.join(settings.BASE_DIR, 'raiz/CA/intermedio/privado/')
    # path2 donde se guarda la peticion de firma
    path2 = os.path.join(settings.BASE_DIR, 'raiz/CA/intermedio/csr/')
    path = path + name
    path2 = path2 + name2
    # print(path2)

    C = 'C='
    C = C + c

    ST = 'ST='
    ST = ST + st

    L = 'L='
    L = L + l

    O = 'O='
    O = O + o

    OU = 'OU='
    OU = OU + ou

    CN = 'CN='
    CN = CN + cn

    subj = '/'
    subj = subj + C + '/' + ST + '/' + L + '/' + O + '/' + OU + '/' + CN

    print('aqui', path, path2, subj)
    # cmd=['openssl','req','-config','raiz/CA/intermedio/openssl.cnf','-key',path,'-new','-sha256','-out',path2,'-subj',subj]
    # print(cmd)
    # subprocess.call(cmd)




    openssl_path = os.path.join(settings.BASE_DIR, 'raiz/CA/intermedio/openssl.cnf')
    cmd = 'openssl req '+' -passin pass:'+contrasena +' -config ' + openssl_path + ' -key ' + path + ' -new -sha256 -out ' + path2 + ' -subj ' + subj
    os.system(cmd)

    print("CSR ha sido creado")
    return path2


# Firmamos el certificado
def firma_cert(path, nombre):
    # En path1 se guarda el certificado firmado
    path1 = os.path.join(settings.BASE_DIR, 'raiz/CA/intermedio/certs/')
    finpath = ".cert.pem"
    path1 = path1 + nombre + finpath
    print(path1)
    # cmd=['openssl','ca','-config','raiz/CA/intermedio/openssl.cnf','-extensions','usr_cert','-days','100','-notext','-md','sha256','-in',path,'-out',path1]
    # subprocess.call(cmd)

    openssl_path = os.path.join(settings.BASE_DIR, 'raiz/CA/intermedio/openssl.cnf')
    cmd = 'openssl ca -config ' + openssl_path + ' -extensions usr_cert -days 100 -notext -md sha256 -in ' + path + ' -out ' + path1 + " -passin pass:pruebainter1"
    os.system(cmd)


# Verificamos si el certificado es validoe n nuestra cadena de confianza
def verifica_cert(path):
    cmd = ['openssl', 'x509', '-noout', '-text', '-in', path]
    # subprocess.call(cmd)
    # Verificando si el certificado es valido en la cadena de confianza
    chain_path = os.path.join(settings.BASE_DIR, 'raiz/CA/intermedio/certs/ca-chain.cert.pem')
    cmd2 = ['openssl', 'verify', '-CAfile', chain_path,
            path]
    p = subprocess.run(cmd2, stdout=subprocess.PIPE)
    # Resultado de la verififcacion
    print(p.stdout)
