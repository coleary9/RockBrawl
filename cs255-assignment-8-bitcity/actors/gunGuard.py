# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import enemy as EN


class GunGuard(EN.Enemy):

    def __init__(self, x, y, id,
                 nodes, mapWidth, mapHeight):
        super(GunGuard, self).__init__(
            x, y, 50, 75, id, nodes, mapWidth, mapHeight,
            "enemy_gunGuard.png")
        self.finishedCoolDown = 750  # all gameObjects have cooldown limit
        self.pointValue = 500 * (self.powerLevel + 1)

    def think(self, playerPosition):
        super(GunGuard, self).think(playerPosition)
        hasShot = self.specCoolDown.getState()
        if not hasShot:
            if abs(playerPosition[0] - self.body.x) + \
                    abs(playerPosition[1] - self.body.y) < 250:
                self.isAttacking = True
        if hasShot and self.startAttack:
            self.setStanding()

       # want them to perform like normal enemies on hills
        if self.body.x > playerPosition[1]:
            return

    # causes guards to keep a distance to shoot at you and not get hit
        inRange = self.body.x > playerPosition[0] - 100 and \
            self.body.x < playerPosition[0] + 100
        isRightOf = self.body.x > playerPosition[0]

        if self.preAttack or self.attackAnimation.getState():
            self.setStanding()
        else:
            if (isRightOf and inRange):
                self.setWalkingRight()
            elif(inRange):
                self.setWalkingLeft()

    def handleAttacks(self, group):
        if self.isAttacking:
            group.add(self.attackFactory.makeProjectile())
            self.isAttacking = False
            self.specCoolDown.fire()
