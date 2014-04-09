# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from images import imageDict as IMG
from levels import tile as TI
import glob

LEFT_JUMP = -1
RIGHT_JUMP = 1
BOTH_JUMP = 0


def genNodes(tiles, mapWidth):
    """
    Find tiles that the enemies should jump on.
    """
    nodes = {}
    for key in tiles:
        if not (key - mapWidth in tiles or
                key - mapWidth * 2 in tiles or
                key - mapWidth * 3 in tiles):
            if not ((key + 1) in tiles or (key - 1) in tiles):
                if glob.DEBUG:
                    tiles[key].image = IMG.load('aiTestTileBothJump.png')
                nodes[key] = BOTH_JUMP
            elif not (key - 1) in tiles:
                if glob.DEBUG:
                    tiles[key].image = IMG.load(
                        'aiTestTileLeftJump.png')
                nodes[key] = LEFT_JUMP
            elif not (key + 1) in tiles:
                if glob.DEBUG:
                    tiles[key].image = IMG.load(
                        'aiTestTileRightJump.png')
                nodes[key] = RIGHT_JUMP
    return nodes
