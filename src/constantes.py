# coding=utf-8

import os


FEN_large = 640
FEN_haut = 640
FEN_taille = (FEN_large, FEN_haut)

GLOBAL_ERROR = -1

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

MAP_ENTRY_POINT = "1"

FPS_base = 100
MAX_FPS = 1000000

BUFFER_SIZE = 4096
TUDP_NONE = "tchat.messages.fetch:Nothing"
TUDP_ASK_MESSAGES = "tchat.messages.fetch"

TILE_SIZE = 32
YTAILLE_carte = 1200
XTAILLE_carte = 1200
BUILDING = 12
BUILDING_GET_ERROR = -9
TILE_GET_ERROR = -10

TILES_RDM_CREATURES = ['6']

LUCK_RDM_CREA = [0, 2]

MENU_SIZE_BAR = 250
MENU_BAR_Y = 275
MENU_BTN_JOUER_SX = 120
MENU_BTN_JOUER_SY = 32
MENU_BTN_JOUER_X = FEN_large // 2 - MENU_BTN_JOUER_SX // 2
MENU_BTN_JOUER_Y = 250

TRIGGER_ERROR = "trigger.error"
TRIGGER_UNDEFINED = "trigger.undefined"
TRIGGER_COMBAT_ZONE = "trigger.combat.lance."  # + ZONE ID
TRIGGER_INFINITE_CALLS = -1

ZONE1 = "zone.1"
ZONE2 = "zone.2"
ZONE3 = "zone.3"
ZONE4 = "zone.4"
ZONE5 = "zone.5"
ZONE6 = "zone.6"
ZONE7 = "zone.7"
ZONE8 = "zone.8"
ZONE9 = "zone.9"
ZONEa = "zone.a"
ZONEb = "zone.b"
ZONEc = "zone.c"
ZONEd = "zone.d"
ZONEe = "zone.e"
ZONEf = "zone.f"
ZONEg = "zone.g"

SAVE_X = 20
SAVE_Y = 250
SAVE_SX = FEN_large - SAVE_X * 2
SAVE_SY = FEN_haut - SAVE_Y * 2
SAVE_X_PERSO_DECALAGE = 70

ZONE_ADV_ERROR = -2
OBJET_GET_ERROR = -8

POL_NORMAL_TAILLE = 10
POL_GRANDE_TAILLE = 16
POL_PETITE_TAILLE = 8
POLICE_PATH = os.path.join("..", "assets", "gui", "freesansbold.ttf")

HAUT = 0
BAS = 1
GAUCHE = 2
DROITE = 3
AUCUNE = -1
INVENTAIRE = 4
MENU = 5
SCREENSCHOT = 6
NEXT_PAGE = 7
PREVIOUS_PAGE = 8
SHOW_FPS = 9
VALIDATION = 10

MAX_CREATURES = 52
MAX_CREATURES_IN_TEAM = 6
MAX_RATIO_CAP = 100
MAX_LEVEL = 1000
MAX_PP_PER_ATK = 100
MAX_ITEM = 99

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
RENDER_ERROR = -3

FCREA_X = 20
FCREA_Y = 20
FCREA_TITRE_Y = FCREA_Y + 10
FCREA_SIZE_X = FEN_large - 2 * FCREA_X
FCREA_SIZE_Y = FEN_haut - 2 * FCREA_Y
FCREA_MARGE_X = 10
FCREA_MARGE_Y = 10
FCREA_SIZE_X_CASE = FCREA_SIZE_X // 2
FCREA_SIZE_Y_CASE = (FCREA_SIZE_Y - FCREA_MARGE_Y * MAX_CREATURES_IN_TEAM - 1) // MAX_CREATURES_IN_TEAM
FCREA_MARGE_TXT_X = 4
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

PAUSE = 0
ANIM1 = 1
ANIM2 = 2

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
MENU_TXT_CAT_X = MENU_X_CAT + 10
MENU_TXT_CAT_Y = MENU_Y_CAT + 10

DEFAUT_TILE = '0'

EXTENSION = '.umd'

TRIGGER = 5

BASIC_SPEED = 8
DIV_DT_BASIC = 1
DIV_DT_VELO = 0.5
DIV_DT_COURSE = 0.8

