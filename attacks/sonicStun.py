# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from projectile import Projectile
from pygame import Rect, transform


class SonicStun(Projectile):

    """A sonic stun attack in the game."""

    def __init__(
            self, attacker):
        w = 100
        h = 200
        super(SonicStun, self).__init__(attacker, w, h,
                                        500, 0, None)
        self.body.gravity = 0
        self.body.y -= h / 2
        self.rectOffset = self.body.facing * 20
        self.hasStun = True

    def setCollided(self, collidesWith):
        pass

    def draw(self, pos, surf):
        """Draw the sonic stun on the screen."""
        screenPos = self.getScreenPos(pos)
        surf.blit(surf, screenPos,
                  Rect(screenPos[0] - self.rectOffset, screenPos[1],
                       self.body.width, self.body.height))
