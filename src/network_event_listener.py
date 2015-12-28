# coding=utf-8

import socket
import json
from constantes import *


class NetworkEventsListener:
    def __init__(self, s: socket.socket, p: tuple, perso):
        self._sock = s
        self._params = p
        self._buffer_size = BUFFER_SIZE
        self._enabled = True if s else False
        self._connected = False
        self._recv_to_send_cmd = {
            UDP_CARTE_CHANGE: UDP_ASK_CARTE_CHANGES,
            UDP_PLAYERS_CHANGE: UDP_ASK_PLAYERS_CHANGES,
            UDP_MESSAGES_CHANGE: UDP_ASK_MESSAGES
        }
        self.perso = perso
        self.rang = RANG_NUL
        self._controlers = {}

    def on_connect(self):
        self.send({
            'pseudo': self.perso.get_pseudo(),
            'pos': self.perso.get_pos()
        })

    def disable(self):
        self._enabled = False

    def enable(self):
        self._enabled = True

    def is_enabled(self):
        return self._enabled

    def get_sock(self):
        return self._sock

    def get_params(self):
        return self._params

    def add_controler(self, type: str, controler: object):
        self._controlers[type] = controler

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
                "pseudo": self.perso.get_pseudo(),
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
            return json.loads(self._sock.recv(self._buffer_size).decode())
        return UDP_NOTHING_NEW

    def refresh_mypos(self):
        self.send(UDP_SEND_MYPOS)
        if self._recv() == UDP_LISTENNING:
            self.send(self.perso.get_pos())

    def listen(self):
        if self._enabled:
            if not self._connected:
                self.on_connect()
                if self._recv() == UDP_CONNECTED:
                    self._connected = True
                else:
                    print("Impossible de se connecter correctement au serveur ...")

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
                            # do some stuff dealing with these values
                            pass

            self.refresh_mypos()