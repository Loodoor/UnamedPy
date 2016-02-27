# coding=utf-8

import socket
import json
from constantes import *
from utils import ugen_key
from random import random
import debug


class NetworkEventsListener:
    def __init__(self, s: socket.socket, p: tuple):
        self._sock = s
        self._params = p
        self._buffer_size = BUFFER_SIZE
        self._enabled = True if s else False
        self._connected = False
        self._recv_to_send_cmd = {
            UDP_CARTE_CHANGE: UDP_ASK_CARTE_CHANGES,
            UDP_PLAYERS_CHANGE: UDP_ASK_PLAYERS_CHANGES
        }
        self.rang = RANG_NUL
        self._controlers = {}
        self._connection_key = ugen_key(random() * 10000)

    def check_before_connecting(self) -> bool:
        if 'perso' in self._controlers and 'others' in self._controlers and 'adventure' in self._controlers:
            return True
        return False

    def on_connect(self):
        self.send({
            'pseudo': self._controlers['adventure'].get_pseudo(),
            'pos': self._controlers['perso'].get_pos(),
            'key': self._connection_key,
            'avatar': self._controlers['perso'].get_skin_path()
        })
        debug.println("Connexion")

    def disable(self):
        debug.println("Désactivation de la connexion")
        self._enabled = False

    def enable(self):
        self._enabled = True

    def is_enabled(self):
        return self._enabled

    def get_sock(self):
        return self._sock

    def get_params(self):
        return self._params

    def add_controler(self, type_: str, controler: object):
        self._controlers[type_] = controler

    def _ask_rang(self):
        if self.rang == RANG_NUL:
            self.send(UDP_ASK_MYRANG)
            self.rang = self._recv()

    def chat_message(self, message: str):
        self._ask_rang()
        self.send(UDP_SEND_MSG)
        if self._recv() == UDP_LISTENNING:
            self.send({
                "message": message,
                "pseudo": self._controlers['adventure'].get_pseudo(),
                "rang": self.rang
            })

    def get_chat_messages(self):
        self.send(UDP_ASK_MESSAGES)
        return self._recv()

    def disconnect(self):
        self.send(UDP_SEND_DISCONNECT)

    def send(self, message: str or dict or list):
        if self._enabled:
            self._sock.sendto(json.dumps(message).encode(), self._params)

    def _recv(self):
        if self._enabled:
            try:
                return json.loads(self._sock.recv(self._buffer_size).decode())
            except ConnectionResetError:
                debug.println("La connexion a été fermée par le serveur. "
                              "Contactez l'administrateur si vous pensez que cela est un problème technique")
                self.disable()
        return UDP_NOTHING_NEW

    def refresh_mypos(self):
        self.send(UDP_SEND_MYPOS)
        if self._recv() == UDP_LISTENNING:
            self.send({
                'pos': self._controlers['perso'].get_pos(),
                'dir': self._controlers['perso'].get_dir()
            })

    def listen(self):
        if self._enabled:
            if not self._connected:
                debug.println("Connection en cours")
                if self.check_before_connecting():
                    debug.println("Connexion vérifiée")
                    self.on_connect()
                    debug.println("En attente du serveur")
                    if self._recv() == UDP_CONNECTED:
                        debug.println("Connecté !")
                        self._connected = True
                    else:
                        debug.println("Impossible de se connecter correctement au serveur, la connexion a été refusée ou a échoué")
                        self.disable()
                else:
                    debug.println("Impossible de se connecter correctement au serveur, des controlers sont manquant")
                    self.disable()

            self.send(UDP_ASK_NEWS)
            ret = self._recv()
            changes = {}

            if isinstance(ret, list):
                if UDP_NOTHING_NEW in ret:
                    pass
                else:
                    for key, code in self._recv_to_send_cmd.items():
                        if key in ret:
                            self.send(code)
                            changes[key] = self._recv()
                    if changes:
                        for key, val in changes.items():
                            if key == UDP_CARTE_CHANGE:
                                pass
                            if key == UDP_PLAYERS_CHANGE:
                                if isinstance(val, list):
                                    for perso in val:
                                        self._controlers['others'].move_this(perso)

            self.refresh_mypos()