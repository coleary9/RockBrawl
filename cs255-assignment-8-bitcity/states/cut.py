# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import state
import glob
from pygame import key
from pygame import display
from pygame import Rect
import pygame.draw
from pygame.locals import *
import os

from images import gameImage as GI
from sounds import music as M


class Cut(state.State):

    def __init__(self, s, level):
        super(Cut, self).__init__(s)
        self.level = level
        self.toLevel = "press return to continue"
        self.image = None
        self.image = GI.GameImage("cut" + str(self.level) + ".png")
        if self.level == 1:
            M.voiceOver()
        self.titleimage = glob.FONT.render(
            self.toLevel,
            True,
            glob.SELECTED_FONT_COLOR)
        self.titlerect = self.titleimage.get_rect()
        self.titlerect.x = .1 * \
            (glob.Screen.WIDTH - self.titleimage.get_width())
        self.titlerect.y = glob.Screen.HEIGHT * .05
        pygame.draw.rect(self.s,
                         glob.SELECTED_FONT_COLOR,
                         Rect(0, 0, glob.Screen.WIDTH, glob.Screen.HEIGHT))

    def draw(self):

        self.image.drawCentered(self.s)
        self.s.blit(self.titleimage, self.titlerect)

        display.flip()

    def processActions(self, keys, dt):
        result = super(Cut, self).processKeys(keys, dt)
        if result != state.standardString:
            return result
        elif keys[glob.mappedKeys["select"]]:
            return glob.gameString
