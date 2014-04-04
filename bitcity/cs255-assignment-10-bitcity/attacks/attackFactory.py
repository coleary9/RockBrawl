# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from attacks.projectile import Projectile, ArcProjectile
from attacks.blast import Blast
from attacks.melee import Melee


class AttackFactory(object):

    """Creates attack sprites"""

    def __init__(self, attacker):
        self.attacker = attacker

    def makeMelee(self):
        return Melee(self.attacker)

    def makeProjectile(self):
        return Projectile(self.attacker)

    def makeSpecial(self):
        return specialsList[self.attacker.playernum](self.attacker)

    def makeArcProjectile(self):
        return ArcProjectile(self.attacker)

# List of special attacks corresponding to different bandmembers.
specialsList = [lambda a: Blast(a), lambda a: Projectile(a)]
