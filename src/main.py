# coding=utf-8

import os
from exceptions import ErreurRepertoire

if os.path.split(os.getcwd())[1] != "src":
    raise ErreurRepertoire("Le répertoire courant n'est pas correct, le jeu ne peut pas se lancer")
print("Chargement ...")

import pygame
import random
import socket
from glob import glob
from pygame.locals import *

import game
import utils
from ecran import MyScreen
from constantes import *
from textentry import TextBox
from aventure_manager import Adventure


def get_alea_text(path: str="textes") -> str:
    files = glob(os.path.join("..", "assets", "menu", path, "*.txt"))
    with open(random.choice(files), encoding="utf-8") as text_reader:
        texte = text_reader.read()
    return texte


def main():
    print("Initialisation de Pygame ...", pygame.init())
    print("Initialisation de Pygame.Font ...", pygame.font.init())

    ecran = MyScreen(pygame.display.set_mode((FEN_large, FEN_haut), HWSURFACE))
    ecran.set_bw(True)
    pygame.display.set_caption("Unamed - v" + VERSION)
    police = pygame.font.Font(POLICE_PATH, 16)
    police_jouer = pygame.font.Font(POLICE_PATH, 20)
    police_annot = pygame.font.Font(POLICE_PATH, 12)
    police_annot.set_italic(True)
    police_title = pygame.font.Font(POLICE_PATH, 20)
    police_title.set_underline(True)
    police_title.set_bold(True)
    title = police_title.render("Unamed", 1, (255, 255, 255))
    jouer = police_jouer.render("Jouer !", 1, (255, 255, 255))
    reseau = police_jouer.render("Réseau", 1, (255, 255, 255))
    bienvenue = [
        "Bienvenue à toi, chercheur !",
        "Tu vas entrer sur l'île d'Unamed, prépare toi à une toute nouvelle aventure !"
    ]
    adventure = Adventure(ecran, police)
    adventure.load()
    alea_texte = police_annot.render(get_alea_text(), 1, (255, 255, 255))
    fond = pygame.image.load(os.path.join("..", "assets", "menu", "fond.png")).convert_alpha()
    load_texts = glob(os.path.join("..", "assets", "menu", "chargement", "*.txt"))
    max_len = int(MENU_SIZE_BAR // len(load_texts))
    loading_text = police.render(open(load_texts.pop(random.randint(0, len(load_texts) - 1)),
                                      encoding='utf-8').read(),
                                 1, (255, 255, 255))

    print("Appuyez sur 'J' pour lancer le jeu")

    continuer = 1
    has_already_played = adventure.has_already_played()
    chargement = False
    en_reseau = False
    avancement = 0

    print("Aucune partie trouvée" if not has_already_played else "Une partie a bien été trouvée")

    while continuer:
        for event in pygame.event.get():
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
                continuer = 0
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    alea_texte = police_annot.render(get_alea_text(), 1, (255, 255, 255))
                if event.key == K_SPACE and chargement:
                    avancement = 246  # pour accélérer le chargement
            if event.type == MOUSEBUTTONUP:
                xp, yp = event.pos
                if MENU_BTN_JOUER_X <= xp <= MENU_BTN_JOUER_X + MENU_BTN_JOUER_SX and \
                                        MENU_BTN_JOUER_Y <= yp <= MENU_BTN_JOUER_Y + MENU_BTN_JOUER_SY:
                    chargement = True
                if MENU_BTN_RESEAU_X <= xp <= MENU_BTN_RESEAU_X + MENU_BTN_RESEAU_SX and \
                                        MENU_BTN_RESEAU_Y <= yp <= MENU_BTN_RESEAU_Y + MENU_BTN_RESEAU_SY:
                    chargement = True
                    en_reseau = True

        #Affichage
        ecran.blit(fond, (0, 0))
        ecran.blit(title, (FEN_large // 2 - title.get_width() // 2, 20))

        if not has_already_played:
            i = 0
            for txt in bienvenue:
                tmp = police.render(txt, 1, (255, 255, 255))
                ecran.blit(tmp, (FEN_large // 2 - tmp.get_width() // 2, 100 + 20 * i))
                i += 1
        else:
            ecran.blit(alea_texte, (FEN_large // 2 - alea_texte.get_width() // 2, 75))

        if chargement:
            pygame.draw.rect(ecran, (150, 150, 150), (FEN_large // 2 - MENU_SIZE_BAR // 2, MENU_BAR_Y, MENU_SIZE_BAR, 22))
            pygame.draw.rect(ecran, (30, 160, 30), (FEN_large // 2 - MENU_SIZE_BAR // 2 + 2, MENU_BAR_Y + 2, avancement, 18))
            ecran.blit(loading_text, (FEN_large // 2 - loading_text.get_width() // 2, MENU_SIZE_BAR))
            avancement += MENU_SPEED_LOADING
            if not int(avancement) % max_len and len(load_texts) != 0 and float(int(avancement)) == avancement:
                if len(load_texts) - 1 > 0:
                    loading_text = police.render(open(load_texts.pop(random.randint(0, len(load_texts) - 1)),
                                                      encoding='utf-8').read(),
                                                 1, (255, 255, 255))
                else:
                    loading_text = police.render(open(load_texts.pop(0), encoding='utf-8').read(),
                                                 1, (255, 255, 255))
            if avancement >= 246 and chargement:
                if not has_already_played:
                    adventure.next()
                chargement = False
                avancement = 0
                temp = utils.ULoader()
                temp.load()
                del temp
                if en_reseau:
                    print("Entrée en mode réseau ...")
                    ecran.fill(0)
                    pygame.display.flip()
                    ip = TextBox(ecran, x=100, y=ecran.get_height() // 2,
                                 sx=ecran.get_width(),
                                 sy=ecran.get_height(),
                                 placeholder="IP du serveur : ")
                    ip.mainloop()
                    jeu = game.Game(ecran, "first", adventure=adventure,
                                    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                                    p=(ip.get_text(), 5500))
                else:
                    jeu = game.Game(ecran, "first", adventure=adventure)
                jeu.start()
                del jeu
        else:
            pygame.draw.rect(ecran, (50, 180, 180), (MENU_BTN_JOUER_X, MENU_BTN_JOUER_Y,
                                                     MENU_BTN_JOUER_SX, MENU_BTN_JOUER_SY))
            ecran.blit(jouer, (MENU_BTN_JOUER_X + (MENU_BTN_JOUER_SX - jouer.get_width()) // 2 + 2,
                               MENU_BTN_JOUER_Y + (MENU_BTN_JOUER_SY - jouer.get_height()) // 2 + 2))
            pygame.draw.rect(ecran, (180, 50, 180), (MENU_BTN_RESEAU_X, MENU_BTN_RESEAU_Y,
                                                     MENU_BTN_RESEAU_SX, MENU_BTN_RESEAU_SY))
            ecran.blit(reseau, (MENU_BTN_RESEAU_X + (MENU_BTN_RESEAU_SX - reseau.get_width()) // 2 + 2,
                                MENU_BTN_RESEAU_Y + (MENU_BTN_RESEAU_SY - reseau.get_height()) // 2 + 2))

        pygame.display.flip()

    pygame.quit()

    print("Le programme s'est terminé proprement")

if __name__ == '__main__':
    main()