# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import random

from attack import AttackObject
from images.frameHandler import RotatingFrameHandler


class Projectile(AttackObject):

    """A projectile in the game."""

    def __init__(
            self, attacker, width=15, height=5, lifetime=500, dmg=1,
            spriteName="bullet.png"):
        y = attacker.body.y + \
            attacker.body.height / 2 - height / 2
        if (attacker.body.facing > 0):
            x = attacker.body.x + \
                attacker.body.width
        else:
            x = attacker.body.x - width
        super(Projectile, self).__init__(attacker, x, y, width, height,
                                         lifetime, .1, -.05, dmg, spriteName)
        self.body.vx = 2 * self.body.facing + attacker.body.vx
        self.body.vy = attacker.body.vy

    def setCollided(self, collidesWith):
        if not 'noCollide' in collidesWith.prop:
            self.lifetime.fizzle()


class Toss(Projectile):

    """An animated toss in the game."""

    def __init__(
            self, attacker, width=27, height=23, lifetime=500,
            dmg=1, spriteName="single_drumstick.png"):
        super(Toss, self).__init__(attacker, width, height, lifetime,
                                   dmg, spriteName)
        self.frameHandler = RotatingFrameHandler(spriteName, width, height,
                                                 attacker.body.facing)

    def update(self, dt):
        self.frameHandler.update(dt)
        return super(Toss, self).update(dt)


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


class StunProjectile(Projectile):

    """A harmless visual stun effect."""

    def __init__(self, stunnedVictim, width=10, height=10,
                 spriteName="stunned_effect.png"):
        super(StunProjectile, self).__init__(stunnedVictim, width, height,
                                             1000, 0, spriteName)
        self.body.x = stunnedVictim.body.rect.centerx - width / 2
        self.body.y = stunnedVictim.body.rect.top + \
            stunnedVictim.body.height * 0.2
        self.body.facing = random.choice((1, -1))
        mult = width / 10
        self.body.vx = random.uniform(0.01 * mult, 0.03 * mult) \
            * self.body.facing
        self.body.vy = random.uniform(-0.03 * mult, -0.01 * mult)
        self.body.gravity = 0.00003