# coding=utf-8

import pickle as json
import socket
from constantes import *


def get_from_where(users: dict, news_: list, kind: str, addr):
    work = []
    for elem in news_:
        if users[addr]['pseudo'] not in elem['sawit'] and elem['type'] == kind:
            work.append(elem['content'])
            elem['sawit'].append(users[addr]['pseudo'])
    return work


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
    sport = input("Entrez le port [5500] > ")
    if sport.strip() == "":
        sport = 5500
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

news_ = []
askers = (
    UDP_ASK_CARTE_CHANGES,
    UDP_ASK_MESSAGES,
    UDP_ASK_PLAYERS_CHANGES
)

while serveur_lance:
    data, addr = connexion_principale.recvfrom(BUFFER_SIZE)
    if data:
        if addr not in users.keys():
            users[addr] = json.loads(data.decode())
            connexion_principale.sendto(json.dumps(UDP_CONNECTED).encode(), addr)
            print("Un client s'est connecté ! Youpi !\t* Pseudo : {0}".format(users[addr]['pseudo']))
        else:
            datas = json.loads(data)
            if isinstance(datas, str):
                if datas in predefined.keys():
                    connexion_principale.sendto(json.dumps(predefined[datas].encode()), addr)
                else:
                    # ASK
                    if datas in askers:
                        work = []
                        if datas == UDP_ASK_CARTE_CHANGES:
                            work = get_from_where(users, news_, UDP_CARTE_CHANGE, addr)
                        elif datas == UDP_ASK_MESSAGES:
                            work = get_from_where(users, news_, UDP_MESSAGES_CHANGE, addr)
                        elif datas == UDP_ASK_PLAYERS_CHANGES:
                            work = get_from_where(users, news_, UDP_PLAYERS_CHANGE, addr)
                        if not work:
                            connexion_principale.sendto(json.dumps(UDP_NOTHING_NEW).encode(), addr)
                        else:
                            connexion_principale.sendto(json.dumps(work).encode(), addr)
                    if datas == UDP_ASK_NEWS:
                        kind = []
                        for elem in news_:
                            if users[addr]['pseudo'] not in elem['sawit']:
                                kind.append(elem['type'])
                        if kind:
                            connexion_principale.sendto(json.dumps(kind).encode(), addr)
                        else:
                            connexion_principale.sendto(json.dumps([UDP_NOTHING_NEW]).encode(), addr)
                    elif datas == UDP_ASK_MYRANG:
                        if users[addr]['pseudo'] in pred_users.keys():
                            connexion_principale.sendto(json.dumps(pred_users[users[addr]['pseudo']]).encode(), addr)
                        else:
                            connexion_principale.sendto(json.dumps(RANG_JOUEUR).encode(), addr)
                    # SEND
                    elif datas == UDP_SEND_MSG:
                        print("message en réception ...")
                        connexion_principale.sendto(json.dumps(UDP_LISTENNING).encode(), addr)
                        d_tmp, a_tmp = connexion_principale.recvfrom(BUFFER_SIZE)
                        if a_tmp == addr:
                            print("message recu !")
                            content = json.loads(d_tmp.decode())
                            print(content)
                            news_ += [{
                                'type': UDP_MESSAGES_CHANGE,
                                'content': content,
                                'sawit': []
                            }]
                    elif datas == UDP_SEND_MYPOS:
                        connexion_principale.sendto(json.dumps(UDP_LISTENNING).encode(), addr)
                        d_tmp, a_tmp = connexion_principale.recvfrom(BUFFER_SIZE)
                        if a_tmp == addr:
                            content = json.loads(d_tmp.decode())
                            users[addr]['pos'] = content
                            news_ += [{
                                'type': UDP_PLAYERS_CHANGE,
                                'content': {
                                    'addr': addr,
                                    'pseudo': users[addr]['pseudo'],
                                    'pos': users[addr]['pseudo']
                                },
                                'sawit': []
                            }]
                    elif datas == UDP_SEND_DISCONNECT:
                        print(users[addr] + " se déconnecte du serveur. Au revoir !")
                        del users[addr]
            elif isinstance(datas, list):
                pass