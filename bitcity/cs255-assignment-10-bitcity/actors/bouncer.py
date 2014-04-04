# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import enemy as EN
from metro import CoolDownMetro
import copy


class Bouncer(EN.Enemy):

    def __init__(self, x, y, id,
                 nodes, mapWidth, mapHeight):
        super(Bouncer, self).__init__(
            x, y, 50, 75, id, nodes, mapWidth, mapHeight,
            "bouncer.png")
        self.attackCoolDown = CoolDownMetro(1000)
        self.canJump = False  # To disable falling animation as well as jumping
        self.meleeDmg = 200
        self.health = 50
        self.startAttack = False
        self.pointValue = 5000

    def update(self, dt, playerPosition):

        self.preAttack = self.chargeAttack.getState()
        if not self.preAttack and self.startAttack:
            self.isAttacking = True
            self.startAttack = False
            self.attackAnimation.fire()
        return super(Bouncer, self).update(dt, playerPosition)

    def think(self, playerPosition):
        super(Bouncer, self).think(playerPosition)
        hasShot = self.attackCoolDown.getState()
        isRightOf = self.body.x > playerPosition[0]
        if not hasShot:
            if abs(playerPosition[0] - self.body.x) + \
                    abs(playerPosition[1] - self.body.y) < 250:
                if isRightOf:
                    self.setWalkingLeft()
                else:
                    self.setWalkingRight()
                self.chargeAttack.fire()
                self.startAttack = True

    def handleAttacks(self, group):
        if self.isAttacking:
                attack = self.attackFactory.makeMelee()
                group.add(attack)
                self.isAttacking = False
                self.attackCoolDown.fire()