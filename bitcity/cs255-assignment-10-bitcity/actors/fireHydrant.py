# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import enemy as EN


class FireHydrant(EN.Enemy):

    def __init__(self, x, y, id,
                 nodes, mapWidth, mapHeight):
        super(FireHydrant, self).__init__(
            x, y, 50, 75, id, nodes, mapWidth, mapHeight,
            "gunGuard.png")
        self.finishedCoolDown = 750  # all gameObjects have cooldown limit
        self.pointValue = 500

    def think(self, playerPosition):
        hasShot = self.specCoolDown.getState()
        if not hasShot:
            self.isAttacking = True

    def hit(self, attackObj):
        pass

    def handleAttacks(self, group):
        if self.isAttacking:
                group.add(self.attackFactory.makeArcProjectile())
                self.isAttacking = False
                self.specCoolDown.fire()
