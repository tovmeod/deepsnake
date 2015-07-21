__author__ = 'avraham'

import pygame
from numpy import random


class Keys(object):
    noop = 0
    up = 1
    down = 2
    left = 3
    right = 4
    actions = (noop, up, down, left, right)

keys ={pygame.K_UP: Keys.up, pygame.K_DOWN: Keys.down, pygame.K_LEFT: Keys.left, pygame.K_RIGHT: Keys.right}


class Subscriber(object):
    def decide(self):
        return random.choice(Keys.actions)

    def get_pressed(self):
        key_pressed = pygame.key.get_pressed()
        for k, v in keys.iteritems():
            if key_pressed[k]:
                return v
        return Keys.noop

    def state_changed(self):
        pass

    def dead(self):
        pass