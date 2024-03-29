# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import glob
from attacks.projectile import StunProjectile
from metro import CoolDownMetro


class StunParticleGenerator(object):

    """An object that spawns stun effects."""

    def __init__(self, stunnedVictim, width=10, height=10,
                 imageName="stunned_effect.png"):
        self.width = width
        self.height = height
        self.imageName = imageName
        self.stunnedVictim = stunnedVictim
        self.stunParticles = []
        self.pacer = CoolDownMetro(100)

    def update(self, dt, isStunned):
        if isStunned:
            if not self.pacer.tick(dt):
                self.pacer.fire()
                self.stunParticles.append(
                    StunProjectile(self.stunnedVictim,
                                   self.width, self.height,
                                   self.imageName))
        for p in reversed(self.stunParticles):
            if not p.update(dt):
                self.stunParticles.remove(p)

    def draw(self, pos, surf):
        [p.draw(pos, surf) for p in self.stunParticles]
