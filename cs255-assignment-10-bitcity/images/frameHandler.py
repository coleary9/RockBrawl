# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from pygame import Surface
from pygame.transform import flip

from images import imageDict as IMG, gameImage as GI
from images import frameLoader as FL
from metro import Metro


class FrameHandler(object):

    """Abstract class to represent an image handler."""

    def __init__(self, width, height, spriteName):
        raise Exception("FrameHandler is abstract, don't init it.")

    def update(self, dt, isAtt, collidedY, direction, shouldBlink):
        pass

    def reloadSprite(self):
        pass

    def getImage(self, facing):
        raise Exception("You must implement the getImage method.")


class PassiveFrameHandler(FrameHandler):

    """Handles frame holding of a sprite with only one image."""

    def __init__(self, spriteName):
        if spriteName is None:
            # Eventually gameObject should compose a drawing component
            # once we stop using pygame's collisions.
            # For now we give it a blank surface instead.
            surf = Surface((0, 0)).convert_alpha()
            self.visible = False
        else:

            surf = IMG.load(spriteName)
            self.visible = True
        # List with [1] = right-facing and [-1] = left-facing.
        self.frames = [None, FL.loadFrame(surf),
                       FL.loadFrame(flip(surf, True, False))]

    def getImage(self, facing):
        return self.frames[facing]


class ActiveFrameHandler(FrameHandler):

    """Handles frame holding and updating of a sprite."""

    def __init__(
            self, width, height,
            spriteName):
        self.width = width
        self.height = height
        self.blinker = Metro(100, 100)
        self.spriteSheet = IMG.load(spriteName)
        self.reloadSprite()
        self.supervisor = FrameSupervisor(self.images, 1)
        self.visible = True

    def update(self, dt, attackTime, collidedY, direction, shouldBlink):
        if shouldBlink:
            self.visible = self.blinker.tick(dt)
        else:
            self.visible = True
        self.updateSprite(dt, attackTime, collidedY, direction)

    def updateSprite(self, dt, attackTime, collidedY, direction):
        if 0 < attackTime < 4 * self.supervisor.frameTime:
            frameIndex = 4
        elif collidedY == 0:
            frameIndex = 3
        elif not direction == 0:
            frameIndex = 2
        else:
            frameIndex = 1

        self.supervisor = makeSupervisor(
            frameIndex, self.supervisor, self.images)
        self.supervisor.update(dt)

    def reloadSprite(self):
        self.images = FL.loadFrames(self.spriteSheet, self.width,
                                    self.height, self.height, self.height * 2)

    def getImage(self, facing):
        return self.supervisor.getImage(self.images, facing)


class FrameSupervisor(object):

    """Handles advancing the frame according to a set of rules."""

    def __init__(self, images, index):
        self.length = len(images[index])
        self.gen = frameGens[index](self.length)
        # the frame location we are in for our anim
        self.frame = self.gen.next()
        self.frameTime = 100  # length of one frame in milliseconds
        self.metro = Metro(self.frameTime, 0)
        self.index = index

    def update(self, dt):
        if self.metro.tick(dt):
            self.frame = self.gen.next()

    def getImage(self, images, facing):
        return images[self.index * facing][self.frame]


def normalFrameGen(length):
    # Spit out 0, 1, 2, 3, 0, 1, 2, 3...
    while True:
        for x in xrange(length):
            yield x


def jumpFrameGen(length):
    # Spit out 0, 1, 2, 3, 3, 3, 3, 3...
    for x in xrange(length):
        yield x
    while True:
        yield x

frameGens = [None, normalFrameGen, normalFrameGen,
             jumpFrameGen, jumpFrameGen]


def makeSupervisor(index, currentSupervisor, images):
    """Factory function to make a frame supervisor object."""
    if currentSupervisor.index == index:
        return currentSupervisor
    return FrameSupervisor(images, index)