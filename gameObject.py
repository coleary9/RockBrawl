# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import pygame
import pygame.display
from pygame import sprite

from physics.body import Body
import glob


class GameObject(sprite.Sprite):

    """An object in the game."""

    def __init__(
            self, x, y, width, height,
            frameHandler):
        pygame.sprite.Sprite.__init__(self)  # first, make a self
        self.image = pygame.Surface([width, height])  # This will be changed
        # Dimensions stuff
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        # Physics.
        self.body = Body(x, y, width, height)
        self.rect.x = self.body.x
        self.rect.y = self.body.y

        # Sprite frame handling
        self.frameHandler = frameHandler

        self.updateImage()

        self.propLastCollide = None

        self.fullTime = 0

    def draw(self, pos, surf):
        """Draw the GameObject on the screen if it is in a visible state."""
        if not self.frameHandler.visible:
            return
        surf.blit(self.image, self.getScreenPos(pos))

    def update(self, dt):
        self.fullTime += dt

        self.updateImage()

        self.body.update(dt)

        self.rect.x = self.body.x
        self.rect.y = self.body.y

        super(GameObject, self).update()

    def getScreenPos(self, playerPosition):
        """
        Gets the screen-adjusted position of the sprite's rect.
        Due to sidescrolling, we need to offset by the player's position.
        The x/yOffs are usually zero but may need to be set for non-standard-
        sized frames like melee attacks.
        """
        return (self.rect.x - playerPosition[0] + self.image.xOff,
                self.rect.y - playerPosition[1] + self.image.yOff)

    def updateImage(self):
        """Update the current image of our sprite animation."""
        self.image = self.frameHandler.getImage(self.body.facing)

    def isInRect(self, pos):
        """
        Returns True if the sprite is within the displayed screen,
        False otherwise.
        """
        screenPos = self.getScreenPos(pos)
        return -self.rect.width < screenPos < \
            glob.Screen.WIDTH + self.rect.width and \
            -self.rect.width < screenPos < \
            glob.Screen.HEIGHT + self.rect.width

    def setCollided(self, collidesWith):
        """
        Handle collision restitution for the GameObject with another object.
        Only handles tile collisions at the moment.
        Return "remove" to remove tile.
        """
        self.propLastCollide = collidesWith.prop
        self.body.collidePlatform(collidesWith)

    def reloadSprite(self):
        """Reloads the GameObject's sprite from memory."""
        self.frameHandler.reloadSprite()

    def pos(self):
        """Returns a tuple of the position of the GameObject's body."""
        return (self.body.x, self.body.y)
