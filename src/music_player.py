__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

from constantes import *
import rendering_engine

from glob import glob
import random


class MusicPlayer:
    def __init__(self):
        self.folder = os.path.join("..", "assets", "sons")
        self.sounds = []
        self.sounds_path = glob(os.path.join(self.folder, "*.wav"))
        self.__current = -1
        self.__rdm_playing_list = []

    def select(self, sound_index: int):
        if 0 <= sound_index < len(self.sounds):
            self.__current = sound_index

    def get_random(self) -> int:
        return int(random.random() * (len(self.sounds) - 1))

    def get_music_id(self):
        return self.__current

    def select_random(self):
        self.__current = self.get_random()

    def create_random_playlist(self):
        for _ in range(100):
            self.__rdm_playing_list.append(self.get_random())

    def play(self, loop: int=-1):
        # va tourner à l'infini par défaut
        if self.__current != -1 and not self.is_playing():
            if self.__rdm_playing_list:
                try:
                    self.__current = self.__rdm_playing_list.pop()
                except IndexError:
                    self.create_random_playlist()
                    self.__current = self.__rdm_playing_list.pop()
            rendering_engine.load_music(self.sounds_path[self.__current])
            rendering_engine.play_music(loops=loop)

    def stop(self):
        if self.__current != -1 and self.is_playing():
            rendering_engine.stop_music()

    def fadeout(self, value: float):
        if self.__current != -1 and self.is_playing():
            rendering_engine.fadeout_music(value)

    def get_rdm_playlist(self) -> list:
        return self.__rdm_playing_list

    def is_playing(self) -> bool:
        return bool(rendering_engine.is_mixer_busy())