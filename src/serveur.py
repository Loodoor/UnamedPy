# coding=utf-8

import json
import socket
from constantes import *

print("Démarrage du serveur ...")

print("_" * 77 + "\n" + "|/-\\" * (79 // 4) + "\n" + "|   " * (79 // 4))

hote = ''
try:
    hote = socket.gethostbyname(socket.gethostname())
except NameError as nom_err:
    print(nom_err)
except TypeError as type_err:
    print(type_err)
print("Écoute sur le serveur {0}.".format(hote))

sport = 60000
while 1:
    sport = input("Entrez le port [60000] > ")
    if sport.strip() == "":
        sport = 60000
        break
    try:
        sport = sport.strip()
        int(sport)
        break
    except ValueError:
        print("Dis Toto, t'as pas compris ? Il me faut un chiffre !")

port = int(sport)
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
connexion_principale.bind((hote, port))
print("Le serveur écoute à présent sur le port {0} depuis {1}.".format(port, hote))

serveur_lance = True

users = {}

if os.path.exists("config.srv"):
    with open("config.srv") as config:
        predefined = eval(config.read())
else:
    predefined = {
        UDP_ASK_SERV_NAME: "MyServeur",
    }

BUFFER_SIZE = 4096

while serveur_lance:
    data, addr = connexion_principale.recvfrom(BUFFER_SIZE)
    if data:
        if addr not in users.keys():
            users[addr] = json.loads(data)
        else:
            datas = json.loads(data)
            if isinstance(datas, str):
                if datas in predefined.keys():
                    connexion_principale.sendto(json.dumps(predefined[datas]), addr)
                else:
                    pass
            else:
                pass