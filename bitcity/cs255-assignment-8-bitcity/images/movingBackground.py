# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremey Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>
from pygame import key
from pygame import display
from pygame import Rect
import pygame.draw

from pygame.locals import *
import os

from images import gameImage as GI
import glob


class MovingBackground(object):

    """A class defining a moving background picture."""

    def __init__(self, s):
        """Constructor."""
        self.image = GI.GameImage("bg1.png")
        self.x = -4
        self.vx = -0.02
        self.s = s
        self.width = self.image.width / 2

    def draw(self):
        """Perform all graphical tasks for this frame."""
        self.image.draw(self.s, (self.x, 0))

    def update(self, dt):
        """Perform all calculations for the amount of time that has passed."""
        if not self.image.height == glob.Screen.HEIGHT:
            self.image.stretch()

        if self.x >= 0 or self.x <= -self.width:
            self.vx *= -1
        self.x = min(0, max(-self.width,
                            self.x + self.vx * dt))

if __name__ == "__main__":
    main()
