# coding=utf-8

import json
import socket
from utils import usep_lst_in_smallers
from constantes import *
from datetime import datetime


buffer_for_file = []


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
    except OSError:
        print("Le message était : ", message, ", et l'adresse : ", addr)
        sys.exit(0)


def print_or_save(*msg, sep=' ', end='\n') -> None:
    global infile
    global buffer_for_file

    if not infile:
        print(*msg, sep=sep, end=end)
    else:
        buffer_for_file.append(sep.join(msg) + end)


def save_logs() -> bool:
    global buffer_for_file
    global connexion_principale
    global start_time
    global predefined
    global pred_users
    global users
    global news

    print("\t * Création des logs ...")
    log_nb = 0
    for logs in usep_lst_in_smallers(buffer_for_file, 500):
        header = [
            "Fichier de log généré automatiquement",
            "500 lignes de log maximum par fichier",
            "Fichier n° {}".format(log_nb),
            "***\t***\t***"
        ]
        if not log_nb:
            header += [
                "Serveur sur : {}".format(connexion_principale),
                "Lancé à : {}".format(start_time.strftime("%d/%m/%Y - %H:%M:%S")),
                "Sauvegarde à : {}".format(datetime.now().strftime("%d/%m/%Y - %H:%M:%S")),
                "Nombre de lignes de logs : {}".format(len(buffer_for_file)),
                "Commandes prédéfinies : {}".format(predefined),
                "Utilisateurs préenregistrés : {}".format(pred_users),
                "Taille maximale d'un packet : {}".format(BUFFER_SIZE),
                "Nombre de joueurs au moment de la sauvegarde : {}".format(len(users)),
                "Nombre de mises à jour de données à faire aux clients au moment de la sauvegarde : ".format(len(news)),
                "***\t***\t***"
            ]
        with open(os.path.join("..", "serverlogs", "log{}.log".format(log_nb)), "w") as file:
            print("\t * Enregistrement {] ...".format(log_nb))
            file.writelines(header + logs)
        log_nb += 1
    print("\t * Logs créés et sauvegardés")
    return True


start_time = datetime.now()
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

infile = False
while 1:
    tmp = input("Voulez-vous enregistrer les log dans des fichiers (ou les afficher) [O/N] ?\n> ")
    if tmp.lower() in 'on' and tmp.strip():
        if tmp.lower() == 'o':
            infile = True
        break
    else:
        print("Entrez O (oui) ou N (non) !")

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
    pred_users = {
        "folaefolc": {
            "rang": RANG_ADMIN
        }
    }

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
                print_or_save("Un client s'est connecté ! Youpi !\t* Pseudo : {0}".format(users[addr]['pseudo']))
            else:
                send(connexion_principale, UDP_CONNECTION_REFUSED, addr)
                print_or_save("La connexion a été refusée pour {} en raison des paramètres de configuration".format(datas['pseudo']))
        else:
            datas = json.loads(data.decode())
            if isinstance(datas, int):
                if datas in predefined.keys():
                    send(connexion_principale, predefined[datas], addr)
                else:
                    # ASK
                    if datas in askers:
                        print_or_save("Reçu un code de demande de changement ({})".format(datas))
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
                            cnt = {
                                'type': UDP_MESSAGES_CHANGE,
                                'content': content,
                                'sawit': [],
                                'from': users[addr]['pseudo']
                            }
                            news_ += [cnt]
                            print_or_save("{} a ajouté un message : {}".format(users[addr]['pseudo'], cnt))

                    elif datas == UDP_SEND_MYPOS:
                        send(connexion_principale, UDP_LISTENNING, addr)
                        d_tmp, a_tmp = connexion_principale.recvfrom(BUFFER_SIZE)
                        if a_tmp == addr:
                            content = json.loads(d_tmp.decode())
                            users[addr]['pos'] = content['pos']
                            users[addr]['dir'] = content['dir']
                            cnt = {
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
                            }
                            news_ += [cnt]
                            print_or_save("{} se déplace. Nouvelles informations : {}".format(users[addr]['pseudo'], cnt))

                    elif datas == UDP_SEND_DISCONNECT:
                        print_or_save(users[addr] + " se déconnecte du serveur. Au revoir !")
                        del users[addr]
                    elif datas == UDP_ASK_TO_SAVE_LOGS and users[addr]['pseudo'] in pred_users.keys():
                        if pred_users[users[addr]['pseudo']]['rang'] == RANG_ADMIN:
                            print("Sauvegarde ...")
                            save_logs()
                            print_or_save("{} a demandé à sauvegarder les logs".format(users[addr]['pseudo']))
            elif isinstance(datas, list):
                pass