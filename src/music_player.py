__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

from constantes import *
import rendering_engine

from glob import glob
import time
import random


class MusicPlayer:
    def __init__(self):
        self.folder = os.path.join("..", "assets", "sons")
        self.sounds_path = glob(os.path.join(self.folder, "*.wav"))
        self.__current = -1
        self.__rdm_playing_list = []
        self.__playing = False
        self.__looping = False
        self.__music_lenght = 60 * 3 + 30  # c'est une moyenne
        self.__start_playing_at = 0

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
        if self.__current != -1 and not self.is_playing():
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

            rendering_engine.load_music(self.sounds_path[self.__current])
            rendering_engine.play_music(loops=loop)
        else:
            if not self.__looping:
                if time.time() >= self.__start_playing_at + self.__music_lenght:
                    self.__playing = False

    def stop(self):
        if self.__current != -1 and self.is_playing():
            rendering_engine.stop_music()
            self.__playing = False

    def fadeout(self, value: float):
        if self.__current != -1 and self.is_playing():
            rendering_engine.fadeout_music(value)
            self.__playing = False

    def get_rdm_playlist(self) -> list:
        return self.__rdm_playing_list

    def is_playing(self) -> bool:
        return self.__playing