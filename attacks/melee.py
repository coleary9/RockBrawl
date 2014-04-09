# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from attack import AttackObject


class Melee(AttackObject):

    """A hand-to-hand attack object in the game."""

    def __init__(self, attacker):
        if attacker.body.facing < 0:
            x = attacker.body.x
        else:
            x = attacker.rect.right - attacker.body.width / 2
        super(Melee, self).__init__(attacker, x,
                                    attacker.body.y, attacker.body.width / 2,
                                    attacker.body.height, 500, .8, -.25,
                                    attacker.meleeDmg)
