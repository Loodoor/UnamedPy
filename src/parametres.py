# coding=utf-8

import pickle, _pickle
from constantes import *
from pygame.locals import *
from exceptions import ClassNonChargee
import ree
from utils import ureplace_bool_str
import debug
from gui import GUIBulleAsking


class ParametresManager:
    def __init__(self):
        self._default_config = {
            "controls": {
                HAUT: K_UP,
                BAS: K_DOWN,
                GAUCHE: K_LEFT,
                DROITE: K_RIGHT,
                CHAT: K_KP_DIVIDE,
                MENU: K_RSHIFT,
                SCREENSCHOT: K_F5,
                SHOW_FPS: K_BACKSPACE,
                VALIDATION: K_RETURN,
                MAJ: K_LSHIFT
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
        self.path_to_settings = os.path.join("..", "assets", "configuration", "config" + EXTENSION)

    def _pre_load(self):
        if not os.path.exists(self.path_to_settings):
            with open(self.path_to_settings, "wb") as wsettings:
                debug.println("Creating default configuration")
                pickle.Pickler(wsettings).dump(self._default_config)

    def load(self):
        self._pre_load()
        try:
            with open(self.path_to_settings, 'rb') as file:
                debug.println("Loading settings")
                self.params = pickle.Unpickler(file).load()
        except _pickle.UnpicklingError:
            debug.println("Loading settings failed")
            os.remove(self.path_to_settings)
            self._pre_load()

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
        debug.println("Saving settings ...")
        with open(self.path_to_settings, "wb") as wsettings:
            pickle.Pickler(wsettings).dump(self.params)
        debug.println("Saving finished !")


def gui_access(ecran, police):
    def create_textes():
        return [police.render("Contrôles", POL_ANTIALISING, (10, 10, 10))] + [
            police.render("{} : {}".format(const_to_str[cst], ree.get_key_name(controls[cst])),
                          POL_ANTIALISING, (10, 10, 10)) for cst in order
        ] + [
            police.render(
                "Musique : {}".format(
                    ureplace_bool_str(params.get("music"), ['on', 'off'])), POL_ANTIALISING, (10, 10, 10)),
            police.render("Animations : {}".format(
                ureplace_bool_str(params.get("play_anims"), ['on', 'off'])), POL_ANTIALISING, (10, 10, 10)),
            police.render("DeltaTime par défaut : {}".format(
                ureplace_bool_str(params.get("delta_time")["has_default"], ['on', 'off'])), POL_ANTIALISING, (10, 10, 10)),
            police.render("Valeur par défaut (valable uniquement si activé ; en sec) : {}".format(
                params.get("delta_time")["default"]), POL_ANTIALISING, (10, 10, 10))
        ]


    done = False

    params = ParametresManager()
    params.load()

    fond = ree.load_image(os.path.join("..", "assets", "gui", "fd_params.png"))
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
    order = [HAUT, BAS, GAUCHE, DROITE, CHAT, MENU, SCREENSCHOT, SHOW_FPS, VALIDATION]
    controls = params.get("controls")

    settings_txt_list = create_textes()

    selected = -1

    ecran.fill(0)  # besoin d'effacer l'écran sinon c'est moche :p

    while not done:
        for event in ree.get_event():
            if event == QUIT:
                exit(1)
            if event == (KEYDOWN, K_ESCAPE):
                done = True

            if event == (KEYUP, K_RETURN):
                if selected == 10:
                    params.set("music", not params.get("music"))
                if selected == 11:
                    params.set("play_anims", not params.get("play_anims"))
                if selected == 12:
                    tmp = params.get("delta_time")
                    tmp.update({"has_default": not tmp["has_default"]})
                    params.set("delta_time", tmp)
                if selected == 13:
                    debug.println("DEMANDE à FAIRE !")
            if 0 < selected < 10 and event == KEYUP:
                code = event.key
                tmp = params.get("controls")
                tmp.update({order[selected - 1]: code})
                params.set("controls", tmp)
            settings_txt_list = create_textes()

            if event == MOUSEBUTTONUP:
                xp, yp = event.pos
                real_y = (yp - PARAMS_Y_START_LISTE) // PARAMS_ESP_Y_LIGNE
                if 0 <= real_y < len(settings_txt_list):
                    selected = real_y
                else:
                    selected = -1

        ecran.blit(fond, (PARAMS_X, PARAMS_Y))
        ecran.blit(titre, ((FEN_large - titre.get_width()) // 2, PARAMS_Y_TITRE))
        for i, texte in enumerate(settings_txt_list):
            if i == selected and i:
                ree.draw_rect(
                    ecran,
                    (
                        PARAMS_X_LISTE - 2,
                        PARAMS_Y_START_LISTE + i * PARAMS_ESP_Y_LIGNE - 2,
                        texte.get_width() + 4,
                        texte.get_height() + 4
                    ),
                    (180, 50, 50)
                )
            ecran.blit(texte, (PARAMS_X_LISTE, PARAMS_Y_START_LISTE + i * PARAMS_ESP_Y_LIGNE))

        ree.flip()

    params.save()