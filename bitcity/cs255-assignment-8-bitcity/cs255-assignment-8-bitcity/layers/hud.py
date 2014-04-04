# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremey Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import glob
import pygame
from pygame import Color, time
import math

HEALTH_COLOR = (198, 73, 65, 0)
INTOX_COLOR = (200, 200, 0, 0)
POISON_COLOR = (135, 31, 120, 0)
COOL_COLOR = (191, 235, 255, 0)
hpPixels = 175
hpHeight = 24
offsetRight = 25


class Hud(object):

    """graphical stuff to draw like health"""

    def __init__(self, s, player):
        self.surfBorder = pygame.Surface((hpPixels + 4, hpHeight + 4))
        self.surfBorder.fill(glob.FONT_COLOR)
        self.player = player

        # Init FPS timer.
        if glob.DEBUG:
            self.clock = time.Clock()

    def draw(self, camera):
        """Draws the hud."""
        s = camera.surf
        player = self.player
        if player.health < 0:
            return
        # draw score
        surfScore = glob.FONT.render(
            "Score: " + str(glob.SCORE),
            True,
            glob.FONT_COLOR)
        scoreW = (s.get_width() / 2) - surfScore.get_width() / 2
        s.blit(surfScore, (scoreW, 0))

        # calculate width of hp bar and border
        healthW = player.health * hpPixels / player.maxHealth
        surfHealth = pygame.Surface((healthW, hpHeight))
        surfHealth.fill(HEALTH_COLOR)
        # calculate position of hp bar and border
        healthPos = s.get_width() - hpPixels - offsetRight
        # draw hp
        s.blit(self.surfBorder, (healthPos - 2, hpHeight - 2))
        s.blit(surfHealth, (healthPos, hpHeight))

        # draw inebriation
        # using HP box proporitions for simplicity
        intoxW = player.intox * hpPixels / player.maxIntox
        surfIntox = pygame.Surface((intoxW, hpHeight))
        if player.intox < 50:
            surfIntox.fill(INTOX_COLOR)
        else:
            surfIntox.fill(POISON_COLOR)
        s.blit(self.surfBorder, (healthPos - 2, (hpHeight * 2) - 2))
        s.blit(surfIntox, (healthPos, (hpHeight * 2)))
        # intox

        coolDownW = player.specCoolDown.getPercent() * hpPixels
        if coolDownW == 0:
            coolDownW = hpPixels
        surfCoolDown = pygame.Surface((coolDownW, hpHeight))
        surfCoolDown.fill(COOL_COLOR)
        s.blit(self.surfBorder, (healthPos - 2, (hpHeight * 3) - 2))
        s.blit(surfCoolDown, (healthPos, (hpHeight * 3)))

        if glob.DEBUG:
            # Draw FPS.
            self.clock.tick()
            surf = glob.FONT.render(
                "FPS: %3.2f" % (self.clock.get_fps()),
                True, glob.FONT_COLOR)
            s.blit(surf, (24, 24))

    def update(self, dt):
        pass

    def refresh(self, player):
        self.player = player
