# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import glob
import math

halfTile = glob.tileSize / 2


class Camera(object):

    """
    Class to draw objects at proper offsets for the sidescroller
    and handle various screen effects like drunkenness.
    """

    def __init__(self, s, initX=0, initY=0):

        self.surf = s
        self.x = initX
        self.y = initY
        self.lastX = self.x
        self.lastY = self.y
        self.pos = (self.x, self.y)
        self.angle = 0
        self.radius = 0

    def draw(self, drawMe):
        """Draws the drawable object at an offset on the screen."""
        drawMe.draw(self.pos, self.surf)

    def update(self, dt, playerPos, playerIntox):
        """Updates the camera position."""
        self.angle += .00005 * playerIntox * dt
        self.radius = playerIntox / 20
        if self.angle > 360:
            self.angle = 0
        self.lastX = self.x
        self.lastY = self.y
        self.x = weightedAve(self.x, playerPos[0])
        self.y = weightedAve(self.y, playerPos[1])
        self.x += math.cos(self.angle) * self.radius
        self.y += math.sin(self.angle) * self.radius
        self.setPos((self.x, self.y))

    def setPos(self, pos):
        """Sets the camera position."""
        self.pos = pos

    def tileChanged(self):
        """
        Returns True if the camera is on the same tile as last update,
        False otherwise.
        """
        return int(self.x / halfTile) != \
            int(self.lastX / halfTile) \
            or int(self.y / halfTile) != \
            int(self.lastY / halfTile)


def weightedAve(big, small):
    """
    Returns a weighted average where the first argument is weighted heavier
    than the first. Note that this func does not take dt into account and
    will perform differently with different FPS. This should be fixed
    eventually.
    """
    return big * 0.98 + small * 0.02
