import os
import pygame
from pygame.locals import *
from FPS_regulator import IAFPS
from constantes import *


class Game:
    def __init__(self, ecran):
        self.fps_regulator = IAFPS(FPS_base)
        self.continuer = 1
        self.ecran = ecran

    def save(self):
        pass

    def get_events(self, events):
        for event in events:
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
                self.continuer = 0

    def start(self):
        print("Working !")

        self.continuer = 1

        while self.continuer:
            #Evénements
            self.get_events(pygame.event.get())

            #FPS
            self.fps_regulator.actualise()
            dt = self.fps_regulator.get_DeltaTime()

            #Affichage
            pygame.draw.rect(self.ecran, (55, 178, 25), (0, 0) + self.ecran.get_size())

            pygame.display.flip()