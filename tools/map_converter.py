__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

import glob
import pickle
from constantes import *
from carte import SubCarte


def run():
    for file in glob.glob(os.path.join("..", "assets", "map", "*.umd")):
        old = pickle.Unpickler(open(file, 'rb')).load()
        carte, objets, buildings, zid, pnjs, spawns = old
        new_carte = []
        for y, line in enumerate(carte):
            new_ligne = []
            for x, case in enumerate(line):
                new_case = ['9990']
                for il, layer in enumerate(case):
                    new_case.append(layer)
                    if il == 2:
                        break
                new_ligne.append(new_case)
            new_carte.append(new_ligne)
        new = SubCarte(new_carte, objets, buildings, zid, pnjs, spawns, {}, os.path.split(file)[1].replace('.umd', '')[3:])
        pickle.Pickler(open(file, 'wb')).dump(new)
        print("done ! - {}".format(os.path.split(file)[1].replace('.umd', '')[3:]))


if __name__ == '__main__':
    run()