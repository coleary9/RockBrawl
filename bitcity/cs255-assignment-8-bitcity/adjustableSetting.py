# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import glob

"""
Displays a setting that is adjustable with arrow keys.
"""


class AdjustableSetting(object):

    def __init__(self, s, title, description, setting, width, height):
        self.s = s
        self.title = title
        self.description = description
        self.setting = setting
        self.width = width
        self.height = height

    def draw(self):
        """Perform all graphical tasks for this frame."""
        self.drawTitle()
        self.drawSetting()

    def drawTitle(self):
        col = glob.FONT_COLOR
        surf = glob.FONT.render(self.title, True, col)
        width, height = surf.get_size()
        left = (self.width - width) / 2
        top = self.height / 10
        self.s.blit(surf, (left, top))

    def drawSetting(self):
        col = glob.FONT_COLOR
        surf = glob.FONT.render(str(self.setting), True, col)
        width, height = surf.get_size()
        left = (self.width - width) / 2
        top = self.height / 3 + height * 0
        self.s.blit(surf, (left, top))

        surf = glob.FONT.render(self.description, True, col)
        width, height = surf.get_size()
        top = self.height / 3 + height * 4
        left = (self.width - width) / 2
        self.s.blit(surf, (left, top))

    def processKeys(self, keys, dt, timeAlive):
        if keys[glob.mappedKeys["select"]]:
            return glob.menuString, timeAlive
        elif keys[glob.mappedKeys["left"]]:
            if self.setting > 0:
                self.setting -= 1
                timeAlive = 130
        elif keys[glob.mappedKeys["right"]]:
            if self.setting < 100:
                self.setting += 1
                timeAlive = 130
        return None, timeAlive
