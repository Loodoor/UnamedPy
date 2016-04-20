# coding=utf-8

from gui import GUIBulle, GUIBulleWaiting, GUIBulleAsking, GUIBulle2Choices
from constantes import *
from utils import upg_bar
import creatures_mgr
from zones_attaques_manager import ZonesManager
import debug


def calcul_degats(degats_basiques: int, specs_atk: dict, specs_def: dict, coeff_types: int, my_type: int) -> int:
    x = 1.3 if specs_atk[ATK_TYP] == my_type else 1
    return (((specs_atk[SPEC_NIV] * 0.4 + 2) * x * degats_basiques / (specs_def[SPEC_DEF] * 50)) + 2) * coeff_types


def calcul_esquive(specs_atk: list, specs_def: list) -> bool:
    return True if specs_atk[SPEC_VIT] >= 2 * specs_def[SPEC_VIT] else False


Y_ADV_FALL = 0


class AttaquesTable:
    def __init__(self):
        self.table = []
        self._attacks = {}
        self.path = os.path.join("..", "assets", "configuration", "attaques" + EXTENSION)

    def can_i_learn(self, type_crea: int, attaque_name: str, attacks_learnt: list) -> bool:
        attacks_learnt = [atk.get_nom() for atk in attacks_learnt]
        if attaque_name in self._attacks.keys():
            obligator = self._attacks[attaque_name]
            if type_crea in obligator and not (attaque_name in attacks_learnt):
                return True
            return False
        return True

    def get_attack_from_name(self, name: str):
        for attack in self.table:
            if attack.get_nom() == name:
                return attack
        return GLOBAL_ERROR

    def get_all_attacks_with_type(self, type_: int):
        work = []
        for attack in self.table:
            if attack.get_type() == type_:
                work.append(attack)
        return work

    def load(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                datas = file.read()
        except OSError:
            datas = []

        self._traiter_datas(datas)

    def _traiter_datas(self, datas: list):
        dct = eval(datas)
        # nom::type::degats::description::cout::type1(int)-type2(int)-...&niveau_necessaire
        for attaque in dct:
            self._attacks[attaque['name']] = [
                None,  # liste de types pouvant apprendre l'attaque
            ]
            type_ = T_NORMAL
            cout_ = int(int(attaque['precision']) / 37)
            state_ = None
            if attaque.get("paralise", False):
                state_ = "paralise"
            if attaque.get("poison", False):
                state_ = "poison"
            if attaque.get("brule", False):
                state_ = "brule"
            self.table.append(creatures_mgr.Attaque(attaque['name'], type_, int(attaque['puissance']), attaque['effect'], state=state_, cout=cout_))


class Combat:
    def __init__(self, ecran, creature_joueur, zone: ZonesManager, zone_id: int, indexer, font, storage,
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
        self.indic_captured = ree.load_image(os.path.join("..", "assets", "gui", "captured.png"))
        self.font = font
        self.selected_atk = 0
        self.storage = storage
        self.renderer_manager = renderer_manager
        self.equipe = equipe
        self.fond = ree.load_image(os.path.join("..", "assets", "gui", "fd_combat.png"))
        self._fond_atk = ree.load_image(os.path.join("..", "assets", "gui", "fd_attaque.png"))
        self._fond_atk_selected = ree.load_image(os.path.join("..", "assets", "gui", "fd_attaque_selected.png"))
        self._fond_barre_vie = ree.load_image(os.path.join("..", "assets", "gui", "fd_barre_vie_creature.png"))
        self._fond_socle_pokemon = ree.load_image(os.path.join("..", "assets", "gui", "fd_combat_pokemon.png"))

    def on_start(self):
        debug.println("adv id", self.adversaire.get_id())
        debug.println("zid", self.zid)
        self.has_started = True
        global Y_ADV_FALL
        Y_ADV_FALL = 0

    def on_end(self):
        if not self.indexer.get_viewed(self.get_adversary().get_id()):
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
                self.has_attacked = False
                self.compteur_tour += 1
        else:
            g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                self.get_my_creature().get_pseudo() + " est paralisé ! Il n'a pas pu attaquer",
                                self.font)
            g.update()
            del g
            self.compteur_tour += 1

    def _manage_adversary_death(self):
        global Y_ADV_FALL
        while Y_ADV_FALL < 50:
            self.render()
            ree.flip()
        g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                            self.get_adversary().get_pseudo() + " est vaincu !", self.font)

        g.update()
        del g

        # gestion de l'xp
        level_up = self.get_my_creature().gagner_xp(self.get_adversary())
        self.render()  # mise à jour de la barre d'xp
        if not isinstance(level_up, (int, float)):
            g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                self.get_my_creature().get_pseudo() + " a gagné un niveau !",
                                self.font)
            g.update()
            del g

            has_level_up = False
            for new in level_up:
                g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                    [
                                        "Niveau : +1 !   Attaque : +" + str(new[SPEC_ATK]) + " !",
                                        "Défense : +" + str(new[SPEC_DEF]) + " !   Vitesse : +" + str(new[SPEC_VIT]) + " !",
                                        "Points de vie : +" + str(new[SPEC_MAX_PVS]) + " !"
                                    ], self.font)
                g.update()
                del g
                has_level_up = True
            if has_level_up:
                id_ = self.indexer.get_evolve_by_id_level(self.get_my_creature().get_id(), self.get_my_creature().get_niv())
                if id_:
                    self.get_my_creature().evolve_in(id_)
                for attaque in self.indexer.get_attacks_table().table:
                    if self.indexer.get_attacks_table().can_i_learn(
                        self.get_my_creature().get_type(),
                        attaque.get_nom(),
                        self.get_my_creature().get_attacks_learnt()
                    ):
                        if not self.get_my_creature().add_attack_bis(attaque):
                            g = GUIBulle2Choices(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                                 [
                                                     self.get_my_creature().get_pseudo() + " va apprendre {} !".format(attaque.get_nom()),
                                                     "Pour continuer, appuyez sur Entrée. Sinon appuyez sur une autre touche pour abandonner"
                                                 ],
                                                 self.font)
                            if g.update():
                                # faire choisir une attaque à oublier
                                g2 = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                                     "Quelle attaque {} doit oublier ?".format(self.get_my_creature().get_pseudo()),
                                                     self.font)
                                g2.update()
                                g3 = GUIBulleAsking(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Laquelle ? ", self.font)
                                g3.update()
                                attacks_names_available = [a.get_nom() for a in self.get_my_creature().get_attacks()]
                                while g3.get_text() not in attacks_names_available:
                                    g3 = GUIBulleAsking(self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                                                        [
                                                            " - ".join(attacks_names_available),
                                                            "Laquelle ? "
                                                        ],
                                                        self.font)
                                    g3.update()
                                self.get_my_creature().forget_attack_by_name(g3.get_text())
                                g4 = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                                     "{} va oublier l'attaque {} !".format(
                                                         self.get_my_creature().get_pseudo(),
                                                         g3.get_text()
                                                     ),
                                                     self.font)
                                g4.update()
                                self.get_my_creature().add_attack_bis(attaque)
                                del g2, g3, g4
                            del g
                        else:
                            g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                                self.get_my_creature().get_pseudo() + " a appris {} !".format(
                                                    attaque.get_nom()),
                                                self.font)
                            g.update()
                            del g
                        break
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
        if 0 <= self.selected_atk <= len(self.get_my_creature().get_attacks()) - 1:
            dgts = self.get_my_creature().attaquer(self.selected_atk)
            if dgts != -1:
                self.get_adversary().taper(calcul_degats(dgts,
                                                         self.get_my_creature().get_specs(),
                                                         self.get_adversary().get_specs(),
                                                         self.storage.get_coeff(
                                                             self.get_my_creature().get_type(),
                                                             self.get_adversary().get_type()
                                                         ),
                                                         self.get_my_creature().get_type()))

                state = self.get_my_creature().get_attacks()[self.selected_atk].get_state()
                if random.random() <= SPEC_ETAT_AFFECT_PERCENT:
                    if state == "poisone":
                        self.get_adversary().set_spec(SPEC_ETATS.poison)
                    if state == "brule":
                        self.get_adversary().set_spec(SPEC_ETATS.brule)
                    if state == "paralise":
                        self.get_adversary().set_spec(SPEC_ETATS.paralise)

                self.render()

                g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                    self.get_my_creature().get_pseudo() +
                                    " utilise " +
                                    self.get_my_creature().get_attacks()[self.selected_atk].get_nom() +
                                    " !",
                                    self.font)
                g.update()
                del g
            else:
                self.get_adversary().taper(
                    calcul_degats(self.get_my_creature().lutte(),
                                  self.get_my_creature().get_specs(),
                                  self.get_adversary().get_specs(),
                                  self.storage.get_coeff(
                                      self.get_my_creature().get_type(),
                                      self.get_adversary().get_type()
                                  ),
                                  self.get_my_creature().get_type()))
                self.render()

                g = GUIBulleWaiting(self.ecran, (COMB_X_BULLE, COMB_Y_BULLE),
                                    [
                                        "{} n'a plus de PP pour attaquer !".format(self.get_my_creature().get_pseudo()),
                                        "{} utilise lutte !".format(self.get_my_creature().get_pseudo())
                                    ], self.font)
                g.update()
                del g

    def valide(self):
        if 0 <= self.selected_atk < len(self.get_my_creature().get_attacks()):
            self.has_attacked = True
            self.attaquer()

    def mouseover(self, xp: int, yp: int):
        if COMB_X_ATK <= xp <= COMB_X_ATK + COMB_SX_ATK_FIELD:
            real_y = (yp - COMB_Y_ADV - COMB_SY_ADV) // (COMB_SY_ATK_FIELD + 10) - 1
            self.selected_atk = real_y

    def clic(self, xp: int, yp: int):
        self.mouseover(xp, yp)
        self.valide()

    def render(self):
        # en attendant d'avoir un paysage
        self.ecran.blit(self.fond, (COMB_X, COMB_Y))

        # affichage des "socles"
        self.ecran.blit(self._fond_socle_pokemon, (COMB_X_ADV - (self._fond_socle_pokemon.get_width() - 150) // 2, COMB_Y_ADV + (150 - self._fond_socle_pokemon.get_height())))
        self.ecran.blit(self._fond_socle_pokemon, (COMB_X_ME - (self._fond_socle_pokemon.get_width() - 150) // 2, COMB_Y_ME + (150 - self._fond_socle_pokemon.get_height())))

        # affichage des créatures
        global Y_ADV_FALL
        if self.get_adversary().is_dead() and Y_ADV_FALL < 50:
            Y_ADV_FALL += 0.25
        if Y_ADV_FALL < 50:
            self.ecran.blit(self.get_adversary().get_image(), (COMB_X_ADV, COMB_Y_ADV + Y_ADV_FALL))
        self.ecran.blit(self.get_my_creature().get_image(), (COMB_X_ME, COMB_Y_ME))

        # affichage des barres de vie
        if not self.get_adversary().is_dead():
            upg_bar(self.ecran, (COMB_X_ADV, COMB_Y_ADV - COMB_SY_LIFE_BAR, COMB_SX_LIFE_BAR, COMB_SY_LIFE_BAR),
                    self.get_adversary().get_pvs() // self.get_adversary().get_max_pvs() * (COMB_SX_LIFE_BAR - BAR_ESP * 2), bg=False)
        self.ecran.blit(self._fond_barre_vie, (COMB_X_ADV, COMB_Y_ADV - COMB_SY_LIFE_BAR))

        if not self.get_my_creature().is_dead():
            upg_bar(self.ecran, (COMB_X_ME, COMB_Y_ME - COMB_SY_LIFE_BAR, COMB_SX_LIFE_BAR, COMB_SY_LIFE_BAR),
                    self.get_my_creature().get_pvs() // self.get_my_creature().get_max_pvs() * (COMB_SX_LIFE_BAR - BAR_ESP * 2), bg=False)
        self.ecran.blit(self._fond_barre_vie, (COMB_X_ME, COMB_Y_ME - COMB_SY_LIFE_BAR))

        # mes pv
        self.ecran.blit(self.font.render("PV: {}".format(self.get_my_creature().get_pvs()), POL_ANTIALISING, (10, 10, 10)),
                        (COMB_X_ME + COMB_SX_LIFE_BAR + 14, COMB_Y_ME - COMB_SY_LIFE_BAR - 8))

        # xp de ma créature
        upg_bar(self.ecran, (COMB_X_ME, COMB_Y_ME + 10, COMB_SX_XP_BAR, COMB_SY_XP_BAR),
                int(self.get_my_creature().get_xp() / self.get_my_creature().get_seuil_xp() * (COMB_SX_XP_BAR - BAR_ESP * 2)),
                esp=1)

        # affichage des noms des créatures
        if self.indexer.get_viewed(self.get_adversary().get_id()):
            self.ecran.blit(self.font.render("{} :: niv. {}".format(
                            self.indexer.get_by_id(self.get_adversary().get_id()).name,
                            self.get_adversary().get_niv()), POL_ANTIALISING, (10, 10, 10)),
                            (COMB_X_ADV, COMB_Y_ADV - COMB_SY_TXT_NAME - COMB_SY_LIFE_BAR - 10))
        else:
            self.ecran.blit(self.font.render("??? :: niv. {}".format(self.get_adversary().get_niv()),
                                             POL_ANTIALISING, (10, 10, 10)),
                            (COMB_X_ADV, COMB_Y_ADV - COMB_SY_TXT_NAME - COMB_SY_LIFE_BAR - 10))
        self.ecran.blit(self.font.render("{} :: niv. {} ({})".format(self.get_my_creature().get_pseudo(), self.get_my_creature().get_niv(), self.get_my_creature().get_formatted_state()),
                                         POL_ANTIALISING, (10, 10, 10)),
                        (COMB_X_ME, COMB_Y_ME - COMB_SY_TXT_NAME - COMB_SY_LIFE_BAR - 10))

        # affichage d'un indicateur pour dire s'il on a déjà capturé la créature adverse ou non
        if self.indexer.get_captured(self.get_adversary()):
            self.ecran.blit(self.indic_captured, (COMB_X_ADV + COMB_CHECK_SX + 10, COMB_Y_ADV - COMB_SY_TXT_NAME))

        # affichage du choix des attaques
        i = 1
        for atk in self.get_my_creature().get_attacks():
            if i - 1 == self.selected_atk:
                self.ecran.blit(self._fond_atk_selected, (COMB_X_ATK, COMB_Y_ADV + COMB_SY_ADV + (COMB_SY_ATK_FIELD + 10) * i))
            else:
                self.ecran.blit(self._fond_atk, (COMB_X_ATK, COMB_Y_ADV + COMB_SY_ADV + (COMB_SY_ATK_FIELD + 10) * i))
            self.ecran.blit(self.font.render(atk.get_nom() +
                                             ", dégâts: " + str(atk.get_dgts()), POL_ANTIALISING, (10, 10, 10)),
                            (COMB_X_ATK + 32, COMB_Y_ADV + COMB_SY_ADV + (COMB_SY_ATK_FIELD + 10) * i + 4))
            self.ecran.blit(self.font.render("Description: " + atk.get_texte(), POL_ANTIALISING, (10, 10, 10)),
                            (COMB_X_ATK + 32, COMB_Y_ADV + COMB_SY_ADV + (COMB_SY_ATK_FIELD + 10) * i + COMB_SY_TXT_NAME + 2))
            i += 1

        # affichage du nombre PPS
        self.ecran.blit(self.font.render("PP : " + str(self.get_my_creature().get_pps()) + "/" +
                                         str(self.get_my_creature().get_max_pps()), POL_ANTIALISING, (10, 10, 10)),
                        (COMB_X_ATK, COMB_Y_ADV + COMB_SY_ADV + COMB_SY_ATK_FIELD - 10))
