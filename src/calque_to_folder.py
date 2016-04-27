import random
import string
import glob
import ree
import os


def main():
    # start
    ree.init()
    ec = ree.create_window((128, 148))
    ree.set_caption("Calque2folder")

    # loop
    for file in glob.glob(os.path.join("..", "assets", "calques_pnj", "*.png")):
        # loading
        im = ree.load_image(file)

        # rendering
        ree.draw_rect(ec, (0, 0) + ec.get_size(), (0, 0, 0))
        ec.blit(im, (0, 0))

        # cutting
        ims = [ree.create_surface((128 // 4, 148 // 4)) for _ in range(16)]
        for u in range(16):
            ims[u].fill((255, 0, 255))
            ims[u].blit(im, (0, 0), ((u % 4) * 128 // 4, (u // 4) * 148 // 4, 128 // 4, 148 // 4))

        # saving
        # directory = os.path.join("..", "assets", "pnj", ''.join(random.sample(list(string.ascii_lowercase), 5)))
        directory = os.path.join("..", "assets", "pnj", os.path.basename(file).split('.')[0])
        os.mkdir(directory)
        for c, new in enumerate(ims):
            new.set_colorkey(new.get_at((0, 0)))
            if 0 <= c < 4:
                pref = "bas"
            elif 4 <= c < 8:
                pref = "gauche"
            elif 8 <= c < 12:
                pref = "droite"
            else:
                pref = "haut"
            ree.save_image(new, os.path.join(directory, pref + str(c % 4) + '.png'))

        # blitting
        ree.flip()

        # waiting
        while True:
            if ree.poll_event() == ree.KEYUP:
                break

    # quit
    ree.quit_()


if __name__ == '__main__':
    main()