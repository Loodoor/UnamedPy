# coding=utf-8

import pickle
from constantes import *


class MoneyManager:
    def __init__(self):
        self.money = 3000
        self.path = os.path.join('..', 'saves', 'money' + EXTENSION)

    def get(self):
        return self.money

    def use(self, quantity: int):
        if self.money - quantity >= 0:
            self.money -= quantity
            return True
        return False

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'rb') as money_rb:
                self.money = pickle.Unpickler(money_rb).load()

    def save(self):
        with open(self.path, 'wb') as money_save:
            pickle.Pickler(money_save).dump(self.money)