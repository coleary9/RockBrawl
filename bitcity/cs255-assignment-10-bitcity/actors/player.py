# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from pygame import display, Rect, image, Surface

import math

import glob
from images import imageDict as IMG
from actor import Actor
from images import frameLoader as FL
import bandMember as BM
from sounds import music as M
from metro import CoolDownMetro
import random
from pygame.locals import *  # For keys


class Player(Actor):

    """A player in the game."""

    def __init__(self, x, y, width, height, enemies):
        super(Player, self).__init__(
            x, y, width, height, "guitar_with_attack.png", 1000, 1000)
        self.body.maxSpeed = 0.5  # we're fast
        # list of band members
        self.players = \
            [BM.BandMember(
                "guitar_with_attack.png",
                0.5,
                -0.55,
                50,
                75,
                CoolDownMetro(60000),
                CoolDownMetro(470),
                5),
                BM.BandMember(
                    "rival_guitar_with_attack.png",
                    0.2,
                    -.9,
                    50,
                    75,
                    CoolDownMetro(250),
                    CoolDownMetro(470),
                    40)]
        self.playernum = 0
        # music junk
        M.initMusic()  # this will need to be passed the current level

        self.win = False

        self.intox = 0
        self.maxIntox = 100  # hud purposes for now, later for PSN
        self.desoberingRate = 0.0002  # desobering constant

        self.hasDrank = False
        self.hasSwitched = False

        self.enemies = enemies  # Keep track of enemies
        self.id = 'Player'  # For debugging purposes
        self.specCoolDown = \
            self.players[self.playernum].specCoolDown
        self.attackCoolDown = \
            self.players[self.playernum].attackCoolDown

    def killIfNecessary(self):
        # Kills a player if necessary.
        # Hardcoded for now.
        if self.body.y > 5000:
            self.health = -50

    def update(self, dt):
        super(Player, self).update(dt)
        for bandMbr in self.players:
            if self.players[self.playernum] != bandMbr:
                bandMbr.specCoolDown.tick(dt)
                bandMbr.attackCoolDown.tick(dt)

        self.killIfNecessary()

        if self.intox > 0:  # decrease intoxication:
            self.intox -= (dt * self.desoberingRate)
            self.intox = max(0, self.intox)
        else:
            self.intox = 0

        if self.intox > 50:  # poison check
            self.health -= 0.0004 * dt

        return True  # The player is never removed from the game.

    # called by game to switch player
    def switchPlayer(self):
        if glob.LEVEL != 1:
            self.players[self.playernum].specCoolDown = self.specCoolDown
            self.players[self.playernum].attackCoolDown = self.attackCoolDown
            # increments player list
            if (self.playernum < len(self.players) - 1):
                self.playernum += 1
            else:
                self.playernum = 0
            currMember = self.players[self.playernum]
            self.specCoolDown = currMember.specCoolDown
            self.attackCoolDown = currMember.attackCoolDown

            self.switchSprite(currMember)
            self.switchBody(currMember)
            M.nextMusic(self.playernum)

    def switchSprite(self, currMember):
        """
        Switches from one sprite to the other.
        """
        self.image = Surface([currMember.width, currMember.height])
        self.frameHandler.spriteSheet = IMG.load(currMember.spriteSheet)
        self.frameHandler.reloadSprite()
        self.updateImage()

    def switchBody(self, currMember):
        """
        Changes the speed and power based on the player.
        """
        self.body.maxSpeed = currMember.maxSpeed
        self.body.jumpPower = currMember.jumpPower

    def processAction(self, keys, dt, attackGroup):
        """
        Process key actions for the player.
        """

        if keys[glob.mappedKeys["block"]]:
            self.isBlocking = True
        else:
            self.isBlocking = False

        if self.isBlocking:
            self.setStanding()
            return

        if keys[glob.mappedKeys["attack"]]:
            if not self.attackCoolDown.getState() and not self.isBlocking:
                self.attackCoolDown.fire()
                attackGroup.add(self.attackFactory.makeMelee())

        if keys[glob.mappedKeys["special"]]:
            if not self.specCoolDown.getState() and not self.isBlocking:
                self.specCoolDown.fire()
                attackGroup.add(self.attackFactory.makeSpecial())

        if keys[glob.mappedKeys["switch"]] or \
           keys[glob.mappedKeys["other switch"]]:
            if not self.hasSwitched and not self.isBlocking:
                self.switchPlayer()
                self.hasSwitched = True
        else:
            self.hasSwitched = False

        if keys[glob.mappedKeys["right"]] and keys[glob.mappedKeys["left"]]:
            self.setStanding()
        elif keys[glob.mappedKeys["left"]]:
            self.setWalkingLeft()
        elif keys[glob.mappedKeys["right"]]:
            self.setWalkingRight()
        else:
            self.setStanding()
        if keys[glob.mappedKeys["up"]]:
            self.body.isJumping = True

        # Debug
        if glob.DEBUG:
            if keys[K_v]:
                attackGroup.add(self.attackFactory.makeArcProjectile())

            if keys[K_d]:
                if not self.hasDrank:
                    self.drink()
                    self.hasDrank = True
            else:
                self.hasDrank = False

    def drink(self):
        """
        Heal the player by a constant percentage of health, but
        also induce some side effects.
        """
        self.health += self.maxHealth * 0.15
        if self.health > self.maxHealth:
            self.health = self.maxHealth
        self.intox += 9
        if self.intox > self.maxIntox:
            self.intox = self.maxIntox

    # OVERRIDES
    def setCollided(self, collidesWith):
        super(Player, self).setCollided(collidesWith)

        result = self.body.collidePlatform(collidesWith)
        if result is None:
            return  # Since most tiles don't have property
        if result == "beer":
            self.drink()
            return "remove"
        elif result == "win":
            self.win = True
        elif result == "barrier":
            if len(filter(
                lambda e: e.body.x <= collidesWith.x and
                    collidesWith.x - 800 <= e.body.x, self.enemies)) == 0:
                return "remove"