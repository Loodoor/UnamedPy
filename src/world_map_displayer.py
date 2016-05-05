__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

from carte import CarteRenderer
from constantes import *
import ree


ree.init()


class A:
    def __init__(self):
        self.villes_vues = [
            "Chemin no 1",
            "Chemin no 2",
            "Chemin no 3",
            "Chemin no 4",
            "Chemin no 5",
            "Chemin no 6",
            "Chemin no 7",
            "Chenal no 1",
            "Chenal no 2",
            "Une île",
            "Tour centrale",
            "Port",
            "Tomat'oh",
            "North'bourn",
            "Januswi",
            "Arry'cover",
            "Pah'tapey",
            "Piderflor",
            "Muth'ira",
            "Silancard"
        ]

w = ree.create_window((FEN_large, FEN_haut))
a = A()
m = CarteRenderer(w, ree.load_font(POLICE_PATH, POL_NORMAL_TAILLE), a)
m.load()
c = ree.create_clock()

while True:
    c.tick(30)

    ev = ree.poll_event()
    if ev == ree.QUIT:
        break
    if ev == ree.MOUSEBUTTONDOWN:
        m.clic(*ev.pos)
    if ev == (MOUSEBUTTONDOWN, 5):
        m.increase_transparency()
    if ev == (MOUSEBUTTONDOWN, 4):
        m.decrease_transparency()
    if ev == ree.KEYUP:
        m = CarteRenderer(w, ree.load_font(POLICE_PATH, POL_NORMAL_TAILLE), a)
        m.load()
        print("Reloading")
    m.update()

    ree.flip()

ree.quit_()