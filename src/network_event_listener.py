# coding=utf-8

import socket
import json
from constantes import *


class NetworkEventsListener:
    def __init__(self, s: socket.socket, p: tuple):
        self._sock = s
        self._params = p
        self._buffer_size = BUFFER_SIZE

    def send(self, message: str):
        self._sock.sendto(json.dumps(message), self._params)

    def _recv(self):
        return self._sock.recv(self._buffer_size)

    def listen(self):
        self.send("")
        ret = self._recv()
        if ret != UDP_NOTHING_NEW:
            pass