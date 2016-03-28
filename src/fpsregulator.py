# coding=utf-8

__author__ = 'Moustillon'

import time
from constantes import MAX_FPS


class IAFPS:
    def __init__(self, fps: int=-1):
        self.fps = fps / 10 if fps != -1 else MAX_FPS
        self.defaut_value = self.fps
        self.reduction = 0.0005
        self.wait = 0.001
        self.cpt_tour = 0
        self.frame_rate = 0
        self.begin_time = time.time() + 0.1
        self.cur_time = time.time()
        self.last_time = time.time()
        self.frame_time = 0
        self.count_frames = 0
        self.dt_compute = 0
        self.fps_compute = 0

    def get_fps(self):
        if self.dt_compute > 1:
            self.dt_compute = 0
            self.fps_compute = 0
            return -1.0
        return self.fps_compute

    def actualise(self):
        self.count_frames += 1
        self.fps_compute += 1
        if self.begin_time < time.time():
            self.cpt_tour = 0
            self.timer(self.cpt_tour)
        else:
            self.cpt_tour += 1
        self.delta_time_update()

    def delta_time_update(self):
        if self.count_frames % 2:
            self.cur_time = time.time()
        else:
            self.last_time = time.time()
        if self.cur_time > self.last_time:
            self.frame_time = self.cur_time - self.last_time
        else:
            self.frame_time = self.last_time - self.cur_time
        self.dt_compute += self.get_deltatime()

    def get_deltatime(self):
        return self.frame_time

    def timer(self, frame_rate: int):
        self.frame_rate = frame_rate
        if self.frame_rate > self.fps:
            self.wait += self.reduction
        elif self.frame_rate < self.fps:
            self.wait -= self.reduction
            if self.wait <= 0:
                self.wait = 0

    def pause(self):
        time.sleep(self.wait)

    def set_fps(self, nv_fps: int):
        self.fps = nv_fps / 10

    def default(self):
        self.fps = self.defaut_value