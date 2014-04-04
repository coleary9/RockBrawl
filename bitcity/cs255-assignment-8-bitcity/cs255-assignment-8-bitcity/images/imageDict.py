# BitCity Studios:
# Cameron Mc'Leary <coleary9@jhu.edu>
# Stewie Griffin  <sgriff27@jhu.edu>
# Jeremeye Dolinkoe <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shatit  <shavitmichael@gmail.com>

import pygame
from pygame import image, surface

from os import path


IMAGES = {}


def load(imageName):
    """Loads an alpha image into memory."""
    img = IMAGES.get(imageName)
    if img is not None:
        return img
    if "red_" in imageName:
        imageName = imageName.replace("red_", "")
    if "orange_" in imageName:
        imageName = imageName.replace("orange_", "")
    fullName = path.join(path.dirname(__file__),
                         imageName)
    img = image.load(fullName).convert_alpha()
    IMAGES[imageName] = img
    # Below is hopefully temporary
    if "enemy" in imageName:
        img1 = img.copy()
        img1.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
        IMAGES["red_" + imageName] = img1
        img2 = img.copy()
        img2.fill((255, 127, 0), special_flags=pygame.BLEND_RGB_MULT)
        IMAGES["orange_" + imageName] = img2
    if "vocalist.png" == imageName or imageName == "guitar.png" \
            or "drummer.png" == imageName:
        img1 = img.copy()
        img1.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
        IMAGES["red_" + imageName] = img1
    return IMAGES[imageName]


def loadNonAlpha(imageName):
    """Loads a non-alpha image into memory."""
    img = IMAGES.get(imageName)
    if img is not None:
        return img
    fullName = path.join(path.dirname(__file__),
                         imageName)
    IMAGES[imageName] = image.load(fullName).convert()
    return IMAGES[imageName]
