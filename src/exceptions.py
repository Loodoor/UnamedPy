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


class ListePleine(Exception):
    def __init__(self):
        super().__init__(
            "La liste étant déjà pleine, le code ne peut pas s'exécuter dans des conditions normales."
            " Cela peu avoir pour effet de déstabiliser le gameplay ou même le jeu entier. Merci de reporter "
            "cette erreur à Folaefolc, main dev' d'Unamed"
        )


class CarteInexistante(Exception):
    def __init__(self, path=""):
        super().__init__(
            "La carte demandée à l'adresse '{}' semble ne pas exister. Merci de reporter cette erreur à Folaefolc, "
            "main dev' d'Unamed".format(path)
        )


class ErreurContenuCarte(Exception):
    def __init__(self):
        super().__init__(
            "Le contenu de la carte n'est pas correct. Il est apparant que la source de la carte a été modifiée de"
            " manière très peu normale, que ce soit par une tiers personne ou un défaut logiciel. Essayez de réinstaller"
            " le jeu."
        )