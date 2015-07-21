import pygame
from controller import Keys


class SnakePart(object):
    def __init__(self, pos, color=(0, 255, 0)):
        self.m_x = pos[0]
        self.m_y = pos[1]
        self.x = self.m_x * 10
        self.y = self.m_y * 10
        self.color = color

    def blit(self,screen):
        rect = pygame.Rect(self.x, self.y, 10, 10)
        pygame.draw.rect(screen, self.color, rect)


class Snake(object):
    def __init__(self, width, height):
        self.x = 38
        self.y = 0

        self.length = 10

        self.tail = []
        self.time_tick = 40
        self.speed = 20
        self.time = 0
        self.last_key = None
        self.h_x = -1
        self.h_y = 0

        self.head_color = (0,0,255)
        self.head = SnakePart((self.x,self.y), self.head_color)
        self.point = 0
        self.is_dead = False

    def restart(self):
        self.x = 38
        self.y = 0
        self.is_dead = False
        self.length = 10
        self.tail = []
        self.speed = 1
        self.time = 0
        self.h_x = -1
        self.h_y = 0

    def update(self, dt, screen, subscriber):
        self.update_position(dt, subscriber)
        self.blit(screen)
        self.check_dead()

    def check_dead(self):
        for t in self.tail :
            if t.m_x == self.x and t.m_y == self.y:
                self.is_dead = True
            if self.x < 0 or self.x > 40 or self.y < 0 or self.y > 40:
                self.is_dead = True

    def increase_length(self, value, point):
        self.length += value
        self.point += point

    def update_position(self, dt, subs):
        self.time += dt
        # key_pressed = pygame.key.get_pressed()
        key_pressed = subs.get_pressed()
        # if key_pressed[pygame.K_UP] and self.h_y != +1:
        if key_pressed == Keys.up and self.h_y != +1:
            self.h_x = 0
            self.h_y = -1
        # elif key_pressed[pygame.K_DOWN] and self.h_y != -1:
        elif key_pressed == Keys.down and self.h_y != -1:
            self.h_x = 0
            self.h_y = +1
        # elif key_pressed[pygame.K_LEFT] and self.h_x != +1:
        elif key_pressed == Keys.left and self.h_x != +1:
            self.h_x = -1
            self.h_y = 0
        # elif key_pressed[pygame.K_RIGHT] and self.h_x != -1:
        elif key_pressed == Keys.right and self.h_x != -1:
            self.h_x = +1
            self.h_y = 0
        if self.time >= self.time_tick:
            self.tail.insert(0,SnakePart((self.x,self.y)))
            self.x += self.h_x
            self.y += self.h_y
            self.head.x,self.head.y = self.x*10,self.y*10
            if len(self.tail) > self.length:
                self.tail.pop(len(self.tail) -1)
            self.time = 0

    def blit(self,screen):
        for t in self.tail:
            t.blit(screen)
        self.head.blit(screen)
