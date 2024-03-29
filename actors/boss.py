# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import enemy as EN
import meleeEnemy as M
from metro import CoolDownMetro
import copy
from images.frameHandler import ActiveFrameHandler
from attacks import attackFactory as AF

GUITARIST = 0
DRUMMER = 1
VOCALIST = 2

# Invisible Enemy that spawns Rivals


class Boss(EN.Enemy):

    def __init__(self, x, y, id,
                 nodes, mapWidth, mapHeight, enemyGroup):
        super(Boss, self).__init__(
            0, 0, 0, 0, id, nodes, mapWidth, mapHeight,
            "enemy_bouncer.png")
        self.nodes = nodes
        self.initX = x
        self.initY = y
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.enemyGroup = enemyGroup
        self.pointValue = 25000
        self.health = 200
        self.meleeDmg = 10

        self.current = 0
        self.enemy = Guitar(
            self.initX,
            self.initY,
            self.nodes,
            self.mapWidth,
            self.mapHeight)

        self.enemyGroup.add(self.enemy)

    def update(self, dt, playerPosition):
        self.enemy.specCoolDown.tick(dt)
        if self.enemy.health <= 0:
            self.current += 1
            if self.current == 1:
                self.enemy = Vocalist(
                    self.initX,
                    self.initY,
                    self.nodes,
                    self.mapWidth,
                    self.mapHeight)
                self.enemyGroup.add(self.enemy)
            elif self.current == 2:
                self.enemy = Drummer(
                    self.initX,
                    self.initY,
                    self.nodes,
                    self.mapWidth,
                    self.mapHeight)
                self.enemyGroup.add(self.enemy)
            else:
                return False
        return True

    def think(self, playerPosition):
        super(Boss, self).think(playerPosition)
        hasShot = self.attackCoolDown.getState()
        isRightOf = self.body.x > playerPosition[0]
        if not hasShot:
            if abs(playerPosition[0] - self.body.x) + \
                    abs(playerPosition[1] - self.body.y) < 250:
                if isRightOf:
                    self.setWalkingLeft()
                else:
                    self.setWalkingRight()
                self.chargeAttack.fire()
                self.startAttack = True

    def handleAttacks(self, group):
        if self.isAttacking:
                attack = self.attackFactory.makeMelee()
                group.add(attack)
                self.isAttacking = False
                self.attackCoolDown.fire()
        self.enemy.handleSpecial(group)


class Guitar(M.MeleeEnemy):

    def __init__(self, initX, initY, nodes, mapWidth, mapHeight):
        super(Guitar, self).__init__(
            initX, initY, 50, 75, 1, nodes, mapWidth, mapHeight,
            "red_guitar.png")
        self.pointValue = 25000
        self.frameHandler = ActiveFrameHandler(50, 75,
                                               "red_guitar.png", 8)
        self.specCoolDown = CoolDownMetro(15000)

    def getPower(self):
        return 2  # BOSS

    def handleSpecial(self, group):
        if not self.specCoolDown.getState():
            self.stunCoolDown.fire()
            self.specCoolDown.fire()
            group.add(AF.specialsList[GUITARIST](self))


class Drummer(M.MeleeEnemy):

    def __init__(self, initX, initY, nodes, mapWidth, mapHeight):
        super(Drummer, self).__init__(
            initX, initY, 55, 65, 1, nodes, mapWidth, mapHeight,
            "drummer.png")
        self.pointValue = 25000
        self.frameHandler = ActiveFrameHandler(55, 65,
                                               "red_drummer.png", 10, 55, 65, 0, 0, 0)
        self.specCoolDown = CoolDownMetro(5000)

    def getPower(self):
        return 2  # BOSS

    def handleSpecial(self, group):
        if not self.specCoolDown.getState():
            self.specCoolDown.fire()
            group.add(AF.specialsList[DRUMMER](self))


class Vocalist(M.MeleeEnemy):

    def __init__(self, initX, initY, nodes, mapWidth, mapHeight):
        super(Vocalist, self).__init__(
            initX, initY, 50, 75, 1, nodes, mapWidth, mapHeight,
            "vocalist.png")
        self.pointValue = 25000
        self.frameHandler = ActiveFrameHandler(50, 75,
                                               "red_vocalist.png", 8, 125, 150, -75, 0, -75)
        self.specCoolDown = CoolDownMetro(10000)

    def getPower(self):
        return 2  # BOSS

    def handleSpecial(self, group):
        if not self.specCoolDown.getState():
            self.specCoolDown.fire()
            group.add(AF.specialsList[VOCALIST](self))
