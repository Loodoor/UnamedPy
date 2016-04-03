# coding=utf-8

from constantes import *
from exceptions import ErreurRepertoire
import debug

if os.path.split(os.getcwd())[1] not in ["src", "build"]:
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
import rendering_engine
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
    tmp = rendering_engine.init()
    debug.println("Initialisation de Pygame ... {modules} ; {erreurs}".format(
        modules="Modules chargés : {}".format(tmp[0]),
        erreurs="Erreurs de chargement : {}".format(tmp[1])
    ))
    debug.println("Initialisation de Pygame.Font ...", rendering_engine.init_font())
    debug.println("Initialisation de Pygame.Mixer ...", rendering_engine.init_mixer())

    if DEBUG_LEVEL >= 1:
        ecran = rendering_engine.create_window((DEBUG_FEN_large, DEBUG_FEN_haut), HWSURFACE)
    else:
        ecran = rendering_engine.create_window((FEN_large, FEN_haut), HWSURFACE)
    clock = rendering_engine.create_clock()
    rendering_engine.set_caption("Unamed - v{}".format(VERSION))
    police = rendering_engine.load_font(POLICE_PATH, POL_NORMAL_TAILLE)
    police_annot = rendering_engine.load_font(POLICE_PATH, POL_NORMAL_TAILLE)
    police_annot.set_italic(True)
    title = rendering_engine.load_image(os.path.join("..", "assets", "menu", "logo_alpha.png"))
    bienvenue = [
        "Bienvenue à toi, chercheur !",
        "Tu vas entrer sur l'île d'Unamed, prépare toi à une toute nouvelle aventure !"
    ]
    adventure = Adventure(ecran, police)
    adventure.load()
    alea_texte = police_annot.render(get_alea_text(), 1, (255, 255, 255))
    fond = rendering_engine.load_image(os.path.join("..", "assets", "menu", "fond.png"))
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
    jeu = None
    loadeur = None
    finished_loading = False
    avancement = 0
    btn_reseau = rendering_engine.load_image(os.path.join("..", "assets", "gui", "fd_btn_reseau.png"))
    btn_jeu = rendering_engine.load_image(os.path.join("..", "assets", "gui", "fd_btn_jeu.png"))
    btn_params = rendering_engine.load_image(os.path.join("..", "assets", "gui", "fd_btn_params.png"))

    try:
        with open(os.path.join("..", "assets", "configuration", "maxavcmt" + EXTENSION), "r") as file:
            max_avancement = int(file.read())
    except OSError:
        max_avancement = 98

    debug.println("Menu chargé en %3.4f sec" % (time.time() - start_at))
    debug.println("Aucune partie trouvée" if not has_already_played else "Une partie a bien été trouvée")

    temp = utils.ULoader()
    temp.load()
    del temp
    debug.println("Chargement et création des valeurs par défaut terminé")

    while continuer:
        dt = clock.tick()
        for event in rendering_engine.get_event():
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
                continuer = 0
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    alea_texte = police_annot.render(get_alea_text(), 1, (255, 255, 255))
            if event.type == MOUSEBUTTONUP:
                xp, yp = event.pos
                if MENU_BTN_JOUER_X <= xp <= MENU_BTN_JOUER_X + MENU_BTN_SX and \
                        MENU_BTN_JOUER_Y <= yp <= MENU_BTN_JOUER_Y + MENU_BTN_SY:
                    chargement = True
                if MENU_BTN_RESEAU_X <= xp <= MENU_BTN_RESEAU_X + MENU_BTN_SX and \
                        MENU_BTN_RESEAU_Y <= yp <= MENU_BTN_RESEAU_Y + MENU_BTN_SY:
                    chargement = True
                    en_reseau = True
                if MENU_BTN_PARAMS_X <= xp <= MENU_BTN_PARAMS_X + MENU_BTN_SX and \
                        MENU_BTN_PARAMS_Y <= yp <= MENU_BTN_PARAMS_Y + MENU_BTN_SY:
                    gui_access(ecran, police)

        # création de l'instance de jeu
        if en_reseau:
            if not jeu:
                debug.println("Entrée en mode réseau ...")
                ecran.fill(0)
                rendering_engine.flip()
                ip = TextBox(ecran, x=100, y=ecran.get_height() // 2,
                             sx=ecran.get_width(),
                             sy=ecran.get_height(),
                             placeholder="IP du serveur : ")
                ip.mainloop()
                jeu = game.Game(ecran, "first", adventure=adventure,
                                s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
                                p=(ip.get_text(), 5500))
        else:
            jeu = game.Game(ecran, "first", adventure=adventure) if not jeu else jeu

        # création du "loadeur"
        if jeu and not loadeur:
            loadeur = jeu.prepare()

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
                                                 POL_ANTIALISING, (255, 255, 255))
                else:
                    loading_text = police.render(open(load_texts.pop(0), encoding='utf-8').read(),
                                                 POL_ANTIALISING, (255, 255, 255))
            if finished_loading and chargement:
                debug.println("L'avancement max est {}".format(avancement))
                if avancement != max_avancement:
                    max_avancement = avancement
                avancement = 0
                if not has_already_played and not DEBUG_LEVEL:
                    adventure.next()
                elif not has_already_played and DEBUG_LEVEL:
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

        rendering_engine.flip()

    rendering_engine.quit_()

    with open(os.path.join("..", "assets", "configuration", "maxavcmt" + EXTENSION), "w") as file:
        file.write(str(max_avancement))

    debug.println("Le programme s'est terminé proprement")

if __name__ == '__main__':
    main()