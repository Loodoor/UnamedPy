# coding=utf-8

import os
import time
import math
import sys
import ree
import random

# besoin absolu !
from pygame.locals import *


class UEnumFactory:
    seed = 0

    def __init__(self, *args):
        self.list_value_numbers = range(len(args) + UEnumFactory.seed)
        self.dict_attrib = dict(zip(args, self.list_value_numbers))
        self.dict_reverse = dict(zip(self.list_value_numbers, args))
        UEnumFactory.seed += 1

    def create(self):
        objet = UEnum()
        objet.dict_reverse = self.dict_reverse
        objet.__dict__.update(self.dict_attrib)
        return objet


class UEnum:
    def __init__(self):
        self.dict_reverse = {}

    def __str__(self):
        return "__dict__ : " + str(self.__dict__) + "\nself.dict_reverse : " + str(self.dict_reverse)

    def __contains__(self, item):
        if item in self.dict_reverse.keys():
            return True
        return False


FEN_large = 640
FEN_haut = 640
FEN_taille = (FEN_large, FEN_haut)

DEBUG_LEVEL = 1
DEBUG_FEN_large = 840
DEBUG_FEN_haut = 640

VERSION = "0.1"

GLOBAL_ERROR = -1

CORE_SETTINGS = UEnumFactory(
    # "nuzlocke"
).create()

"""
controlers disponnibles :
    perso
    adventure
    equipe
    computer
    music
"""

CHEATS_CODES = {
    # "code": {
    #     "controler": "controler sur lequel agir",
    #     "methode": "methode"
    # }
    "0001": {
        "controler": "perso",
        "methode": "change_moving_state"
    },
    "0002": {
        "controler": "renderer",
        "methode": "invert_renderer"
    }
}

"""
-1 : GLOBAL_ERROR
-2 : ZONE_ADV_ERROR
-3 : RENDER_ERROR
-4 : ATK_IMPOSSIBLE
-5 : PC_GET__ERROR
-6 : PC_POP__ERROR
-7 : POK_SEARCH_ERROR
-8 : OBJET_GET_ERROR
-9 : BUILDING_GET_ERROR
-10 : TILE_GET_ERROR
"""

OBJETS_ID = UEnumFactory(
    "AntiPara",
    "AntiBrule",
    "AntiPoison",
    "Attaqueplus",
    "Defenseplus",
    "Vitesseplus",
    "Elixir",
    "ElixirAugmente",
    "SuperElixir",
    "HyperElixir",
    "ElixirMax",
    "PotionSimple",
    "SuperPotion",
    "HyperPotion",
    "MegaPotion",
    "PotionMax",
    "SimpleBall",
    "NormalBall",
    "SuperiorBall",
    "UltraBall"
).create()

ID_STARTER = 0

NOM_POKEDEX = "Dexeur"

INPUT_CHAR = ">"
IMAGE_SHOW_CHAR = ":"
ME_SPEAKING_CHAR = "$"
LOAD_CINEMATIQUE_CHAR = "@"
IF_CHAR = "&"
NOT_CHAR = "!"

MAP_ENTRY_POINT = "1"

FPS_base = 100
MAX_FPS = 1000000

BUFFER_SIZE = 8192

JOY_DEPLACE_SOURIS = 8

UDP_ASK_NEWS = 1
UDP_ASK_MESSAGES = 2
UDP_ASK_CARTE_CHANGES = 3
UDP_ASK_PLAYERS_CHANGES = 4
UDP_ASK_SERV_NAME = 5
UDP_ASK_MYRANG = 6
UDP_MSG_NONE = 7
UDP_NOTHING_NEW = 8
UDP_CARTE_CHANGE = 9
UDP_PLAYERS_CHANGE = 10
UDP_MESSAGES_CHANGE = 11
UDP_SEND_MSG = 12
UDP_SEND_MYPOS = 13
UDP_SEND_DISCONNECT = 14
UDP_CONNECTED = 15
UDP_LISTENNING = 16
UDP_CONNECTION_REFUSED = 17
UDP_ASK_TO_SAVE_LOGS = 18
UDP_ASK_MYWORLD = 19
UDP_ASK_MYMAP = 20

