# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>
from pygame import font
from pygame import Color
import pygame
from os import path, remove
from cPickle import dump, load

"""Global variables and utility functions for the game."""

# Interpreter flags
DEBUG = False


class Screen(object):

    """Enum-like class for Screen constants."""
    WIDTH = 800
    HEIGHT = 600


class Volume(object):

    """A Dumb gross fix for saving the volume."""
    VOLUME = 100  # Volume Level out of 100.


class Keys(object):

    """another gross fix to save key settings"""
    currentKeys = []


class Joystick(object):

    """holder class for any intalizied JoyStick"""
    pass

# class JoystickKeys(object):
    """holds the controls for a joystick similar to Keys
       if a                                                   """
    joystickKeys = []

tileSize = 32  # Assigned by parser, so not a "constant".


# What game level we are on
LEVEL = 1

# for pausing
isPaused = False

# State constants
cutString = "cut"
titleString = "Title"
exitString = "Quit"
gameString = "Continue"
levelString = "Select LeveL"
menuString = "Main Menu"
highScoreString = "High Scores"
settingsString = "Settings"
youWinString = "You Win"
stateString = "State"
resolutionString = "Resolution"
volumeString = "Volume"
brightnessString = "Brightness"
keySettings = "Controller Settings"
tinyRes = "800 x 600"
smallRes = "1024 x 768"
mediumRes = "1600 x 900"
largeRes = "1920 x 1080"

typesOfAttacks = [exitString, "select", "god mode", "up", "down", "left",
                  "right", "attack", "special", "block", "switch", "other switch", "pause"]

# Mapping array
defaultKeys = [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_LCTRL, pygame.K_UP,
               pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_x,
               pygame.K_s, pygame.K_LCTRL, pygame.K_LSHIFT, pygame.K_RSHIFT,
               pygame.K_p]

if len(Keys.currentKeys) < 1:
    Keys.currentKeys = defaultKeys

mappedKeys = dict(zip(typesOfAttacks, Keys.currentKeys))

joystick = False


def getFile(fileName):
    """Returns the absolute path of a file."""
    return path.join(path.dirname(__file__), fileName)

# Level variables
levelChoices = [None, 'Level 1', 'Level 2', 'level 3', menuString]
levelDict = {levelChoices[1]: "levels/level1.tmx",
             levelChoices[2]: "levels/level2.tmx",
             levelChoices[3]: "levels/level3.tmx"}
previousLevelScore = 0
SCORE = 0
newScore = False

# Font constants
FONT = None
FONT_COLOR = Color(61, 72, 78, 255)
SELECTED_FONT_COLOR = Color(225, 236, 242, 0)
FONT_PATH = getFile("fonts/CHINESER.TTF")
FONT_SIZE = 32

SETTINGS_FILE = 'settings.pickle'


def createPersistentDict():
    """Returns a dict representation of settings."""
    return {"sh": Screen.HEIGHT,
            "sw": Screen.WIDTH,
            "v": Volume.VOLUME,
            "k": Keys.currentKeys
            }


def loadFromPersistentDict(pers):
    """Loads settings from a pickle dictionary."""
    Screen.HEIGHT = pers['sh']
    Screen.WIDTH = pers['sw']
    Volume.VOLUME = pers['v']
    Keys.currentKeys = pers['k']


def saveSettings():
    """Saves to a pickle."""
    settingsFile = open(getFile(SETTINGS_FILE), 'w+')
    dump(createPersistentDict(), settingsFile)
    settingsFile.close()


def loadSettings():
    """Loads settings from a pickle file."""
    fileName = getFile(SETTINGS_FILE)
    if path.exists(fileName):
        try:
            settingsFile = open(fileName)
            loadFromPersistentDict(load(settingsFile))
            settingsFile.close()
        except Exception:
            remove(fileName)
