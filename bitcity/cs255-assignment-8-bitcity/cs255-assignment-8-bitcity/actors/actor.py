# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import pygame
from pygame import mixer
import os
import math

from metro import CoolDownMetro
import glob
from physics.walkingBody import WalkingBody
from gameObject import GameObject
from images.frameHandler import ActiveFrameHandler
from attacks.attackFactory import AttackFactory
from sounds import music as M
from stunParticleGenerator import StunParticleGenerator


class Actor(GameObject):

    """An object that can walk and attack in the game."""

    def __init__(
            self, x, y, width, height,
            spriteName, health=80, maxHealth=100):

        # Active sprite frame handling.
        frameHandler = ActiveFrameHandler(width, height,
                                          spriteName)

        super(Actor, self).__init__(x, y, width, height, frameHandler)

        # For physics and walking
        self.body = WalkingBody(x, y, width, height)

        self.health = health
        self.maxHealth = maxHealth

        self.attackFactory = AttackFactory(self)
        self.meleeDmg = 3
        self.type = 'player'

        # Attack Flags
        self.isAttacking = False
        self.isBlocking = False
        # For projectiles not firing constantly
        self.specCoolDown = CoolDownMetro(15)
        # To limit the rate of attack
        self.attackCoolDown = CoolDownMetro(1000)
        # To control blinking after being hit
        self.blinkMetro = CoolDownMetro(500)
        # To control pre-Attack animation
        self.chargeAttack = CoolDownMetro(900)  # 4 frames of pre
        self.attackAnimation = CoolDownMetro(400)
        self.stunCoolDown = CoolDownMetro(3000)
        self.stunParticles = StunParticleGenerator(self)
        self.preAttack = False  # if the actor is in pre-Attack mode
        self.canJump = True  # Whether the actor has a jump/fall animation

    def update(self, dt):
        self.coolDownTicks(dt)
        if self.preAttack:
            jumpAnim = 0
        elif self.canJump:
            jumpAnim = self.body.collidedY
        else:
            jumpAnim = 1
        isStunned = self.stunCoolDown.getState()
        if isStunned:
            self.setStanding()
        self.stunParticles.update(dt, isStunned)
        self.frameHandler.update(dt, self.attackCoolDown.getTime(),
                                 jumpAnim, self.body.direction,
                                 self.blinkMetro.tick(dt), self.isBlocking)
        super(Actor, self).update(dt)

    def coolDownTicks(self, dt):
        self.specCoolDown.tick(dt)  # for projectile attacks
        self.attackCoolDown.tick(dt)  # for melee attacks
        self.chargeAttack.tick(dt)  # For charging animation
        self.attackAnimation.tick(dt)
        self.stunCoolDown.tick(dt)

    def setWalkingLeft(self):
        if not self.stunCoolDown.getState():
            self.body.setMovingLeft()

    def setWalkingRight(self):
        if not self.stunCoolDown.getState():
            self.body.setMovingRight()

    def setStanding(self):
        self.body.setStill()

    def jump(self):
        if not self.stunCoolDown.getState():
            self.body.isJumping = True

    def setCollided(self, collidesWith):
        result = self.body.collidePlatform(collidesWith)
        if result == "death":
            self.health = 0

    def hit(self, attackObj):
        """ Hit detection"""
        if not self.isBlocking and attackObj.hasNotHit(self):
            attackObj.addVictim(self)
            self.blinkMetro.fire()
            self.processDamage(attackObj.damage)
            if attackObj.hasStun:
                self.stunCoolDown.fire()
            return True
        return False

    def processDamage(self, dmg):
        self.health = max(0, self.health - dmg)

    def draw(self, pos, surf):
        self.stunParticles.draw(pos, surf)
        super(Actor, self).draw(pos, surf)
