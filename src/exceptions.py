# coding=utf-8


class ErreurRepertoire(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class FonctionnaliteNonImplementee(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class CreaturesNonTrouvees(Exception):
    def __init__(self):
        super().__init__(
            "Désolé, aucune créature ne semble exister. Essayez de réinstaller le jeu pour "
            "résoudre le problème. Sinon, contactez moi sur Zeste de Savoir (.com) (Folaefolc)"
            " pour m'indiquer votre problème"
        )


class ErreurDeCreationDeClass(Exception):
    def __init__(self):
        super().__init__(
            "Une erreur s'est produite lors de la création d'un objet de type personnalisé "
            "(class). Merci de reporter cette erreur à Folaefolc, main dev' d'Unamed"
        )


class ListePleine(Exception):
    def __init__(self):
        super().__init__(
            "La liste étant déjà pleine, le code ne peut pas s'exécuter dans des conditions normales."
            " Cela peu avoir pour effet de destabiliser le gameplay ou même le jeu entier. Merci de reporter "
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
            " manière anormale, que ce soit par une tiers personne ou un défaut logiciel. Essayez de réinstaller"
            " le jeu."
        )


class AchatImpossible(Exception):
    def __init__(self):
        super().__init__(
            "Il n'est apparemment pas possible d'acheter un objet dans cette boutique."
            " Cela peut être dû à un défaut logiciel ou bien au fait que vous n'ayez pas assez"
            " d'argent."
        )


class CategorieInexistante(Exception):
    def __init__(self):
        super().__init__()


class ClassNonChargee(Exception):
    def __init__(self, class_name: str="''", method: str="''"):
        super().__init__(
            "La méthode load() de la class {} ayant levé cette exception aurait dû être appelée avant de vouloir "
            "accéder à la méthode {}".format(class_name, method)
        )


class CinematiqueIntrouvable(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NuzlockeError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ControlerManquant(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class MethodeManquante(Exception):
    def __init__(self, *args):
        super().__init__(*args)