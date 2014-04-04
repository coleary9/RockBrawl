# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>


import pygame
from pygame.locals import *
import glob
from pygame.sprite import Group


class DynamicGroup(Group):

    """The basic empty group interface."""

    def __init__(self):
        """
        Constructor.
        """
        Group.__init__(self)

    def draw(self, camera):
        """Perform all graphical tasks for this frame."""
        for obj in self:
            camera.draw(obj)

    def update(self, dt):
        """Perform all calculations for the amount of time that has passed."""
        for obj in self:
            if not obj.update(dt):
                self.remove(obj)


class EnemiesGroup(DynamicGroup):

    """A group with a reference to the player."""

    def addPlayerReference(self, player):
        self.player = player

    def update(self, dt):
        pos = self.player.pos()
        for obj in self:
            if not obj.update(dt, pos):
                self.remove(obj)

if __name__ == "__main__":
    main()
