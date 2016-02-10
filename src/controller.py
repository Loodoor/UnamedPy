__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

from constantes import *
from utils import uround


STATE = 0
TIME = 1


class JoystickController:
    def __init__(self, joystick: pygame.joystick.Joystick):
        """
            Comment utiliser cette classe ?
            1/ L'initialiser
            2/ à chaque tour de boucle (principale), appeler update_states()
            3/ gérer les événements avec les méthodes is_XXX_pressed(XXX)
            4/ récupérer les valeurs avec get_XXX(XXX) si la méthode is_XXX_pressed(XXX) a renvoyé True
        """
        self.joystick = joystick
        self.state = {
            # la valeur doit être un int, -1 / 0 / 1
            'axis': {
                axe: [0, time.time()] for axe in range(self.joystick.get_numaxes())
            },
            # les valeurs doivent être des int, -1 / 0 / 1
            'hat': {
                hat: [(0, 0), time.time()] for hat in range(self.joystick.get_numhats())
            },
            # la valeur doit être un int, 0 / 1
            'button': {
                button: [0, time.time()] for button in range(self.joystick.get_numbuttons())
            },
            # les valeurs doivent être des int, -1 / 0 / 1
            'ball': {
                ball: [(0, 0), time.time()] for ball in range(self.joystick.get_numballs())
            }
        }
        self.repeat = 2 / 1000

    def set_repeat(self, repeat: float):
        self.repeat = repeat / 1000

    def update_states(self):
        # axes
        for axis in self.state['axis'].keys():
            tmp = self.joystick.get_axis(axis)
            if tmp < -0.5:
                self.state['axis'][axis] = [-1, time.time()]
            elif tmp >= 0.5:
                self.state['axis'][axis] = [1, time.time()]
            else:
                self.state['axis'][axis] = [0, time.time()]

        # hats
        for hat in self.state['hat'].keys():
            self.state['hat'][hat] = [self.joystick.get_hat(hat), time.time()]

        # buttons
        for button in self.state['button'].keys():
            self.state['button'][button] = [self.joystick.get_button(button), time.time()]

        # balls
        for ball in self.state['ball'].keys():
            tmp_x, tmp_y = self.joystick.get_ball(ball)
            tmp_x = -1 if tmp_x < -0.5 else 1 if tmp_x >= 0.5 else 0
            tmp_y = -1 if tmp_y < -0.5 else 1 if tmp_y >= 0.5 else 0
            self.state['ball'][ball] = [(tmp_x, tmp_y), time.time()]

    def get_axis(self, axis):
        if axis in self.state['axis'].keys():
            if self.state['axis'][axis][STATE] != 0 and not uround((time.time() - self.state['axis'][axis][TIME]) % self.repeat, 0.1):
                return self.state['axis'][axis][STATE]
            return 0
        raise ValueError("L'axe n°{} n'existe pas".format(axis))

    def get_hat(self, hat):
        if hat in self.state['hat'].keys():
            if self.state['hat'][hat][STATE] != (0, 0) and not uround((time.time() - self.state['hat'][hat][TIME]) % self.repeat, 0.1):
                return self.state['hat'][hat][STATE]
            return 0, 0
        raise ValueError("Le hat n°{} n'existe pas".format(hat))

    def get_button(self, button):
        if button in self.state['button'].keys():
            if self.state['button'][button][STATE] != 0 and not uround((time.time() - self.state['button'][button][TIME]) % self.repeat, 0.1):
                return self.state['button'][button][STATE]
            return 0
        raise ValueError("Le bouton n°{} n'existe pas".format(button))

    def get_ball(self, ball):
        if ball in self.state['ball'].keys():
            if self.state['ball'][ball][STATE] != (0, 0) and not uround((time.time() - self.state['ball'][ball][TIME]) % self.repeat, 0.1):
                return self.state['ball'][ball][STATE]
            return 0, 0
        raise ValueError("La ball n°{} n'existe pas".format(ball))

    def is_button_pressed(self, button):
        return 0 != self.get_button(button)

    def is_hat_pressed(self, hat):
        return (0, 0) != self.get_hat(hat)

    def is_ball_pressed(self, ball):
        return (0, 0) != self.get_ball(ball)

    def is_axis_pressed(self, axis):
        return 0 != self.get_axis(axis)