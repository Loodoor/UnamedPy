# coding=utf-8

import pickle
from constantes import *
from pygame.locals import *
from exceptions import ClassNonChargee
import rendering_engine


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
            "joy_controls": {
                DROITE: {
                    "axis": {
                        "nb": 0,
                        "value": 1
                    },
                    "hat": {
                        "nb": 0,
                        "value": (1, 0)
                    }
                },
                GAUCHE: {
                    "axis": {
                        "nb": 0,
                        "value": -1
                    },
                    "hat": {
                        "nb": 0,
                        "value": (-1, 0)
                    }
                },
                BAS: {
                    "axis": {
                        "nb": 1,
                        "value": 1
                    },
                    "hat": {
                        "nb": 0,
                        "value": (0, 1)
                    }
                },
                HAUT: {
                    "axis": {
                        "nb": 1,
                        "value": -1
                    },
                    "hat": {
                        "nb": 0,
                        "value": (0, -1)
                    }
                },
                CHAT: {
                    "button": 3,
                    "value": 1
                },
                MENU: {
                    "button": 2,
                    "value": 1
                },
                SCREENSCHOT: {
                    "button": 6,
                    "value": 1
                },
                SHOW_FPS: {
                    "button": 7,
                    "value": 1
                },
                VALIDATION: {
                    "button": 0,
                    "value": 1
                },
                NEXT_PAGE: {
                    "button": 5,
                    "value": 1
                },
                PREVIOUS_PAGE: {
                    "button": 4,
                    "value": 1
                },
                UP_PAGE: {
                    "axis": {
                        "nb": 1,
                        "value": -1
                    },
                    "hat": {
                        "nb": 0,
                        "value": (0, -1)
                    }
                },
                DOWN_PAGE: {
                    "axis": {
                        "nb": 1,
                        "value": 1
                    },
                    "hat": {
                        "nb": 0,
                        "value": (0, 1)
                    }
                }
            },
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
        elif open(self.path_to_settings, 'rb').read() == "":
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


def gui_access(ecran):
    done = False
    fond = rendering_engine.load_image(os.path.join("..", "assets", "gui", "fd_params.png"))
    ecran.fill(0)

    while not done:
        for event in rendering_engine.get_event():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                done = True
            if event.type == MOUSEBUTTONUP:
                xp, yp = event.pos

        ecran.blit(fond, (PARAMS_X, PARAMS_Y))

        rendering_engine.flip()