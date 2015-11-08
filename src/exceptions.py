# coding=utf-8


class ErreurRepertoire(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class FonctionnaliteNonImplementee(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class CreaturesNonTrouvees(Exception):
    def __init__(self):
        super().__init__("Désolé, aucune créature ne semble exister. Essayez de réinstaller le jeu pour "
                         "résoudre le problème. Sinon, contactez moi sur Zeste de Savoir (.com) (Folaefolc)"
                         " pour m'indiquer votre problème"
        )