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
from sounds import music as M
import state
import glob

MAIN_CHOICES = [
    glob.gameString,
    glob.levelString,
    glob.settingsString,
    glob.highScoreString,
    glob.exitString]

# LEVEL_CHOICES = glob.levelChoices[1:]  # Since the first element is None

SETTINGS_CHOICES = [glob.resolutionString,
                    glob.volumeString,
                    glob.difficultyString,
                    glob.keySettings, glob.menuString]

RESOLUTION_CHOICES = [glob.tinyRes, glob.smallRes, glob.mediumRes,
                      glob.largeRes]
#@StaticMethod


def getLevelChoices():
        """Gets the possible level selection"""
        # Start at 1 since the first element is None
        if glob.DEBUG:
            return glob.levelChoices[1:]
        return glob.levelChoices[1: glob.Levels.lastLevel + 1]


class Menu(state.State):

    """
    A state defining a generic menu with a moving background picture.
    Menu is genericized in that you can give it whatever state strings
    you want and it will allow you to transition between them. These
    state strings are defined in globs.py. The SETTINGS_CHOICES is just
    a list of these state strings for the settings menu. It's in menu.py
    as a static global list. The state strings also double as the text
    displayed in a menu.
    """

    def __init__(self, s, title, choicesList):
        """
        Constructor.
        """
        super(Menu, self).__init__(s)
        self.name = title
        # Set the background
        self.background = MB.MovingBackground(s)
        self.choices = choicesList
        self.pos = 0
        M.menuMusic()

    def draw(self):
        """Perform all graphical tasks for this frame."""
        self.background.draw()
        for i in range(0, len(self.choices)):
            self.drawItem(i)

        self.drawTitle()
        display.flip()

    def update(self, dt):
        """Perform all calculations for the amount of time that has passed."""
        super(Menu, self).update(dt)
        self.background.update(dt)

    def drawItem(self, i):
        """Draws the text of a menu choice."""
        col = glob.FONT_COLOR
        backCol = glob.SELECTED_FONT_COLOR
        surf = glob.FONT.render(self.choices[i], True, col)
        width, height = surf.get_size()
        left = (self.width - width) / 2
        top = self.height / 3 + height * i
        if i == self.pos:
            backCol, col = col, backCol
            r = Rect(left, top, width, height)
            pygame.draw.rect(self.s, backCol, r)
            surf = glob.FONT.render(self.choices[i], True, col)
        self.s.blit(surf, (left, top))

    def drawTitle(self):
        """Draws the menu title."""
        col = glob.FONT_COLOR
        backCol = glob.SELECTED_FONT_COLOR
        surf = glob.FONT.render(self.name, True, col)
        width, height = surf.get_size()
        left = (self.width - width) / 2
        top = self.height / 10
        self.s.blit(surf, (left, top))

    def processKeys(self, keys, dt):
        result = super(Menu, self).processKeys(keys, dt)
        if result != state.standardString:
            return result
        elif keys[glob.mappedKeys["select"]]:

            if self.getCurrentChoice() == glob.gameString:
                M.stopMusic()
                if glob.isPaused:
                    return glob.gameString
                return glob.cutString

            return self.getCurrentChoice()
        elif keys[glob.mappedKeys["up"]]:
            self.timeAlive = 0
            self.incMenu(-1)
        elif keys[glob.mappedKeys["down"]]:
            self.timeAlive = 0
            self.incMenu(1)
        return None

    def incMenu(self, amount):
        """Steps by the passed amount in the menu."""
        self.pos += amount
        if self.pos < 0:
            self.pos = len(self.choices) - 1
        elif self.pos > len(self.choices) - 1:
            self.pos = 0

    def getCurrentChoice(self):
        """Returns the current menu choice string."""
        return self.choices[self.pos]


if __name__ == "__main__":
    main()
