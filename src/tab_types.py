# coding=utf-8

from constantes import *


class Storage:
    def __init__(self):
        self.tab = [[0 for _ in range(MAX_T_NBR + 1)] for _ in range(MAX_T_NBR + 1)]

    def init_tab(self):
        # Feu
        self.tab[T_FEU][T_FEU] = 1
        self.tab[T_FEU][T_EAU] = 0.5
        self.tab[T_FEU][T_PLANTE] = 2
        self.tab[T_FEU][T_ELEC] = 1
        self.tab[T_FEU][T_AIR] = 1
        self.tab[T_FEU][T_NORMAL] = 1
        self.tab[T_FEU][T_TERRE] = 0.75
        self.tab[T_FEU][T_POISON] = 1
        self.tab[T_FEU][T_LUMIERE] = 1
        self.tab[T_FEU][T_TENEBRE] = 0

        # Eau
        self.tab[T_EAU][T_FEU] = 2
        self.tab[T_EAU][T_EAU] = 1
        self.tab[T_EAU][T_PLANTE] = 0.5
        self.tab[T_EAU][T_ELEC] = 1.25
        self.tab[T_EAU][T_AIR] = 1
        self.tab[T_EAU][T_NORMAL] = 1
        self.tab[T_EAU][T_TERRE] = 0.75
        self.tab[T_EAU][T_POISON] = 1
        self.tab[T_EAU][T_LUMIERE] = 0
        self.tab[T_EAU][T_TENEBRE] = 1

        # Plante
        self.tab[T_PLANTE][T_FEU] = 0.5
        self.tab[T_PLANTE][T_EAU] = 2
        self.tab[T_PLANTE][T_PLANTE] = 1
        self.tab[T_PLANTE][T_ELEC] = 0.5
        self.tab[T_PLANTE][T_AIR] = 1
        self.tab[T_PLANTE][T_NORMAL] = 1
        self.tab[T_PLANTE][T_TERRE] = 1.25
        self.tab[T_PLANTE][T_POISON] = 0.5
        self.tab[T_PLANTE][T_LUMIERE] = 1
        self.tab[T_PLANTE][T_TENEBRE] = 1

        # Elec
        self.tab[T_ELEC][T_FEU] = 1
        self.tab[T_ELEC][T_EAU] = 1.5
        self.tab[T_ELEC][T_PLANTE] = 0.5
        self.tab[T_ELEC][T_ELEC] = 1
        self.tab[T_ELEC][T_AIR] = 0.75
        self.tab[T_ELEC][T_NORMAL] = 1
        self.tab[T_ELEC][T_TERRE] = 0.5
        self.tab[T_ELEC][T_POISON] = 1
        self.tab[T_ELEC][T_LUMIERE] = 0.75
        self.tab[T_ELEC][T_TENEBRE] = 1.25

        # Air
        self.tab[T_AIR][T_FEU] = 1.25
        self.tab[T_AIR][T_EAU] = 1.25
        self.tab[T_AIR][T_PLANTE] = 0.75
        self.tab[T_AIR][T_ELEC] = 0.75
        self.tab[T_AIR][T_AIR] = 1
        self.tab[T_AIR][T_NORMAL] = 1
        self.tab[T_AIR][T_TERRE] = 0.75
        self.tab[T_AIR][T_POISON] = 0.75
        self.tab[T_AIR][T_LUMIERE] = 1
        self.tab[T_AIR][T_TENEBRE] = 1

        # Normal
        self.tab[T_NORMAL][T_FEU] = 1
        self.tab[T_NORMAL][T_EAU] = 1
        self.tab[T_NORMAL][T_PLANTE] = 1
        self.tab[T_NORMAL][T_ELEC] = 1
        self.tab[T_NORMAL][T_AIR] = 1
        self.tab[T_NORMAL][T_NORMAL] = 1
        self.tab[T_NORMAL][T_TERRE] = 1
        self.tab[T_NORMAL][T_POISON] = 1
        self.tab[T_NORMAL][T_LUMIERE] = 1
        self.tab[T_NORMAL][T_TENEBRE] = 1

        # Terre
        self.tab[T_TERRE][T_FEU] = 1.25
        self.tab[T_TERRE][T_EAU] = 1.25
        self.tab[T_TERRE][T_PLANTE] = 0.75
        self.tab[T_TERRE][T_ELEC] = 1
        self.tab[T_TERRE][T_AIR] = 1
        self.tab[T_TERRE][T_NORMAL] = 1
        self.tab[T_TERRE][T_TERRE] = 1
        self.tab[T_TERRE][T_POISON] = 0.75
        self.tab[T_TERRE][T_LUMIERE] = 1
        self.tab[T_TERRE][T_TENEBRE] = 1

        # Poison
        self.tab[T_POISON][T_FEU] = 1
        self.tab[T_POISON][T_EAU] = 1
        self.tab[T_POISON][T_PLANTE] = 1.5
        self.tab[T_POISON][T_ELEC] = 0.75
        self.tab[T_POISON][T_AIR] = 0.5
        self.tab[T_POISON][T_NORMAL] = 1.5
        self.tab[T_POISON][T_TERRE] = 1.25
        self.tab[T_POISON][T_POISON] = 1
        self.tab[T_POISON][T_LUMIERE] = 0.75
        self.tab[T_POISON][T_TENEBRE] = 0.75

        # Lumière
        self.tab[T_LUMIERE][T_FEU] = 1
        self.tab[T_LUMIERE][T_EAU] = 1
        self.tab[T_LUMIERE][T_PLANTE] = 0.75
        self.tab[T_LUMIERE][T_ELEC] = 0
        self.tab[T_LUMIERE][T_AIR] = 1
        self.tab[T_LUMIERE][T_NORMAL] = 1
        self.tab[T_LUMIERE][T_TERRE] = 1
        self.tab[T_LUMIERE][T_POISON] = 1.25
        self.tab[T_LUMIERE][T_LUMIERE] = 1
        self.tab[T_LUMIERE][T_TENEBRE] = 2

        # Ténébre
        self.tab[T_TENEBRE][T_FEU] = 1.25
        self.tab[T_TENEBRE][T_EAU] = 0
        self.tab[T_TENEBRE][T_PLANTE] = 1.25
        self.tab[T_TENEBRE][T_ELEC] = 0
        self.tab[T_TENEBRE][T_AIR] = 1
        self.tab[T_TENEBRE][T_NORMAL] = 1
        self.tab[T_TENEBRE][T_TERRE] = 1
        self.tab[T_TENEBRE][T_POISON] = 1.25
        self.tab[T_TENEBRE][T_LUMIERE] = 2
        self.tab[T_TENEBRE][T_TENEBRE] = 1

    def stronger(self, type_moi: int, type_adv: int):
        return True if self.tab[type_moi][type_adv] > 1 else False

    def get_coeff(self, type_moi: int, type_adv: int):
        return self.tab[type_moi][type_adv]