#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
pymlsnake - A snake game for Mate Light
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band",]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"

import os
import sys
import getpass
import random
import socket

import pygame
from pygame.locals import *

class Snake(object):
    """
    The snake
    """
    def __init__(self):
        self.grow = False
        self.direction = 1
        self.tiles = []
        self.reset()

    def reset(self):
        """
        reset snake
        """
        self.grow = False
        self.direction = 1
        self.tiles = [(20, 8), (19, 8), (18, 7)]

    def get_pos(self):
        """
        returns the position of the head of the snake
        """
        return self.tiles[-1]

    def bite(self):
        """
        checks if you bite yourself in the tail
        """
        bite = 0
        for tile1 in self.tiles:
            for tile2 in self.tiles:
                if tile1[0] == tile2[0] and tile1[1] == tile2[1]:
                    bite = bite + 1
            if bite > 1:
                return True
            bite = 0
        return False

    def move(self):
        """
        add a new pixel to the snakes head and delete the last one
        """
        # add new tile to front
        if self.direction == 0:
            self.tiles.append((self.tiles[-1][0] - 1, self.tiles[-1][1]))
        elif self.direction == 1:
            self.tiles.append((self.tiles[-1][0] + 1, self.tiles[-1][1]))
        elif self.direction == 2:
            self.tiles.append((self.tiles[-1][0], self.tiles[-1][1] - 1))
        elif self.direction == 3:
            self.tiles.append((self.tiles[-1][0], self.tiles[-1][1] + 1))

        # check collision
        if self.tiles[-1][0] < 0 or self.tiles[-1][0] > 39:
            return False
        elif self.tiles[-1][1] < 0 or self.tiles[-1][1] > 15:
            return False
        elif self.bite():
            return False
        else:
            # delete last tile
            if not self.grow:
                self.tiles.pop(0)
            self.grow = False
            return True


class Game(object):
    """
    The game
    """
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        pygame.init()
        self.fps_clock = pygame.time.Clock()
        pygame.display.set_caption('PyMLSnake')
        pygame.display.set_mode((100, 100))

        self.color_red = (255, 0, 0)
        self.color_green = (0, 255, 0)
        self.color_blue = (0, 0, 255)
        self.color_black = (0, 0, 0)
        self.color_grey = (128, 128, 128)

        self.snake = Snake()
        self.gameover = False
        self.apple = (random.randrange(40), random.randrange(16))
        self.oldapple = self.apple
        self.reset()

        self.surface = []
        for y in range(16):
            row = []
            for x in range(40):
                row.append(self.color_black)
            self.surface.append(row)

    def render(self):
        """
        """
        display_data = []
        for y in self.surface:
            for x in y:
                for color in x:
                    display_data.append(color)

        checksum = bytearray([0, 0, 0, 0])
        data_as_bytes = bytearray(display_data)
        data = data_as_bytes + checksum
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (self.ip, self.port))

    def fill(self, color):
        """
        Fill the surface with a color
        """
        for y in range(16):
            for x in range(40):
                self.surface[y][x] = color

    def dot(self, pos, color):
        """
        Paint one dot with color at pos
        """
        self.surface[pos[1]][pos[0]] = color

    def eventhandler(self):
        """
        change the direction of the snake according to pressed keys
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if self.snake.direction != 1:
                        self.snake.direction = 0
                elif event.key == K_RIGHT:
                    if self.snake.direction != 0:
                        self.snake.direction = 1
                elif event.key == K_UP:
                    if self.snake.direction != 3:
                        self.snake.direction = 2
                elif event.key == K_DOWN:
                    if self.snake.direction != 2:
                        self.snake.direction = 3
                elif event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))

    def run(self):
        """
        contains the gameloop
        """
        while True:
            self.eventhandler()
            if not self.snake.move():
                break

            if self.snake.get_pos() == self.apple:
                self.score = self.score + 1
                self.oldapple = self.apple
                self.apple = (random.randrange(40), random.randrange(16))

            self.fill(self.color_black)
            self.dot(self.apple, self.color_green)

            for i in range(len(self.snake.tiles)):
                # paint dot
                self.dot(self.snake.tiles[i], self.color_red)

            if self.snake.tiles[0] == self.oldapple:
                self.snake.grow = True
                self.oldapple = (50, 50)

            pygame.display.update()
            self.render()
            self.fps_clock.tick(5 + self.score / 5)

        #TODO: write highscore and if this is a new one
        str(self.score)

    def reset(self):
        """
        reset game
        """
        self.score = 0
        try:
            hfile = open('pymlsnakescore', 'r')
            self.highscore = hfile.read()
            hfile.close()
        except IOError:
            self.highscore = '0'
        self.gameover = False

        self.snake.reset()
        self.apple = (random.randrange(40), random.randrange(16))


if __name__ == '__main__':
    GAME = Game('matelight.cbrp3.c-base.org', 1337)
    #GAME = Game('127.0.0.1', 1337)
    GAMELOOP = True
    while(GAMELOOP):
        GAMELOOP = GAME.run()
        GAME.reset()
