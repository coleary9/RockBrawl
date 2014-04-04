# BitCity Studios:
# Cameron Mc'Leary <coleary9@jhu.edu>
# Stewie Griffin  <sgriff27@jhu.edu>
# Jeremeye Dolinkoe <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shatit  <shavitmichael@gmail.com>

from pygame import image

from os import path


IMAGES = {}


def load(imageName):
    """Loads an alpha image into memory."""
    img = IMAGES.get(imageName)
    if img is not None:
        return img
    fullName = path.join(path.dirname(__file__),
                         imageName)
    return image.load(fullName).convert_alpha()


def loadNonAlpha(imageName):
    """Loads a non-alpha image into memory."""
    img = IMAGES.get(imageName)
    if img is not None:
        return img
    fullName = path.join(path.dirname(__file__),
                         imageName)
    return image.load(fullName).convert()
