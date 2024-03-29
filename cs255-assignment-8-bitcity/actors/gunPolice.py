# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import enemy as EN


class GunPolice(EN.Enemy):

    def __init__(self, x, y, id,
                 nodes, mapWidth, mapHeight):
        super(GunPolice, self).__init__(
            x, y, 50, 75, id, nodes, mapWidth, mapHeight,
            "enemy_gunPolice.png")
        self.finishedCoolDown = 750  # all gameObjects have cooldown limit
        self.pointValue = 500 * (self.powerLevel + 1)

    def think(self, playerPosition):
        super(GunPolice, self).think(playerPosition)
        hasShot = self.specCoolDown.getState()
        if not hasShot:
            if abs(playerPosition[0] - self.body.x) + \
                    abs(playerPosition[1] - self.body.y) < 250:
                self.isAttacking = True
        if hasShot and self.startAttack:
            self.setStanding()

    def handleAttacks(self, group):
        if self.isAttacking:
                group.add(self.attackFactory.makeProjectile())
                self.isAttacking = False
                self.specCoolDown.fire()
