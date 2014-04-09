# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import random

from attack import AttackObject


class Projectile(AttackObject):

    """A projectile in the game."""

    def __init__(
            self, attacker, width=15, height=5, lifetime=500, dmg=1,
            spriteName="bullet.png"):
        y = attacker.body.y + \
            attacker.body.height / 2
        if (attacker.body.facing > 0):
            x = attacker.body.x + \
                attacker.body.width
        else:
            x = attacker.body.x
        super(Projectile, self).__init__(attacker, x, y, width, height,
                                         lifetime, dmg, spriteName)
        self.body.vx = 2 * self.body.facing + attacker.body.vx
        self.body.vy = attacker.body.vy

    def setCollided(self, collidesWith):
        if not 'noCollide' in collidesWith.prop:
            self.lifetime.fizzle()


class ArcProjectile(Projectile):

    """A projectile that is slower. It arcs up then down from
        the top of the corresponding attacker.

        These have a random direction and initial velocity."""

    def __init__(self, attacker, width=10, height=10,
                 spriteName="arc.png"):
        super(ArcProjectile, self).__init__(attacker, width, height,
                                            1000, 3, spriteName)
        self.body.facing = random.choice((1, -1))
        self.body.vx = random.uniform(0.2, 0.5) * self.body.facing
        self.body.vy = random.uniform(-0.5, -0.2)