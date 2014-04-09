# BitCity Studios:
# Cameron Mc'Leary <coleary9@jhu.edu>
# Stewie Griffin  <sgriff27@jhu.edu>
# Jeremeye Dolinkoe <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shatit  <shavitmichael@gmail.com>

from pygame import Surface
from pygame import SRCALPHA
import glob


def loadFrame(surf):
    frame = Frame(surf.get_size(), 0, 0)
    frame.blit(surf, (0, 0))
    return frame

normalFrameIndices = [-3, -2, -1, 1, 2, 3]
playerFrameIndices = [-4, -3, -2, -1, 1, 2, 3, 4]
drummerFrameIndices = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]


def loadFrames(spriteSheet, x, y, x2, y2, numNormFrames=6,
               xOffAttL=-25, xOffAttR=0, yOffAtt=-75):
    """A function to load the frame images of a GameObject."""
    numNormAnims = numNormFrames / 2
    images = [[] for i in xrange(numNormFrames + 3)]
    for i in xrange(4):
        # this loads all animations into images, all anims length 4
        frameAttR = Frame((x2, y2), xOffAttR, yOffAtt)
        frameAttL = Frame((x2, y2), xOffAttL, yOffAtt)

        # attL
        frameAttL.blit(spriteSheet, (0, 0), (i * x2, 0, x2, y2))
        images[-numNormAnims - 1].append(frameAttL)

        # Do normal-sized frames.
        for j in xrange(numNormFrames):
            frame = Frame((x, y), 0, 0)
            frame.blit(spriteSheet, (0, 0), (i * x, j * y + y2, x, y))
            # Quick hack for now.
            if numNormFrames <= 6:
                images[normalFrameIndices[j]].append(frame)
            elif numNormFrames <= 8:
                images[playerFrameIndices[j]].append(frame)
            else:
                images[drummerFrameIndices[j]].append(frame)

        # attR
        frameAttR.blit(spriteSheet, (0, 0), (
            i * x2, numNormFrames * y + y2, x2, y2))
        images[numNormAnims + 1].append(frameAttR)

    return images


class Frame(Surface):

    """A smarter surface that stores info about offsets
       and frameTime for a particular frame."""

    def __init__(self, dim, relXOff, relYOff):
        Surface.__init__(self, dim, SRCALPHA)
        self.xOff = glob.Screen.WIDTH * 0.5 + relXOff
        self.yOff = glob.Screen.HEIGHT * 0.5 + relYOff
