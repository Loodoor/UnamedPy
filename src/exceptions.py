class ErreurRepertoire(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class FonctionnaliteNonImplementee(Exception):
    def __init__(self, *args):
        super().__init__(*args)