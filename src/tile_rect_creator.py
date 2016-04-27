import os
import pickle
import ree


with open(os.path.join("..", "assets", "configuration", "tilesrect.umd"), "wb") as file:
    work = {}
    ree.init()
    print("vide pour quitter")
    while True:
        request = input("Code> ")
        if not request.strip():
            break
        work[request] = ree.rect(*[int(c.replace("(", "").replace(")", "")) for c in input("Rect (x, y, w, h)> ").split(',')])
        print("Ajouté !\n")
    pickle.Pickler(file).dump(work)
    ree.quit_()
    print("done")