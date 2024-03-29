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

MINION = 0
MINIBOSS = 1
BOSS = 2
RONPAUL = 3


class Enemy(Actor):

    def __init__(self, x, y, width, height, id,
                 nodes, mapWidth, mapHeight, imagePath):
        self.powerLevel = self.getPower()
        if self.powerLevel == MINIBOSS:
            imagePath = "orange_" + imagePath
        elif self.powerLevel == BOSS:
            imagePath = "red_" + imagePath
        super(Enemy, self).__init__(
            x, y, width, height,
            imagePath)
        self.direction = 1
        self.health = 20 * (self.powerLevel + 1)
        self.type = "enemy"
        self.pointValue = 100 * (self.powerLevel + 1)
        self.nodes = nodes
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        # AI
        self.lastThoughtTime = 0
        self.thoughtInterval = 200
        self.isJumping = False
        self.switchCounter = 0
        self.isVicious = True
        # switch counter is used for when an enemy will consider switching
        # isVicious
        self.stuckCounter = 0  # sees if an  enemy is stuck

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
        self.switchCounter += 1
        if self.isJumping:
            if self.body.collidedY == 1:
                self.isJumpping = False
            else:
                return
        if self.atJumpNode() or self.body.collidedX != 0 and self.canJump:
            self.jump()
            self.isJumping = True

        if self.body.collidedX == 1 or self.body.collidedX == -1:
            self.stuckCounter += 1

        else:
            self.stuckCounter = 0
        if self.stuckCounter > 1:
            self.isVicious = not self.isVicious

        if self.switchCounter > 3:
            self.switchCounter = 0
            self.isVicious = random.randint(0, 100) <= 80
        isRightOf = self.body.x > playerPosition[0]

        # We don't move during pre-Attack
        if self.preAttack or self.attackAnimation.getState():
            self.setStanding()
        else:
            if (self.isVicious and isRightOf) or \
               (not self.isVicious and not isRightOf):
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
        if self.isAttacking and not self.stunCoolDown.getState():
            group.add(self.attackFactory.makeMelee())
            self.isAttacking = False
            self.attackCoolDown.fire()

    def hit(self, attackObj):
        if super(Enemy, self).hit(attackObj):
            M.enemyHitFX()
            self.body.applyForce(attackObj.body.facing * attackObj.xpush,
                                 attackObj.ypush)
            self.setStanding()

    def setCollided(self, collidesWith):
        super(Enemy, self).setCollided(collidesWith)

    def getPower(self):
        # Power level chances for miniboss/boss chance
        # MINION set to 1 for now.
        POWER_CHANCES = {MINION: 0.8, MINIBOSS: 0.95, BOSS: 1}
        r = random.random()
        for k, p in POWER_CHANCES.iteritems():
            if r < p:
                return k
