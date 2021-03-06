__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

from constantes import *
import ree

from glob import glob
import time
import random


class MusicPlayer:
    def __init__(self):
        self.folder = os.path.join("..", "assets", "sons")
        self.sounds_path = glob(os.path.join(self.folder, "*.ogg"))
        self.sounds = {}
        self.__current = -1
        self.__rdm_playing_list = []
        self.__playing = False
        self.__looping = False
        self.__start_playing_at = 0

        self.__stop = False

    def load(self):
        for file in self.sounds_path:
            self.sounds[os.path.basename(file)] = ree.load_music_object(file)

    def select(self, sound_index: int):
        if 0 <= sound_index < len(self.sounds_path):
            self.__current = sound_index

    def get_random(self) -> int:
        return int(random.random() * (len(self.sounds_path) - 1))

    def get_music_id(self):
        return self.__current

    def select_random(self):
        self.__current = self.get_random()

    def create_random_playlist(self):
        for _ in range(100):
            self.__rdm_playing_list.append(self.get_random())

    def play(self, loop: int=0):
        # va tourner à l'infini par défaut
        if self.__current != -1 and not self.is_playing() and not self.__stop:
            # playlist aléatoire
            if self.__rdm_playing_list:
                try:
                    self.__current = self.__rdm_playing_list.pop()
                except IndexError:
                    self.create_random_playlist()
                    self.__current = self.__rdm_playing_list.pop()

            self.__playing = True
            self.__start_playing_at = time.time()
            self.__looping = True if loop == -1 else False
        else:
            if not self.__looping:
                if time.time() >= self.__start_playing_at + self.sounds[self.__current].get_length():
                    self.__playing = False

    def stop(self):
        if self.__current != -1 and self.is_playing():
            ree.stop_music(self.sounds[self.__current])
            self.__playing = False
            self.__stop = True

    def fadeout(self, value: float):
        if self.__current != -1 and self.is_playing():
            ree.fadeout_music(value)
            self.__playing = False
            self.__stop = True

    def get_rdm_playlist(self) -> list:
        return self.__rdm_playing_list

    def is_playing(self) -> bool:
        return self.__playing