# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremey Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import pygame
from pygame import time, Rect

import math
import glob

collDirections = ['left', 'right', 'top', 'bottom']


class Body(object):

    """A physics object in the game."""

    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.collidedX = 0
        self.collidedY = 0
        self.x = x
        self.y = y
        self.initX = x
        self.initY = y

        self.lastX = self.x
        self.lastY = self.y
        self.vx = 0
        self.vy = 0
        self.gravity = .001
        self.maxYSpeed = 3
        self.direction = 0
        self.facing = 1
        self.forceTileChanged = False
        self.pushForce = 0

        # Collision rect. This is independent from the Sprite's rect.
        # For now, this will be constant size, while the Sprite rect will
        # flunctuate.
        self.rect = Rect(x, y, width, height)

    def reSpawn(self):
        """ Respawns the body"""
        self.x = self.initX
        self.y = self.initY

    def update(self, dt):

        if self.collidedY < 1:
            self.applyForce(0, self.gravity * dt)

        self.lastX = self.x
        self.lastY = self.y

        self.updatePositionY(dt)
        self.updatePositionX(dt)

        self.rect.x = self.x
        self.rect.y = self.y

        self.collidedY = 0
        self.collidedX = 0

    def updatePositionX(self, dt):
        self.x += self.vx * dt

    def updatePositionY(self, dt):
        if self.vy >= 0:
            self.y += min(self.vy * dt, self.maxYSpeed)
        else:
            self.y += max(self.vy * dt, -self.maxYSpeed)

    def applyForce(self, xForce, yForce):
        """ Applies a force"""
        self.pushForce += xForce
        self.vy += yForce

    def collideBottom(self, tilePos):
        self.collidedY = 1
        self.vy = 0
        self.y = tilePos[1] - self.height + 2  # fudge

    def collideTop(self, tilePos):
        self.collidedY = -1
        self.vy = max(self.vy, 0)
        self.y = tilePos[1] + glob.tileSize

    def collideRight(self, tilePos):
        self.collidedX = 1
        self.vx = 0
        self.x = tilePos[0] - self.width

    def collideLeft(self, tilePos):
        self.collidedX = -1
        self.vx = 0
        self.x = tilePos[0] + glob.tileSize

    def checkForceTileChanged(self):
        if self.forceTileChanged:
            self.forceTileChanged = False
            return True

    def tileChanged(self):
        if self.checkForceTileChanged():
            return True
        return int(self.x / glob.tileSize) != \
            int(self.lastX / glob.tileSize) \
            or int(self.y / glob.tileSize) != \
            int(self.lastY / glob.tileSize)

    def collidePlatform(self, platform):
        """ Very ugly and should be refactored!
         The rect should probably be split into 4 triangles
         and "collided" manually. This shows the concept
         using 4 fudgy rectangles instead.
        """
        if 'noCollide' in platform.prop:
            return
        if 'beer' in platform.prop:
            return 'beer'
        if 'win' in platform.prop:
            return 'win'
        if 'death' in platform.prop:
            return 'death'

        collRules = platform.prop[0]

        # Pretty ugly, temporary hopefully
        # determines whether to default to all collisions if not collision
        # specified
        isDefault = True
        for side in collDirections:
            if side in collRules:
                isDefault = False

        platPos = platform.getAbsolutePos()
        if platform.collideRect(Rect(self.rect.left - self.rect.width / 2 + 2,
                                     self.rect.top + self.rect.height * 0.1,
                                     self.rect.width / 2,
                                     self.rect.height * 0.8)) and \
                ('left' in collRules or isDefault):
            self.collideLeft(platPos)
        elif platform.collideRect(
            Rect(self.rect.left + self.rect.width / 2 + 2,
                 self.rect.top + self.rect.height * 0.1,
                 self.rect.width / 2,
                 self.rect.height * 0.8)) and \
                ('right' in collRules or isDefault):
            self.collideRight(platPos)
        elif platform.collideRect(Rect(self.rect.left + self.rect.width * 0.1,
                                       self.rect.top,
                                       self.rect.width * 0.8,
                                       self.rect.height / 2)) and \
                ('top' in collRules or isDefault):
            self.collideTop(platPos)
        elif platform.collideRect(Rect(self.rect.left + self.rect.width * 0.1,
                                       self.rect.top + self.rect.height / 2,
                                       self.rect.width * 0.8,
                                       self.rect.height / 2)) and \
                ('bottom' in collRules or isDefault):
            self.collideBottom(platPos)

        if 'barrier' in platform.prop:
            return 'barrier'

    def setHeight(self, h):
        self.height = h
        self.rect.height = h

    def setWidth(self, w):
        self.width = w
        self.rect.width = w

    def setPositionBasedOnBottomCenter(self, height, width):
        oldBottomCenter = self.rect.midbottom
        self.setHeight(height)
        self.setWidth(width)
        self.rect.midbottom = oldBottomCenter
