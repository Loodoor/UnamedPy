# coding=utf-8

import pygame
import pickle
from glob import glob
from constantes import *
import trigger_manager
from utils import unothing, udel_same_occurence
from animator import BaseMultipleSpritesAnimator, FluidesAnimator


print("Chemin vers le dossier des cartes : {}".format(os.path.join("..", "assets", "map")))

map_num = input("Numéro vers la map (laissez vide pour garder la valeur par défaut) : ")
map_path = os.path.join("..", "assets", "map", "map" + map_num + EXTENSION)
if map_num == "":
    map_path = os.path.join("..", "assets", "map", "map0" + EXTENSION)
    print("Chargement de la map par défaut")
YTAILLE, XTAILLE, zid = 24, 24, 0
if not os.path.exists(map_path):
    XTAILLE = int(input("Taille de la map horizontalement (en cases) : "))  # ecran.get_height() // TILE_SIZE
    YTAILLE = int(input("Taille de la map verticalement (en cases)   : "))  # ecran.get_width() // TILE_SIZE
    zid = int(input("ZID de la carte : "))

DEFAUT = '0'
continuer = 1
offset = 0
offset2 = 0
curpos = 0
carte = []
assets = {}
objets = {}
buildings = {}
pnj = []
lassets = []
spawns = {}
callback_end_rendering = []

TILE_SIZE += 2

pygame.init()

ecran = pygame.display.set_mode((0, 0))

clock_ = pygame.time.Clock()
clic = 0
layer = 0  # maxi 5 (0 -> ... 4 compris)
fullscreen = False
help_ = True

pygame.font.init()

pygame.key.set_repeat(200, 100)
police = pygame.font.SysFont("comicsansms", 12)

if os.path.exists(map_path):
    with open(map_path, "rb") as file:
        tmp = pickle.Unpickler(file).load()
        try:
            carte, objets, buildings, zid, pnj, spawns = tmp
        except TypeError:
            carte = tmp.carte
            objets = tmp.objets
            buildings = tmp.buildings
            zid = tmp.zid
            pnj = tmp.pnjs
            spawns = tmp.spawns
else:
    for i in range(YTAILLE):
        lst = []
        for j in range(XTAILLE):
            lst.append([DEFAUT, DEFAUT, DEFAUT, DEFAUT, DEFAUT])
        carte.append(lst)

for i in glob(os.path.join("..", "assets", "tiles", "*")):
    # chargement automatique des tiles, leur nom déterminent si elles sont bloquantes ou non
    # chargement d'une tile simple
    if os.path.isfile(i):
        assets[os.path.split(i)[1][:-4]] = pygame.image.load(i).convert_alpha()
        lassets.append(os.path.split(i)[1][:-4])
    # chargement d'une animation
    elif os.path.isdir(i):
        assets[i.split(os.sep)[-1]] = BaseMultipleSpritesAnimator(i)
        lassets.append(i.split(os.sep)[-1])
lassets = [str(i) for i in sorted([int(c) for c in lassets])]
water_animator = FluidesAnimator(assets[TILE_EAU], ANIM_SPEED_EAU)
water_animator.load()


def _draw_tile_at(at_x: int, at_y: int, tile: str, callback_end_rendering: list):
    if tile == TILE_EAU:
        ecran.blit(water_animator.get_anim(), (at_x, at_y))
        if tile not in callback_end_rendering:
            callback_end_rendering.append(tile)
    else:
        if isinstance(assets[tile], pygame.Surface):
            ecran.blit(assets[tile], (at_x, at_y))
        elif isinstance(assets[tile], BaseMultipleSpritesAnimator):
            ecran.blit(assets[tile].get_anim(), (at_x, at_y))
            if tile not in callback_end_rendering:
                callback_end_rendering.append(tile)


def _update_anims(callback_end_rendering: list):
    for anim in callback_end_rendering:
        if anim != TILE_EAU:
            assets[anim].next()
        else:
            water_animator.next()


