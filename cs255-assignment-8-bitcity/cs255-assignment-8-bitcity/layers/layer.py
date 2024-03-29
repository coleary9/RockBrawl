# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>


import pygame
from pygame.locals import *

import glob
from images import gameImage as GI


class Layer(object):

    """The basic empty layer interface."""

    def __init__(self, memberList):
        """
        Constructor.
        """
        self.members = memberList

    def draw(self, camera):
        """Perform all graphical tasks for this frame."""
        for member in self.members:
            member.draw(camera)

    def update(self, dt):
        """Perform all calculations for the amount of time that has passed."""
        for member in self.members:
            member.update(dt)

    def reset(self):
        pass


class BackgroundLayer(object):

    """A parallax-scrolling background layer."""

    def __init__(self, mapWidth):
        """
        Constructor.
        """

        # Set the background image
        self.background = GI.GameImage("bg" + str(glob.LEVEL) + ".png")

        self.scrollCoeff = float(
            (self.background.width / 2)) / (mapWidth * glob.tileSize)

    def draw(self, camera):
        """Draw the background for this frame."""
        self.background.draw(camera.surf,
                             (max(-self.background.width + glob.Screen.WIDTH,
                                  0 - camera.x * self.scrollCoeff), 0))

    def update(self, dt):
        pass

    def reset(self):
        self.background.stretch()

if __name__ == "__main__":
    main()
