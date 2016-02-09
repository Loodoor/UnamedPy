# coding=utf-8

import pickle
from constantes import *
from pygame.locals import *
from exceptions import ClassNonChargee


class ParametresManager:
    def __init__(self):
        self._default_config = {
            "controls": {
                HAUT: K_UP,
                BAS: K_DOWN,
                GAUCHE: K_LEFT,
                DROITE: K_RIGHT,
                CHAT: K_KP0,
                MENU: K_RSHIFT,
                SCREENSCHOT: K_F5,
                SHOW_FPS: K_BACKSPACE,
                VALIDATION: K_RETURN
            },
            "joy_controls": {},
            "secured_controls": {
                NEXT_PAGE: K_RIGHT,
                PREVIOUS_PAGE: K_LEFT,
                UP_PAGE: K_UP,
                DOWN_PAGE: K_DOWN
            },
            "b&w": False,
            "music": True,
            "play_anims": True,
            "delta_time": {
                "has_default": False,
                "default": 1.0
            }
        }
        self.params = {}
        self.path_to_settings = os.path.join("..", "assets", "configuration", "config.json")

    def _pre_load(self):
        if not os.path.exists(self.path_to_settings):
            with open(self.path_to_settings, "wb") as wsettings:
                pickle.Pickler(wsettings).dump(self._default_config)
        elif os.path.exists(self.path_to_settings) and open(self.path_to_settings, 'r').read() == "":
            os.remove(self.path_to_settings)
            self._pre_load()

    def load(self):
        self._pre_load()
        self.params = pickle.Unpickler(open(self.path_to_settings, 'rb')).load()

    def get(self, key: str):
        if self.params:
            return self.params[key]
        else:
            raise ClassNonChargee("ParametresManager", "get")

    def save(self):
        with open(self.path_to_settings, "wb") as wsettings:
            pickle.Pickler(wsettings).dump(self.params)