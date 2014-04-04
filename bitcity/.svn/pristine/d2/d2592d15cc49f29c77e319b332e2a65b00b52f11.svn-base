# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>
from pygame import key
from pygame import display
from pygame import Rect
import pygame.draw

from pygame.locals import *
import os
from images import movingBackground as MB
import state
import glob


class Title(state.State):

    def __init__(self, s):
        super(Title, self).__init__(s)
        self.background = MB.MovingBackground(s)
        self.title = "Rock and Brawl"
        self.text = "Press Enter"

    def draw(self):
        self.background.draw()
        self.showText(self.title,
                      .5, min(.4, self.timeAlive / 4000.0))
        if self.timeAlive % 1000 < 650:
            self.showText(self.text, .5, .6)
        display.flip()

    def showText(self, text, percentX, percentY):
        textImage = glob.FONT.render(text, True, glob.FONT_COLOR)
        textRect = textImage.get_rect()
        textRect.x = percentX * (
            self.s.get_width() - textImage.get_width())
        textRect.y = percentY * (
            self.s.get_height() - textImage.get_height())
        self.s.blit(textImage, textRect)

    def processKeys(self, keys, dt):
        result = super(Title, self).processKeys(keys, dt)
        if result != state.standardString:
            return result
        elif keys[glob.mappedKeys["select"]]:
            return glob.menuString
        return None

    def update(self, dt):
        super(Title, self).update(dt)
        self.background.update(dt)
