# coding=utf-8

import socket
import json
from constantes import *


class NetworkEventsListener:
    def __init__(self, s: socket.socket, p: tuple):
        self._sock = s
        self._params = p
        self._buffer_size = BUFFER_SIZE
        self._recv_to_send_cmd = {
            UDP_CARTE_CHANGE: UDP_ASK_CARTE_CHANGES,
            UDP_PLAYERS_CHANGE: UDP_ASK_PLAYERS_CHANGES,
            UDP_MESSAGES_CHANGE: UDP_ASK_MESSAGES
        }
        self._controlers = {}

    def get_sock(self):
        return self._sock

    def get_params(self):
        return self._params

    def add_controler(self, type: str, controler: object):
        self._controlers[type] = controler

    def send(self, message: str):
        self._sock.sendto(json.dumps(message), self._params)

    def _recv(self):
        return json.loads(self._sock.recv(self._buffer_size))

    def listen(self):
        self.send(UDP_ASK_NEWS)
        ret = self._recv()
        changes = {}

        if isinstance(ret, dict):
            if ret[UDP_NOTHING_NEW]:
                pass
            else:
                for key, code in self._recv_to_send_cmd.items():
                    if ret[key]:
                        self.send(code)
                        changes[key] = self._recv()
                if changes:
                    for key, val in changes.items():
                        # do some stuff dealing with these values
                        pass