# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>


from metro import CoolDownMetro
from gameObject import GameObject
from images.frameHandler import PassiveFrameHandler


class AttackObject(GameObject):

    """An attack object in the game."""

    def __init__(
            self, attacker, x, y, width, height, lifetime, xpush, ypush, dmg=3,
            spriteName=None):

        frameHandler = PassiveFrameHandler(spriteName)
        super(AttackObject, self).__init__(x, y,
                                           width, height, frameHandler)
        self.lifetime = CoolDownMetro(lifetime)
        self.lifetime.fire()
        self.body.facing = attacker.body.facing
        self.damage = dmg
        if attacker.type == 'enemy':
            self.damage *= (attacker.powerLevel + 1)
        self.victims = []
        self.xpush = xpush
        self.ypush = ypush
        self.hasStun = False

    def update(self, dt):
        super(AttackObject, self).update(dt)
        return self.lifetime.tick(dt)

    def hasNotHit(self, victim):
        return not victim in self.victims

    def addVictim(self, victim):
        self.victims.append(victim)

    def setCollided(self, collidesWith):
        pass