T_FEU = 0
T_EAU = 1
T_PLANTE = 2
T_ELEC = 3
T_AIR = 4
T_NORMAL = 5
T_TERRE = 6
T_PLASMA = 7
T_LUMIERE = 8
T_TENEBRE = 9
MAX_T_NBR = 9
TYPES_NUMBER = 10

MAP_RDR_POSX = 10
MAP_RDR_POSY = 10
MAP_RDR_SX = FEN_large - 2 * MAP_RDR_POSX
MAP_RDR_SY = FEN_haut - 2 * MAP_RDR_POSY
MAP_RDR_CARTEX = MAP_RDR_POSX + 10
MAP_RDR_CARTEY = MAP_RDR_POSY + 10

PNJ_TXT_XPOS = 10
PNJ_TXT_YPOS = 10
PNJ_TXT_XS = FEN_large - 2 * PNJ_TXT_XPOS
PNJ_TXT_YS = 100
PNJ_TXT_ALIGN_X = 10
PNJ_TXT_ALIGN_Y = 10
PNJ_TXT_ESP_X = 18
PNJ_TXT_ARRON = 5
PNJ_TXT_X_CLIGNO = PNJ_TXT_XS - 10 + PNJ_TXT_XPOS
PNJ_TXT_Y_CLIGNO = PNJ_TXT_YS - 10 + PNJ_TXT_YPOS

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
POK_X_IMG_CREA = POK_POSX + 10
POK_Y_IMG_CREA = POK_POSY + 10
POK_X_NAME_CREA = POK_X_IMG_CREA + 10
POK_Y_NAME_CREA = POK_Y_TITRE + POK_ESP_Y_ITEM + 10
POK_X_TYPE = POK_X_NAME_CREA
POK_Y_TYPE = POK_Y_NAME_CREA
POK_SY_TYPE = POK_ESP_Y_ITEM
POK_SX_VIEWT = 81
POK_SY_VIEWT = 23
POK_X_VIEWT = POK_X_SIZE - POK_SX_VIEWT
POK_Y_VIEWT = POK_Y_SIZE - POK_SY_VIEWT + 3
POK_X_DESC = POK_X_SIZE - 250
POK_Y_DESC = POK_POSY + 10
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
INVENT_BTN_JETERTT_X = INVENT_BTN_JETER_X
INVENT_BTN_JETERTT_Y = 30 + INVENT_SIZE_BTN_Y + 10
INVENT_BTN_PAGES_SY = 20
INVENT_BTN_PAGES_SX = 20
INVENT_BTN_NEXT = INVENT_IMAGE_X + INVENT_IMAGE_SIZE - INVENT_BTN_PAGES_SX
INVENT_BTN_PREVIOUS = 40
INVENT_BTN_PAGES = INVENT_IMAGE_Y + INVENT_POSY + INVENT_IMAGE_SIZE
INVENT_TXT_POCHE_X = INVENT_POSX + (INVENT_BTN_NEXT + INVENT_BTN_PAGES_SX - INVENT_BTN_PREVIOUS) // 2 + INVENT_BTN_PAGES_SX
INVENT_TXT_POCHE_Y = INVENT_BTN_PAGES

SPEC_ATK = 'attaque'
SPEC_DEF = 'defense'
SPEC_VIT = 'vitesse'
SPEC_NOM = 'pseudo'
SPEC_ID = "unique_id"
SPEC_TYP = 'type'
SPEC_NIV = 'niveau'
SPEC_PVS = 'points de vie'
SPEC_MAX_PVS = 'max points de vie'
MAX_VAL_SPEC = 500

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
ATK_PPS = 'points de pouvoir'
ATK_IMPOSSIBLE = -4
ATK_PP = 0
ATK_MAX_PP = 1

PC_MAX_CREA = 150
PC_CREA_PER_BOX = 30
PC_NBR_BOX = PC_MAX_CREA // PC_CREA_PER_BOX
PC_GET__ERROR = -5
PC_POP__ERROR = -6

HAUTES_HERBES = 6

FIRST_BASIC_FOV = FEN_large // TILE_SIZE + 1
FIRST_BASIC_FOV2 = FEN_haut // TILE_SIZE + 1

COLLIDE_ITEM = lambda c: True if int(c) % 2 else False