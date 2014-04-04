# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from actor import Actor
import random
from pygame import image
from sounds import music as M
from levels import tile as TI
import aiAnalyzer as AI
import glob


class Enemy(Actor):

    def __init__(self, x, y, width, height, id,
                 nodes, mapWidth, mapHeight, imagePath):
        super(Enemy, self).__init__(
            x, y, width, height,
            imagePath)
        self.direction = 1
        self.health = 20
        self.type = "enemy"
        self.id = id
        self.pointValue = 100
        self.nodes = nodes
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight

        # AI
        self.lastThoughtTime = 0
        self.thoughtInterval = 200

    def update(self, dt, playerPosition):
        if self.fullTime - self.lastThoughtTime >= self.thoughtInterval:
            self.think(playerPosition)
        if self.body.lastY > self.mapHeight * glob.tileSize:
            self.health = 0
        super(Enemy, self).update(dt)
        if self.health <= 0:
            glob.SCORE += self.pointValue
            return False
        return True

    def think(self, playerPosition):
        """ AI for the enemy:
        logic for jumping and direction in which to walk in
        """
        self.lastThoughtTime = self.fullTime
        self.thoughtInterval = random.randint(100, 400)
        if self.atJumpNode() or self.body.collidedX != 0 and self.canJump:
            self.jump()
        isVicious = random.randint(0, 100) <= 80
        isRightOf = self.body.x > playerPosition[0]

        # We don't move during pre-Attack
        if self.preAttack or self.attackAnimation.getState():
            self.setStanding()
        else:
            if (isVicious and isRightOf) or (not isVicious and not isRightOf):
                self.setWalkingLeft()
            else:
                self.setWalkingRight()

    def atJumpNode(self):
        """ Determines whether the enemy needs to jump"""
        key = TI.getTileKey(self.rect.midbottom, self.mapWidth)
        if not key in self.nodes:
            return False
        val = self.nodes[key]
        if val == self.direction or \
           val == AI.BOTH_JUMP:
            return True

    def handleAttacks(self, group):
        if self.isAttacking:
                group.add(self.attackFactory.makeMelee())
                self.isAttacking = False
                self.attackCoolDown.fire()

    def hit(self, attackObj):
        if super(Enemy, self).hit(attackObj):
            self.body.applyForce(attackObj.body.facing * 0.8, -0.25)
            self.setStanding()

    def setCollided(self, collidesWith):
        super(Enemy, self).setCollided(collidesWith)