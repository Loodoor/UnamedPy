import pickle
import os
import pygame
from glob import glob
from pygame.locals import *


pygame.init()

ecran = pygame.display.set_mode((0, 0))
continuer = 1
map_path = os.path.join("..", "saves", "map.umd")

TILE_SIZE = 32


carte = []
if os.path.exists(map_path):
    with open(map_path, "wb") as file:
        carte = pickle.Unpickler(file).load()
assets = {}
for i in glob(os.path.join("..", "assets", "tiles", "*.png")):
    assets[i[:-4]] = pygame.image.load(i).convert_alpha()


def render(carte):
    for y in range(len(carte)):
        for x in range(len(carte[y])):
            ecran.blit(assets[carte[y][x]], (x * TILE_SIZE, y * TILE_SIZE))


while continuer:
    pygame.time.Clock().tick(30)
    for event in pygame.event.get():
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            continuer = 0
    render(carte)
    pygame.display.flip()

print("Saving map ...")

with open(map_path, "wb") as file:
    pickle.Pickler(file).dump(map_path)

print("Exited cleanly")
pygame.quit()