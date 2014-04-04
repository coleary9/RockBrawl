# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremey Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>


class BandMember(object):

    """Will contain variables for individual band members"""

    def __init__(self, maxSpeed, jumpPower, frameHandler,
                 width, height, specCoolDown, attackCoolDown, meleeDmg,
                 dmgMult):
        self.maxSpeed = maxSpeed
        self.jumpPower = jumpPower
        self.frameHandler = frameHandler
        self.width = width
        self.height = height
        self.specCoolDown = specCoolDown
        self.attackCoolDown = attackCoolDown
        self.meleeDmg = meleeDmg
        self.dmgMult = dmgMult
