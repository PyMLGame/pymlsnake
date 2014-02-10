# -*- coding: utf-8 -*-

"""
Snake game object
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

# direction for snake travel
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class Snake(object):
    """
    The snake on the screen eating apples and crashing into things
    """
    def __init__(self, parts, direction, dimensions):
        """
        Create a snake with its initial parts and direction.
        """
        self.parts = parts  # last part is head
        self.direction = direction
        self.dimensions = dimensions
        self.grow = False

    def get_pos(self):
        """
        Returns the position of the head of the snake.
        """
        return self.parts[-1]

    def check_bite(self):
        """
        Checks if you bite yourself in the tail.
        """
        if len(self.parts) != len(set(self.parts)):
            return True
        else:
            return False

    def move(self):
        """
        Add a new pixel to the snakes head and delete the last one.
        """
        # add new tile to front
        head = self.parts[-1]
        if self.direction == UP:
            if head[1] == 0:
                self.parts.append((head[0], self.dimensions[1] - 1))
            else:
                self.parts.append((head[0], head[1] - 1))
        elif self.direction == DOWN:
            if head[1] == self.dimensions[1] - 1:
                self.parts.append((head[0], 0))
            else:
                self.parts.append((head[0], head[1] + 1))
        elif self.direction == LEFT:
            if head[0] == 0:
                self.parts.append((self.dimensions[0] - 1, head[1]))
            else:
                self.parts.append((head[0] - 1, head[1]))
        elif self.direction == RIGHT:
            if head[0] == self.dimensions[0] - 1:
                self.parts.append((0, head[1]))
            else:
                self.parts.append((head[0] + 1, head[1]))

        if self.check_bite():
            return False
        else:
            # delete last part (first in the list)
            if not self.grow:
                self.parts.pop(0)
            self.grow = False
            return True