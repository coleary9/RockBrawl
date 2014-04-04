# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from pygame import Surface
from pygame import sprite
from pygame import image
from pygame import SRCALPHA

import glob
from levels import imageTileDict as IMG


class TileSheet(object):

    def __init__(self, source, firstgid):
        self.spriteSheet = IMG.load(source)
        self.tileImages = []
        self.createTileImages()
        self.firstgid = firstgid

    def createTileImages(self):
        numInCols = int(self.spriteSheet.get_height() / glob.tileSize)
        numInRows = int(self.spriteSheet.get_width() / glob.tileSize)
        for c in range(numInCols):
            for r in range(numInRows):
                tileSurf = Surface((glob.tileSize, glob.tileSize), SRCALPHA)
                tileSurf.blit(self.spriteSheet, (0, 0),
                              (r * glob.tileSize, c * glob.tileSize,
                               glob.tileSize, glob.tileSize))
                self.tileImages.append(tileSurf)


class Tile(sprite.Sprite):

    def __init__(self, gid, pos, mapWidth, tileSheet, property):
        sprite.Sprite.__init__(self)

        self.prop = property
        self.gid = gid - tileSheet.firstgid
        self.pos = pos
        self.x = glob.tileSize * (pos % mapWidth)
        self.y = glob.tileSize * (pos / mapWidth)
        if gid < len(tileSheet.tileImages):
            self.image = tileSheet.tileImages[self.gid]
        else:
            self.image = tileSheet.tileImages[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def getAbsolutePos(self):
        return (self.x,
                self.y)

    def draw(self, pos, surf):
        if 'noDraw' not in self.prop:
            surf.blit(self.image, self.getScreenPos(pos))

    def getScreenPos(self, playerPosition):
        return (self.x - playerPosition[0] + glob.Screen.WIDTH * 0.5,
                self.y - playerPosition[1] + glob.Screen.HEIGHT * 0.5)

    def isInRect(self, pos):
        screenPos = self.getScreenPos(pos)
        return -self.rect.width < screenPos < \
            glob.Screen.WIDTH + self.rect.width and \
            -self.rect.width < screenPos < \
            glob.Screen.HEIGHT + self.rect.width

    def collideRect(self, otherRect):
        """
        A Rect collision using >= instead of >.
        Not currently used for anything.
        """
        return not (self.rect.left >= otherRect.right or
                    self.rect.right <= otherRect.left or
                    self.rect.top >= otherRect.bottom or
                    self.rect.bottom <= otherRect.top)

    def __str__(self):
        return 'gid: ' + str(self.gid) + ' pos: ' + str(self.pos) + \
               ' x: ' + str(self.x) + ' y: ' + str(self.y)


def collideTiles(spr, tiles, rect, mapWidth, removedTiles):
    """Collides all tiles that the rect is inside.
    Deletes tiles when they need to be removed.
    """
    topLeft = getTileIndex(rect.topleft)
    bottomRight = getTileIndex(rect.bottomright)
    sprSetCollided = spr.setCollided
    shouldUpdate = False
    for yMult in xrange(topLeft[1] * mapWidth,
                        bottomRight[1] * (mapWidth + 1),
                        mapWidth):
        for x in xrange(topLeft[0], bottomRight[0] + 1):
            key = yMult + x
            if key in tiles:
                if sprSetCollided(tiles[key]) == "remove":
                    removedTiles[key] = tiles[key]
                    del tiles[key]
                    shouldUpdate = True
    return shouldUpdate


def getTileIndex(pos):
    """Convert a rect position into an absolute tile index."""
    x = int(pos[0] / glob.tileSize)
    y = int(pos[1] / glob.tileSize)
    return (x, y)


def getTileKey(pos, mapWidth):
    tileIndex = getTileIndex(pos)
    return tileIndex[0] + tileIndex[1] * mapWidth
