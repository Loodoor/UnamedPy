# coding=utf-8

import pickle
from constantes import *
from pygame.locals import *
from exceptions import ClassNonChargee
import rendering_engine
from utils import ureplace_bool_str
import debug


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

    def set(self, key: str, new):
        if self.params:
            self.params[key] = new
        else:
            raise ClassNonChargee("ParametresManager", "set")

    def save(self):
        with open(self.path_to_settings, "wb") as wsettings:
            pickle.Pickler(wsettings).dump(self.params)


def gui_access(ecran, police):
    done = False

    params = ParametresManager()
    params.load()

    fond = rendering_engine.load_image(os.path.join("..", "assets", "gui", "fd_params.png"))
    titre = police.render("Paramètres", POL_ANTIALISING, (10, 10, 10))
    const_to_str = {
        HAUT: "HAUT",
        BAS: "BAS",
        GAUCHE: "GAUCHE",
        DROITE: "DROITE",
        CHAT: "CHAT",
        MENU: "MENU",
        SCREENSCHOT: "CAPTURE D'ECRAN",
        SHOW_FPS: "AFFICHER LES FPS",
        VALIDATION: "VALIDER (une action)"
    }
    controls = params.get("controls")
    settings_txt_list = [police.render("Contrôles", POL_ANTIALISING, (10, 10, 10))] + [
        police.render("{} : {}".format(const_to_str[cst], rendering_engine.get_key_name(controls[cst])), POL_ANTIALISING, (10, 10, 10)) for cst in controls.keys()
    ] + [
        police.render("Musique : {}".format(ureplace_bool_str(params.get("music"), ['on', 'off'])), POL_ANTIALISING, (10, 10, 10)),
        police.render("Animations : {}".format(ureplace_bool_str(params.get("play_anims"), ['on', 'off'])), POL_ANTIALISING, (10, 10, 10)),
        police.render("DeltaTime par défaut : {}".format(ureplace_bool_str(params.get("delta_time")["has_default"], ['on', 'off'])), POL_ANTIALISING, (10, 10, 10)),
        police.render("Valeur par défaut (valable uniquement si activé ; en sec) : {}".format(params.get("delta_time")["default"]), POL_ANTIALISING, (10, 10, 10))
    ]

    selected = -1

    ecran.fill(0)  # besoin d'effacer l'écran sinon c'est moche :p

    while not done:
        for event in rendering_engine.get_event():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                done = True
            if event.type == KEYUP:
                if event.key == K_RETURN:
                    if selected == 10:
                        params.set("music", not params.get("music"))
                    if selected == 11:
                        params.set("play_anims", not params.get("play_anims"))
                    if selected == 12:
                        tmp = params.get("delta_time")
                        tmp.update({"has_default": not tmp["has_default"]})
                        params.set("delta_time", tmp)
                    if selected == 13:
                        print("DEMANDE à FAIRE !")
                if 0 <= selected < 10:
                    debug.println("reconnaitre le setting cliqué ! (donc lsite au lieu de dico) ; puis assigner")
            if event.type == MOUSEBUTTONUP:
                xp, yp = event.pos
                real_y = (yp - PARAMS_Y_START_LISTE) // PARAMS_ESP_Y_LIGNE
                if 0 <= real_y < len(settings_txt_list):
                    selected = real_y
                else:
                    selected = -1

        ecran.blit(fond, (PARAMS_X, PARAMS_Y))
        ecran.blit(titre, ((FEN_large - titre.get_width()) // 2, PARAMS_Y_TITRE))
        for i, texte in enumerate(settings_txt_list):
            ecran.blit(texte, (PARAMS_X_LISTE, PARAMS_Y_START_LISTE + i * PARAMS_ESP_Y_LIGNE))

        rendering_engine.flip()
    params.save()