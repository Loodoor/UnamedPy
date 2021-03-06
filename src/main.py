# coding=utf-8

from constantes import *
from exceptions import ErreurRepertoire
import debug

if os.path.split(os.getcwd())[1] not in ["src", "build"]:
    raise ErreurRepertoire("Le répertoire courant n'est pas correct, le jeu ne peut pas se lancer")
if not os.path.exists(os.path.join("..", "saves")):
    os.mkdir(os.path.join("..", "saves"))
debug.println("[CORE] Chargement ...")

import socket
from glob import glob
from pygame.locals import *
import time

import game
import utils
import ree
from textentry import TextBox
from aventure_manager import Adventure
from parametres import gui_access


def get_alea_text(path: str="textes") -> str:
    files = glob(os.path.join("..", "assets", "menu", path, "*.txt"))
    with open(random.choice(files), encoding="utf-8") as text_reader:
        texte = text_reader.read()
    return texte


def main():
    start_at = time.time()
    tmp = ree.init()
    debug.println("[CORE] Initialisation de Pygame ... {modules} ; {erreurs}".format(
        modules="Modules chargés : {}".format(tmp[0]),
        erreurs="Erreurs de chargement : {}".format(tmp[1])
    ))
    debug.println("[CORE] Initialisation de Pygame.Font ...", ree.init_font())
    debug.println("[CORE] Initialisation de Pygame.Mixer ...", ree.init_mixer())

    if DEBUG_LEVEL >= 1:
        ecran = ree.create_window((DEBUG_FEN_large, DEBUG_FEN_haut), HWSURFACE)
    else:
        ecran = ree.create_window((FEN_large, FEN_haut), HWSURFACE)
    clock = ree.create_clock()
    ree.set_caption("Unamed - v{}".format(VERSION))
    police = ree.load_font(POLICE_PATH, POL_NORMAL_TAILLE)
    police_annot = ree.load_font(POLICE_PATH, POL_NORMAL_TAILLE)
    police_annot.set_italic(True)
    title = ree.load_image(os.path.join("..", "assets", "menu", "logo_alpha.png"))
    bienvenue = [
        "Bienvenue à toi, chercheur !",
        "Tu vas entrer sur l'île d'Unamed, prépare toi à une toute nouvelle aventure !"
    ]
    adventure = Adventure(ecran, police)
    adventure.load()
    alea_texte = police_annot.render(get_alea_text(), POL_ANTIALISING, (0, 0, 0))
    fond = ree.load_image(os.path.join("..", "assets", "menu", "fond.png"))
    load_texts = glob(os.path.join("..", "assets", "menu", "chargement", "*.txt"))
    max_len = int(MENU_SIZE_BAR // len(load_texts))
    loading_text = police.render(open(load_texts.pop(random.randint(0, len(load_texts) - 1)),
                                      encoding='utf-8').read(),
                                 POL_ANTIALISING, (0, 0, 0))

    debug.println("[CORE] Appuyez sur 'J' pour lancer le jeu")

    continuer = 1
    has_already_played = adventure.has_already_played()
    chargement = False
    jeu = None
    loadeur = None
    finished_loading = False
    avancement = 0
    btn_reseau = ree.load_image(os.path.join("..", "assets", "gui", "fd_btn_reseau.png"))
    btn_jeu = ree.load_image(os.path.join("..", "assets", "gui", "fd_btn_jeu.png"))
    btn_params = ree.load_image(os.path.join("..", "assets", "gui", "fd_btn_params.png"))

    try:
        with open(os.path.join("..", "assets", "configuration", "maxavcmt" + EXTENSION), "r") as file:
            max_avancement = int(file.read())
    except OSError:
        max_avancement = 98

    debug.println("[CORE] Menu chargé en %3.4f sec" % (time.time() - start_at))
    debug.println("[CORE] Aucune partie trouvée" if not has_already_played else "Une partie a bien été trouvée")

    temp = utils.ULoader()
    temp.load()
    del temp
    debug.println("[CORE] Chargement et création des valeurs par défaut terminé")

    while continuer:
        dt = clock.tick()

        for event in ree.get_event():
            if event == (KEYDOWN, K_ESCAPE) or event == QUIT:
                continuer = 0
            if event == (KEYUP, K_RIGHT) or event == (KEYUP, K_LEFT):
                alea_texte = police_annot.render(get_alea_text(), POL_ANTIALISING, (0, 0, 0))
            if event == MOUSEBUTTONUP and not chargement:
                xp, yp = event.pos
                if MENU_BTN_JOUER_X <= xp <= MENU_BTN_JOUER_X + MENU_BTN_SX and \
                        MENU_BTN_JOUER_Y <= yp <= MENU_BTN_JOUER_Y + MENU_BTN_SY:
                    chargement = True
                    jeu = game.Game(ecran, adventure=adventure)
                if MENU_BTN_RESEAU_X <= xp <= MENU_BTN_RESEAU_X + MENU_BTN_SX and \
                        MENU_BTN_RESEAU_Y <= yp <= MENU_BTN_RESEAU_Y + MENU_BTN_SY:
                    chargement = True
                    debug.println("[CORE] Entrée en mode réseau ...")
                    ecran.fill(0)
                    ree.flip()
                    ip = TextBox(ecran, x=100, y=ecran.get_height() // 2,
                                 sx=ecran.get_width(),
                                 sy=ecran.get_height(),
                                 placeholder="IP du serveur : ")
                    ip.mainloop()
                    jeu = game.Game(ecran, adventure=adventure,
                                    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                                    p=(ip.get_text(), 5500))
                if MENU_BTN_PARAMS_X <= xp <= MENU_BTN_PARAMS_X + MENU_BTN_SX and \
                        MENU_BTN_PARAMS_Y <= yp <= MENU_BTN_PARAMS_Y + MENU_BTN_SY:
                    gui_access(ecran, police)

        # création du "loadeur"
        if jeu and not loadeur:
            loadeur = jeu.prepare()

        #Affichage
        ecran.blit(fond, (0, 0))
        ecran.blit(title, (FEN_large // 2 - title.get_width() // 2, 0))

        if not has_already_played:
            i = 0
            for txt in bienvenue:
                tmp = police.render(txt, POL_ANTIALISING, (0, 0, 0))
                ecran.blit(tmp, (FEN_large // 2 - tmp.get_width() // 2, 120 + 20 * i))
                i += 1
        else:
            ecran.blit(alea_texte, (FEN_large // 2 - alea_texte.get_width() // 2, 120))

        if chargement:
            utils.upg_bar(ecran, (FEN_large // 2 - MENU_SIZE_BAR // 2, MENU_BAR_Y, MENU_SIZE_BAR, 22), avancement, max_progress=max_avancement, fg_color=(20, 180, 20))
            ecran.blit(loading_text, (FEN_large // 2 - loading_text.get_width() // 2, MENU_SIZE_BAR))
            if loadeur:
                try:
                    avancement += next(loadeur)
                except StopIteration:
                    finished_loading = True
            if not int(avancement) % max_len and len(load_texts) != 0 and float(int(avancement)) == avancement:
                if len(load_texts) - 1 > 0:
                    loading_text = police.render(open(load_texts.pop(random.randint(0, len(load_texts) - 1)),
                                                      encoding='utf-8').read(),
                                                 POL_ANTIALISING, (0, 0, 0))
                else:
                    loading_text = police.render(open(load_texts.pop(0), encoding='utf-8').read(),
                                                 POL_ANTIALISING, (0, 0, 0))
            if finished_loading and chargement:
                debug.println("[CORE] avancement : {}".format(avancement))
                if avancement != max_avancement:
                    max_avancement = avancement
                avancement = 0
                if not has_already_played and DEBUG_LEVEL in (0, 1, 5):
                    adventure.next()
                elif not has_already_played and DEBUG_LEVEL > 1:
                    adventure.muted_next()
                jeu.start()

                # on remet tout à 0
                jeu = None
                loadeur = None
                finished_loading = False
                chargement = False
        else:
            ecran.blit(btn_jeu, (MENU_BTN_JOUER_X, MENU_BTN_JOUER_Y))
            ecran.blit(btn_reseau, (MENU_BTN_RESEAU_X, MENU_BTN_RESEAU_Y))
            ecran.blit(btn_params, (MENU_BTN_PARAMS_X, MENU_BTN_PARAMS_Y))

        ree.flip()

    ree.quit_()

    with open(os.path.join("..", "assets", "configuration", "maxavcmt" + EXTENSION), "w") as file:
        file.write(str(max_avancement))

    debug.println("[CORE] Le programme s'est terminé proprement")

if __name__ == '__main__':
    main()