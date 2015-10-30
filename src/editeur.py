import pickle
import os
import pygame
from glob import glob
from pygame.locals import *
from constantes import *
import trigger_manager


map_path = input("Path vers la map (laissez vide pour garder la valeur par défaut) : ")
if map_path == "": map_path = os.path.join("..", "saves", "map" + EXTENSION)
YTAILLE, XTAILLE = 24, 24
if map_path not in glob(os.path.join("..", "saves", "*." + EXTENSION)):
    YTAILLE = int(input("Taille de la map horizontalement (en cases) : "))  # ecran.get_height() // TILE_SIZE
    XTAILLE = int(input("Taille de la map verticalement (en cases)   : "))  # ecran.get_width() // TILE_SIZE

DEFAUT = '0'
continuer = 1
offset = 0
offset2 = 0
curpos = 0
carte = []
assets = {}
lassets = []

pygame.init()

ecran = pygame.display.set_mode((0, 0), FULLSCREEN)

clock_ = pygame.time.Clock()
clic = 0
layer = 0  # maxi 5 (0 -> ... 4 compris)
fullscreen = True
help_ = True

pygame.font.init()

pygame.key.set_repeat(200, 100)
police = pygame.font.SysFont("comicsansms", 12)

if os.path.exists(map_path):
    with open(map_path, "rb") as file:
        carte = pickle.Unpickler(file).load()
else:
    for i in range(YTAILLE):
        lst = []
        for j in range(XTAILLE):
            lst.append([DEFAUT, DEFAUT, DEFAUT, DEFAUT, DEFAUT])
        carte.append(lst)

for i in glob(os.path.join("..", "assets", "tiles", "*.png")):
    assets[i[16:-4]] = pygame.image.load(i).convert_alpha()
    lassets.append(i[16:-4])


def render(carte, offset, offset2):
    for y in range(len(carte)):
        for x in range(len(carte[y])):
            xpos = x * TILE_SIZE + offset
            ypos = y * TILE_SIZE + offset2
            obj = carte[y][x]
            if len(obj) <= 5:
                for i in obj[::-1]:
                    ecran.blit(assets[i], (xpos, ypos))
            else:
                for i in obj[-2::-1]:
                    ecran.blit(assets[i], (xpos, ypos))


def create_edit_zone():
    xsize = 300
    marge = xsize - 10

    pygame.draw.rect(ecran, (30, 30, 30), (ecran.get_width() - xsize, 0, xsize, ecran.get_height()))

    ecran.blit(police.render("Layer : " + str(layer), 1, (255, 255, 255)), (ecran.get_width() - marge, 10))
    ecran.blit(police.render("Objet courant : " + str(lassets[curpos]) +
                             ", bloquant : " + str('oui' if int(lassets[curpos]) % 2 else 'non'),
                             1, (255, 255, 255)),
               (ecran.get_width() - marge, 30))
    ecran.blit(police.render("X : {}, Y : {}, trigger : {}"
                             .format(str(pygame.mouse.get_pos()[0] // TILE_SIZE - offset // TILE_SIZE),
                                     str(pygame.mouse.get_pos()[1] // TILE_SIZE - offset2 // TILE_SIZE),
                                     str('oui' if len(carte[pygame.mouse.get_pos()[1] // TILE_SIZE - offset2 // TILE_SIZE][pygame.mouse.get_pos()[0] // TILE_SIZE - offset // TILE_SIZE]) == 6 else 'non')),
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

    for i in range(0, 6):
        tmp = (curpos + i) % len(lassets)
        if tmp == curpos:
            ecran.blit(police.render("Courant -> ", 1, (255, 255, 255)), (ecran.get_width() - marge, 310 + i * 42))
        ecran.blit(assets[lassets[tmp]], (ecran.get_width() - marge + 70, 310 + i * 42))


while continuer:
    clock_.tick(30)
    pygame.draw.rect(ecran, (0, 0, 0), (0, 0) + ecran.get_size())

    for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            continuer = 0
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                curpos = curpos + 1 if curpos + 1 < len(lassets) else curpos
            if event.button == 5:
                curpos = curpos - 1 if curpos - 1 >= 0 else curpos
            if event.button == 1:
                clic = 1
                x, y = event.pos
                mx, my = x // TILE_SIZE - offset // TILE_SIZE, y // TILE_SIZE - offset2 // TILE_SIZE
                carte[my][mx][layer] = lassets[curpos]
        if event.type == MOUSEMOTION:
            if clic:
                x, y = event.pos
                mx, my = x // TILE_SIZE - offset // TILE_SIZE, y // TILE_SIZE - offset2 // TILE_SIZE
                carte[my][mx][layer] = lassets[curpos]
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clic = 0
        if event.type == KEYDOWN:
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
            if event.key == K_RETURN:
                fullscreen = not fullscreen
                if fullscreen:
                    ecran = pygame.display.set_mode((0, 0), FULLSCREEN)
                else:
                    ecran = pygame.display.set_mode((0, 0))
            if event.key == K_h:
                help_ = not help_
            if event.key == K_t:
                x, y = pygame.mouse.get_pos()
                mx, my = x // TILE_SIZE - offset // TILE_SIZE, y // TILE_SIZE - offset2 // TILE_SIZE
                carte[my][mx].append([])

                if fullscreen:
                    fullscreen = not fullscreen
                    if fullscreen:
                        ecran = pygame.display.set_mode((0, 0), FULLSCREEN)
                    else:
                        ecran = pygame.display.set_mode((0, 0))

                code_trigger = input("Code du trigger (placé en {}, {}) : ".format(str(mx), str(my)))
                trigger_manager.TriggersManager.add_trigger_to_path(
                    trigger_manager.Trigger(code_trigger, mx, my, -1)
                )

    render(carte, offset, offset2)

    if help_:
        create_edit_zone()

    ecran.blit(assets[lassets[curpos]], pygame.mouse.get_pos())

    pygame.display.flip()

print("Saving map ...")
print("Carte is not None :", carte is not None)
with open(map_path, "wb") as file:
    pickle.Pickler(file).dump(carte)

print("Exited cleanly")
pygame.quit()