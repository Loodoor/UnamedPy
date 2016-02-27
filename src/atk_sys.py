# coding=utf-8

from gui import GUIBulle, GUIBulleWaiting, GUIBulleAsking
from constantes import *
from utils import upg_bar
import creatures_mgr
from zones_attaques_manager import ZonesManager
import debug


def calcul_degats(degats_basiques: int, specs_atk: dict, specs_def: dict, coeff_types: int, my_type: int) -> int:
    x = 1.3 if specs_atk[ATK_TYP] == my_type else 1
    return (degats_basiques + specs_atk[SPEC_ATK] / specs_def[SPEC_DEF]) * coeff_types * x


def calcul_esquive(specs_atk: list, specs_def: list) -> bool:
    return True if specs_atk[SPEC_VIT] >= 2 * specs_def[SPEC_VIT] else False


class Combat:
    def __init__(self, ecran: pygame.Surface, creature_joueur, zone: ZonesManager, zone_id: int, indexer, font, storage,
                 renderer_manager, equipe):
        self.ecran = ecran
        self.compteur_tour = 0
        self.creature_joueur = creature_joueur
        self.adversaire = creatures_mgr.Creature(0, indexer.get_type_of(0), indexer=indexer)
        self.zones_mgr = zone
        self.zid = zone_id
        self.indexer = indexer
        self.has_started = False
        self.has_attacked = False
        self.has_captured = False
        self.is_running = True
        self.bulle_que_doit_faire = GUIBulle(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE), "Que doit faire ?", font)
        self.indic_captured = pygame.image.load(os.path.join("..", "assets", "gui", "captured.png")).convert_alpha()
        self.font = font
        self.selected_atk = -1
        self.storage = storage
        self.renderer_manager = renderer_manager
        self.equipe = equipe

    def on_start(self):
        debug.println("adv id", self.adversaire.get_id())
        debug.println("zid", self.zid)
        self.has_started = True

    def on_end(self):
        if not self.indexer.get_viewed(self.get_adversary().get_id()) or not self.indexer.get_captured(self.get_adversary().get_id()):
            t = GUIBulleAsking(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Nom pour cette créature : ", self.font)
            t.update()
            name_for_crea = t.get_text()
            del t
            self.indexer.add_name_to_crea(self.adversaire.get_id(), name_for_crea)
        if not self.indexer.get_typeur().get_name(self.get_adversary().get_type()):
            g = GUIBulleAsking(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Nom pour ce type de créature : ", self.font)
            g.update()
            type_name = g.get_text()
            del g
            self.indexer.get_typeur().change_name(self.get_adversary().get_type(), type_name)

        self.indexer.vu_(self.get_adversary().get_id())
        if self.has_captured:
            self.indexer.capturer(self.get_adversary().get_id())

    def find_adv(self):
        self.adversaire = creatures_mgr.Creature(*self.zones_mgr.get_new_adversary(self.zid), indexer=self.indexer)

    def mon_tour(self):
        return True if not self.compteur_tour % 2 else False

    def get_my_creature(self) -> creatures_mgr.Creature:
        return self.creature_joueur

    def get_adversary(self) -> creatures_mgr.Creature:
        return self.adversaire

    def end_fight_for_capture(self):
        g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                            "Bravo ! Vous venez de capturer une nouvelle créature !",
                            self.font)

        g.update()
        del g
        self.has_captured = True
        self.equipe.add_creature(self.get_adversary())
        self.is_running = False

    def _is_active(self):
        if self.renderer_manager.get_renderer() != RENDER_COMBAT:
            return False
        return True

    def update(self):
        if self.is_running:
            if not self.has_started:
                self.on_start()

            self.render()

            self._gerer_etats()

            if self.mon_tour():
                self._manage_my_turn()
            else:
                g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                    self.get_adversary().get_pseudo() +
                                    " ne sait pas quoi faire pour le moment !",
                                    self.font)
                g.update()
                del g
                self.compteur_tour += 1

            if self.get_adversary().is_dead():
                self._manage_adversary_death()

    def _gerer_etats(self):
        for crea in [self.get_my_creature(), self.get_adversary()]:
            if crea.get_state() == SPEC_ETATS.brule:
                crea.taper(SPEC_DGT_BRULURE(crea.get_niv()))
            if crea.get_state() == SPEC_ETATS.poisone:
                crea.taper(SPEC_DGT_POISON(crea.get_niv()))

    def _manage_my_turn(self):
        can_attack = True
        if self.get_my_creature().get_state() == SPEC_ETATS.paralise:
            can_attack = SPEC_LUCK_OF_ATTACK(self.get_my_creature().get_vit())

        if can_attack:
            self.bulle_que_doit_faire.set_text("Que doit faire " + self.get_my_creature().get_pseudo() + " ?")
            self.bulle_que_doit_faire.update()

            if self.has_attacked:
                self.get_adversary().taper(calcul_degats(self.get_my_creature().get_attacks()[self.selected_atk].get_dgts(),
                                                         self.get_my_creature().get_specs(),
                                                         self.get_adversary().get_specs(),
                                                         self.storage.get_coeff(
                                                             self.get_my_creature().get_type(),
                                                             self.get_adversary().get_type()
                                                         ),
                                                         self.get_my_creature().get_type()))
                self.has_attacked = False
                g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                    self.get_my_creature().get_pseudo() +
                                    " utilise " +
                                    self.get_my_creature().get_attacks()[self.selected_atk].get_nom() +
                                    " !",
                                    self.font)
                g.update()
                self.compteur_tour += 1
        else:
            g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                self.get_my_creature().get_pseudo() + " est paralisé ! Il n'a pas pu attaquer",
                                self.font)
            g.update()
            del g
            self.compteur_tour += 1

    def _manage_adversary_death(self):
        g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                            self.get_adversary().get_pseudo() + " est vaincu !", self.font)

        g.update()
        del g

        # gestion de l'xp
        level_up = self.get_my_creature().gagner_xp(self.get_adversary())
        if not isinstance(level_up, (int, float)):
            g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                self.get_my_creature().get_pseudo() + " a gagné un niveau !",
                                self.font)
            g.update()
            del g

            for new in level_up:
                g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                    [
                                        "Niveau : +1 !   Attaque : +" + str(new[SPEC_ATK]) + " !",
                                        "Défense : +" + str(new[SPEC_DEF]) + "!   Vitesse : +" + str(new[SPEC_VIT]) + " !",
                                        "Points de vie : +" + str(new[SPEC_MAX_PVS]) + " !"
                                    ], self.font)
                g.update()
                del g
        else:
            g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                self.get_my_creature().get_pseudo() + " a gagné {} xp !".format(level_up),
                                self.font)
            g.update()
            del g

        self.is_running = False

    def is_finished(self):
        return not self.is_running

    def next(self):
        self.selected_atk = self.selected_atk + 1 if self.selected_atk + 1 < 4 else 0

    def previous(self):
        self.selected_atk = self.selected_atk - 1 if self.selected_atk > 0 else 3

    def attaquer(self):
        if 0 <= self.selected_atk <= MAX_ATK - 1:
            dgts = self.get_my_creature().attaquer(self.selected_atk)
            self.get_adversary().taper(dgts)
            self.valide()

    def valide(self):
        self.has_attacked = True

    def mouseover(self, xp: int, yp: int):
        if COMB_X_ATK <= xp <= COMB_X_ATK + COMB_SX_ATK_FIELD:
            real_y = (yp - COMB_Y_ADV - COMB_SY_ADV) // (COMB_SY_ATK_FIELD + 10) - 1
            self.selected_atk = real_y

    def clic(self, xp: int, yp: int):
        self.mouseover(xp, yp)
        self.attaquer()

    def render(self):
        # en attendant d'avoir un paysage
        pygame.draw.rect(self.ecran, (50, 50, 180), (COMB_X, COMB_Y, COMB_SX, COMB_SY))

        # affichage des créatures
        self.ecran.blit(self.get_adversary().get_image(), (COMB_X_ADV, COMB_Y_ADV))
        self.ecran.blit(self.get_my_creature().get_image(), (COMB_X_ME, COMB_Y_ME))

        # affichage des stats
        if not self.get_adversary().is_dead():
            upg_bar(self.ecran, (COMB_X_ADV, COMB_Y_ADV - COMB_SY_LIFE_BAR - 10, COMB_SX_LIFE_BAR, COMB_SY_LIFE_BAR),
                    self.get_adversary().get_pvs() // self.get_adversary().get_max_pvs() * (COMB_SX_LIFE_BAR - BAR_ESP * 2))
        else:
            pygame.draw.rect(self.ecran, (128, 128, 128),
                             (COMB_X_ADV, COMB_Y_ADV - COMB_SY_LIFE_BAR - 10, COMB_SX_LIFE_BAR, COMB_SY_LIFE_BAR))
        if not self.get_my_creature().is_dead():
            upg_bar(self.ecran, (COMB_X_ME, COMB_Y_ME - COMB_SY_LIFE_BAR - 10, COMB_SX_LIFE_BAR, COMB_SY_LIFE_BAR),
                    self.get_my_creature().get_pvs() // self.get_my_creature().get_max_pvs() * (COMB_SX_LIFE_BAR - BAR_ESP * 2))
        else:
            pygame.draw.rect(self.ecran, (128, 128, 128),
                             (COMB_X_ME, COMB_Y_ME - COMB_SY_LIFE_BAR * 2, COMB_SX_LIFE_BAR, COMB_SY_LIFE_BAR))
        self.ecran.blit(self.font.render("PV: {}".format(self.get_my_creature().get_pvs()), 1, (10, 10, 10)),
                        (COMB_X_ME, COMB_Y_ME - COMB_SY_LIFE_BAR - 8))

        # xp de ma créature
        upg_bar(self.ecran, (COMB_X_ME, COMB_Y_ME - COMB_SY_XP_BAR, COMB_SX_XP_BAR, COMB_SY_XP_BAR),
                int(self.get_my_creature().get_xp() / self.get_my_creature().get_seuil_xp() * (COMB_SX_XP_BAR - BAR_ESP * 2)),
                esp=1)

        # affichage des noms des créatures
        if self.indexer.get_captured(self.get_adversary().get_id()) or self.indexer.get_viewed(self.get_adversary().get_id()):
            self.ecran.blit(self.font.render("{} :: niv. {}".format(
                            self.indexer.get_by_id(self.get_adversary().get_id()).name,
                            self.get_adversary().get_niv()), 1, (10, 10, 10)),
                            (COMB_X_ADV, COMB_Y_ADV - COMB_SY_TXT_NAME - COMB_SY_LIFE_BAR - 10))
        else:
            self.ecran.blit(self.font.render("??? :: niv. {}".format(self.get_adversary().get_niv()),
                                             1, (10, 10, 10)),
                            (COMB_X_ADV, COMB_Y_ADV - COMB_SY_TXT_NAME - COMB_SY_LIFE_BAR - 10))
        self.ecran.blit(self.font.render("{} :: niv. {}".format(self.get_my_creature().get_pseudo(), self.get_my_creature().get_niv()),
                                         1, (10, 10, 10)),
                        (COMB_X_ME, COMB_Y_ME - COMB_SY_TXT_NAME - COMB_SY_LIFE_BAR - 4))
        etat = "Empoisonné" if self.get_my_creature().get_state() == SPEC_ETATS.poisone else "Brûlé" if self.get_my_creature().get_state() == SPEC_ETATS.brule else "Normal"
        self.ecran.blit(self.font.render(etat, 1, (10, 10, 10)),
                        (COMB_X_ME, COMB_Y_ME - COMB_SY_TXT_NAME - 4))

        # affichage d'un indicateur pour dire s'il on a déjà capturé la créature adverse ou non
        if self.indexer.get_captured(self.get_adversary()):
            self.ecran.blit(self.indic_captured, (COMB_X_ADV + COMB_CHECK_SX + 10, COMB_Y_ADV - COMB_SY_TXT_NAME))

        # affichage du choix des attaques
        i = 1
        for atk in self.get_my_creature().get_attacks():
            color = (180, 180, 50) if i - 1 != self.selected_atk else (50, 180, 180)
            pygame.draw.rect(self.ecran, color,
                             (COMB_X_ATK, COMB_Y_ADV + COMB_SY_ADV + (COMB_SY_ATK_FIELD + 10) * i,
                              COMB_SX_ATK_FIELD, COMB_SY_ATK_FIELD))
            self.ecran.blit(self.font.render(atk.get_nom() +
                                             ", dégâts: " + str(atk.get_dgts()), 1, (10, 10, 10)),
                            (COMB_X_ATK, COMB_Y_ADV + COMB_SY_ADV + (COMB_SY_ATK_FIELD + 10) * i))
            self.ecran.blit(self.font.render("Description: " + atk.get_texte(), 1, (10, 10, 10)),
                            (COMB_X_ATK, COMB_Y_ADV + COMB_SY_ADV + (COMB_SY_ATK_FIELD + 10) * i + COMB_SY_TXT_NAME))
            i += 1

        # affichage du nombre PPS
        self.ecran.blit(self.font.render("PP : " + str(self.get_my_creature().get_pps()) + "/" +
                                         str(self.get_my_creature().get_max_pps()), 1, (10, 10, 10)),
                        (COMB_X_ATK, COMB_Y_ADV + COMB_SY_ADV + COMB_SY_ATK_FIELD))