def render(carte, offset, offset2, callback_end_rendering=[]):
    for y in range(len(carte)):
        for x in range(len(carte[y])):
            xpos = x * TILE_SIZE + offset
            ypos = y * TILE_SIZE + offset2
            obj = carte[y][x]
            if len(obj) <= 5:
                for tile in udel_same_occurence(*obj[::-1]):
                    _draw_tile_at(xpos, ypos, tile, callback_end_rendering)
            else:
                for tile in udel_same_occurence(*obj[-2::-1]):
                    _draw_tile_at(xpos, ypos, tile, callback_end_rendering)
            if (x, y) in buildings.keys():
                ecran.blit(police.render(">{}".format(buildings[x, y]), 1, (0, 0, 0)), (xpos, ypos))
            if (x, y) in spawns.keys():
                ecran.blit(police.render("-{}".format(spawns[x, y]), 1, (0, 0, 0)), (xpos, ypos))

    _update_anims(callback_end_rendering)
    callback_end_rendering = []


def create_edit_zone():
    xsize = 320
    marge = xsize - 10

    if 0 <= pygame.mouse.get_pos()[1] // TILE_SIZE - offset2 // TILE_SIZE < len(carte) and \
            0 <= pygame.mouse.get_pos()[0] // TILE_SIZE - offset // TILE_SIZE < len(carte[0]):
        y = pygame.mouse.get_pos()[1] // TILE_SIZE - offset2 // TILE_SIZE
        x = pygame.mouse.get_pos()[0] // TILE_SIZE - offset // TILE_SIZE
        if 0 <= x < len(carte[0]) and 0 <= y < len(carte):
            t = carte[y][x]
        else:
            t = []
    else:
        t = []

    pygame.draw.rect(ecran, (30, 30, 30), (ecran.get_width() - xsize, 0, xsize, ecran.get_height()))

    ecran.blit(police.render("Layer : " + str(layer), 1, (255, 255, 255)), (ecran.get_width() - marge, 10))
    ecran.blit(police.render("Objet courant : " + str(lassets[curpos]) +
                             ", bloquant : " + str('oui' if int(lassets[curpos]) % 2 else 'non'),
                             1, (255, 255, 255)),
               (ecran.get_width() - marge, 30))
    ecran.blit(police.render("X : {}, Y : {}, trigger : {}"
                             .format(str(pygame.mouse.get_pos()[0] // TILE_SIZE - offset // TILE_SIZE),
                                     str(pygame.mouse.get_pos()[1] // TILE_SIZE - offset2 // TILE_SIZE),
                                     str('oui' if len(t) == 6 else 'non')),
                             1, (255, 255, 255)),
               (ecran.get_width() - marge, 50))
    ecran.blit(police.render("Taille de la carte : {}|{}"
                             .format(str(len(carte[0])), str(len(carte))),
                             1, (255, 255, 255)),
               (ecran.get_width() - marge, 70))
    ecran.blit(police.render("Controles :", 1, (255, 255, 255)), (ecran.get_width() - marge, 110))
    ecran.blit(police.render("+|- : changement de layer", 1, (255, 255, 255)), (ecran.get_width() - marge, 130))
    ecran.blit(police.render("HAUT|BAS|GAUCHE|DROITE : déplacement", 1, (255, 255, 255)),
               (ecran.get_width() - marge, 150))
    ecran.blit(police.render("    de la carte", 1, (255, 255, 255)), (ecran.get_width() - marge, 170))
    ecran.blit(police.render("ENTREE : passage en fenêtré | plein écran", 1, (255, 255, 255)),
               (ecran.get_width() - marge, 190))
    ecran.blit(police.render("Clic gauche : poser un bloc", 1, (255, 255, 255)), (ecran.get_width() - marge, 210))
    ecran.blit(police.render("Molette de la souris : changement d'objet", 1, (255, 255, 255)),
               (ecran.get_width() - marge, 230))
    ecran.blit(police.render("H : affiche cette aide ou non", 1, (255, 255, 255)), (ecran.get_width() - marge, 250))
    ecran.blit(police.render("T : ajoute un trigger (vide) sur la case pointée", 1, (255, 255, 255)),
                            (ecran.get_width() - marge, 270))
    ecran.blit(police.render("B : ajoute un lien vers un bâtiment sur la case pointée", 1, (255, 255, 255)),
                            (ecran.get_width() - marge, 310))
    ecran.blit(police.render("D : détruit un lien vers un bâtiment sur la case pointée", 1, (255, 255, 255)),
                            (ecran.get_width() - marge, 330))
    ecran.blit(police.render("G : agrandi la carte en X ou Y d'un nombre choisi", 1, (255, 255, 255)),
                            (ecran.get_width() - marge, 370))
    ecran.blit(police.render("P : diminue la carte en X ou Y d'un nombre choisi", 1, (255, 255, 255)),
               (ecran.get_width() - marge, 390))
    ecran.blit(police.render("S : sauvegarde la map", 1, (255, 255, 255)),
               (ecran.get_width() - marge, 430))
    ecran.blit(police.render("N : ajout d'un point de spawn", 1, (255, 255, 255)),
               (ecran.get_width() - marge, 470))
    ecran.blit(police.render("R : rempli un ensemble de cases avec celle choisie", 1, (255, 255, 255)),
               (ecran.get_width() - marge, 500))


def draw_tiles_tool_bar():
    y = 8
    pygame.draw.rect(ecran, (128, 128, 128),
                     ((ecran.get_width() - 41 * (TILE_SIZE + 2)) // 2, y - 4, (TILE_SIZE + 2) * 40, TILE_SIZE + 8))
    for i in range(0, 18):
        tmp = (curpos + i - 10) % len(lassets)
        x = (ecran.get_width() - 20 * (TILE_SIZE + 2)) // 2 + (TILE_SIZE + 2) * (i - 10)
        if tmp == curpos:
            pygame.draw.rect(ecran, (50, 50, 180), (x - 2 + (TILE_SIZE + 2) * i, y - 2, TILE_SIZE + 4, TILE_SIZE + 4))
        if not isinstance(assets[lassets[tmp]], BaseMultipleSpritesAnimator):
            ecran.blit(assets[lassets[tmp]], (x + (TILE_SIZE + 2) * i, y))
        else:
            ecran.blit(assets[lassets[tmp]].get_anim(), (x + (TILE_SIZE + 2) * i, y))


def fill_map_with_case(start, new, layer):
    for y, line in enumerate(carte):
        for x, case in enumerate(line):
            if case[layer] == start:
                carte[y][x][layer] = new


while continuer:
    clock_.tick(30)
    pygame.draw.rect(ecran, (0, 0, 0), (0, 0) + ecran.get_size())

    for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            continuer = 0
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 5:
                curpos = curpos + 1 if curpos + 1 < len(lassets) else 0
            if event.button == 4:
                curpos = curpos - 1 if curpos - 1 >= 0 else len(assets) - 1
            if event.button == 1:
                clic = 1
                x, y = event.pos
                mx, my = x // TILE_SIZE - offset // TILE_SIZE, y // TILE_SIZE - offset2 // TILE_SIZE
                if lassets[curpos] == TILE_POKEOBJ:
                    print('Ajouter un objet')
                if 0 <= mx < len(carte[0]) and 0 <= my < len(carte):
                    carte[my][mx][layer] = lassets[curpos]
        if event.type == MOUSEMOTION:
            if clic:
                x, y = event.pos
                mx, my = x // TILE_SIZE - offset // TILE_SIZE, y // TILE_SIZE - offset2 // TILE_SIZE
                if 0 <= mx < len(carte[0]) and 0 <= my < len(carte):
                    carte[my][mx][layer] = lassets[curpos]
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clic = 0
        if event.type == KEYDOWN:
            if event.key == K_0 or event.key == K_KP0:
                x, y = pygame.mouse.get_pos()
                mx, my = x // TILE_SIZE - offset // TILE_SIZE, y // TILE_SIZE - offset2 // TILE_SIZE
                if 0 <= mx < len(carte[0]) and 0 <= my < len(carte):
                    obj = carte[my][mx][layer]
                    curpos = lassets.index(obj)
            if event.key == K_RIGHT:
                offset -= TILE_SIZE
            if event.key == K_LEFT:
                offset += TILE_SIZE
            if event.key == K_UP:
                offset2 += TILE_SIZE
            if event.key == K_DOWN:
                offset2 -= TILE_SIZE
            if event.key == K_PLUS or event.key == K_KP_PLUS:
                layer = layer + 1 if layer < 4 else 4
            if event.key == K_MINUS or event.key == K_KP_MINUS:
                layer = layer - 1 if layer > 0 else 0
            if event.key == K_r:
                x, y = pygame.mouse.get_pos()
                mx, my = x // TILE_SIZE - offset // TILE_SIZE, y // TILE_SIZE - offset2 // TILE_SIZE
                if 0 <= mx < len(carte[0]) and 0 <= my < len(carte):
                    print("filling")
                    fill_map_with_case(carte[my][mx][0], lassets[curpos], layer)
            if event.key == K_n:
                x, y = pygame.mouse.get_pos()
                mx, my = x // TILE_SIZE - offset // TILE_SIZE, y // TILE_SIZE - offset2 // TILE_SIZE
                print("Ajout d'un point de spawn")
                if fullscreen:
                    fullscreen = not fullscreen
                    if fullscreen:
                        ecran = pygame.display.set_mode((0, 0), FULLSCREEN)
                    else:
                        ecran = pygame.display.set_mode((0, 0))
                if input("Etes vous sûr [O/N] ? ").lower() == 'o':
                    map_id = input("Map id du spawn > ")
                    spawns[mx, my] = map_id
            if event.key == K_g:
                if fullscreen:
                    fullscreen = not fullscreen
                    if fullscreen:
                        ecran = pygame.display.set_mode((0, 0), FULLSCREEN)
                    else:
                        ecran = pygame.display.set_mode((0, 0))
                print("Agrandissement de la carte")
                if input("Etes vous sûr [O/N] ? ").lower() == 'o':
                    cote = input("Quel coté agrandir [gauche/droite/haut/bas] ? ").lower()
                    while cote not in ['gauche', 'droite', 'haut', 'bas']:
                        cote = input("Quel coté agrandir [gauche/droite/haut/bas] ? ").lower()
                    nombre = input("De combien de cases ? ")
                    while not nombre.isdigit():
                        nombre = input("De combien de cases ? ")
                    nombre = int(nombre)
                    if cote == "gauche":
                        for _ in range(nombre):
                            for y in range(len(carte)):
                                carte[y].insert(0, [DEFAUT, DEFAUT, DEFAUT, DEFAUT, DEFAUT])
                    if cote == "droite":
                        for _ in range(nombre):
                            for y in range(len(carte)):
                                carte[y].append([DEFAUT, DEFAUT, DEFAUT, DEFAUT, DEFAUT])
                    if cote == "haut":
                        for _ in range(nombre):
                            carte.insert(0, [DEFAUT, DEFAUT, DEFAUT, DEFAUT, DEFAUT])
                    if cote == "bas":
                        for _ in range(nombre):
                            t = []
                            for x in range(len(carte[0])):
                                t.append([DEFAUT, DEFAUT, DEFAUT, DEFAUT, DEFAUT])
                            carte.append(t)
            if event.key == K_p:
                if fullscreen:
                    fullscreen = not fullscreen
                    if fullscreen:
                        ecran = pygame.display.set_mode((0, 0), FULLSCREEN)
                    else:
                        ecran = pygame.display.set_mode((0, 0))
                print("Rétrécissement de la carte")
                if input("Etes vous sûr [O/N] ? ").lower() == 'o':
                    cote = input("Quel coté rétrécir [gauche/droite/haut/bas] ? ").lower()
                    while cote not in ['gauche', 'droite', 'haut', 'bas']:
                        cote = input("Quel coté rétrécir [gauche/droite/haut/bas] ? ").lower()
                    nombre = input("De combien de cases ? ")
                    while not nombre.isdigit():
                        nombre = input("De combien de cases ? ")
                    nombre = int(nombre)
                    if cote == "gauche":
                        for _ in range(nombre):
                            for y in range(len(carte)):
                                carte[y].pop(0)
                    if cote == "droite":
                        for _ in range(nombre):
                            for y in range(len(carte)):
                                carte[y].pop()
                    if cote == "haut":
                        for _ in range(nombre):
                            carte.pop(0)
                    if cote == "bas":
                        for _ in range(nombre):
                            carte.pop()
            if event.key == K_RETURN:
                fullscreen = not fullscreen
                if fullscreen:
                    ecran = pygame.display.set_mode((0, 0), FULLSCREEN)
                else:
                    ecran = pygame.display.set_mode((0, 0))
            if event.key == K_h:
                help_ = not help_
            if event.key == K_s:
                print("Saving map ...")
                print("Carte is not None :", carte is not None)
                with open(map_path, "wb") as file:
                    pickle.Pickler(file).dump([carte, objets, buildings, zid, pnj, spawns])
            if event.key == K_b:
                x, y = pygame.mouse.get_pos()
                mx, my = x // TILE_SIZE - offset // TILE_SIZE, y // TILE_SIZE - offset2 // TILE_SIZE

                if fullscreen:
                    fullscreen = not fullscreen
                    if fullscreen:
                        ecran = pygame.display.set_mode((0, 0), FULLSCREEN)
                    else:
                        ecran = pygame.display.set_mode((0, 0))

                id_map = input("Id de la map à charger (la map d'id 1 est située ici : {})\n> ".format(os.path.join("..", "saves", "map", "map1" + EXTENSION)))
                buildings[mx, my] = id_map
            if event.key == K_d:
                x, y = pygame.mouse.get_pos()
                mx, my = x // TILE_SIZE - offset // TILE_SIZE, y // TILE_SIZE - offset2 // TILE_SIZE
                del buildings[mx, my]
            if event.key == K_t:
                x, y = pygame.mouse.get_pos()
                mx, my = x // TILE_SIZE - offset // TILE_SIZE, y // TILE_SIZE - offset2 // TILE_SIZE

                if fullscreen:
                    fullscreen = not fullscreen
                    if fullscreen:
                        ecran = pygame.display.set_mode((0, 0), FULLSCREEN)
                    else:
                        ecran = pygame.display.set_mode((0, 0))

                id_ = input("ID (str) du trigger à poser : ")
                calls = int(input("Nombre d'appels : "))

                carte[my][mx].append(id_)

                trigger_manager.TriggersManager.add_trigger_to_path(
                    trigger_manager.Trigger(id_, mx, my, calls, unothing, id_, map_path)
                )

    render(carte, offset, offset2)

    if help_:
        create_edit_zone()
    draw_tiles_tool_bar()

    mouse_pos = pygame.mouse.get_pos()

    if not isinstance(assets[lassets[curpos]], BaseMultipleSpritesAnimator):
        ecran.blit(assets[lassets[curpos]], (mouse_pos[0] + 10, mouse_pos[1] + 10))
    else:
        ecran.blit(assets[lassets[curpos]].get_anim(), (mouse_pos[0] + 10, mouse_pos[1] + 10))
    pygame.draw.rect(ecran, (128, 128, 128), (mouse_pos[0] + 15 + TILE_SIZE, mouse_pos[1] + 15 + TILE_SIZE, 70, 20))
    x, y = pygame.mouse.get_pos()
    x //= TILE_SIZE
    y //= TILE_SIZE
    x -= offset // TILE_SIZE
    y -= offset2 // TILE_SIZE
    obj = 1
    if 0 <= x < len(carte[0]) and 0 <= y < len(carte):
        obj = carte[y][x][0]
    ecran.blit(police.render("Bloquant" if int(obj) % 2 else 'Non bloquant', 1, (255, 255, 255)),
               (mouse_pos[0] + 17 + TILE_SIZE, mouse_pos[1] + 17 + TILE_SIZE))

    pygame.display.flip()

print("Saving map ...")
print("Carte is not None :", carte is not None)
with open(map_path, "wb") as file:
    pickle.Pickler(file).dump([carte, objets, buildings, zid, pnj, spawns])

print("Exited cleanly")
pygame.quit()