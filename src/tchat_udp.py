import socket
import json
from constantes import *


class TchatUDP:
    def __init__(self, s: socket.socket, params: tuple=('127.0.0.1', 5500)):
        self.s = s
        self.params = params
        self.hote = self.params[0]
        self.port = self.params[1]

    def send_message(self, message):
        self.s.sendto(json.dumps(message), self.params)

    def check_for_message(self):
        self.s.sendto(json.dumps(TUDP_ASK_MESSAGES), self.params)
        responce = self.s.recv(BUFFER_SIZE)
        if responce != TUDP_NONE:
            print(responce)