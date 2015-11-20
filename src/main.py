# coding=utf-8

import os
from exceptions import ErreurRepertoire

if os.path.split(os.getcwd())[1] != "src":
    raise ErreurRepertoire("Le répertoire courant n'est pas correct, le jeu ne peut pas se lancer")
print("Chargement ...")

import game
import pygame
from pygame.locals import *
from constantes import *
import utils
from glob import glob
import random
import time


def get_alea_text(path: str="textes") -> str:
    files = glob(os.path.join("..", "assets", "menu", path, "*.txt"))
    with open(random.choice(files), encoding="utf-8") as text_reader:
        texte = text_reader.read()
    return texte


def main():
    pygame.init()
    pygame.font.init()

    ecran = pygame.display.set_mode((FEN_large, FEN_haut), HWSURFACE)
    pygame.display.set_caption("Unamed")
    police = pygame.font.Font(POLICE_PATH, 16)
    police_annot = pygame.font.Font(POLICE_PATH, 12)
    police_annot.set_italic(True)
    police_title = pygame.font.Font(POLICE_PATH, 20)
    police_title.set_underline(True)
    police_title.set_bold(True)
    title = police_title.render("Unamed", 1, (255, 255, 255))
    help_ = police.render("Appuyez sur 'J' pour lancer le jeu !", 1, (255, 255, 255))
    bienvenue = [
        "Bienvenue à toi, chercheur !",
        "Tu vas entrer sur l'île d'Unamed, prépare toi à une toute nouvelle aventure !"
    ]
    alea_texte = police_annot.render(get_alea_text(), 1, (255, 255, 255))
    fond = pygame.image.load(os.path.join("..", "assets", "menu", "fond.png")).convert_alpha()
    load_texts = glob(os.path.join("..", "assets", "menu", "chargement", "*.txt"))
    max_len = int(MENU_SIZE_BAR // len(load_texts))
    loading_text = police.render(open(load_texts.pop(random.randint(0, len(load_texts) - 1)),
                                      encoding='utf-8').read(),
                                 1, (255, 255, 255))

    print("Appuyez sur 'J' pour lancer le jeu")

    continuer = 1
    has_already_played = utils.uhas_already_played()
    chargement = False
    avancement = 0

    temp = utils.ULoader()
    temp.load()
    del temp

    jeu = game.Game(ecran)

    while continuer:
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
                continuer = 0
            if event.type == KEYDOWN:
                if event.key == K_j:
                    chargement = True
                if event.key == K_SPACE:
                    alea_texte = police_annot.render(get_alea_text(), 1, (255, 255, 255))

        #Affichage
        ecran.blit(fond, (0, 0))
        ecran.blit(title, (FEN_large // 2 - title.get_width() // 2, 20))

        if not has_already_played:
            for txt in bienvenue:
                tmp = police.render(txt, 1, (255, 255, 255))
                ecran.blit(tmp, (FEN_large // 2 - tmp.get_width() // 2, 100))
        else:
            ecran.blit(alea_texte, (FEN_large // 2 - alea_texte.get_width() // 2, 75))

        if chargement:
            pygame.draw.rect(ecran, (150, 150, 150), (FEN_large // 2 - MENU_SIZE_BAR // 2, MENU_BAR_Y, MENU_SIZE_BAR, 22))
            pygame.draw.rect(ecran, (30, 160, 30), (FEN_large // 2 - MENU_SIZE_BAR // 2 + 2, MENU_BAR_Y + 2, avancement, 18))
            ecran.blit(loading_text, (FEN_large // 2 - loading_text.get_width() // 2, MENU_SIZE_BAR))
            avancement += 0.125
            if not int(avancement) % max_len and len(load_texts) != 0 and float(int(avancement)) == avancement:
                if len(load_texts) - 1 > 0:
                    loading_text = police.render(open(load_texts.pop(random.randint(0, len(load_texts) - 1)),
                                                      encoding='utf-8').read(),
                                                 1, (255, 255, 255))
                else:
                    loading_text = police.render(open(load_texts.pop(0), encoding='utf-8').read(),
                                                 1, (255, 255, 255))
            if avancement >= 246 and chargement:
                chargement = False
                avancement = 0
                jeu.start()

        ecran.blit(help_, (FEN_large // 2 - help_.get_width() // 2, FEN_haut - 10 - help_.get_height()))

        pygame.display.flip()

    pygame.quit()

    print("Le programme s'est terminé proprement")

if __name__ == '__main__':
    main()