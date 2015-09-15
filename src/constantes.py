FEN_large = 640
FEN_haut = 640
FEN_taille = (FEN_large, FEN_haut)

FPS_base = -1
MAX_FPS = 1000000

TILE_SIZE = 32
YTAILLE_carte = 1200
XTAILLE_carte = 1200

TILECODE = 0
BATIMENTSIZE = 1

HAUT = 0
BAS = 1
GAUCHE = 2
DROITE = 3
INVENTAIRE = 4
MENU = 5

PAUSE = 0
ANIM1 = 1
ANIM2 = 2

POCHE_COMMUNS = 0
POCHE_CAPTUREURS = 1
POCHE_MEDICAMENTS = 2
POCHE_OBJETS_RARES = 3
POCHE_CT_CS = 4

DEFAUT_TILE = '0'

EXTENSION = '.umd'

BASIC_SPEED = 4
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

SPEC_ATK = 'attaque'
SPEC_DEF = 'defense'
SPEC_VIT = 'vitesse'
SPEC_OBE = 'obeissance'
SPEC_NOM = 'pseudo'
SPEC_CRA = 'creature'
SPEC_TYP = 'type'
SPEC_NIV = 'niveau'
SPEC_PVS = 'points de vie'

BORNES_GAIN_LVLUP = (1, 3)

FIRST_BASIC_FOV = FEN_large // TILE_SIZE + 1
FIRST_BASIC_FOV2 = FEN_haut // TILE_SIZE + 1

COLLIDE_ITEM = lambda c: True if int(c) % 2 else False
COLLIDE = lambda x, y, c, tc: True if COLLIDE_ITEM(c[y][x][tc]) else False