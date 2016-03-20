__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

import glob
import pickle
from constantes import *
from carte import SubCarte


def converter(file_path: str):
    old = pickle.Unpickler(open(file_path, 'rb')).load()
    carte, objets, buildings, zid, pnjs, spawns = old
    new_carte = []
    for line in carte:
        new_ligne = []
        for case in line:
            new_case = ['9990']
            for il, layer in enumerate(case):
                new_case.append(layer)
                if il == 2:
                    break
            new_ligne.append(new_case)
        new_carte.append(new_ligne)
    new = SubCarte(new_carte, objets, buildings, zid, pnjs, spawns, {}, os.path.split(file_path)[1].replace('.umd', '')[3:])
    pickle.Pickler(open(file_path, 'wb')).dump(new)
    print("done ! - {}".format(os.path.split(file_path)[1].replace('.umd', '')[3:]))


def run():
    cmd = input("Convert all [y/n] ? ")
    if cmd.lower() == "y":
        for file in glob.glob(os.path.join("..", "assets", "map", "*.umd")):
            converter(file)
    else:
        file_path = input("Path to the file to convert in the new format > ")
        converter(file_path)


if __name__ == '__main__':
    run()