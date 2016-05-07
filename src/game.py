# coding=utf-8

import socket

import carte
import debug
import indexer
import atk_sys
import money_mgr
import tab_types
import personnage
import captureurs
import chat_manager
import menu_in_game
import music_player
import equipe_manager
import computer_manager
import renderer_manager
import zones_attaques_manager
from constantes import *
from gui import GUISauvegarde, GUIBulleWaiting
from utils import uscreenschot
from creatures_mgr import Creature
from aventure_manager import Adventure
from parametres import ParametresManager
from controller import JoystickController
from exceptions import FonctionnaliteNonImplementee
from network_event_listener import NetworkEventsListener
# from fpsregulator import IAFPS

from animator import CinematiqueCreator


class Game:
    def __init__(self, ecran, adventure: Adventure, s: socket.socket=None,
                 p: tuple=('127.0.0.1', 5500)):
        self.__start_at__ = 0

        self.adventure = adventure

        # self.fps_regulator = IAFPS(FPS_base)
        self.fps_regulator = ree.create_clock()
        self.continuer = 1
        self.ecran = ecran
        self.sock = s
        self.params = p
        self.renderer_manager = renderer_manager.RendererManager()
        self.show_fps = False

        # Polices
        self.police_normale = ree.load_font(POLICE_PATH, POL_NORMAL_TAILLE)
        self.police_grande = ree.load_font(POLICE_PATH, POL_GRANDE_TAILLE)
        self.police_petite = ree.load_font(POLICE_PATH, POL_PETITE_TAILLE)

        # Managers
        self.carte_mgr = carte.CartesManager(self.ecran, self.renderer_manager, self.police_normale)
        self.oth_persos_mgr = personnage.OthPersonnagesManager(self.ecran, self.carte_mgr)
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
        self.mini_map = carte.CarteRenderer(self.ecran, self.police_normale, self.adventure)
        self.attaques_table = atk_sys.AttaquesTable()
        self.parametres = ParametresManager()
        self.musics_player = music_player.MusicPlayer()

        # Entités
        self.personnage = personnage.Personnage(self.carte_mgr, self.ecran, self.police_grande)

        # Contrôles
        self.controles = {}
        self.controles_joy = {}
        self.joystick = None

        self.__ctrls = {}
        self._default_dt = 1.0
        self._play_music = True
        self._play_anims = True

    def load(self):
        for i in carte.maps_retriver("http://dev.jeanba.fr/mapmaker_web/public"):
            yield i

        self.parametres.load()
        yield 1

        self.controles = self.parametres.get("controls")
        yield 1
        self.controles_joy = self.parametres.get("joy_controls")
        yield 1
        self.__ctrls = self.parametres.get("secured_controls")
        yield 1
        self._default_dt = self.parametres.get("delta_time")["default"]
        yield 1
        self._play_music = self.parametres.get("music")
        yield 1
        self._play_anims = self.parametres.get("play_anims")
        yield 1

        self.personnage.load()
        yield 1
        self.carte_mgr.load()
        yield 1
        for i in self.indexeur.load():
            yield i
        self.equipe_mgr.load()
        yield 1
        self.pc_mgr.load()
        yield 1
        self.zones_manager.load()
        yield 1
        self.money.load()
        yield 1
        self.attaques_table.load()
        yield 1

        self.chat_mgr.update_quit_event(K_ESCAPE)
        yield 1

        self.network_ev_listener.add_controler('perso', self.personnage)
        yield 1
        self.network_ev_listener.add_controler('others', self.oth_persos_mgr)
        yield 1
        self.network_ev_listener.add_controler('adventure', self.adventure)
        yield 1

        self.chat_mgr.add_controler("perso", self.personnage)
        yield 1
        self.chat_mgr.add_controler("adventure", self.adventure)
        yield 1
        self.chat_mgr.add_controler("equipe", self.equipe_mgr)
        yield 1
        self.chat_mgr.add_controler("computer", self.pc_mgr)
        yield 1
        self.chat_mgr.add_controler("music", self.musics_player)
        yield 1
        self.chat_mgr.add_controler("renderer", self.renderer_manager)
        yield 1

        self.carte_mgr.add_perso(self.personnage)
        yield 1

        self.indexeur.add_attacks_table(self.attaques_table)
        yield 1

        self.tab_types.init_tab()
        yield 1

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

    def process_event(self, event, dt: int):
        if self.joystick:
            self.joystick.update_states()

        if event == QUIT:
            if self.network_ev_listener.is_enabled():
                self.network_ev_listener.disconnect()
            self.musics_player.fadeout(300)
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
        if event == (KEYUP, self.controles[SCREENSCHOT]) or \
                (self.joystick and self.joystick.is_button_pressed(self.controles_joy[SCREENSCHOT]["button"])):
            self.screenshot()
        if event == (KEYUP, self.controles[SHOW_FPS]) or \
                (self.joystick and self.joystick.is_button_pressed(self.controles_joy[SHOW_FPS]["button"])):
            self.show_fps = not self.show_fps
        if event == (KEYUP, self.controles[CHAT]) or \
                (self.joystick and self.joystick.is_button_pressed(self.controles_joy[CHAT]["button"])):
            if not self.renderer_manager.get_renderer() == RENDER_CHAT:
                self.renderer_manager.change_renderer_for(RENDER_CHAT)

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

    def process_events_carte(self, event, dt: int=1):
        if event == (KEYUP, self.controles[MENU]):
            self.renderer_manager.invert_renderer()
        if event == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.mini_map.clic(xp, yp)
        if event == (MOUSEBUTTONDOWN, 5):
            self.mini_map.increase_transparency()
        if event == (MOUSEBUTTONDOWN, 4):
            self.mini_map.decrease_transparency()

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.invert_renderer()
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                xp, yp = ree.get_mouse_pos()
                self.mini_map.clic(xp, yp)

    def process_events_save(self, event, dt: int=1):
        pass

    def process_events_pokedex(self, event, dt: int=1):
        if event == (KEYDOWN, self.controles[MENU]):
            self.renderer_manager.invert_renderer()
        if event == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.indexeur.clic(xp, yp)

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                xp, yp = ree.get_mouse_pos()
                self.indexeur.clic(xp, yp)
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.invert_renderer()

    def process_events_pc(self, event, dt: int=1):
        if event == (KEYDOWN, self.controles[MENU]):
            self.renderer_manager.invert_renderer()
        if event == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.pc_mgr.clic(xp, yp)

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                xp, yp = ree.get_mouse_pos()
                self.pc_mgr.clic(xp, yp)
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.invert_renderer()

    def process_events_menu_in_game(self, event, dt: int=1):
        if event == (KEYDOWN, self.controles[MENU]):
            self.renderer_manager.invert_renderer()
        if event == (KEYDOWN, self.__ctrls[NEXT_PAGE]):
            self.menu_in_game.next()
        if event == (KEYDOWN, self.__ctrls[PREVIOUS_PAGE]):
            self.menu_in_game.previous()
        if event == (KEYDOWN, self.controles[VALIDATION]):
            new_renderer = self.menu_in_game.valider_choix()
            self.renderer_manager.change_renderer_for(new_renderer)
            if new_renderer == RENDER_INVENTAIRE:
                self.personnage.inventaire.open(RENDER_GAME)
        if event == MOUSEBUTTONUP:
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

        self.menu_in_game.mouseover(ree.get_mouse_pos())

    def process_events_creatures(self, event, dt: int=1):
        if event == (KEYDOWN, self.controles[MENU]):
            self.renderer_manager.invert_renderer()
        if event == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.equipe_mgr.clic(xp, yp)

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                xp, yp = ree.get_mouse_pos()
                self.equipe_mgr.clic(xp, yp)
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.invert_renderer()

    def process_events_chat(self, event, dt: int=1):
        if self.chat_mgr.is_running():
            self.chat_mgr.event(event)
        else:
            self.renderer_manager.invert_renderer()

    def process_events_boutique(self, event, dt: int=1):
        raise FonctionnaliteNonImplementee

    def process_events_combat(self, event, dt: int=1):
        if event == (KEYDOWN, self.__ctrls[NEXT_PAGE]) or event == (KEYDOWN, self.__ctrls[DOWN_PAGE]):
            self.cur_combat.next()
        if event == (KEYDOWN, self.__ctrls[PREVIOUS_PAGE]) or event == (KEYDOWN, self.__ctrls[UP_PAGE]):
            self.cur_combat.previous()
        if event == (KEYDOWN, self.controles[VALIDATION]):
            self.cur_combat.valide()
        if event == (KEYDOWN, self.controles[MENU]):
            self.renderer_manager.change_renderer_for(RENDER_INVENTAIRE)
            self.personnage.inventaire.open(RENDER_COMBAT)
        if event == MOUSEBUTTONUP:
            xp, yp = event.pos
            if event.button == 1:
                self.cur_combat.clic(xp, yp)
        if event == MOUSEMOTION:
            xp, yp = event.pos
            self.cur_combat.mouseover(xp, yp)

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            xp, yp = ree.get_mouse_pos()
            self.cur_combat.mouseover(xp, yp)
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                xp, yp = ree.get_mouse_pos()
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
            ree.set_mouse_pos(ree.get_mouse_pos()[0], ree.get_mouse_pos()[1] - JOY_DEPLACE_SOURIS)
        if self.joystick.get_axis(self.controles_joy[BAS]["axis"]["nb"]) == self.controles_joy[BAS]["axis"]["value"]:
            ree.set_mouse_pos(ree.get_mouse_pos()[0], ree.get_mouse_pos() + JOY_DEPLACE_SOURIS)
        if self.joystick.get_axis(self.controles_joy[GAUCHE]["axis"]["nb"]) == self.controles_joy[GAUCHE]["axis"]["value"]:
            ree.set_mouse_pos(ree.get_mouse_pos()[0] - JOY_DEPLACE_SOURIS, ree.get_mouse_pos())
        if self.joystick.get_axis(self.controles_joy[DROITE]["axis"]["nb"]) == self.controles_joy[DROITE]["axis"]["value"]:
            ree.set_mouse_pos(ree.get_mouse_pos()[0] + JOY_DEPLACE_SOURIS, ree.get_mouse_pos())

    def process_events_inventaire(self, event, dt: int=1):
        if event == (KEYDOWN, self.controles[MENU]):
            self.renderer_manager.change_for_last_renderer()
            self.personnage.inventaire.close()
        if event == (KEYDOWN, self.__ctrls[NEXT_PAGE]):
            self.personnage.inventaire_next()
        if event == (KEYDOWN, self.__ctrls[PREVIOUS_PAGE]):
            self.personnage.inventaire_previous()
        if event == MOUSEBUTTONUP:
            xp, yp = event.pos
            self.personnage.inventaire_clic(xp, yp)

        # joystick
        if self.joystick:
            self.joystick_deplace_souris()
            if self.joystick.is_button_pressed(self.controles_joy[VALIDATION]["button"]):
                xp, yp = ree.get_mouse_pos()
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
            done(self)
        elif self.personnage.inventaire.get_obj_messenger().pour["renderer"] == RENDER_COMBAT:
            if self.cur_combat:
                ball = captureurs.CapturersTable.get_ball_with_id(self.personnage.inventaire.get_obj_messenger().objet["id"])
                passed = len([1 for _ in range(MAX_ESSAIS_BALL) if ball.use(self.cur_combat.get_adversary())])
                done(self)
                if passed / MAX_ESSAIS_BALL >= PERCENT_CAPTURE_NECESSAIRE:
                    self.cur_combat.end_fight_for_capture()
                else:
                    g = GUIBulleWaiting(
                        self.ecran, (POS_BULLE_X, POS_BULLE_Y),
                        "Zut alors ! La capture a ratée :(",
                        self.police_normale
                    )
                    g.update()
                    del g
        elif self.personnage.inventaire.get_obj_messenger().pour["renderer"] == RENDER_CREATURES:
            if self.equipe_mgr.is_a_creature_selected():
                cat, new = self.personnage.inventaire.get_obj_messenger().objet["spec"], \
                    self.personnage.inventaire.get_obj_messenger().objet["new"]
                new += self.equipe_mgr.get_selected_creature().get_specs()[cat]
                self.equipe_mgr.get_selected_creature().set_spec(categorie=cat, new=new)
                done(self)

    def process_events_game(self, event, dt: int):
        # clavier
        if event == (KEYDOWN, self.controles[HAUT]):
            self.personnage.move(HAUT, dt)
        if event == (KEYDOWN, self.controles[BAS]):
            self.personnage.move(BAS, dt)
        if event == (KEYDOWN, self.controles[GAUCHE]):
            self.personnage.move(GAUCHE, dt)
        if event == (KEYDOWN, self.controles[DROITE]):
            self.personnage.move(DROITE, dt)
        if event == (KEYDOWN, self.controles[MENU]):
            self.renderer_manager.change_renderer_for(RENDER_MENU_IN_GAME)

        if event == (KEYUP, self.controles[HAUT]):
            self.personnage.end_move()
        if event == (KEYUP, self.controles[BAS]):
            self.personnage.end_move()
        if event == (KEYUP, self.controles[GAUCHE]):
            self.personnage.end_move()
        if event == (KEYUP, self.controles[DROITE]):
            self.personnage.end_move()

        if event == (KEYUP, self.controles[VALIDATION]):
            self.personnage.search_and_talk_to_pnj()
        if event == (KEYUP, self.controles[MAJ]):
            self.personnage.change_moving_state()

        # joystick
        if self.joystick:
            if self.joystick.is_button_pressed(self.controles_joy[MENU]["button"]):
                self.renderer_manager.change_renderer_for(RENDER_MENU_IN_GAME)

            if self.joystick.get_axis(self.controles_joy[HAUT]["axis"]["nb"]) == self.controles_joy[HAUT]["axis"]["value"]:
                self.personnage.move(HAUT, dt)
            else:
                self.personnage.end_move()

            if self.joystick.get_axis(self.controles_joy[BAS]["axis"]["nb"]) == self.controles_joy[BAS]["axis"]["value"]:
                self.personnage.move(BAS, dt)
            else:
                self.personnage.end_move()

            if self.joystick.get_axis(self.controles_joy[GAUCHE]["axis"]["nb"]) == self.controles_joy[GAUCHE]["axis"]["value"]:
                self.personnage.move(GAUCHE, dt)
            else:
                self.personnage.end_move()

            if self.joystick.get_axis(self.controles_joy[DROITE]["axis"]["nb"]) == self.controles_joy[DROITE]["axis"]["value"]:
                self.personnage.move(DROITE, dt)
            else:
                self.personnage.end_move()

    def prepare(self):
        debug.println("Le jeu démarre ...")
        self.__start_at__ = time.time()

        # Variables ayant besoin d'être rechargées avant le lancement du jeu (en cas de lancement multiple du jeu)
        self.continuer = 1
        yield 1

        self.renderer_manager.clear_all()
        yield 1
        self.renderer_manager.ban_renderer(
            RENDER_COMBAT,
            RENDER_INVENTAIRE,
            RENDER_CREATURES,
            RENDER_POKEDEX,
            RENDER_CARTE,
            RENDER_MENU_IN_GAME,
            RENDER_BOUTIQUE,
            RENDER_SAVE,
            RENDER_PC
        )
        yield 1

        self.personnage.set_carte_mgr(self.carte_mgr)
        yield 1

        self.mini_map.load()
        yield 1

        self.pc_mgr.add_equipe(self.equipe_mgr)
        yield 1
        self.equipe_mgr.add_pc(self.pc_mgr)
        yield 1

        for i in self.load():
            yield i

        ree.init_joystick()
        yield 1
        if ree.count_joysticks() > 0:
            joystick = ree.create_joystick()
            joystick.init()
            self.joystick = JoystickController(joystick)
            debug.println("Un joystick a été trouvé")

        ree.set_key_repeat(200, 100)
        yield 1
        if self.joystick:
            self.joystick.set_repeat(40)

        self.musics_player.create_random_playlist()
        yield 1

        self.musics_player.select(self.musics_player.get_rdm_playlist().pop())
        yield 1

        debug.println("Le jeu a démarré en %3.4f sec" % (time.time() - self.__start_at__))

    def render(self, dt: float=1.0):
        if self.renderer_manager.can_i_render():
            self.carte_mgr.update(dt)

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
                self.cur_combat = atk_sys.Combat(self.ecran, self.equipe_mgr.get_creature(0), self.zones_manager,
                                                 self.carte_mgr.get_zid(), self.indexeur, self.police_normale,
                                                 self.tab_types, self.renderer_manager, self.equipe_mgr)
                self.cur_combat.find_adv()
            if self.cur_combat:
                if not self.cur_combat.is_finished():
                    self.cur_combat.update()
                else:
                    self.cur_combat.on_end()
                    self.renderer_manager.change_for_last_renderer()
                    self.cur_combat = None
            if not self.equipe_mgr.is_not_empty():
                self.renderer_manager.change_without_logging_last(RENDER_GAME)
        elif self.renderer_manager.get_renderer() == RENDER_MENU_IN_GAME:
            ree.draw_rect(self.ecran, (0, 0) + self.ecran.get_size(), (0, 0, 0))
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
            ree.draw_rect(self.ecran, (0, 0, 10 + texte.get_width(), 10 + texte.get_height()),
                                       (150, 150, 150))
            self.ecran.blit(texte, (5, 5))

    def start(self):
        # if self.adventure.get_progress() == 1:
        #     # on vient de commencer
        #     self.equipe_mgr.add_creature(
        #         Creature(ID_STARTER, self.indexeur.get_type_of(0), indexer=self.indexeur, alea_niv=0))
        #     self.equipe_mgr.get_creature(0).set_pseudo(self.adventure.get_values()['first creature name'])
        #     self.equipe_mgr.get_creature(0).add_attack("Charge", T_NORMAL, 10, "Charge l'ennemi de tout son poids")
        self.personnage.set_skin_path(self.adventure.get_values()['sprite'])

        while self.continuer:
            # FPS
            # self.fps_regulator.actualise() ; dt = self.fps_regulator.get_deltatime()
            dt = self.fps_regulator.tick()

            # Evénements
            self.process_event(ree.poll_event(), dt)
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
                                 "Spawns en bleu",
                                 "Passages en rouge",
                                 "- - Musique - -",
                                 "Is Playing : {}".format(self.musics_player.is_playing()),
                                 "Musique actuelle : {}".format(self.musics_player.get_music_id()),
                                 "Playlist vide : {}".format(not self.musics_player.get_rdm_playlist()),
                                 "- - Carte - -",
                                 "Zone id: {}".format(self.carte_mgr.get_zid()),
                                 "Map id : {}".format(self.carte_mgr.current_carte.id),
                                 "Offsets : {}".format([float("%4.3f" % i) for i in self.carte_mgr.get_ofs()]),
                                 "Entités affichées : {}".format(self.carte_mgr.get_draw_entites()),
                                 "- - Personnage - -",
                                 "Direction: {}".format(self.personnage.get_dir()),
                                 "Position: {}".format(self.personnage.get_real_pos()),
                                 "Position (cases): {}".format(self.personnage.get_pos_in_tiles()),
                                 "DivDt : {}".format(self.personnage.get_speed_diviseur()),
                                 "- - Réseau - -",
                                 "En réseau: {}".format(self.sock is not None),
                                 "Params: {}".format(self.params if self.sock is not None else "NA"),
                                 x=DEBUG_FEN_large - 200,
                                 line_width=200,
                                 sy=DEBUG_FEN_haut)

            if self._play_music:
                self.musics_player.play()

            ree.flip()

        self.renderer_manager.change_renderer_for(RENDER_SAVE)
        while True:
            dt = self.fps_regulator.tick(FPS_base)
            self.render(dt)

            ree.poll_event()

            ree.flip()

            if self.renderer_manager != RENDER_SAVE:
                break