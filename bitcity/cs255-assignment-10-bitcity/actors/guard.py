# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from meleeEnemy import MeleeEnemy


class Guard(MeleeEnemy):

    def __init__(self, x, y, id,
                 nodes, mapWidth, mapHeight):
        super(Guard, self).__init__(
            x, y, 50, 75, id, nodes, mapWidth, mapHeight,
            "guard.png")
