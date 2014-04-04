# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import glob
from actors import guard as GD
from actors import rivalGuitar as RG, gunGuard as GG, bouncer as B, fireHydrant as F


class EnemySpawner(object):

    """An object that spawns enemies."""

    def __init__(self, numEnemies, enemyType,
                 x, y, enemiesGroup, nodes, mapWidth, mapHeight):
        self.numEnemies = numEnemies
        self.enemyType = enemyType
        self.x = x
        self.y = y
        self.spawnX = glob.Screen.WIDTH / 2
        self.spawnY = glob.Screen.HEIGHT / 2
        self.enGroup = enemiesGroup
        self.nodes = nodes
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight

    def update(self, position):
        """
        Check whether player is far enough along to trigger
        enemy spawning.
        """
        if (abs(position[0] - self.x) <= self.spawnX) and\
                (abs(self.y - position[1]) <= self.spawnY):
            self.createEnemies()
            return True
        return False

    def createEnemies(self):
        """Factory method to create enemies."""
        if self.enemyType == "GSpawn":
            for e in xrange(self.numEnemies):
                baddie = GD.Guard(
                    self.x,
                    self.y,
                    e,
                    self.nodes,
                    self.mapWidth,
                    self.mapHeight)
                self.enGroup.add(baddie)
        elif self.enemyType == "RSpawn":
            for e in xrange(self.numEnemies):
                baddie = RG.RivalGuitar(
                    self.x,
                    self.y,
                    e,
                    self.nodes,
                    self.mapWidth,
                    self.mapHeight)
                self.enGroup.add(baddie)
        elif self.enemyType == "GNSpawn":
            for e in xrange(self.numEnemies):
                baddie = GG.GunGuard(
                    self.x,
                    self.y,
                    e,
                    self.nodes,
                    self.mapWidth,
                    self.mapHeight)
                self.enGroup.add(baddie)
        elif self.enemyType == "BSpawn":
            for e in xrange(self.numEnemies):
                baddie = B.Bouncer(
                    self.x,
                    self.y,
                    e,
                    self.nodes,
                    self.mapWidth,
                    self.mapHeight)
                self.enGroup.add(baddie)
        elif self.enemyType == "FSpawn":
            for e in xrange(self.numEnemies):
                baddie = F.FireHydrant(
                    self.x,
                    self.y,
                    e,
                    self.nodes,
                    self.mapWidth,
                    self.mapHeight)
                self.enGroup.add(baddie)