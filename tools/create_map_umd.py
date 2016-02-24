# coding=utf-8

import pickle
import os


def main():
    with open(os.path.join("..", "assets", "map", "map.umd"), "wb") as map_:
        paths = {
            "1": ["..", "assets", "map", "map0.umd"],
            "2": ["..", "assets", "map", "map1.umd"]
        }
        done = input("Continuer [O/N] ? > ").lower() == 'n'
        while not done:
            number = input("Numéro de la map : ")
            path_ = input("Chemin vers la carte (séparateur : espace) : ").split()
            if number not in paths.keys():
                paths[number] = path_
                if not input("Continuer (Entrée pour arrêter) ?").strip():
                    done = False
            else:
                print("Code déjà utilisé !")
        print("Sauvegarde ...")
        pickle.Pickler(map_).dump(paths)
        print("Sauvegardé !")


if __name__ == '__main__':
    main()