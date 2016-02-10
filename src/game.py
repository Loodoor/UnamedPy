# coding=utf-8

import socket
import pygame
from pygame.locals import *

import carte
import indexer
import atk_sys
import money_mgr
import tab_types
import personnage
import chat_manager
import menu_in_game
import equipe_manager
import computer_manager
import renderer_manager
import zones_attaques_manager
from constantes import *
from gui import GUISauvegarde
from utils import uscreenschot
from fpsregulator import IAFPS
from aventure_manager import Adventure
from parametres import ParametresManager
from exceptions import FonctionnaliteNonImplementee
from network_event_listener import NetworkEventsListener
from controller import JoystickController


class Game:
    def __init__(self, ecran: pygame.Surface, perso_choice: str, adventure: Adventure, s: socket.socket=None,
                 p: tuple=('127.0.0.1', 5500), controles: dict={}):
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

        # Entités
        self.personnage = personnage.Personnage(self.ecran, self.police_grande, perso_choice)

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
        self.parametres = ParametresManager()
        self.parametres.load()

        # Contrôles
        self.controles = self.parametres.get("controls")
        self.controles.update(controles)
        self.controles_joy = self.parametres.get("joy_controls")
        controles = {}  # vider le dico à chaque fois !
        self.joystick = None

        self.__ctrls = self.parametres.get("secured_controls")

        self.load()

    def load(self):
        self.carte_mgr.load()
        self.personnage.load()
        self.indexeur.load()
        self.equipe_mgr.load()
        self.pc_mgr.load()
        self.zones_manager.load()
        self.money.load()

        self.chat_mgr.update_quit_event(self.controles[CHAT])

        self.network_ev_listener.add_controler('perso', self.personnage)
        self.network_ev_listener.add_controler('others', self.oth_persos_mgr)
        self.network_ev_listener.add_controler('adventure', self.adventure)

        self.tab_types.init_tab()

    def save(self):
        print("Sauvegarde ...")
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

        if event.type == QUIT:
            if self.network_ev_listener.enable():
                self.network_ev_listener.disconnect()
            self.save()
            sys.exit()

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
            raise FonctionnaliteNonImplementee("Cas non géré. Merci de reporter ce traceback à Folaefolc, main dev d'Unamed")

        # Global
        if event.type == KEYUP:
            if event.key == self.controles[SCREENSCHOT]:
                self.screenshot()
            if event.key == self.controles[SHOW_FPS]:
                self.show_fps = not self.show_fps
            if event.key == self.controles[CHAT]:
                if not self.renderer_manager.get_renderer() == RENDER_CHAT:
                    self.renderer_manager.change_renderer_for(RENDER_CHAT)
                else:
                    self.renderer_manager.invert_renderer()

    def process_events_carte(self, event: pygame.event, dt: int=1):
        """
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.invert_rendering()
        """
        raise FonctionnaliteNonImplementee

    def process_events_save(self, event: pygame.event, dt: int=1):
        pass

    def process_events_pokedex(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.indexeur.clic(xp, yp)

    def process_events_pc(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.pc_mgr.clic(xp, yp)

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
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            tmp = self.menu_in_game.clic(xp, yp)
            if tmp != RENDER_ERROR:
                self.renderer_manager.change_renderer_for(tmp)

        self.menu_in_game.mouseover(pygame.mouse.get_pos())

    def process_events_creatures(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.equipe_mgr.clic(xp, yp)

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
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            if event.button == 1:
                self.cur_combat.clic(xp, yp)
        if event.type == MOUSEMOTION:
            xp, yp = event.pos
            self.cur_combat.mouseover(xp, yp)

    def process_events_inventaire(self, event: pygame.event, dt: int=1):
        if event.type == KEYDOWN:
            if event.key == self.controles[MENU]:
                self.renderer_manager.invert_renderer()
            if event.key == self.__ctrls[NEXT_PAGE]:
                self.personnage.inventaire_next()
            if event.key == self.__ctrls[PREVIOUS_PAGE]:
                self.personnage.inventaire_previous()
        if event.type == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.personnage.inventaire_clic(xp, yp)

        # joystick

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
        self.move_perso(dt)

        # joystick
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

    def prepare(self):
        # Variables ayant besoin d'être rechargés avant le lancement du jeu (en cas de lancement multiple du jeu)
        self.continuer = 1

        self.renderer_manager.clear_all()
        self.renderer_manager.ban_renderer(RENDER_COMBAT)

        self.personnage.set_carte_mgr(self.carte_mgr)

        self.pc_mgr.add_equipe(self.equipe_mgr)
        self.equipe_mgr.add_pc(self.pc_mgr)

        self.load()

        pygame.key.set_repeat(200, 100)

        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            self.joystick = JoystickController(joystick)
            print("Un joystick a été trouvé")

        print("Le jeu démarre ...")

    def render(self, dt: int=1):
        self.carte_mgr.update() if self.renderer_manager.can_i_render() else None

        if self.renderer_manager.get_renderer() == RENDER_GAME:
            self.personnage.update()
            self.oth_persos_mgr.draw_them()
        elif self.renderer_manager.get_renderer() == RENDER_INVENTAIRE:
            self.personnage.inventaire_update()
        elif self.renderer_manager.get_renderer() == RENDER_CHAT:
            self.chat_mgr.update()
        elif self.renderer_manager.get_renderer() == RENDER_BOUTIQUE:
            raise FonctionnaliteNonImplementee
        elif self.renderer_manager.get_renderer() == RENDER_COMBAT:
            if self.equipe_mgr.is_not_empty() and not self.cur_combat:
                self.cur_combat = atk_sys.Combat(self.ecran, self.equipe_mgr.get_creature(0), self.zones_manager,
                                                 self.carte_mgr.get_zid(), self.indexeur, self.police_normale,
                                                 self.tab_types)
                self.cur_combat.find_adv()
                self.top, self.bottom, self.right, self.left = [False] * 4
            if self.cur_combat and not self.cur_combat.is_finished():
                self.cur_combat.update()
            if self.cur_combat.is_finished():
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
            raise FonctionnaliteNonImplementee
        elif self.renderer_manager.get_renderer() == RENDER_CREATURES:
            self.equipe_mgr.update()
        elif self.renderer_manager.get_renderer() == RENDER_POKEDEX:
            self.indexeur.update()
        elif self.renderer_manager.get_renderer() == RENDER_PC:
            self.pc_mgr.update()

        if self.show_fps:
            texte = self.police_normale.render("%3i FPS" % int(self.fps_regulator.get_fps()), 1, (0, 0, 0))
            pygame.draw.rect(self.ecran, (150, 150, 150), (0, 0, 10 + texte.get_width(), 10 + texte.get_height()))
            self.ecran.blit(texte, (5, 5))

    def start(self):
        self.prepare()

        while self.continuer:
            # FPS
            # self.fps_regulator.actualise() ; dt = self.fps_regulator.get_DeltaTime()
            dt = self.fps_regulator.tick(FPS_base)

            # Evénements
            self.process_event(pygame.event.poll(), dt)

            self.network_ev_listener.listen()

            # Affichage
            self.render(dt)

            pygame.display.flip()

        self.save()