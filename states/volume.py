# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from pygame import display

from images import movingBackground as MB
import state
import glob
from adjustableSetting import AdjustableSetting

"""
The Volume menu state.
"""


class Volume(state.State):

    def __init__(self, s):
        super(Volume, self).__init__(s)
        self.background = MB.MovingBackground(s)
        self.adjSetting = AdjustableSetting(
            s, "Volume",
            "Use Left & Right Arrow Keys to change volume",
            glob.Settings.VOLUME, self.width, self.height)

    def update(self, dt):
        """Perform all calculations for the amount of time that has passed."""
        super(Volume, self).update(dt)
        glob.Settings.VOLUME = self.adjSetting.setting
        self.background.update(dt)

    def draw(self):
        """Perform all graphical tasks for this frame."""
        self.background.draw()
        self.adjSetting.draw()
        display.flip()

    def processKeys(self, keys, dt):
        result = super(Volume, self).processKeys(keys, dt)
        if result != state.standardString:
            return result
        result, self.timeAlive = self.adjSetting.processKeys(keys, dt,
                                                             self.timeAlive)
        return result
