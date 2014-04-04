# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>
from pygame import *

import glob
import state
from images import movingBackground as MB


class YouWin(state.State):

    def __init__(self, s):
        super(YouWin, self).__init__(s)
        self.background = MB.MovingBackground(s)
        self.wintext = "The band rocks on through the crowd! Congratulations!"
        self.losetext = "You died, try again!"
        glob.isPaused = False
        if glob.newScore:
            self.textsurf = glob.FONT.render(
                self.wintext,
                True,
                glob.FONT_COLOR)
        elif glob.LEVEL > len(glob.levelDict):
            glob.LEVEL = 1
        else:
            self.textsurf = glob.FONT.render(
                self.losetext,
                True,
                glob.FONT_COLOR)
        self.textrect = self.textsurf.get_rect()
        self.textrect.x = (s.get_width() - self.textsurf.get_width()) / 2
        self.textrect.y = (s.get_height() - self.textsurf.get_height()) / 2

    def draw(self):
        self.background.draw()
        self.s.blit(self.textsurf, self.textrect)
        display.flip()

    def update(self, dt):
        super(YouWin, self).update(dt)
        self.background.update(dt)

    def processKeys(self, keys, dt):
        result = super(YouWin, self).processKeys(keys, dt)
        if result != state.standardString:
            return result
        elif keys[glob.mappedKeys["select"]]:
            return glob.highScoreString
        return None
