# coding=utf-8

import pickle
import os


def main():
    with open(os.path.join("..", "saves", "map.umd"), "wb") as map_:
        paths = {
            "1": ["..", "saves", "map", "start.umd"],
            "2": ["..", "saves", "map", "map1.umd"]
        }
        while True:
            number = input("Numéro de la map : ")
            path_ = input("Chemin vers la carte (séparateur : espace) : ").split()
            if number not in paths.keys():
                paths[number] = path_
                if not input("Continuer (Entrée pour arrêter) ?").strip():
                    break
            else:
                print("Code déjà utilisé !")
        print("Sauvegarde ...")
        pickle.Pickler(map_).dump(paths)
        print("Sauvegardé !")


if __name__ == '__main__':
    main()