# coding=utf-8

from os import path
from constantes import *
import pickle


class InGameAction:
    def __init__(self, id_: str=""):
        self.id = id_

    def exec(self, *args):
        pass


class Trigger:
    def __init__(self, map_: str, id_: str=TRIGGER_UNDEFINED, at_x: int=-1, at_y: int=-1, how_many_calls: int=1,
                 action: callable or InGameAction=print or InGameAction(), *args):
        self.id = id_
        self.at_x = at_x
        self.at_y = at_y
        self.max_calls = how_many_calls
        self.calls = self.max_calls
        self.action = action
        self.args = args
        self.map = map_

    def get_id(self):
        return self.id

    def get_max_calls(self):
        return self.max_calls

    def get_left_calls(self):
        return self.calls

    def call(self, cur_map: str):
        if self.max_calls != -1:
            if self.max_calls - 1 >= 0:
                if isinstance(self.action, callable):
                    self.action(*self.args)
                else:
                    self.action.exec(*self.args)
                self.calls -= 1
        else:
            if isinstance(self.action, callable):
                self.action(*self.args)
            else:
                self.action.exec(*self.args)

    def at_pos(self):
        return self.at_x, self.at_y

    def move_to(self, new_x: int, new_y: int):
        self.at_x = new_x
        self.at_y = new_y

    def compute_to_dict(self):
        """Préférer l'usage de cette méthode plutôt que de compute_to_list"""
        return {self.id: [self.at_x, self.at_y, self.action, self.args], "map": self.map}

    def compute_to_list(self):
        return [self.id, self.at_x, self.at_y, self.action, self.args]


class TriggersManager:
    def __init__(self):
        self.path = path.join("..", "saves", "triggers" + EXTENSION)
        self.triggers = []
        self.already_used = []

    @staticmethod
    def add_trigger_to_path(new_trigger: Trigger):
        path_ = path.join("..", "saves", "triggers" + EXTENSION)
        if path.exists(path_):
            with open(path_, 'rb') as path_rb:
                sv = pickle.Unpickler(path_rb).load()
                sv.append(new_trigger)
                pickle.Pickler(open(path_, 'wb')).dump(sv)
        else:
            with open(path_, 'wb') as path_wb:
                pickle.Pickler(path_wb).dump([new_trigger])

    def get_trigger_id_at_pos(self, at_x: int, at_y: int):
        for trigger in self.triggers:
            if trigger.at_pos() == (at_x, at_y):
                return trigger.get_id()
        return TRIGGER_ERROR

    def call_trigger_at_pos(self, at_x: int, at_y: int, cur_map: str):
        for trigger in self.triggers:
            if trigger.at_pos() == (at_x, at_y):
                if trigger.get_id() not in self.already_used:
                    trigger.call(cur_map)
                    if not trigger.get_left_calls():
                        self.already_used.append(trigger.get_id())

    def call_trigger_with_id(self, id_: str, cur_map: str):
        for trigger in self.triggers:
            if trigger.get_id() == id_ and trigger.get_id() not in self.already_used:
                trigger.call(cur_map)
                if not trigger.get_left_calls():
                    self.already_used.append(trigger.get_id())

    def load(self):
        if path.exists(self.path):
            with open(self.path, 'rb') as trigger_rb:
                self.triggers = pickle.Unpickler(trigger_rb).load()

    def save(self):
        with open(self.path, 'wb') as trigger_wb:
            pickle.Pickler(trigger_wb).dump(self.triggers)