# coding=utf-8

import json
import socket
from constantes import *


def get_from_where(usr: dict, news: list, kindof: str, address) -> list:
    smth = []
    todel = []
    for i in range(len(news)):
        e = news[i]
        if usr[address]['pseudo'] not in e['sawit'] and e['type'] == kindof:
            smth.append(e['content'])
            news[i]['sawit'].append(usr[address]['pseudo'])
            if len(news[i]['sawit']) == len(usr):
                todel.append(i)
    for elem in todel[::-1]:
        news.pop(elem)
    return smth


def send(co, message, addr) -> None:
    try:
        co.sendto(json.dumps(message).encode(), addr)
    except OSError as e:
        print("Le message était : ", message, ", et l'adresse : ", addr)
        sys.exit(0)


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
while True:
    try:
        connexion_principale.bind((hote, port))
    except OSError:
        port += 1
        print("Connexion échouée.  |  Tentative de connexion sur le port [{}]".format(port))
    else:
        break
print("Le serveur écoute à présent sur le port {0} depuis {1}.".format(port, hote))

serveur_lance = True

users = {}

if os.path.exists("config.srv"):
    with open("config.srv") as config:
        predefined = eval(config.read())
else:
    predefined = {
        "servname": "MyServeur",
        "banlist": []
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
            datas = json.loads(data.decode())
            if datas['pseudo'] not in predefined['banlist']:
                users[addr] = datas
                send(connexion_principale, UDP_CONNECTED, addr)
                print("Un client s'est connecté ! Youpi !\t* Pseudo : {0}".format(users[addr]['pseudo']))
            else:
                send(connexion_principale, UDP_CONNECTION_REFUSED, addr)
        else:
            datas = json.loads(data.decode())
            if isinstance(datas, int):
                if datas in predefined.keys():
                    send(connexion_principale, predefined[datas], addr)
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
                            send(connexion_principale, UDP_NOTHING_NEW, addr)
                        else:
                            send(connexion_principale, work, addr)
                    if datas == UDP_ASK_NEWS:
                        kind = []
                        for elem in news_:
                            if users[addr]['pseudo'] not in elem['sawit'] and elem['type'] != UDP_MESSAGES_CHANGE:
                                kind.append(elem['type'])
                        if kind:
                            send(connexion_principale, kind, addr)
                        else:
                            send(connexion_principale, [UDP_NOTHING_NEW], addr)
                    elif datas == UDP_ASK_MYRANG:
                        if users[addr]['pseudo'] in pred_users.keys():
                            send(connexion_principale, pred_users[users[addr]['pseudo']]['rang'], addr)
                        else:
                            send(connexion_principale, RANG_JOUEUR, addr)
                    # SEND
                    elif datas == UDP_SEND_MSG:
                        send(connexion_principale, UDP_LISTENNING, addr)
                        d_tmp, a_tmp = connexion_principale.recvfrom(BUFFER_SIZE)
                        if a_tmp == addr:
                            content = json.loads(d_tmp.decode())
                            news_ += [{
                                'type': UDP_MESSAGES_CHANGE,
                                'content': content,
                                'sawit': [],
                                'from': users[addr]['pseudo']
                            }]
                    elif datas == UDP_SEND_MYPOS:
                        send(connexion_principale, UDP_LISTENNING, addr)
                        d_tmp, a_tmp = connexion_principale.recvfrom(BUFFER_SIZE)
                        if a_tmp == addr:
                            content = json.loads(d_tmp.decode())
                            users[addr]['pos'] = content['pos']
                            users[addr]['dir'] = content['dir']
                            news_ += [{
                                'type': UDP_PLAYERS_CHANGE,
                                'content': {
                                    'addr': addr,
                                    'pseudo': users[addr]['pseudo'],
                                    'pos': users[addr]['pos'],
                                    'dir': users[addr]['dir'],
                                    'avatar': users[addr]['avatar'],
                                    'id': users[addr]['key']
                                },
                                'sawit': [],
                                'from': users[addr]['pseudo']
                            }]
                    elif datas == UDP_SEND_DISCONNECT:
                        print(users[addr] + " se déconnecte du serveur. Au revoir !")
                        del users[addr]
            elif isinstance(datas, list):
                pass