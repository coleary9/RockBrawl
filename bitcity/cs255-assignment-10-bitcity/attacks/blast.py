# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from attack import AttackObject


class Blast(AttackObject):

    """A blast attack in the game."""

    def __init__(
            self, attacker,
            spriteName="blast.png"):
        w, h = 500, 500
        x = attacker.body.rect.centerx - w / 2
        y = attacker.body.rect.centery - h / 2

        super(Blast, self).__init__(attacker, x, y, w, h,
                                    5000, 25, spriteName)
        self.body.gravity = 0