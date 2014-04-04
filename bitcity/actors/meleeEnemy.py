# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from enemy import Enemy


class MeleeEnemy(Enemy):

    def __init__(self, x, y, width, height, id,
                 nodes, mapWidth, mapHeight, spriteName):
        super(MeleeEnemy, self).__init__(
            x, y, width, height, id, nodes, mapWidth, mapHeight,
            spriteName)

    def think(self, playerPosition):
        super(MeleeEnemy, self).think(playerPosition)
        if abs(playerPosition[0] - self.body.x) + \
                abs(playerPosition[1] - self.body.y) < 200 and not \
                self.attackCoolDown.getState():

            self.isAttacking = True  # only attacks within 100 blocks of player
        else:
            self.isAttacking = False
