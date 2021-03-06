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


def parse_type(kind: str) -> int:
    if kind == "FEU":
        return T_FEU
    if kind == "EAU":
        return T_EAU
    if kind == "PLANTE":
        return T_PLANTE
    if kind == "ELEC":
        return T_ELEC
    if kind == "AIR":
        return T_AIR
    if kind == "TERRE":
        return T_TERRE
    if kind == "POISON":
        return T_POISON
    if kind == "LUMIERE":
        return T_LUMIERE
    if kind == "TENEBRE":
        return T_TENEBRE

    return T_NORMAL


def run_bulle(kind: str, ecran: ree.surf, texte: str or list, font: ree.font, pos: tuple=(POS_BULLE_X, POS_BULLE_Y)) -> str or bool or None:
    if kind == "waiting":
        g = GUIBulleWaiting(ecran, pos, texte, font)
        g.update()
        return
    elif kind == "asking":
        g = GUIBulleAsking(ecran, pos, texte, font)
        g.update()
        return g.get_text()
    elif kind == "choice":
        g = GUIBulle2Choices(ecran, pos, texte, font)
        return g.update()
    raise ValueError("This kind ('{}') for GUIBulle does not exist".format(kind))


Y_ADV_FALL = 0
Y_FALL = 0


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

    def get_attack_from_name(self, name: str) -> creatures_mgr.Attaque:
        for attack in self.table:
            if attack.get_nom() == name:
                return attack
        return GLOBAL_ERROR

    def get_all_attacks_with_type(self, type_: int) -> list:
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
        for attaque in dct:
            self._attacks[attaque['name']] = attaque['types_ok']  # liste de types pouvant apprendre l'attaque
            type_ = parse_type(attaque['a_type'])
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
        self.bulle_que_doit_faire = GUIBulle(self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Que doit faire ?", font)
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
        debug.println("[COMBAT] ID de l'adversaire", self.adversaire.get_id())
        debug.println("[COMBAT] Zone ID", self.zid)
        self.has_started = True
        global Y_ADV_FALL
        Y_ADV_FALL = 0
        global Y_FALL
        Y_FALL = 0

    def on_end(self):
        if not self.indexer.get_viewed(self.get_adversary().get_id()):
            name_for_crea = run_bulle("asking", self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Nom pour cette créature : ", self.font)
            self.indexer.add_name_to_crea(self.adversaire.get_id(), name_for_crea)
            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      "La créature a été ajouté au " + NOM_POKEDEX + " !")
        if not self.indexer.get_typeur().get_name(self.get_adversary().get_type()):
            type_name = run_bulle("asking", self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Nom pour ce type de créature : ", self.font)
            self.indexer.get_typeur().change_name(self.get_adversary().get_type(), type_name)
            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      "Le type a été ajouté au " + NOM_POKEDEX + " !")

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
        run_bulle("waiting", self.ecran, (POS_BULLE_Y, POS_BULLE_Y),
                  "Bravo ! Vous venez de capturer une nouvelle créature !",
                  self.font)
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
                self._manage_adversary_turn()
            self.compteur_tour += 1

            if self.get_adversary().is_dead():
                self._manage_adversary_death()
            if self.get_my_creature().is_dead():
                self._manage_my_death()

    def _gerer_etats(self):
        for crea in [self.get_my_creature(), self.get_adversary()]:
            if crea.get_state() == SPEC_ETATS.brule:
                crea.taper(SPEC_DGT_BRULURE(crea.get_niv()))
            if crea.get_state() == SPEC_ETATS.poisone:
                crea.taper(SPEC_DGT_POISON(crea.get_niv()))

    def _manage_adversary_turn(self):
        can_attack = True
        if self.get_adversary().get_state() == SPEC_ETATS.paralise:
            can_attack = SPEC_LUCK_OF_ATTACK(self.get_adversary().get_vit())

        if can_attack:
            self.attaquer(self.get_adversary(), self.get_my_creature(), random.randrange(len(self.get_adversary().get_attacks())))
        else:
            if self.get_adversary().get_pseudo() != DEFAULT_NAME_UNKNOWN:
                texte = self.get_adversary().get_pseudo() + " est paralisé ! Il n'a pas pu attaquer"
            else:
                texte = "L'ennemi est paralisé ! Il n'a pas pu attaquer"
            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      texte,
                      self.font)

    def _manage_my_turn(self):
        can_attack = True
        if self.get_my_creature().get_state() == SPEC_ETATS.paralise:
            can_attack = SPEC_LUCK_OF_ATTACK(self.get_my_creature().get_vit())

        if can_attack:
            self.bulle_que_doit_faire.set_text("Que doit faire " + self.get_my_creature().get_pseudo() + " ?")
            self.bulle_que_doit_faire.update()

            if self.has_attacked:
                self.has_attacked = False
        else:
            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      self.get_my_creature().get_pseudo() + " est paralisé ! Il n'a pas pu attaquer",
                      self.font)

    def _manage_my_death(self):
        global Y_FALL
        Y_FALL = 0
        while Y_FALL < 50:
            self.render()
            ree.flip()
        if "nuzlocke" not in CORE_SETTINGS:
            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      self.get_my_creature().get_pseudo() + " est vaincu !", self.font)
        else:
            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      self.get_my_creature().get_pseudo() + " est mort !", self.font)
            self.equipe.increment_death_counter()
            self.equipe.remove(self.get_my_creature())
            del self.creature_joueur

        self.is_running = False

    def _manage_adversary_death(self):
        global Y_ADV_FALL
        Y_ADV_FALL = 0
        while Y_ADV_FALL < 50:
            self.render()
            ree.flip()
        if "nuzlocke" not in CORE_SETTINGS:
            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      self.get_adversary().get_pseudo() + " est vaincu !", self.font)
        else:
            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      self.get_adversary().get_pseudo() + " est mort !", self.font)

        # gestion de l'xp
        level_up = self.get_my_creature().gagner_xp(self.get_adversary())
        self.render()  # mise à jour de la barre d'xp
        if not isinstance(level_up, (int, float)):
            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      self.get_my_creature().get_pseudo() + " a gagné un niveau !",
                      self.font)

            has_level_up = False
            for new in level_up:
                run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                          [
                              "Niveau : +1 !   Attaque : +" + str(new[SPEC_ATK]) + " !   Défense : +" + str(new[SPEC_DEF]) + " !",
                              "Vitesse : +" + str(new[SPEC_VIT]) + " !   Points de vie : +" + str(new[SPEC_MAX_PVS]) + " !"
                          ], self.font)
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
                            a = run_bulle("choice", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                                          [
                                              self.get_my_creature().get_pseudo() + " va apprendre {} !".format(
                                                  attaque.get_nom()),
                                              "Pour continuer, appuyez sur Entrée. Sinon appuyez sur une autre touche pour abandonner"
                                          ],
                                          self.font)
                            if a:
                                # faire choisir une attaque à oublier
                                run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                                          "Quelle attaque {} doit oublier ?".format(
                                              self.get_my_creature().get_pseudo()),
                                          self.font)

                                g3 = run_bulle("asking", self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Laquelle ? ", self.font)

                                attacks_names_available = [a.get_nom() for a in self.get_my_creature().get_attacks()]
                                while g3 not in attacks_names_available:
                                    g3 = run_bulle("asking", self.ecran, (POS_BULLE_X, POS_BULLE_Y), "Laquelle ? ",
                                                   self.font)

                                self.get_my_creature().forget_attack_by_name(g3)

                                run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                                          "{} va oublier l'attaque {} !".format(
                                              self.get_my_creature().get_pseudo(),
                                              g3
                                          ),
                                          self.font)
                                self.get_my_creature().add_attack_bis(attaque)
                        else:
                            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                                      self.get_my_creature().get_pseudo() + " a appris {} !".format(
                                          attaque.get_nom()),
                                      self.font)
                        break
        else:
            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      self.get_my_creature().get_pseudo() + " a gagné {} xp !".format(level_up),
                      self.font)

        self.is_running = False

    def is_finished(self):
        return not self.is_running

    def next(self):
        self.selected_atk = self.selected_atk + 1 if self.selected_atk + 1 < 4 else 0

    def previous(self):
        self.selected_atk = self.selected_atk - 1 if self.selected_atk > 0 else 3

    def attaquer(self, crea: creatures_mgr.Creature, adv: creatures_mgr.Creature, choice: int):
        dgts = crea.attaquer(choice)
        if dgts != -1:
            adv.taper(calcul_degats(dgts,
                                    crea.get_specs(),
                                    adv.get_specs(),
                                    self.storage.get_coeff(
                                        crea.get_type(),
                                        adv.get_type()
                                    ),
                                    crea.get_type()))

            state = crea.get_attacks()[choice].get_state()
            if random.random() <= SPEC_ETAT_AFFECT_PERCENT:
                if state == "poisone":
                    adv.set_state(SPEC_ETATS.poison)
                if state == "brule":
                    adv.set_state(SPEC_ETATS.brule)
                if state == "paralise":
                    adv.set_state(SPEC_ETATS.paralise)

            self.render()

            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      crea.get_pseudo() +
                      " utilise " +
                      crea.get_attacks()[choice].get_nom() +
                      " !",
                      self.font)
        else:
            adv.taper(
                calcul_degats(crea.lutte(),
                              crea.get_specs(),
                              adv.get_specs(),
                              self.storage.get_coeff(
                                  crea.get_type(),
                                  adv.get_type()
                              ),
                              crea.get_type()))
            self.render()

            run_bulle("waiting", self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                      [
                          "{} n'a plus de PP pour attaquer !".format(crea.get_pseudo()),
                          "{} utilise lutte !".format(crea.get_pseudo())
                      ], self.font)

    def valide(self):
        if 0 <= self.selected_atk < len(self.get_my_creature().get_attacks()):
            self.has_attacked = True
            self.attaquer(self.get_my_creature(), self.get_adversary(), self.selected_atk)

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
        # adversaire
        global Y_ADV_FALL
        if self.get_adversary().is_dead() and Y_ADV_FALL < 50:
            Y_ADV_FALL += 0.25
        if Y_ADV_FALL < 50:
            self.ecran.blit(self.get_adversary().get_image(), (COMB_X_ADV, COMB_Y_ADV + Y_ADV_FALL))
        # ma créature
        global Y_FALL
        if self.get_my_creature().is_dead() and Y_FALL < 50:
            Y_FALL += 0.25
        if Y_ADV_FALL < 50:
            self.ecran.blit(self.get_my_creature().get_image(), (COMB_X_ME, COMB_Y_ME + Y_FALL))

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
            self.ecran.blit(self.font.render(DEFAULT_NAME_UNKNOWN + " :: niv. {}".format(self.get_adversary().get_niv()),
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
