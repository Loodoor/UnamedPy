# coding=utf-8

import socket
from pygame.locals import *

import carte
import debug
import indexer
import atk_sys
import money_mgr
import tab_types
import personnage
import chat_manager
import menu_in_game
import objets_manager
import equipe_manager
import computer_manager
import renderer_manager
import zones_attaques_manager
from constantes import *
from gui import GUISauvegarde
from utils import uscreenschot
# from fpsregulator import IAFPS
from creatures_mgr import Creature
from aventure_manager import Adventure
from parametres import ParametresManager
from controller import JoystickController
from exceptions import FonctionnaliteNonImplementee
from network_event_listener import NetworkEventsListener


class Game:
    def __init__(self, ecran: pygame.Surface, perso_choice: str, adventure: Adventure, s: socket.socket=None,
                 p: tuple=('127.0.0.1', 5500), controles: dict={}):
        self.__start_at__ = time.time()

        self.adventure = adventure

        # self.fps_regulator = IAFPS(FPS_base)
        self.fps_regulator = pygame.time.Clock()
        self.continuer = 1
        self.ecran = ecran
        self.sock = s
        self.params = p
        self.renderer_manager = renderer_manager.RendererManager()
        self.show_fps = False

        self.right = False
        self.left = False
        self.top = False
        self.bottom = False

        # Polices
        self.police_normale = pygame.font.Font(POLICE_PATH, POL_NORMAL_TAILLE)
        self.police_grande = pygame.font.Font(POLICE_PATH, POL_GRANDE_TAILLE)
        self.police_petite = pygame.font.Font(POLICE_PATH, POL_PETITE_TAILLE)

        # Managers
        self.carte_mgr = carte.CartesManager(self.ecran, self.renderer_manager)
        self.oth_persos_mgr = personnage.OthPersonnagesManager(self.ecran)
        self.indexeur = indexer.Indexer(self.ecran, self.police_grande, self.renderer_manager)
        self.equipe_mgr = equipe_manager.EquipeManager(self.ecran, self.police_grande, self.indexeur, self.renderer_manager)
        self.pc_mgr = computer_manager.ComputerManager(self.ecran, self.police_grande, self.renderer_manager)
        self.tab_types = tab_types.Storage()
        self.cur_combat = None
        self.menu_in_game = menu_in_game.Menu(self.ecran, self.police_grande)
        self.zones_manager = zones_attaques_manager.ZonesManager(self.indexeur)
        self.money = money_mgr.MoneyManager()
        self.gui_save_mgr = GUISauvegarde(self.ecran, self.police_grande)
        self.network_ev_listener = NetworkEventsListener(self.sock, self.params)
        self.chat_mgr = chat_manager.ChatManager(self.ecran, self.police_normale, self.network_ev_listener,
                                                 self.adventure.get_pseudo(), RANG_NUL)
        self.mini_map = carte.CarteRenderer(self.ecran, self.carte_mgr)
        self.objets_table = objets_manager.ObjectTable()
        self.attaques_table = atk_sys.AttaquesTable()
        self.parametres = ParametresManager()
        self.parametres.load()

        # Entités
        self.personnage = personnage.Personnage(self.carte_mgr, self.ecran, self.police_grande, perso_choice)

        # Contrôles
        self.controles = self.parametres.get("controls")
        self.controles.update(controles)
        self.controles_joy = self.parametres.get("joy_controls")
        controles = {}  # vider le dico à chaque fois !
        self.joystick = None

        self.__ctrls = self.parametres.get("secured_controls")

    def load(self):
        self.carte_mgr.load()
        self.personnage.load()
        self.indexeur.load()
        self.equipe_mgr.load()
        self.pc_mgr.load()
        self.zones_manager.load()
        self.money.load()
        self.attaques_table.load()

        self.chat_mgr.update_quit_event(self.controles[CHAT])

        self.network_ev_listener.add_controler('perso', self.personnage)
        self.network_ev_listener.add_controler('others', self.oth_persos_mgr)
        self.network_ev_listener.add_controler('adventure', self.adventure)

        self.carte_mgr.add_perso(self.personnage)

        self.indexeur.add_attacks_table(self.attaques_table)

        if self.adventure.get_progress() == 1:
            # on vient de commencer
            self.equipe_mgr.add_creature(Creature(ID_STARTER, self.indexeur.get_type_of(0), indexer=self.indexeur, alea_niv=0))
            self.equipe_mgr.get_creature(0).set_pseudo(self.adventure.get_values()['first creature name'])
            self.equipe_mgr.get_creature(0).add_attack("Charge", T_NORMAL, 10, "Charge l'ennemi de tout son poids")

        self.tab_types.init_tab()

    def save(self):
        debug.println("Sauvegarde ...")
        self.carte_mgr.save()
        self.personnage.save()
        self.parametres.save()
        # self.adventure.save()
        # self.money.save()
        # self.indexeur.save()
        # self.equipe_mgr.save()
        # self.pc_mgr.save()
        # self.zones_manager.save()

    def screenshot(self):
        uscreenschot(self.ecran)

    def process_event(self, event: pygame.event, dt: int=1):
        if self.joystick:
            self.joystick.update_states()

        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            if self.network_ev_listener.is_enabled():
                self.network_ev_listener.disconnect()
            self.continuer = False

        # Différents mode de gestion des événements
        if self.renderer_manager.get_renderer() == RENDER_GAME:
            # le jeu en lui même
            self.process_events_game(event, dt)
        elif self.renderer_manager.get_renderer() == RENDER_INVENTAIRE:
            # l'inventaire
            self.process_events_inventaire(event, dt)
        elif self.renderer_manager.get_renderer() == RENDER_CHAT:
            # le chat
            self.process_events_chat(event, dt)
        elif self.renderer_manager.get_renderer() == RENDER_COMBAT:
            # quand on est en combat
            if self.cur_combat:
                self.process_events_combat(event, dt)
        elif self.renderer_manager.get_renderer() == RENDER_BOUTIQUE:
            # dans une boutique
            self.process_events_boutique(event, dt)
        elif self.renderer_manager.get_renderer() == RENDER_MENU_IN_GAME:
            # le menu intermédiaire
            self.process_events_menu_in_game(event, dt)
        elif self.renderer_manager.get_renderer() == RENDER_SAVE:
            # la sauvegarde
            self.process_events_save(event, dt)
        elif self.renderer_manager.get_renderer() == RENDER_CARTE:
            # la mini carte
            self.process_events_carte(event, dt)
        elif self.renderer_manager.get_renderer() == RENDER_CREATURES:
            # quand on consulte ses creatures
            self.process_events_creatures(event, dt)
        elif self.renderer_manager.get_renderer() == RENDER_PC:
            # quand on est sur un PC pour gérer ses creatures
            self.process_events_pc(event, dt)
        elif self.renderer_manager.get_renderer() == RENDER_POKEDEX:
            # le pokedex
            self.process_events_pokedex(event, dt)
        elif self.renderer_manager.get_renderer() == RENDER_ERROR:
            # autre ...
            raise FonctionnaliteNonImplementee("Cas non géré. Merci de reporter ce traceback à Folaefolc, main dev' d'Unamed")

        # Global
        if event.type == KEYUP and event.key == self.controles[SCREENSCHOT] or \
                (self.joystick and self.joystick.is_button_pressed(self.controles_joy[SCREENSCHOT]["button"])):
            self.screenshot()
        if event.type == KEYUP and event.key == self.controles[SHOW_FPS] or \
                (self.joystick and self.joystick.is_button_pressed(self.controles_joy[SHOW_FPS]["button"])):
            self.show_fps = not self.show_fps
        if event.type == KEYUP and event.key == self.controles[CHAT] or \
                (self.joystick and self.joystick.is_button_pressed(self.controles_joy[CHAT]["button"])):
            if not self.renderer_manager.get_renderer() == RENDER_CHAT:
                self.renderer_manager.change_renderer_for(RENDER_CHAT)
            else:
                self.renderer_manager.invert_renderer()
        if event.type == KEYUP:
            if event.key == self.controles[HAUT]:
                self.top = False
                self.personnage.end_move()
            if event.key == self.controles[BAS]:
                self.bottom = False
                self.personnage.end_move()
            if event.key == self.controles[GAUCHE]:
                self.left = False
                self.personnage.end_move()
            if event.key == self.controles[DROITE]:
                self.right = False
                self.personnage.end_move()

        # Gestion des objets
        if self.personnage.inventaire.get_obj_messenger():
            to_go = self.personnage.inventaire.get_obj_messenger().pour["renderer"]
            if not self.renderer_manager.is_current_special() or self.renderer_manager.get_renderer() != to_go:
                if to_go == RENDER_COMBAT and not self.cur_combat:
                    pass
                else:
                    if not self.renderer_manager.is_current_special():
                        self.renderer_manager.change_for_special_renderer(to_go)
                self.personnage.inventaire.close()
            self._manage_object_action()

    def process_events_carte(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.invert_renderer()

    def process_events_save(self, event: pygame.event, dt: int=1):
        pass

    def process_events_pokedex(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.indexeur.clic(xp, yp)

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                xp, yp = pygame.mouse.get_pos()
                self.indexeur.clic(xp, yp)
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.invert_renderer()

    def process_events_pc(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.pc_mgr.clic(xp, yp)

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                xp, yp = pygame.mouse.get_pos()
                self.pc_mgr.clic(xp, yp)
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.invert_renderer()

    def process_events_menu_in_game(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
            if event.key == self.__ctrls[NEXT_PAGE]:
                self.menu_in_game.next()
            if event.key == self.__ctrls[PREVIOUS_PAGE]:
                self.menu_in_game.previous()
            if event.key == self.controles[VALIDATION]:
                new_renderer = self.menu_in_game.valider_choix()
                self.renderer_manager.change_renderer_for(new_renderer)
                if new_renderer == RENDER_INVENTAIRE:
                    self.personnage.inventaire.open(RENDER_GAME)
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            tmp = self.menu_in_game.clic(xp, yp)
            if tmp != RENDER_ERROR:
                self.renderer_manager.change_renderer_for(tmp)

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.invert_renderer()
            if self.joystick.is_button_pressed(self.controles_joy[NEXT_PAGE]["button"]):
                self.menu_in_game.next()
            if self.joystick.is_button_pressed(self.controles_joy[PREVIOUS_PAGE]["button"]):
                self.menu_in_game.previous()
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                new_renderer = self.menu_in_game.valider_choix()
                self.renderer_manager.change_renderer_for(new_renderer)
                if new_renderer == RENDER_INVENTAIRE:
                    self.personnage.inventaire.open(RENDER_GAME)

        self.menu_in_game.mouseover(pygame.mouse.get_pos())

    def process_events_creatures(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.equipe_mgr.clic(xp, yp)

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                xp, yp = pygame.mouse.get_pos()
                self.equipe_mgr.clic(xp, yp)
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.invert_renderer()

    def process_events_chat(self, event: pygame.event, dt: int=1):
        if self.chat_mgr.is_running():
            self.chat_mgr.event(event)
        else:
            self.renderer_manager.invert_renderer()

    def process_events_boutique(self, event: pygame.event, dt: int=1):
        raise FonctionnaliteNonImplementee

    def process_events_combat(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.__ctrls[NEXT_PAGE] or event.key == self.__ctrls[DOWN_PAGE]:
                self.cur_combat.next()
            if event.key == self.__ctrls[PREVIOUS_PAGE] or event.key == self.__ctrls[UP_PAGE]:
                self.cur_combat.previous()
            if event.key == self.controles[VALIDATION]:
                self.cur_combat.valide()
            if event.key == self.controles[MENU]:
                self.renderer_manager.change_renderer_for(RENDER_INVENTAIRE)
                self.personnage.inventaire.open(RENDER_COMBAT)
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            if event.button == 1:
                self.cur_combat.clic(xp, yp)
        if event.type == MOUSEMOTION:
            xp, yp = event.pos
            self.cur_combat.mouseover(xp, yp)

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            xp, yp = pygame.mouse.get_pos()
            self.cur_combat.mouseover(xp, yp)
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                xp, yp = pygame.mouse.get_pos()
                self.cur_combat.clic(xp, yp)
            if self.joystick.is_button_pressed(self.controles_joy[NEXT_PAGE]["button"]):
                self.cur_combat.next()
            if self.joystick.is_button_pressed(self.controles_joy[PREVIOUS_PAGE]["button"]):
                self.cur_combat.previous()
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.change_renderer_for(RENDER_INVENTAIRE)
                self.personnage.inventaire.open(RENDER_COMBAT)

    def joystick_deplace_souris(self):
        if self.joystick.get_axis(self.controles_joy[HAUT]["axis"]["nb"]) == self.controles_joy[HAUT]["axis"]["value"]:
            pygame.mouse.set_pos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - JOY_DEPLACE_SOURIS)
        if self.joystick.get_axis(self.controles_joy[BAS]["axis"]["nb"]) == self.controles_joy[BAS]["axis"]["value"]:
            pygame.mouse.set_pos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + JOY_DEPLACE_SOURIS)
        if self.joystick.get_axis(self.controles_joy[GAUCHE]["axis"]["nb"]) == self.controles_joy[GAUCHE]["axis"]["value"]:
            pygame.mouse.set_pos(pygame.mouse.get_pos()[0] - JOY_DEPLACE_SOURIS, pygame.mouse.get_pos()[1])
        if self.joystick.get_axis(self.controles_joy[DROITE]["axis"]["nb"]) == self.controles_joy[DROITE]["axis"]["value"]:
            pygame.mouse.set_pos(pygame.mouse.get_pos()[0] + JOY_DEPLACE_SOURIS, pygame.mouse.get_pos()[1])

    def process_events_inventaire(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.change_for_last_renderer()
                self.personnage.inventaire.close()
            if event.key == self.__ctrls[NEXT_PAGE]:
                self.personnage.inventaire_next()
            if event.key == self.__ctrls[PREVIOUS_PAGE]:
                self.personnage.inventaire_previous()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.personnage.inventaire_clic(xp, yp)

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                xp, yp = pygame.mouse.get_pos()
                self.personnage.inventaire_clic(xp, yp)
            if self.joystick.is_button_pressed(self.controles_joy[NEXT_PAGE]["button"]):
                self.personnage.inventaire_next()
            if self.joystick.is_button_pressed(self.controles_joy[PREVIOUS_PAGE]["button"]):
                self.personnage.inventaire_previous()
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.change_for_last_renderer()
                self.personnage.inventaire.close()

    def _manage_object_action(self):
        def done(game):
            game.renderer_manager.unlock_special()
            game.personnage.inventaire.clear_obj_messenger()
            game.render()

        if self.personnage.inventaire.get_obj_messenger().pour["renderer"] == RENDER_GAME:
            if self.personnage.inventaire.get_obj_messenger().objet["id"] == OBJETS_ID.Chaussures:
                self.personnage.run()
                done(self)
            if self.personnage.inventaire.get_obj_messenger().objet["id"] == OBJETS_ID.Velo:
                self.personnage.ride()
                done(self)
        elif self.personnage.inventaire.get_obj_messenger().pour["renderer"] == RENDER_COMBAT:
            if self.cur_combat:
                passed = len([1 for _ in range(MAX_ESSAIS_BALL) if random.random() <= self.personnage.inventaire.get_obj_messenger().objet["capture"]])
                done(self)
                if passed / MAX_ESSAIS_BALL >= PERCENT_CAPTURE_NECESSAIRE:
                    self.cur_combat.end_fight_for_capture()
        elif self.personnage.inventaire.get_obj_messenger().pour["renderer"] == RENDER_CREATURES:
            if self.equipe_mgr.is_a_creature_selected():
                cat, new = self.personnage.inventaire.get_obj_messenger().objet["spec"], \
                    self.personnage.inventaire.get_obj_messenger().objet["new"]
                new += self.equipe_mgr.get_selected_creature().get_specs()[cat]
                self.equipe_mgr.get_selected_creature().set_spec(categorie=cat, new=new)
                done(self)

    def process_events_game(self, event: pygame.event, dt: int=1):
        # clavier
        if event.type == KEYDOWN:
            if event.key == self.controles[HAUT]:
                self.top, self.bottom = True, False
            if event.key == self.controles[BAS]:
                self.top, self.bottom = False, True
            if event.key == self.controles[GAUCHE]:
                self.left, self.right = True, False
            if event.key == self.controles[DROITE]:
                self.left, self.right = False, True
            if event.key == self.controles[MENU]:
                self.renderer_manager.change_renderer_for(RENDER_MENU_IN_GAME)
        self.move_perso(dt)

        # joystick
        if self.joystick:
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.change_renderer_for(RENDER_MENU_IN_GAME)

            if self.joystick.get_axis(self.controles_joy[HAUT]["axis"]["nb"]) == self.controles_joy[HAUT]["axis"]["value"]:
                self.top, self.bottom = True, False
            else:
                self.top = False
                self.personnage.end_move()

            if self.joystick.get_axis(self.controles_joy[BAS]["axis"]["nb"]) == self.controles_joy[BAS]["axis"]["value"]:
                self.top, self.bottom = False, True
            else:
                self.bottom = False
                self.personnage.end_move()

            if self.joystick.get_axis(self.controles_joy[GAUCHE]["axis"]["nb"]) == self.controles_joy[GAUCHE]["axis"]["value"]:
                self.left, self.right = True, False
            else:
                self.left = False
                self.personnage.end_move()

            if self.joystick.get_axis(self.controles_joy[DROITE]["axis"]["nb"]) == self.controles_joy[DROITE]["axis"]["value"]:
                self.left, self.right = False, True
            else:
                self.right = False
                self.personnage.end_move()
            self.move_perso(dt)

    def move_perso(self, dt: int=1):
        if self.top:
            self.personnage.move(HAUT, dt)
        if self.bottom:
            self.personnage.move(BAS, dt)
        if self.right:
            self.personnage.move(DROITE, dt)
        if self.left:
            self.personnage.move(GAUCHE, dt)

    def reset_moves(self):
        self.top, self.bottom, self.right, self.left = [False] * 4

    def prepare(self):
        # Variables ayant besoin d'être rechargées avant le lancement du jeu (en cas de lancement multiple du jeu)
        self.continuer = 1

        self.renderer_manager.clear_all()
        self.renderer_manager.ban_renderer(
            RENDER_COMBAT,
            RENDER_INVENTAIRE,
            RENDER_CREATURES,
            RENDER_POKEDEX
        )

        self.personnage.set_carte_mgr(self.carte_mgr)

        self.pc_mgr.add_equipe(self.equipe_mgr)
        self.equipe_mgr.add_pc(self.pc_mgr)

        self.load()

        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            self.joystick = JoystickController(joystick)
            debug.println("Un joystick a été trouvé")

        pygame.key.set_repeat(200, 100)
        if self.joystick:
            self.joystick.set_repeat(40)

        debug.println("Le jeu démarre ...")

    def render(self, dt: int=1):
        self.carte_mgr.update() if self.renderer_manager.can_i_render() else None

        if self.renderer_manager.get_renderer() == RENDER_GAME:
            self.personnage.update()
            self.oth_persos_mgr.draw_them()
            self.carte_mgr.draw_top_layer()
        elif self.renderer_manager.get_renderer() == RENDER_INVENTAIRE:
            self.personnage.inventaire_update()
        elif self.renderer_manager.get_renderer() == RENDER_CHAT:
            self.chat_mgr.update()
        elif self.renderer_manager.get_renderer() == RENDER_BOUTIQUE:
            raise FonctionnaliteNonImplementee
        elif self.renderer_manager.get_renderer() == RENDER_COMBAT:
            if self.equipe_mgr.is_not_empty() and not self.cur_combat:
                self.reset_moves()
                self.cur_combat = atk_sys.Combat(self.ecran, self.equipe_mgr.get_creature(0), self.zones_manager,
                                                 self.carte_mgr.get_zid(), self.indexeur, self.police_normale,
                                                 self.tab_types, self.renderer_manager, self.equipe_mgr)
                self.cur_combat.find_adv()
                self.top, self.bottom, self.right, self.left = [False] * 4
            if self.cur_combat and not self.cur_combat.is_finished():
                self.cur_combat.update()
            if self.cur_combat.is_finished():
                self.cur_combat.on_end()
                self.renderer_manager.change_for_last_renderer()
                self.cur_combat = None
        elif self.renderer_manager.get_renderer() == RENDER_MENU_IN_GAME:
            self.menu_in_game.update()
        elif self.renderer_manager.get_renderer() == RENDER_SAVE:
            if not self.gui_save_mgr.is_saving():
                self.gui_save_mgr.start_saving(firstcall=self.save, callback=self.renderer_manager.invert_renderer)
            self.gui_save_mgr.update()
            if self.gui_save_mgr.is_saved_finished():
                self.gui_save_mgr.reinit()
        elif self.renderer_manager.get_renderer() == RENDER_CARTE:
            self.mini_map.update()
        elif self.renderer_manager.get_renderer() == RENDER_CREATURES:
            self.equipe_mgr.update()
        elif self.renderer_manager.get_renderer() == RENDER_POKEDEX:
            self.indexeur.update()
        elif self.renderer_manager.get_renderer() == RENDER_PC:
            self.pc_mgr.update()

        if self.show_fps:
            texte = self.police_normale.render("%3i FPS" % int(self.fps_regulator.get_fps()), 1, (0, 0, 0))
            pygame.draw.rect(self.ecran, (150, 150, 150),
                            (FEN_large - 10 + texte.get_width(), 0,
                             10 + texte.get_width(), 10 + texte.get_height()))
            self.ecran.blit(texte, (5, 5))

    def start(self):
        self.prepare()

        debug.println("Le jeu a démarré en %3.4f sec" % (time.time() - self.__start_at__))

        while self.continuer:
            # FPS
            # self.fps_regulator.actualise() ; dt = self.fps_regulator.get_DeltaTime()
            dt = self.fps_regulator.tick(FPS_base)

            # Evénements
            self.process_event(pygame.event.poll(), dt)

            self.network_ev_listener.listen()

            # Affichage
            self.render(dt)

            # Debug info
            debug.onscreen_debug(self.ecran, self.police_normale,
                                 "Créatures (poche): {}".format(len(self.equipe_mgr.get_all())),
                                 "Créatures (pc): {}".format(len(self.pc_mgr.get_all())),
                                 "Objet messenger : {}".format(self.personnage.inventaire.get_obj_messenger()),
                                 "- - Rendu - -",
                                 "Renderer: {}".format(self.renderer_manager.get_renderer()),
                                 "Delatime : %3.1f ms" % dt,
                                 "FPS : %3.2f" % self.fps_regulator.get_fps(),
                                 "- - Carte - -",
                                 "Zone id: {}".format(self.carte_mgr.get_zid()),
                                 "Map id : {}".format(self.carte_mgr.current_carte.id),
                                 "Offsets : {}".format([float("%4.3f" % i) for i in self.carte_mgr.get_ofs()]),
                                 "- - Personnage - -",
                                 "Direction: {}".format(self.personnage.get_dir()),
                                 "Position: {}".format(self.personnage.get_pos()),
                                 "Position (cases): {}".format(self.personnage.get_pos_in_tiles()),
                                 "UP: {} | DOWN: {}".format(self.top, self.bottom),
                                 "RIGHT: {} | LEFT: {}".format(self.right, self.left),
                                 "- - Réseau - -",
                                 "En réseau: {}".format(self.sock is not None),
                                 "Params: {}".format(self.params if self.sock is not None else "NA"),
                                 x=DEBUG_FEN_large - 200,
                                 line_width=200,
                                 sy=DEBUG_FEN_haut)

            pygame.display.flip()

        self.renderer_manager.change_renderer_for(RENDER_SAVE)
        while True:
            dt = self.fps_regulator.tick(FPS_base)
            self.render(dt)

            pygame.event.poll()

            pygame.display.flip()

            if self.renderer_manager != RENDER_SAVE:
                break