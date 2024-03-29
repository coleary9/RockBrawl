# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

from pygame import Surface
from pygame.transform import flip, rotate

from images import imageDict as IMG, gameImage as GI
from images import frameLoader as FL
from metro import Metro


class FrameHandler(object):

    """Abstract class to represent an image handler."""

    def __init__(self, width, height, spriteName):
        raise Exception("FrameHandler is abstract, don't init it.")

    def update(self, dt, isAtt, collidedY, direction, shouldBlink,
               isBlocking):
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


class RotatingFrameHandler(PassiveFrameHandler):

    """Handles a passive sprite that rotates over time."""

    def __init__(self, spriteName, w, h, facing):
        self.rotation = 0
        super(RotatingFrameHandler, self).__init__(spriteName)
        self.width = w
        self.height = h
        self.facing = facing

    def update(self, dt):
        self.rotation -= 2 * dt * self.facing

    def getImage(self, facing):
        surf = FL.Frame((self.width, self.height), 0, 0)
        surf.blit(
            rotate(self.frames[facing], self.rotation), (0, 0))
        return surf


class ActiveFrameHandler(FrameHandler):

    """Handles frame holding and updating of a sprite."""

    def __init__(
            self, width, height,
            spriteName, numNormFrames=6, width2=75, height2=150,
            xOffAttL=-25, xOffAttR=0, yOffAtt=-75):
        self.width = width
        self.height = height
        self.numNormFrames = numNormFrames
        self.width2 = width2
        self.height2 = height2
        self.xOffAttL = xOffAttL
        self.xOffAttR = xOffAttR
        self.yOffAtt = yOffAtt
        self.blinker = Metro(100, 100)
        self.spriteSheet = IMG.load(spriteName)
        self.reloadSprite()
        self.supervisor = FrameSupervisor(self.images, 1)
        self.visible = True
        # Frame index assignments
        normFramesAbs = numNormFrames / 2
        self.ATTACK_FRAME = normFramesAbs + 1
        self.BLOCK_FRAME = normFramesAbs
        self.JUMP_FRAME = 3
        self.RUN_FRAME = 2
        self.STAND_FRAME = 1

    def update(self, dt, attackTime, collidedY, direction, shouldBlink,
               isBlocking):
        if shouldBlink:
            self.visible = self.blinker.tick(dt)
        else:
            self.visible = True
        self.updateSprite(dt, attackTime, collidedY, direction, isBlocking)

    def updateSprite(self, dt, attackTime, collidedY, direction,
                     isBlocking):
        if 0 < attackTime < 4 * self.supervisor.frameTime:
            frameIndex = self.ATTACK_FRAME
        elif isBlocking:
            frameIndex = self.BLOCK_FRAME
        elif collidedY == 0:
            frameIndex = self.JUMP_FRAME
        elif not direction == 0:
            frameIndex = self.RUN_FRAME
        else:
            frameIndex = self.STAND_FRAME

        self.supervisor = makeSupervisor(
            frameIndex, self.supervisor, self.images)
        self.supervisor.update(dt)

    def reloadSprite(self):
        self.images = FL.loadFrames(self.spriteSheet, self.width,
                                    self.height, self.width2, self.height2,
                                    self.numNormFrames,
                                    self.xOffAttL, self.xOffAttR,
                                    self.yOffAtt)

    def getImage(self, facing):
        return self.supervisor.getImage(self.images, facing)

    def resetAnimation(self):
        self.supervisor.resetAnimation()


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

    def resetAnimation(self):
        self.gen = frameGens[self.index](self.length)


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
             jumpFrameGen, jumpFrameGen, jumpFrameGen, jumpFrameGen]


def makeSupervisor(index, currentSupervisor, images):
    """Factory function to make a frame supervisor object."""
    if currentSupervisor.index == index:
        return currentSupervisor
    return FrameSupervisor(images, index)
