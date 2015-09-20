FEN_large = 640
FEN_haut = 640
FEN_taille = (FEN_large, FEN_haut)

FPS_base = -1
MAX_FPS = 1000000

TILE_SIZE = 32
YTAILLE_carte = 1200
XTAILLE_carte = 1200

POL_NORMAL_TAILLE = 12
POL_GRANDE_TAILLE = 18
POL_PETITE_TAILLE = 9

TILECODE = 0
BATIMENTSIZE = 1

HAUT = 0
BAS = 1
GAUCHE = 2
DROITE = 3
INVENTAIRE = 4
MENU = 5
SCREENSCHOT = 6
NEXT_PAGE = 7
PREVIOUS_PAGE = 8

RENDER_GAME = 0
RENDER_INVENTAIRE = 1
RENDER_COMBAT = 2
RENDER_BOUTIQUE = 3
RENDER_MENU_IN_GAME = 4
RENDER_CARTE = 5
RENDER_SAVE = 6
RENDER_CREATURES = 7

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
MENU_QUITTER = 4
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

BASIC_SPEED = 8
DIV_DT_BASIC = 1
DIV_DT_VELO = 0.5

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

VU = 0
CAPTURE = 1

MAX_CREATURES = 52
MAX_RATIO_CAP = 100
MAX_LEVEL = 1000
MAX_PP_PER_ATK = 100
MAX_ITEM = 99

UPGRADE_RANGE_SPEC = (1, 3)

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
INVENT_SIZE_BTN_X = 30
INVENT_SIZE_BTN_Y = 20
INVENT_BTN_JETER_X = INVENT_X_SIZE - INVENT_SIZE_BTN_X - 10
INVENT_BTN_JETER_Y = 30
INVENT_BTN_JETERTT_X = INVENT_BTN_JETER_X
INVENT_BTN_JETERTT_Y = 30 + INVENT_SIZE_BTN_X + 10
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
SPEC_CREA = 'creature'
SPEC_TYP = 'type'
SPEC_NIV = 'niveau'
SPEC_PVS = 'points de vie'
MAX_VAL_SPEC = 1000

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
ATK_IMPOSSIBLE = -1
ATK_PP = 0
ATK_MAX_PP = 1

HAUTES_HERBES = 6

FIRST_BASIC_FOV = FEN_large // TILE_SIZE + 1
FIRST_BASIC_FOV2 = FEN_haut // TILE_SIZE + 1

COLLIDE_ITEM = lambda c: True if int(c) % 2 else False
COLLIDE = lambda x, y, c, tc: True if COLLIDE_ITEM(c[y][x][tc]) else False