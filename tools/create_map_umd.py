# coding=utf-8

import pickle
import os


def main():
    with open(os.path.join("..", "saves", "map.umd"), "wb") as map_:
        path_ = [os.path.join("..", "saves", "map", "start.umd")]
        pickle.Pickler(map_).dump(path_)


if __name__ == '__main__':
    main()