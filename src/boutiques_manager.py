# coding=utf-8

import pygame
from pygame.locals import *
from constantes import *
from money_mgr import MoneyManager
from exceptions import AchatImpossible


class _ObjectSold:
    def __init__(self):
        self.name = ""
        self.sold = False
        self.quantity_to_buy = -1
        self.total_price = 0


class BoutiqueManager:
    def __init__(self, ecran: pygame.Surface, money: MoneyManager):
        self.ecran = ecran
        self.page = 0
        self.objects_to_sell = {}
        self.money = money
        self.confirm_selling_of = _ObjectSold
        self.fond = pygame.image.load(os.path.join("..", "assets", "gui", "fd_boutique.png")).convert_alpha()

    def buy(self, object_: str, quantity: int):
        self.confirm_selling_of = _ObjectSold()
        self.confirm_selling_of.name = object_
        self.confirm_selling_of.quantity_to_buy = quantity
        self.confirm_selling_of.total_price = quantity * self.get_price_of(object_)
        return self.get_quantity_of(object_) * quantity

    def validate(self):
        self.confirm_selling_of.sold = True
        if not self.money.use(self.confirm_selling_of.total_price):
            raise AchatImpossible

    def get_quantity_of(self, object_: str):
        return self.objects_to_sell[object_]['quantity']

    def get_price_of(self, object_: str):
        return self.objects_to_sell[object_]['price']

    def update(self):
        self.render()

    def render(self):
        self.ecran.blit(self.fond, (SHOP_X, SHOP_Y))