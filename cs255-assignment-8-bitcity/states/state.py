# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>


import pygame
from pygame.locals import *
import glob

minStateTimeAlive = 200
standardString = "stateProcessed"


class State(object):

    """The basic empty state interface."""

    def __init__(self, s):
        """
        Constructor.
        """
        self.s = s
        self.width = self.s.get_width()
        self.height = self.s.get_height()
        self.name = glob.stateString
        self.timeAlive = 0

    def draw(self):
        """Perform all graphical tasks for this frame."""
        pass

    def update(self, dt):
        """Perform all calculations for the amount of time that has passed."""
        self.timeAlive += dt

    def processKeys(self, keys, dt):
        if keys[glob.mappedKeys[glob.exitString]]:
            return glob.exitString
        elif self.timeAlive < minStateTimeAlive:
            return None
        return standardString

    def processActions(self, keys, dt):
        return self.processKeys(keys, dt)

    def quit(self):
        pygame.quit()

    def reset(self, s):
        """Set a few things back to their initial values."""
        self.s = s
        self.width = self.s.get_width()
        self.height = self.s.get_height()
        self.timeAlive = 0

if __name__ == "__main__":
    main()