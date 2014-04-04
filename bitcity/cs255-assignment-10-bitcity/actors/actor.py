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
        self.preAttack = False  # if the actor is in pre-Attack mode
        self.canJump = True  # Whether the actor has a jump/fall animation

    def update(self, dt):
        self.coolDownTicks(dt)
        if self.preAttack:
            jumpAnnim = 0
        elif self.canJump:
            jumpAnnim = self.body.collidedY
        else:
            jumpAnnim = 1
        self.frameHandler.update(dt, self.attackCoolDown.getTime(),
                                 jumpAnnim, self.body.direction,
                                 self.blinkMetro.tick(dt))
        super(Actor, self).update(dt)

    def coolDownTicks(self, dt):
        self.specCoolDown.tick(dt)  # for projectile attacks
        self.attackCoolDown.tick(dt)  # for melee attacks
        self.chargeAttack.tick(dt)  # For charging animation
        self.attackAnimation.tick(dt)

    def setWalkingLeft(self):
        self.body.setMovingLeft()

    def setWalkingRight(self):
        self.body.setMovingRight()

    def setStanding(self):
        self.body.setStill()

    def jump(self):
        self.body.isJumping = True

    def setCollided(self, collidesWith):
        result = self.body.collidePlatform(collidesWith)
        if result == "death":
            self.health = 0

    def hit(self, attackObj):
        """ Hit detection"""
        if not self.isBlocking and attackObj.hasNotHit(self):
            attackObj.addVictim(self)
            M.hitFX()
            self.blinkMetro.fire()
            self.health -= attackObj.damage
            if self.health < 0:
                self.health = 0
            return True
        return False
