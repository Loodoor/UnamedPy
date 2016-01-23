# coding=utf-8

import socket
import json


BUFFER_SIZE = 8192

UDP_ASK_NEWS = 1
UDP_ASK_MESSAGES = 2
UDP_ASK_CARTE_CHANGES = 3
UDP_ASK_PLAYERS_CHANGES = 4
UDP_ASK_SERV_NAME = 5
UDP_ASK_MYRANG = 6
UDP_MSG_NONE = 7
UDP_NOTHING_NEW = 8
UDP_CARTE_CHANGE = 9
UDP_PLAYERS_CHANGE = 10
UDP_MESSAGES_CHANGE = 11
UDP_SEND_MSG = 12
UDP_SEND_MYPOS = 13
UDP_SEND_DISCONNECT = 14
UDP_CONNECTED = 15
UDP_LISTENNING = 16
UDP_CONNECTION_REFUSED = 17
UDP_ASK_TO_SAVE_LOGS = 18

co = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
params = (input("IP: "), 5500)
_enabled = True
co.settimeout(30)


def send(message: str or dict or list or int):
    global _enabled
    if _enabled:
        co.sendto(json.dumps(message).encode(), params)


def _recv():
    global _enabled
    if _enabled:
        try:
            return json.loads(co.recv(BUFFER_SIZE).decode())
        except ConnectionResetError:
            print("La connexion a été fermée par le serveur. "
                  "Contactez l'administrateur si vous pensez que cela est un problème technique")
        except socket.timeout:
            print("Le serveur n'a pas répondu à temps")
    return UDP_NOTHING_NEW


while True:
    cmd = input("$ ")
    send(eval(cmd))
    print(_recv())