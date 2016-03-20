# coding=utf-8

from constantes import *
from exceptions import ErreurRepertoire
import debug

if os.path.split(os.getcwd())[1] != "src":
    raise ErreurRepertoire("Le répertoire courant n'est pas correct, le jeu ne peut pas se lancer")
if not os.path.exists(os.path.join("..", "saves")):
    os.mkdir(os.path.join("..", "saves"))
debug.println("Chargement ...")

import socket
from glob import glob
from pygame.locals import *
import time

import game
import utils
# from ecran import MyScreen
from textentry import TextBox
from aventure_manager import Adventure


def get_alea_text(path: str="textes") -> str:
    files = glob(os.path.join("..", "assets", "menu", path, "*.txt"))
    with open(random.choice(files), encoding="utf-8") as text_reader:
        texte = text_reader.read()
    return texte


def main():
    start_at = time.time()
    tmp = pygame.init()
    debug.println("Initialisation de Pygame ... {modules} ; {erreurs}".format(
        modules="Modules chargés : {}".format(tmp[0]),
        erreurs="Erreurs de chargement : {}".format(tmp[1])
    ))
    debug.println("Initialisation de Pygame.Font ...", pygame.font.init())

    if DEBUG_LEVEL >= 1:
        ecran = pygame.display.set_mode((DEBUG_FEN_large, DEBUG_FEN_haut), HWSURFACE)
    else:
        ecran = pygame.display.set_mode((FEN_large, FEN_haut), HWSURFACE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Unamed - v" + VERSION)
    police = pygame.font.Font(POLICE_PATH, POL_NORMAL_TAILLE)
    police_annot = pygame.font.Font(POLICE_PATH, POL_NORMAL_TAILLE)
    police_annot.set_italic(True)
    title = pygame.image.load(os.path.join("..", "assets", "menu", "logo_alpha.png")).convert_alpha()
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
                                 POL_ANTIALISING, (255, 255, 255))

    debug.println("Appuyez sur 'J' pour lancer le jeu")

    continuer = 1
    has_already_played = adventure.has_already_played()
    chargement = False
    en_reseau = False
    avancement = 0
    btn_reseau = pygame.image.load(os.path.join("..", "assets", "gui", "fd_btn_reseau.png")).convert_alpha()
    btn_jeu = pygame.image.load(os.path.join("..", "assets", "gui", "fd_btn_jeu.png")).convert_alpha()

    debug.println("Menu chargé en %3.4f sec" % (time.time() - start_at))
    debug.println("Aucune partie trouvée" if not has_already_played else "Une partie a bien été trouvée")

    while continuer:
        dt = clock.tick()
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
        ecran.blit(title, (FEN_large // 2 - title.get_width() // 2, 0))

        if not has_already_played:
            i = 0
            for txt in bienvenue:
                tmp = police.render(txt, POL_ANTIALISING, (255, 255, 255))
                ecran.blit(tmp, (FEN_large // 2 - tmp.get_width() // 2, 120 + 20 * i))
                i += 1
        else:
            ecran.blit(alea_texte, (FEN_large // 2 - alea_texte.get_width() // 2, 120))

        if chargement:
            pygame.draw.rect(ecran, (150, 150, 150), (FEN_large // 2 - MENU_SIZE_BAR // 2, MENU_BAR_Y, MENU_SIZE_BAR, 22))
            pygame.draw.rect(ecran, (30, 160, 30), (FEN_large // 2 - MENU_SIZE_BAR // 2 + 2, MENU_BAR_Y + 2, avancement, 18))
            ecran.blit(loading_text, (FEN_large // 2 - loading_text.get_width() // 2, MENU_SIZE_BAR))
            avancement += MENU_SPEED_LOADING
            if not int(avancement) % max_len and len(load_texts) != 0 and float(int(avancement)) == avancement:
                if len(load_texts) - 1 > 0:
                    loading_text = police.render(open(load_texts.pop(random.randint(0, len(load_texts) - 1)),
                                                      encoding='utf-8').read(),
                                                 POL_ANTIALISING, (255, 255, 255))
                else:
                    loading_text = police.render(open(load_texts.pop(0), encoding='utf-8').read(),
                                                 POL_ANTIALISING, (255, 255, 255))
            if avancement >= 246 and chargement:
                chargement = False
                avancement = 0
                temp = utils.ULoader()
                temp.load()
                del temp
                if en_reseau:
                    debug.println("Entrée en mode réseau ...")
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
                jeu.prepare()
                if not has_already_played:
                    adventure.next()
                jeu.start()
                del jeu
        else:
            ecran.blit(btn_jeu, (MENU_BTN_JOUER_X, MENU_BTN_JOUER_Y))
            ecran.blit(btn_reseau, (MENU_BTN_RESEAU_X, MENU_BTN_RESEAU_Y))

        pygame.display.flip()

    pygame.quit()

    debug.println("Le programme s'est terminé proprement")

if __name__ == '__main__':
    main()