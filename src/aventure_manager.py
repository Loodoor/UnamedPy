# coding=utf-8

from constantes import *
from pickle import Pickler, Unpickler
from gui import GUIBulleWaiting, GUIBulleAsking
import debug


# Attention, y a du hardcode dans l'air ^^'
class Adventure:
    def __init__(self, ecran, font):
        self.user_pseudo = "testeur"
        self.progress = 0
        self.ecran = ecran
        self.font = font
        self.path = os.path.join("..", "saves", "adventure" + EXTENSION)
        self.textes = {}
        self.loaded = False
        self.values = {}
        self._actions = []
        self.villes_vues = []

        self._image_prof = ree.load_image(os.path.join("..", "assets", "aventure", "professeur.png"))
        self._image_ombre_prof = ree.load_image(os.path.join("..", "assets", "aventure", "professeur_ombre.png"))
        self._image_conduc = ree.load_image(os.path.join("..", "assets", "aventure", "conducteur_avion.png"))
        self._world_map = ree.load_image(os.path.join("..", "assets", "aventure", "worldmap.png"))

        self.fond = ree.load_image(os.path.join('..', 'assets', 'gui', 'fd_aventure.png'))

    def get_progress(self):
        return self.progress

    def has_already_played(self):
        if not self.progress:
            return False
        return True

    def _begin(self):
        ask_for = ""
        name_of_image = ""
        g = GUIBulleWaiting(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "", self.font)
        i = 0
        for texte in self.textes['part2']:
            self.ecran.blit(self.fond, (0, 0))

            if texte[0] == INPUT_CHAR:
                ask_smth = True
                ask_for = texte[texte[1:].index(INPUT_CHAR) + 2:-1]
                g.set_text(texte[1:texte[1:].index(INPUT_CHAR) + 1])
            elif texte[0] == IMAGE_SHOW_CHAR:
                name_of_image = texte.replace(":", "")
                continue
            elif texte[0] == ME_SPEAKING_CHAR:
                g.set_color('green')
            else:
                ask_smth = False
                if '{' not in texte and '}' not in texte:
                    g.set_text(texte[:-1])
                else:
                    g.set_text(texte[:-1].format(pseudo=self.user_pseudo))

            if texte[0] != ME_SPEAKING_CHAR:
                g.reinit_color()

            if "image prof" in name_of_image:
                self.ecran.blit(self._image_prof, (
                    (FEN_large - self._image_prof.get_width()) // 2,
                    (FEN_haut - self._image_prof.get_height() - BULLE_SY) // 2
                ))
            if "image ombre prof" in name_of_image:
                self.ecran.blit(self._image_ombre_prof, (
                    (FEN_large - self._image_ombre_prof.get_width()) // 2,
                    (FEN_haut - self._image_ombre_prof.get_height() - BULLE_SY) // 2
                ))
            if "conducteur avion" in name_of_image:
                self.ecran.blit(self._image_conduc, (
                    (FEN_large - self._image_conduc.get_width()) // 2,
                    (FEN_haut - self._image_conduc.get_height() - BULLE_SY) // 2
                ))

            g.update()

            if ask_smth:
                ask_smth = False
                if ask_for == "pseudo":
                    t = GUIBulleAsking(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Pseudo : ", self.font)
                    t.update()
                    self.user_pseudo = t.get_text()
                    with open(os.path.join("..", "saves", "pseudo" + EXTENSION), "wb") as pseudo_w:
                        Pickler(pseudo_w).dump(self.user_pseudo)
                elif ask_for == "creature":
                    t = GUIBulleAsking(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Nom : ", self.font)
                    t.update()
                    self.values["first creature name"] = t.get_text()
            i += 1

            ree.flip()
        del g

    def _part2(self):
        pass

    def next(self):
        if self.loaded:
            try:
                self._actions[self.progress]()
            except IndexError:
                debug.println("L'aventure semble terminée, impossible d'avencer plus")
            self.progress += 1
        else:
            debug.println("Merci de charger l'AdventureManager avant d'utiliser cette méthode")

    def muted_next(self):
        if self.loaded:
            if not self.progress:
                with open(os.path.join("..", "saves", "pseudo" + EXTENSION), "wb") as pseudo_w:
                    Pickler(pseudo_w).dump(self.user_pseudo)
                self.values["first creature name"] = "testeur"
                self.values["sprite"] = "maleplayer"
            self.progress += 1
        else:
            debug.println("Merci de charger l'AdventureManager avant d'utiliser cette méthode")

    def set_pseudo(self, new: str):
        self.user_pseudo = new

    def get_pseudo(self):
        return self.user_pseudo

    def get_values(self):
        return self.values

    def load(self):
        self._actions.append(self._begin)
        self._actions.append(self._part2)

        if os.path.exists(self.path):
            with open(self.path, "rb") as reader:
                tmp = Unpickler(reader).load()
                self.user_pseudo = tmp['pseudo']
                self.progress = tmp['progress']

        files = ['beginning.txt', 'part2.txt']
        try:
            for name in files:
                with open(os.path.join("..", "assets", "aventure", name), "r", encoding="utf-8") as file:
                    self.textes[name.split('.')[0]] = file.readlines()
        except OSError:
            debug.println("Un fichier de sauvegarde n'existe pas. Impossible de continuer.")
            sys.exit(0)
        self.loaded = True

    def save(self):
        with open(self.path, "wb") as writer:
            Pickler(writer).dump({
                "pseudo": self.user_pseudo,
                "progress": self.progress
            })