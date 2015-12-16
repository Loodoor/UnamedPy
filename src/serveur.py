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
if os.path.exists("users.srv"):
    with open("users.srv") as users:
        pred_users = eval(users.read())
else:
    pred_users = {}

BUFFER_SIZE = 4096

news_from_user = {}

while serveur_lance:
    data, addr = connexion_principale.recvfrom(BUFFER_SIZE)
    if data:
        if addr not in users.keys():
            users[addr] = json.loads(data)
            connexion_principale.sendto(json.dumps(UDP_CONNECTED), addr)
        else:
            datas = json.loads(data)
            if isinstance(datas, str):
                if datas in predefined.keys():
                    connexion_principale.sendto(json.dumps(predefined[datas]), addr)
                else:
                    if datas == UDP_ASK_CARTE_CHANGES:
                        connexion_principale.sendto(json.dumps(UDP_NOTHING_NEW), addr)
                    elif datas == UDP_ASK_PLAYERS_CHANGES:
                        connexion_principale.sendto(json.dumps(UDP_NOTHING_NEW), addr)
                    elif datas == UDP_ASK_MESSAGES:
                        connexion_principale.sendto(json.dumps(UDP_NOTHING_NEW), addr)
                    elif datas == UDP_ASK_NEWS:
                        connexion_principale.sendto(json.dumps([UDP_NOTHING_NEW]), addr)
                    elif datas == UDP_ASK_MYRANG:
                        if users[addr]['pseudo'] in pred_users.keys():
                            connexion_principale.sendto(json.dumps(pred_users[users[addr]['pseudo']]), addr)
                        else:
                            connexion_principale.sendto(json.dumps(RANG_JOUEUR), addr)
                    elif datas == UDP_SEND_MSG:
                        connexion_principale.sendto(json.dumps(UDP_LISTENNING), addr)
                        d_tmp, a_tmp = connexion_principale.recvfrom(BUFFER_SIZE)
                        if a_tmp == addr:
                            content = json.loads(d_tmp)
                            news_from_user[users[addr]['pseudo']] = {
                                'type': UDP_MESSAGES_CHANGE,
                                'content': content
                            }
                    elif datas == UDP_SEND_MYPOS:
                        pass
            elif isinstance(datas, list):
                pass