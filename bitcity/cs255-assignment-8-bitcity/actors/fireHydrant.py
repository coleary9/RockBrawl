# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import enemy as EN
from images.frameHandler import PassiveFrameHandler

from metro import CoolDownMetro


class FireHydrant(EN.Enemy):

    def __init__(self, x, y, id,
                 nodes, mapWidth, mapHeight):
        super(FireHydrant, self).__init__(
            x, y, 25, 50, id, nodes, mapWidth, mapHeight,
            "enemy_fireHydrant.png")
        self.frameHandler = PassiveFrameHandler("enemy_fireHydrant.png")
        self.finishedCoolDown = 750  # all gameObjects have cooldown limit
        self.pointValue = 500
        self.specCoolDown = CoolDownMetro(100)

    def think(self, playerPosition):
        hasShot = self.specCoolDown.getState()
        if not hasShot:
            self.isAttacking = True

    def hit(self, attackObj):
        """ Hit detection"""
        if not self.isBlocking and attackObj.hasNotHit(self):
            attackObj.addVictim(self)
            self.blinkMetro.fire()
            self.health -= attackObj.damage
            if self.health < 0:
                self.health = 0
            return True
        return False

    def handleAttacks(self, group):
        if self.isAttacking:
                group.add(self.attackFactory.makeArcProjectile())
                self.isAttacking = False
                self.specCoolDown.fire()

    def getPower(self):
        return 0
