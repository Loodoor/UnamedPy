from constantes import *
from indexer import Indexer
import os


class ULoader:
    def __init__(self):
        self.path = os.path.join("..", "saves", "utils" + EXTENSION)

    def load(self):
        if not os.path.exists(self.path):
            self.create()

    def create(self):
        # création des créatures
        Indexer.add_new("", 0, T_NORMAL, "")

    def reload(self):
        self.load()