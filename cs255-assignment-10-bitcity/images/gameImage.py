# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremey Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>


import pygame
from pygame import time, image, Rect
from pygame.transform import scale

import glob
from images import imageDict as IMG

import os


class GameImage:

    """An image in the game."""

    def __init__(self, name):
        self.name = name
        self.fullName = os.path.join(os.path.dirname(__file__),
                                     self.name)
        self.surf = IMG.loadNonAlpha(name)
        self.width, self.height = self.surf.get_size()
        self.stretch()

    def draw(self, s, pos):
        """Blit the image onto the current surface."""
        s.blit(self.surf, pos)

    def stretch(self):
        newHeight = glob.Screen.HEIGHT
        newWidth = int((float(newHeight) / self.height) * self.width)
        self.surf = scale(self.surf, (newWidth, newHeight))
        self.width, self.height = self.surf.get_size()

if __name__ == "__main__":
    main()
