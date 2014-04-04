# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import pygame
from pygame import time, Rect

import math
import glob
from body import Body


class WalkingBody(Body):

    """A walking physics object in the game."""

    def __init__(self, x, y, width, height):
        super(WalkingBody, self).__init__(x, y, width, height)
        self.jumpPower = -0.55
        self.isJumping = False
        self.normalAccelConstant = 0.1
        self.normalAccel = 0
        self.maxSpeed = 0.2
        self.dragMult = 0.009

    def update(self, dt):

        if self.collidedY < 1:
            self.applyForce(0, self.gravity * dt)

        if self.isJumping:
            self.jump()

        self.lastX = self.x
        self.lastY = self.y

        self.updatePositionY(dt)
        self.updatePositionX(dt)

        self.rect.x = self.x
        self.rect.y = self.y

        self.collidedY = 0
        self.collidedX = 0
        self.isJumping = False

    def updatePositionX(self, dt):
        a = -self.dragMult * self.vx + self.normalAccel
        self.vx = max(min((self.vx + dt * a), self.maxSpeed), -self.maxSpeed)
        self.x += (self.vx + self.pushForce) * dt
        self.reducePush(dt)

    def reducePush(self, dt):
        if self.pushForce > 0:
            self.pushForce = max(self.pushForce - (.005 * dt), 0)
        elif self.pushForce < 0:
            self.pushForce = min(self.pushForce + (.005 * dt), 0)

    def setMovingLeft(self):
        self.direction = -1
        self.facing = self.direction
        self.normalAccel = self.normalAccelConstant * self.facing

    def setMovingRight(self):
        self.direction = 1
        self.facing = self.direction
        self.normalAccel = self.normalAccelConstant * self.facing

    def setStill(self):
        self.direction = 0
        self.normalAccel = 0

    def jump(self):
        if self.collidedY > 0:
            self.applyForce(0, self.jumpPower)
