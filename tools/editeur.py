import pickle
import os
import pygame
from glob import glob
from pygame.locals import *


pygame.init()

ecran = pygame.display.set_mode((1100, 700))

TILE_SIZE = 32
YTAILLE = ecran.get_height() // TILE_SIZE
XTAILLE = ecran.get_width() // TILE_SIZE
DEFAUT = '0'

continuer = 1
offset = 0
offset2 = 0
curpos = 0
carte = []
assets = {}
lassets = []
map_path = os.path.join("..", "saves", "map.umd")

clock = pygame.time.Clock()

pygame.key.set_repeat(200, 100)

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
            for i in obj[::-1]:
                ecran.blit(assets[i], (xpos, ypos))

clock = pygame.time.Clock()
clic = 0
layer = 0  # maxi 5 (0 -> ... 4 compris)

while continuer:
    clock.tick(30)
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

    pygame.display.set_caption("Layer : " + str(layer) + " Objet courant : " + str(lassets[curpos]) +
                               " X : " + str(pygame.mouse.get_pos()[0] // TILE_SIZE - offset // TILE_SIZE) +
                               " Y : " + str(pygame.mouse.get_pos()[1] // TILE_SIZE - offset2 // TILE_SIZE))

    render(carte, offset, offset2)

    ecran.blit(assets[lassets[curpos]], pygame.mouse.get_pos())

    pygame.display.flip()

print("Saving map ...")
print(carte is not None)
with open(map_path, "wb") as file:
    pickle.Pickler(file).dump(carte)

print("Exited cleanly")
pygame.quit()