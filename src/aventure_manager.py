# coding=utf-8

from constantes import *
from pickle import Pickler, Unpickler
from gui import GUIBulleWaiting, GUIBulleAsking
import debug
from animator import CinematiqueCreator


# Attention, y a du hardcode dans l'air ^^'
class Adventure:
    def __init__(self, ecran, font):
        self.progress = 0
        self.ecran = ecran
        self.font = font
        self.path = os.path.join("..", "saves", "adventure" + EXTENSION)
        self.textes = {}
        self.loaded = False
        self.values = {
            "pseudo": "testeur"
        }
        self._actions = []
        self.villes_vues = []

        self._images = {
            "professeur": ree.load_image(os.path.join("..", "assets", "aventure", "professeur.png")),
            "professeur_ombre": ree.load_image(os.path.join("..", "assets", "aventure", "professeur_ombre.png")),
            "conducteur_avion": ree.load_image(os.path.join("..", "assets", "aventure", "conducteur_avion.png")),
            "world_map": ree.load_image(os.path.join("..", "assets", "aventure", "worldmap.png"))
        }

        self.fond = ree.load_image(os.path.join('..', 'assets', 'gui', 'fd_aventure.png'))

    def get_progress(self):
        return self.progress

    def has_already_played(self):
        if not self.progress:
            return False
        return True

    def _parse_scene(self, scene: str):
        ask_for = ""
        name_of_image = ""
        ask_smth = False
        g = GUIBulleWaiting(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "", self.font)
        i = 0
        for texte in self.textes[scene]:
            self.ecran.blit(self.fond, (0, 0))

            if texte[0] == INPUT_CHAR:
                ask_smth = True
                ask_for = texte[texte[1:].index(INPUT_CHAR) + 2:-1]
                g.set_text(texte[1:texte[1:].index(INPUT_CHAR) + 1])
            elif texte[0] == IMAGE_SHOW_CHAR:
                name_of_image = texte.replace(":", "").strip()
                continue
            elif texte[0] == IF_CHAR:
                if texte[1] != NOT_CHAR:
                    var, cond, next = texte[1:].split('^')
                else:
                    var, cond, next = texte[2:].split('^')
                next = next.split('|')
                var = var.format(**self.values)
                if texte[1] == NOT_CHAR:
                    test = var != cond
                else:
                    test = var == cond
                if test:
                    if next[0][0] != ME_SPEAKING_CHAR:
                        if next[0].strip():
                            g.set_text(next[0])
                        else:
                            continue
                    else:
                        g.set_text(next[0][1:])
                        g.set_color('green')
                else:
                    if next[1][0] != ME_SPEAKING_CHAR:
                        if next[1].strip():
                            g.set_text(next[1])
                        else:
                            continue
                    else:
                        g.set_text(next[1][1:])
                        g.set_color('green')
            elif texte[0] == LOAD_CINEMATIQUE_CHAR:
                sc = CinematiqueCreator(self.ecran, os.path.join("..", "assets", "cinematiques", texte[1:].strip() + EXTENSION))
                sc.load()
                sc.play()
                continue
            elif texte[0] == ME_SPEAKING_CHAR:
                g.set_color('green')
                g.set_text(texte[1:])
            else:
                ask_smth = False
                if '{' not in texte and '}' not in texte:
                    g.set_text(texte[:-1])
                else:
                    g.set_text(texte[:-1].format(**self.values))

            if texte[0] != ME_SPEAKING_CHAR:
                g.reinit_color()

            if name_of_image:
                self.ecran.blit(self._images[name_of_image], (
                    (FEN_large - self._images[name_of_image].get_width()) // 2,
                    (FEN_haut - self._images[name_of_image].get_height() - BULLE_SY) // 2
                ))

            g.update()

            if ask_smth:
                ask_smth = False
                t = GUIBulleAsking(self.ecran, (POS_BULLE_X, POS_BULLE_Y), texte[1:texte[1:].index(INPUT_CHAR) + 1], self.font)
                t.update()
                self.values[ask_for] = t.get_text()

                if ask_for == "pseudo":
                    with open(os.path.join("..", "saves", "pseudo" + EXTENSION), "wb") as pseudo_w:
                        Pickler(pseudo_w).dump(self.values["pseudo"])
            i += 1

            ree.flip()
        del g

    def determine_sexe(self):
        if self.values['garcon'] == 'oui' and self.values['sur_choix_sex'] == 'oui':
            return 'male'
        if self.values['garcon'] == 'oui' and self.values['sur_choix_sex'] != 'oui':
            return 'girl'
        if self.values['garcon'] != 'oui' and self.values['sur_choix_sex'] == 'oui':
            return 'girl'
        if self.values['garcon'] != 'oui' and self.values['sur_choix_sex'] != 'oui':
            return 'male'

    def next(self):
        if self.loaded:
            try:
                self._parse_scene(self._actions[self.progress])
                # on récupère les valeurs après
                if self.progress == 0:
                    self.values['sprite'] = self.determine_sexe() + 'player'
            except IndexError:
                debug.println("L'aventure semble terminée, impossible d'avencer plus")
            self.progress += 1
        else:
            debug.println("Merci de charger l'AdventureManager avant d'utiliser cette méthode")

    def muted_next(self):
        if self.loaded:
            if not self.progress:
                self.values["first creature name"] = "testeur"
                self.values["sprite"] = "maleplayer"
                self.values["pseudo"] = "testeur"
            self.progress += 1
        else:
            debug.println("Merci de charger l'AdventureManager avant d'utiliser cette méthode")

    def set_pseudo(self, new: str):
        self.values["pseudo"] = new

    def get_pseudo(self):
        return self.values["pseudo"]

    def get_values(self):
        return self.values

    def load(self):
        with open(os.path.join("..", "assets", "aventure", "scenes.txt"), "r", encoding="utf-8") as scenesrd:
            self._actions = eval(scenesrd.read())

        if os.path.exists(self.path):
            with open(self.path, "rb") as reader:
                tmp = Unpickler(reader).load()
                self.progress = tmp['r']
                self.values = tmp['l']
                self.villes_vues = tmp["v"]

        try:
            for name in self._actions:
                with open(os.path.join("..", "assets", "aventure", name + ".txt"), "r", encoding="utf-8") as file:
                    self.textes[name] = file.readlines()
        except OSError:
            debug.println("Un fichier de sauvegarde n'existe pas. Impossible de continuer.")
            exit(1)
        self.loaded = True

    def save(self):
        with open(self.path, "wb") as writer:
            Pickler(writer).dump({
                "r": self.progress,
                "l": self.values,
                "v": self.villes_vues
            })