TILE_SIZE = 16
PERSO_SIZE_X = 32
PERSO_SIZE_Y = 37
TILE_EAU = '3'
TILE_RAIN = '9992'
TILE_POKEOBJ = '10'

YTAILLE_carte = 1200
XTAILLE_carte = 1200
BUILDING = 12
BUILDING_GET_ERROR = -9
TILE_GET_ERROR = -10

TILES_RDM_CREATURES = ['6', '68', '170', '198']

LUCK_RDM_CREA = (0, 1000)
LUCK_CREA_APPEAR = 657  # => 65.7% de chance de pas voir de créature donc

DEFAULT_POS_AT_BEGINNING = (FEN_large // 2, FEN_haut // 2)

BULLE_SX = 620
BULLE_SY = 100
POS_BULLE_X = (FEN_large - BULLE_SX) // 2
POS_BULLE_Y = FEN_haut - BULLE_SY - 10

MENU_SPEED_LOADING = 0.25
MENU_SIZE_BAR = 250
MENU_BAR_Y = 275
MENU_BTN_SX = 120
MENU_BTN_SY = 32
MENU_BTN_JOUER_X = FEN_large // 2 - MENU_BTN_SX // 2
MENU_BTN_JOUER_Y = 250
MENU_BTN_RESEAU_X = FEN_large // 2 - MENU_BTN_SX // 2
MENU_BTN_RESEAU_Y = MENU_BTN_JOUER_Y + MENU_BTN_SY + 10
MENU_BTN_PARAMS_X = FEN_large // 2 - MENU_BTN_SX // 2
MENU_BTN_PARAMS_Y = MENU_BTN_RESEAU_Y + MENU_BTN_SY + 10
MENU_TXT_BOX_SX = 280
MENU_TXT_BOX_SY = 28
MENU_TXT_BOX_X = FEN_large // 2 - MENU_TXT_BOX_SX // 2
MENU_TXT_BOX_Y = 180
MENU_X_PLZ_PSEUDO = 200
MENU_Y_PLZ_PSEUDO = 100

PARAMS_X = 20
PARAMS_Y = 20
PARAMS_Y_TITRE = PARAMS_Y + 10
PARAMS_X_LISTE = PARAMS_X + 20
PARAMS_Y_START_LISTE = PARAMS_Y_TITRE + 30
PARAMS_ESP_Y_LIGNE = 25

WORLD_DEFAULT = 2
MAP_DEFAULT = 1

MAX_TIME_CHANGED_MAP = 200

TRIGGER_ERROR = "trigger.error"
TRIGGER_UNDEFINED = "trigger.undefined"
TRIGGER_INFINITE_CALLS = -1

BAR_ESP = 2

ZONE0 = 0
ZONE1 = 1
ZONE2 = 2
ZONE3 = 3
ZONE4 = 4
ZONE5 = 5
ZONE6 = 6
ZONE7 = 7
ZONE8 = 8
ZONE9 = 9
ZONEa = 10
ZONEb = 11
ZONEc = 12
ZONEd = 13
ZONEe = 14
ZONEf = 15

COMB_X = 0
COMB_Y = 0
COMB_SX = FEN_large
COMB_SY = FEN_haut
COMB_X_ADV = COMB_SX // 3 * 2 + COMB_X
COMB_Y_ADV = COMB_Y + 65
COMB_SX_LIFE_BAR = 100
COMB_SY_LIFE_BAR = 20
COMB_SX_XP_BAR = 100
COMB_SY_XP_BAR = 6
COMB_CHECK_SX = 16
COMB_CHECK_SY = 16
COMB_SY_TXT_NAME = 18
COMB_SX_ADV = 150
COMB_SY_ADV = 150
COMB_SX_ATK_FIELD = FEN_large - 80 - COMB_SX_ADV
COMB_SY_ATK_FIELD = 45
COMB_X_ATK = FEN_large - COMB_SX_ATK_FIELD - 10
COMB_X_ME = COMB_X + 40
COMB_Y_ME = COMB_SY // 3 * 2 + COMB_Y - COMB_SY_ATK_FIELD - 10

SAVE_X = 20
SAVE_Y = 250
SAVE_SX = FEN_large - SAVE_X * 2
SAVE_SY = FEN_haut - SAVE_Y * 2
SAVE_X_PERSO_DECALAGE = 70

ZONE_ADV_ERROR = -2
OBJET_GET_ERROR = -8

POL_PETITE_TAILLE = 18
POL_NORMAL_TAILLE = 20
POL_GRANDE_TAILLE = 26
POLICE_PATH = os.path.join("..", "assets", "gui", "pkmnemn.ttf")
POL_ANTIALISING = False

HAUT = 0
BAS = 1
GAUCHE = 2
DROITE = 3
AUCUNE = -1
CHAT = 4
MENU = 5
SCREENSCHOT = 6
NEXT_PAGE = 7
PREVIOUS_PAGE = 8
SHOW_FPS = 9
VALIDATION = 10
MAJ = 13
UP_PAGE = 11
DOWN_PAGE = 12

MAX_CREATURES = 52
MAX_CREATURES_IN_TEAM = 6
MAX_RATIO_CAP = 100
MAX_LEVEL = 300
MAX_PP_PER_ATK = 100
MAX_ITEM = 99

CHAT_SX = 320
CHAT_SY = 100
CHAT_SX_BOX = CHAT_SX
CHAT_SY_BOX = 28
CHAT_X_BOX = FEN_large - CHAT_SX_BOX
CHAT_Y_BOX = FEN_haut - CHAT_SY_BOX
CHAT_X_MESSAGES = FEN_large - CHAT_SX
CHAT_Y_MESSAGES = FEN_haut - CHAT_SY
CHAT_SY_MESSAGE = 16
CHAT_COULEUR_SERVICE = (180, 50, 180)
CHAT_COULEUR_ADMIN = (180, 50, 50)
CHAT_COULEUR_MODO = (50, 180, 50)
CHAT_COULEUR_JOUEUR = (0, 0, 0)

RANG_SERVICE = 128
RANG_ADMIN = 64
RANG_MODO = 32
RANG_JOUEUR = 16
RANG_NUL = 0

RENDER_GAME = 0
RENDER_INVENTAIRE = 1
RENDER_COMBAT = 2
RENDER_BOUTIQUE = 3
RENDER_MENU_IN_GAME = 4
RENDER_CARTE = 5
RENDER_SAVE = 6
RENDER_CREATURES = 7
RENDER_PC = 8
RENDER_POKEDEX = 9
RENDER_CHAT = 10
RENDER_ERROR = -3

FCREA_X = 20
FCREA_Y = 20
FCREA_TITRE_Y = FCREA_Y + 10
FCREA_SIZE_X = FEN_large - 2 * FCREA_X
FCREA_SIZE_Y = FEN_haut - 2 * FCREA_Y
FCREA_MARGE_X = 10
FCREA_MARGE_Y = 10
FCREA_MARGE_Y_RAPPORT_TITRE = 25
FCREA_SIZE_X_CASE = FCREA_SIZE_X // 2
FCREA_SIZE_Y_CASE = (FCREA_SIZE_Y - FCREA_MARGE_Y * MAX_CREATURES_IN_TEAM - 1) // MAX_CREATURES_IN_TEAM
FCREA_MARGE_TXT_X = 12
FCREA_MARGE_TXT_Y = 4
FCREA_MARGE_TXT_Y2 = FCREA_MARGE_TXT_Y + 18
FCREA_BTN_SX = 20
FCREA_BTN_SY = 20
FCREA_NEXT_X = FCREA_SIZE_X - 10
FCREA_NEXT_Y = FCREA_Y + 10 * 2 + FCREA_BTN_SY
FCREA_PREVIOUS_X = FCREA_SIZE_X - 10
FCREA_PREVIOUS_Y = FCREA_Y + 10
FCREA_AUTRE_MGR_SX = 70
FCREA_AUTRE_MGR_SY = FCREA_BTN_SY
FCREA_AUTRE_MGR_X = FCREA_SIZE_X - FCREA_AUTRE_MGR_SX + 10
FCREA_AUTRE_MGR_Y = FCREA_SIZE_Y - 10
FCREA_PASSE_CREA_TO__SX = FCREA_AUTRE_MGR_SX + 10
FCREA_PASSE_CREA_TO__SY = FCREA_BTN_SY
FCREA_PASSE_CREA_TO__X = FCREA_X + 10
FCREA_PASSE_CREA_TO__Y = FCREA_SIZE_Y - 10
FCREA_IMAGE_XY_MARGE = 2
FCREA_IMAGE_SX = FCREA_SIZE_Y_CASE - 2 * FCREA_IMAGE_XY_MARGE  # ne pas faire attention c'est normal,
FCREA_IMAGE_SY = FCREA_IMAGE_SX                                # si on veut avoir une image carrée
FCREA_IMAGE_X = FCREA_SIZE_X_CASE - FCREA_IMAGE_SX - 10
FCREA_IMAGE_Y = FCREA_SIZE_Y_CASE - FCREA_IMAGE_SY
FCREA_SPECS_AFF_X = FCREA_X + FCREA_MARGE_X + FCREA_SIZE_X_CASE + 30
FCREA_SPECS_AFF_Y = FCREA_Y + FCREA_MARGE_Y + FCREA_MARGE_Y_RAPPORT_TITRE

SHOP_X = 10
SHOP_Y = 10
SHOP_SX = FEN_large - 2 * SHOP_X
SHOP_SY = FEN_haut - 2 * SHOP_Y

STATES_MOVE = UEnumFactory("idle", "running", "walking", "riding").create()
PAUSE = 0
ANIM1 = 1
ANIM2 = 2
ANIM3 = 3
RIDE1 = 4
RIDE2 = 5
RIDE3 = 6  # optionnel
ANIM_SPEED_EAU = 0.75
ANIM_SPEED_RAIN = 0.8
ANIM_DEFAULT_SPEED_MSPA = 0.1

PROB_RAIN = 0.3

POCHE_COMMUNS = 0
POCHE_CAPTUREURS = 1
POCHE_MEDICAMENTS = 2
POCHE_OBJETS_RARES = 3
POCHE_CT_CS = 4

MENU_CREATURES = 0
MENU_SAC = 1
MENU_SAUV = 2
MENU_CARTE = 3
MENU_POKEDEX = 4
MENU_QUITTER = 5
MENU_X = 20
MENU_Y = 100
MENU_SIZE_X = FEN_large - 2 * MENU_X
MENU_SIZE_Y = FEN_haut - 2 * MENU_Y
MENU_X_CAT = 10
MENU_Y_CAT = 10
MENU_SIZE_X_CAT = (MENU_SIZE_X - 3 * MENU_X_CAT) // 2
MENU_SIZE_Y_CAT = (MENU_SIZE_Y - 4 * MENU_Y_CAT) // 3
MENU_TXT_CAT_X = MENU_X_CAT + 15
MENU_TXT_CAT_Y = MENU_Y_CAT + 6

DEFAUT_TILE = '0'

EXTENSION = '.umd'

TRIGGER = 5

BASIC_SPEED = 4
DIV_DT_BASIC = 1
DIV_DT_COURSE = 0.7
DIV_DT_VELO = 0.45

T_FEU = 0
T_EAU = 1
T_PLANTE = 2
T_ELEC = 3
T_AIR = 4
T_NORMAL = 5
T_TERRE = 6
T_POISON = 7
T_LUMIERE = 8
T_TENEBRE = 9
MAX_T_NBR = 9
TYPES = [
    T_FEU,
    T_EAU,
    T_PLANTE,
    T_ELEC,
    T_AIR,
    T_NORMAL,
    T_TERRE,
    T_POISON,
    T_LUMIERE,
    T_TENEBRE,
]
TYPES_NUMBER = 10

MAP_RDR_POSX = 0
MAP_RDR_POSY = 0
MAP_RDR_POSX_DESC = MAP_RDR_POSX + 5
MAP_RDR_POSY_DESC = MAP_RDR_POSY + 5
MAP_RDR_MARGE = 10
MAP_RDR_SX = FEN_large
MAP_RDR_SY = FEN_haut
MAP_RDR_CASE_SIZE = 16
MAP_RDR_VIDE = '.'
MAP_RDR_LEGENDE_X = MAP_RDR_POSX + 10
MAP_RDR_LEGENDE_Y = FEN_haut - MAP_RDR_POSY - FEN_haut // 7
MAP_RDR_LEGENDE_MARGEY = MAP_RDR_CASE_SIZE + 6

MAP_FD_NAME_MAP_X = 0
MAP_FD_NAME_MAP_Y = 30

PNJ_TXT_XPOS = 10
PNJ_TXT_YPOS = 10
PNJ_TXT_XS = FEN_large - 2 * PNJ_TXT_XPOS
PNJ_TXT_YS = 100
PNJ_TXT_ALIGN_X = 10
PNJ_TXT_ALIGN_Y = 10
PNJ_TXT_ESP_X = 18
PNJ_TXT_ARRON = 5
PNJ_TXT_X_CLIGNO = PNJ_TXT_XS - 30 + PNJ_TXT_XPOS
PNJ_TXT_Y_CLIGNO = PNJ_TXT_YS - 30 + PNJ_TXT_YPOS

VU = 0
CAPTURE = 1

UPGRADE_RANGE_SPEC = (1, 3)

POK_POSX = 20
POK_POSY = 20
POK_X_SIZE = FEN_large - 2 * POK_POSX
POK_Y_SIZE = FEN_haut - 2 * POK_POSY
POK_ESP_Y_ITEM = 22
POK_X_TITRE = POK_POSX + 10
POK_Y_TITRE = POK_POSY + 10
POK_X_DESC = POK_X_SIZE - 260
POK_Y_DESC = POK_POSY + 10
POK_SX_IMAGE_CREA = 125
POK_SY_IMAGE_CREA = 125
POK_X_IMG_CREA = POK_X_DESC
POK_Y_IMG_CREA = POK_Y_DESC
POK_X_NAME_CREA = POK_POSX + 10
POK_Y_NAME_CREA = POK_Y_TITRE + POK_ESP_Y_ITEM + 10
POK_X_TYPE = POK_POSX + 40
POK_Y_TYPE = POK_Y_TITRE + POK_ESP_Y_ITEM * 2 + 10
POK_SY_TYPE = 32
POK_SX_VIEWT = 81
POK_SY_VIEWT = 23
POK_X_VIEWT = POK_X_SIZE - POK_SX_VIEWT
POK_Y_VIEWT = POK_Y_SIZE - POK_SY_VIEWT + 3
POK_SX_SEL_STADE = 81
POK_SY_SEL_STADE = 23
POK_X_SEL_STADE = POK_POSX + 10
POK_Y_SEL_STADE = POK_Y_SIZE - POK_SY_SEL_STADE + 3
POK_SX_FENSST = 300
POK_SY_FENSST = 100
POK_X_FENSST = FEN_large // 2 - POK_SX_FENSST // 2
POK_Y_FENSST = FEN_haut // 2 - POK_SY_FENSST // 2

POK_SEARCH_ERROR = -7

INVENT_POSX = 20
INVENT_POSY = 20
INVENT_MAX_X_ITEM = 450
INVENT_ESP_ITEM = 20
INVENT_X_SIZE = FEN_large - 2 * INVENT_POSX
INVENT_Y_SIZE = FEN_haut - 2 * INVENT_POSY
INVENT_X_ITEM = INVENT_POSX + (INVENT_X_SIZE // 7) * 4
INVENT_Y_ITEM = 60
INVENT_TXT_AIDE_X = 30
INVENT_TXT_AIDE_Y = INVENT_POSY + INVENT_Y_SIZE // 2
INVENT_IMAGE_X = INVENT_POSX + 20
INVENT_IMAGE_Y = INVENT_POSY + 20
INVENT_IMAGE_SIZE = 200
INVENT_SIZE_BTN_X = 45
INVENT_SIZE_BTN_Y = 20
INVENT_BTN_JETER_X = INVENT_X_SIZE - INVENT_SIZE_BTN_X
INVENT_BTN_JETER_Y = 30
INVENT_BTN_JETERTT_X = INVENT_X_SIZE - INVENT_SIZE_BTN_X
INVENT_BTN_JETERTT_Y = 30 + INVENT_SIZE_BTN_Y + 10
INVENT_BTN_USE_X = INVENT_X_SIZE - INVENT_SIZE_BTN_X
INVENT_BTN_USE_Y = 30 + (INVENT_SIZE_BTN_Y + 10) * 2
INVENT_BTN_PAGES_SY = 20
INVENT_BTN_PAGES_SX = 20
INVENT_BTN_NEXT = INVENT_IMAGE_X + INVENT_IMAGE_SIZE - INVENT_BTN_PAGES_SX
INVENT_BTN_PREVIOUS = 40
INVENT_BTN_PAGES = INVENT_IMAGE_Y + INVENT_POSY + INVENT_IMAGE_SIZE
INVENT_TXT_POCHE_X = INVENT_POSX + (INVENT_BTN_NEXT + INVENT_BTN_PAGES_SX - INVENT_BTN_PREVIOUS) // 2 + INVENT_BTN_PAGES_SX
INVENT_TXT_POCHE_Y = INVENT_BTN_PAGES

tmp = UEnumFactory(
    "normal",
    "paralise",
    "poisone",
    "brule"
)
SPEC_ETATS = tmp.create()
del tmp
SPEC_ETAT_AFFECT_PERCENT = 0.5
SPEC_DGT_BRULURE = lambda niveau: niveau // 2 * 3
SPEC_DGT_POISON = lambda niveau: niveau // 2 * 4
SPEC_LUCK_OF_ATTACK = lambda vit: random.randint(0, 100) + vit >= 50

SPEC_ATK = 'attaque'
SPEC_DEF = 'defense'
SPEC_VIT = 'vitesse'
SPEC_NOM = 'pseudo'
SPEC_ETAT = 'etat'
SPEC_ID = 'unique_id'
SPEC_TYP = 'type'
SPEC_NIV = 'niveau'
SPEC_PVS = 'points de vie'
SPEC_MAX_PVS = 'max points de vie'
SPEC_XP = 'points experience'
SPEC_PPS = 'points de pouvoir'
SPEC_MAX_PPS = 'max points de pouvoir'
SPEC_XP_GAGNE = 25
SPEC_PROBA_SHINEY = 0.003
SPEC_SEUIL_XP_LVL_UP = 10
MAX_VAL_SPEC = 500
MAX_ATK = 4
DEFAULT_PPS = 35
MAX_ESSAIS_BALL = 8
PERCENT_CAPTURE_NECESSAIRE = 0.75

GUI_Y_ESP = 23

CAP_NOM = 'nom'
CAP_PSEUDO = 'pseudo'
CAP_TYPE = 'type'
CAP_NIV = 'niveau'
CAP_SPECS = 'specs'
CAP_PV = 'points de vie'

ATK_NOM = 'nom'
ATK_TYP = 'type'
ATK_DEGATS = 'degats'
ATK_TXT = 'texte'
ATK_COUT = 'cout de l\'attaque'
ATK_STATE = 'etat infligeable'
ATK_IMPOSSIBLE = -4

PC_MAX_CREA = 150
PC_CREA_PER_BOX = 30
PC_NBR_BOX = PC_MAX_CREA // PC_CREA_PER_BOX
PC_GET__ERROR = -5
PC_POP__ERROR = -6

FIRST_BASIC_FOV = FEN_large // TILE_SIZE
FIRST_BASIC_FOV2 = FEN_haut // TILE_SIZE

COLLIDE_ITEM = lambda c: bool(int(c) % 2)
