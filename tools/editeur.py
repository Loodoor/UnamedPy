import pickle
import os
import pygame
from glob import glob
from pygame.locals import *


pygame.init()

TILE_SIZE = 32
YTAILLE = 1200
XTAILLE = 1200
TILECODE = 0
BATISIZE = 1
DEFAUT = '0'

ecran = pygame.display.set_mode((1100, 700))
continuer = 1
offset = 0
offset2 = 0
curpos = 0
scale = TILE_SIZE
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
            lst.append(DEFAUT)
        carte.append(lst)

for i in glob(os.path.join("..", "assets", "tiles", "*.png")):
    assets[i[16:-4]] = pygame.image.load(i).convert_alpha()
    lassets.append(i[16:-4])


def render(carte, offset, offset2, scale):
    for y in range(len(carte)):
        for x in range(len(carte[y])):
            xpos = x * scale + offset
            ypos = y * scale + offset2
            if 0 <= xpos <= ecran.get_size()[0] and 0 <= ypos <= ecran.get_size()[1]:
                img = assets[carte[y][x][TILECODE]]
                img = pygame.transform.scale(img, (scale, scale))
                ecran.blit(img, (xpos, ypos))


while continuer:
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
                x, y = event.pos
                mx, my = x // scale - offset // scale, y // scale - offset2 // scale
                carte[my][mx] = [lassets[curpos], assets[lassets[curpos]].get_size()]
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
                scale += 1
            if event.key == K_MINUS or event.key == K_KP_MINUS:
                scale = scale - 1 if scale - 1 >= 1 else scale

    pygame.display.set_caption("Scale : " + str(scale) + " Objet courant : " + str(lassets[curpos]) +
                               " X : " + str(pygame.mouse.get_pos()[0] // scale - offset // scale) +
                               " Y : " + str(pygame.mouse.get_pos()[1] // scale - offset2 // scale))

    render(carte, offset, offset2, scale)

    ecran.blit(assets[lassets[curpos]], pygame.mouse.get_pos())

    pygame.display.flip()

print("Saving map ...")
print(carte is not None)
with open(map_path, "wb") as file:
    pickle.Pickler(file).dump(carte)

print("Exited cleanly")
pygame.quit()