__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

from carte import CarteRenderer
from constantes import *
import ree


ree.init()

w = ree.create_window((FEN_large, FEN_haut))
m = CarteRenderer(w, ree.load_font(POLICE_PATH, POL_NORMAL_TAILLE))
m.load()
c = ree.create_clock()

while True:
    c.tick(30)

    ev = ree.poll_event()
    if ev == ree.QUIT:
        break
    if ev == ree.MOUSEBUTTONDOWN:
        m.clic(*ev.pos)
    if ev == ree.KEYUP:
        m = CarteRenderer(w, ree.load_font(POLICE_PATH, POL_NORMAL_TAILLE))
        m.load()
        print("Reloading")
    m.update()

    ree.flip()

ree.quit_()