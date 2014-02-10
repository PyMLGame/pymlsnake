#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

"""
Snake for Mate Light
====================

This is a clone of the well known snake game for Mate Light using pymlgame.
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2013, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

import random

import pymlgame

from snake import Snake, UP, DOWN, LEFT, RIGHT


class Game(object):
    """
    The main game class that holds the gameloop.
    """
    def __init__(self, host, port, width, height):
        """
        Create a screen and define some game specific things.
        """
        self.host = host
        self.port = port
        self.width = width
        self.height = height
        self.screen = pymlgame.Screen(self.host, self.port,
                                      self.width, self.height)
        self.clock = pymlgame.Clock()
        self.ctlr = pymlgame.Controller(self.host, self.port + 1)

        part = (int(self.width / 2), int(self.height / 2))
        self.snake = Snake([(part[0] - 2, part[1]), (part[0] - 1, part[1]),
                            part], RIGHT, (self.width, self.height))
        self.gameover = False
        self.apple = self.generate_apple()
        self.apple_surface = pymlgame.Surface(1, 1)
        self.apple_surface.draw_dot((0, 0), pymlgame.GREEN)
        self.oldapple = self.apple
        self.score = 0
        self.highscore = self.get_highscore()

        self.reset()

    def update(self):
        """
        Update the screens contents in every loop.
        """
        if not self.snake.move():
                    self.gameover = True

        if self.snake.get_pos() == self.apple:
                self.score += 1
                self.oldapple = self.apple
                self.apple = self.generate_apple()

    def render(self):
        """
        Send the current screen content to Mate Light.
        """
        self.screen.reset()

        # draw snake
        surface = pymlgame.Surface(self.width, self.height)
        for part in self.snake.parts:
            surface.draw_dot(part, pymlgame.RED)
        self.screen.blit(surface)

        # draw apple
        self.screen.blit(self.apple_surface, self.apple)

        if self.snake.parts[0] == self.oldapple:
            self.snake.grow = True
            self.oldapple = None

        self.screen.update()

        # accelerate every 5 points by 1 fps
        self.clock.tick(5 + int(self.score / 5))

    def handle_events(self):
        """
        Loop through all events.
        """
        for event in self.ctlr.get_events():
            if event.type == pymlgame.NEWCTLR:
                print('new ctlr with uid:', event.uid)
            elif event.type == pymlgame.KEYDOWN:
                if event.button == pymlgame.CTLR_UP:
                    if self.snake.direction != DOWN:
                        self.snake.direction = UP
                elif event.button == pymlgame.CTLR_DOWN:
                    if self.snake.direction != UP:
                        self.snake.direction = DOWN
                elif event.button == pymlgame.CTLR_LEFT:
                    if self.snake.direction != RIGHT:
                        self.snake.direction = LEFT
                elif event.button == pymlgame.CTLR_RIGHT:
                    if self.snake.direction != LEFT:
                        self.snake.direction = RIGHT
            elif event.type == pymlgame.PING:
                print('ping from', event.uid)

    def gameloop(self):
        """
        A game loop that circles through the methods.
        """
        try:
            while not self.gameover:
                self.handle_events()
                self.update()
                self.render()
            print('game over - score:', self.score)
            print('current highscore:', self.highscore)
            if self.score > int(self.highscore):
                self.write_highscore()
        except KeyboardInterrupt:
            pass
        self.ctlr.quit()

    def reset(self):
        """
        Reset the game
        """
        self.score = 0
        self.highscore = self.get_highscore()
        self.gameover = False

        self.snake.reset()
        self.apple = self.generate_apple()

    def generate_apple(self):
        return (random.randrange(self.width),
                random.randrange(self.height))

    def write_highscore(self):
        """
        Write new highscore to a file.
        """
        try:
            with open('highscore', 'w') as f:
                if f.writable():
                    f.writelines(str(self.score))
            return True
        except IOError:
            return False

    @staticmethod
    def get_highscore():
        """
        Reads the current highscore from a file.
        """
        highscore = 0
        try:
            with open('highscore', 'r') as f:
                highscore = f.readline()
        except IOError:
            pass
        return highscore


if __name__ == '__main__':
    GAME = Game('127.0.0.1', 1337, 50, 28)
    GAME.gameloop()