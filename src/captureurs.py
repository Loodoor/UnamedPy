# coding=utf-8

from constantes import *
import random
from creatures_mgr import Creature


class CapturersTable:
    instance = None

    def __init__(self):
        if CapturersTable.instance != self or not CapturersTable.instance:
            CapturersTable.instance = self

        self.table = [
            Capturer(
                10,
                [T_FEU, T_AIR, T_EAU, T_TENEBRE, T_TERRE, T_ELEC, T_PLASMA, T_PLANTE, T_LUMIERE, T_NORMAL],
                OBJETS_ID.SimpleBall
            ),
            Capturer(
                25,
                [T_FEU, T_AIR, T_EAU, T_TENEBRE, T_TERRE, T_ELEC, T_PLASMA, T_PLANTE, T_LUMIERE, T_NORMAL],
                OBJETS_ID.NormalBall
            ),
            Capturer(
                55,
                [T_FEU, T_AIR, T_EAU, T_TENEBRE, T_TERRE, T_ELEC, T_PLASMA, T_PLANTE, T_LUMIERE, T_NORMAL],
                OBJETS_ID.SuperiorBall
            ),
            Capturer(
                100,
                [T_FEU, T_AIR, T_EAU, T_TENEBRE, T_TERRE, T_ELEC, T_PLASMA, T_PLANTE, T_LUMIERE, T_NORMAL],
                OBJETS_ID.UltraBall
            )
        ]

    @staticmethod
    def get_ball_with_id(id_: int) -> Capturer:
        if CapturersTable.instance:
            for ball in CapturersTable.table:
                if ball.id == id_:
                    return ball
            return GLOBAL_ERROR
        raise AttributeError("Need to create an object instance of CapturersTable")


class Capturer:
    def __init__(self, ratio: int, type_capt: list, id_: int):
        self.ratio = ratio  # 100
        self.type_capt = type_capt
        self.id = id_

    def use(self, creature: Creature):
        return random.randint(0, MAX_RATIO_CAP) >= self.ratio and creature.get_type() in self.type_capt