# coding=utf-8

import re
import textentry
from constantes import *
from network_event_listener import NetworkEventsListener
from exceptions import ControlerManquant, MethodeManquante


class ChatManager:
    def __init__(self, ecran, font, reseau_mgr: NetworkEventsListener,
                 pseudo: str, rang: int):
        self.ecran = ecran
        self.font = font
        self.reseau_mgr = reseau_mgr
        self.pseudo = pseudo
        self.rang = rang
        self.stack = []
        self.text_entry = textentry.TextBox(self.ecran, x=CHAT_X_BOX, y=CHAT_Y_BOX,
                                            sx=CHAT_SX_BOX, sy=CHAT_SY_BOX, bgcolor=(70, 70, 70))
        self.quit = None
        self.fond = ree.load_image(os.path.join("..", "assets", "gui", "fd_chat.png"))
        self._controlers = {}

    @staticmethod
    def is_cheat_code(chaine: str) -> bool:
        if re.match(r'^!(\d+|\w+) *.*', chaine):
            return True
        return False

    def _manage_cheat_code(self, code: str):
        try:
            code, args = code[1:].split(' ')
        except ValueError:
            code = code[1:]
            args = []
        if code in CHEATS_CODES.keys():
            if CHEATS_CODES[code]['controler'] in self._controlers.keys():
                if hasattr(self._controlers[CHEATS_CODES[code]['controler']], CHEATS_CODES[code]['methode']):
                    m = getattr(self._controlers[CHEATS_CODES[code]['controler']], CHEATS_CODES[code]['methode'])
                    m(*args)
                else:
                    raise MethodeManquante("La méthode", CHEATS_CODES[code]['methode'], "du controler", CHEATS_CODES[code]['controler'], "est manquante")
            else:
                raise ControlerManquant("Le controler", CHEATS_CODES[code]['controler'], "manque à l'appel. Cheat code impossible à utiliser")

    def add_controler(self, name: str, controler: object):
        self._controlers[name] = controler

    def update_quit_event(self, new):
        self.quit = new

    def update(self):
        self.render()

        if not self.text_entry.type_enter():
            self.text_entry.render()
        else:
            if self.text_entry.get_text().strip():
                if not ChatManager.is_cheat_code(self.text_entry.get_text()):
                    self.reseau_mgr.chat_message(self.text_entry.get_text())
                    self.new_message(self.text_entry.get_text())
                else:
                    self._manage_cheat_code(self.text_entry.get_text())
            self.text_entry.reset()

    def network_fetch_messages(self):
        datas = self.reseau_mgr.get_chat_messages()
        if isinstance(datas, list):
            self.stack.append(datas)
        else:
            self.stack = [
                {
                    'message': "Erreur côté serveur",
                    'pseudo': "Service",
                    'rang': RANG_SERVICE
                }
            ]

    def get_messages(self):
        if self.reseau_mgr.is_enabled():
            self.network_fetch_messages()
        return self.stack[::-1]

    def update_name(self, new_name: str):
        self.pseudo = new_name

    def update_rang(self, new_rang: int):
        self.rang = new_rang

    def is_running(self):
        return self.text_entry.is_running()

    def event(self, e):
        if e != (KEYDOWN, self.quit):
            if e == KEYDOWN:
                self.text_entry.event(e)
        else:
            self.text_entry.running = False

        if e == QUIT:
            exit(1)

    def new_message(self, msg: str):
        self.stack += [
            {
                "pseudo": self.pseudo,
                "message": msg,
                "rang": self.rang
            }
        ]

    def render(self):
        self.ecran.blit(self.fond, (CHAT_X_MESSAGES, CHAT_Y_MESSAGES))
        i = 0
        color = (255, 255, 255)
        for msg in self.get_messages():
            if msg["rang"] == RANG_ADMIN:
                color = CHAT_COULEUR_ADMIN
            if msg["rang"] == RANG_MODO:
                color = CHAT_COULEUR_MODO
            if msg["rang"] == RANG_JOUEUR:
                color = CHAT_COULEUR_JOUEUR
            if msg["rang"] == RANG_SERVICE:
                color = CHAT_COULEUR_SERVICE
            self.ecran.blit(self.font.render(msg["message"], POL_ANTIALISING, color),
                            (CHAT_X_MESSAGES, CHAT_Y_MESSAGES + i * CHAT_SY_MESSAGE))
            i += 1