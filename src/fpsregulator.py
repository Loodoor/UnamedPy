# coding=utf-8

__author__ = 'Moustillon'

import time
from constantes import MAX_FPS
from math import trunc


class IAFPS:
    def __init__(self, FPS: int):
        self.FPS = FPS / 10 if FPS != -1 else MAX_FPS
        self.defaut_value = self.FPS
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
        self.deltaTime_update()

    def deltaTime_update(self):
        if self.count_frames % 2:
            self.cur_time = time.time()
        else:
            self.last_time = time.time()
        if self.cur_time > self.last_time:
            self.frame_time = self.cur_time - self.last_time
        else:
            self.frame_time = self.last_time - self.cur_time
        self.dt_compute += self.get_DeltaTime()

    def get_DeltaTime(self):
        return self.frame_time

    def timer(self, frame_rate: int):
        self.frame_rate = frame_rate
        if self.frame_rate > self.FPS:
            self.wait += self.reduction
        elif self.frame_rate < self.FPS:
            self.wait -= self.reduction
            if self.wait <= 0:
                self.wait = 0
                #print("temps de pause (sec) :: " + str(self.wait))
                #print("frame_rate compté dans la boucle :: " + str(self.frame_rate))

    def pause(self):
        time.sleep(self.wait)

    def set_FPS(self, nv_FPS):
        self.FPS = nv_FPS / 10

    def default(self):
        self.FPS = self.defaut_value