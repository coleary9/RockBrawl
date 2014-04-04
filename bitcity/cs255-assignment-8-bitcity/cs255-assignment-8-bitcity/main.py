# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import pygame
from pygame import display, time, event, key, font
from pygame.locals import *

from types import LambdaType
import os
import math
import argparse
from states import game as G, menu as M, highScore as HS, youWin as YW
from states import exit as EX, state as ST, title as TI, cut, joystick
from states import volume as V, difficulty as D
import glob

# States are defined as a dictionary.
# An uninitialized state key gets a lambda expression as its value.

# To make a new state and hook it up, several things need to be done.
# You need to add it to the state dict at the top of main.py.
# You need to add a constructor call to the stateBuilder function.
# If the state you want to make does not fit any available template
# (like a menu), you'll also have to write a class which inherits
# from state.State. If you want to make a new state similar to a
# currently written state, consider making the existing state more
# generic or extracting parts of it into classes rather than copying
# and pasting code.

states = {glob.titleString: lambda s: TI.Title(s),
          glob.menuString:
          lambda s: M.Menu(s, glob.menuString, M.MAIN_CHOICES),
          glob.gameString:
          lambda s: loadLevel(s, glob.levelChoices[glob.LEVEL]),
          glob.cutString: lambda s: cut.Cut(s, glob.LEVEL),
          glob.levelString:
          lambda s: M.Menu(s, glob.levelString, M.getLevelChoices()),
          glob.highScoreString: lambda s: HS.HighScore(s),
          glob.youWinString: lambda s: winLevel(s),
          glob.exitString: lambda s: EX.Exit(s),
          glob.settingsString:
          lambda s: M.Menu(s, glob.settingsString, M.SETTINGS_CHOICES),
          glob.resolutionString:
          lambda s: M.Menu(s, glob.resolutionString, M.RESOLUTION_CHOICES),
          glob.volumeString: lambda s: V.Volume(s),
          glob.difficultyString: lambda s: D.Difficulty(s),
          glob.keySettings: lambda s: joystick.joystick(s),
          glob.tinyRes: lambda s: setResolution(glob.tinyRes, s),
          glob.smallRes: lambda s: setResolution(glob.smallRes, s),
          glob.mediumRes: lambda s: setResolution(glob.mediumRes, s),
          glob.largeRes: lambda s: setResolution(glob.largeRes, s)}


def main(**args):
    # Set global constants from command line flags.
    setFlags(args)

    glob.loadSettings()
    glob.mappedKeys = dict(zip(glob.typesOfAttacks, glob.Keys.currentKeys))
    # Init pygame.
    pygame.init()
    s = display.set_mode([glob.Screen.WIDTH, glob.Screen.HEIGHT])
    s.convert_alpha()
    glob.FONT = font.Font(glob.FONT_PATH, glob.FONT_SIZE)

    # Init game state.
    state, s = stateBuilder(glob.titleString, s)
    clock = time.Clock()
    leftover = 0
    INTERVAL_CONST = 5
    interval = INTERVAL_CONST

    # Run main game loop until the user quits.

    result = None
    while result != glob.exitString:
        # Find the delta time to figure out how much stuff should move.
        leftover += clock.tick()

        # Draw the current frame.
        state.draw()
        # Process event queue.
        for ev in event.get([KEYUP, pygame.QUIT]):
            if ev.type == pygame.QUIT:
                result = glob.exitString

        interval = min(leftover, INTERVAL_CONST)
        while leftover >= interval and result != glob.exitString:

            # Do calculations for current game state.
            reset = state.update(interval)
            if reset:
                # Resets dt
                clock.tick()
                leftover = 0
                break
            leftover -= interval
            if interval <= 0:
                break
            # processActions handles non-event-based keyboard input
            # AND handles states deciding to end/pause (e.g. for game win,
            # pause, etc).
            # Right now, the only way to transition between states
            # is via key presses. If the processKey of the current state
            # returns a non-None value, the stateBuilder function returns
            # the new state. This can be either a saved state or a new state.
            result = processKeysAndActions(state, interval)
            if result is not None:
                states[state.name] = state
                state, s = stateBuilder(result, s)
                # Resets dt
                clock.tick()
                leftover = 0

    # Quit the game.
    state.quit()

    glob.saveSettings()


def processKeysAndActions(state, dt):
    keys = list(key.get_pressed())
    if(glob.joystick):
        for f in glob.joystickKeys:
            if f():
                keys[glob.Keys.currentKeys[glob.joystickKeys.index(f)]] = 1
    return state.processActions(keys, dt)


def stateBuilder(result, s):

    if result in glob.levelDict:
        glob.LEVEL = glob.levelChoices.index(result)
        return loadLevel(s, result), s
    """
    If the result is a state key string which has an uninitialized value,
    constructs and returns the new state. Otherwise, returns the
    saved state after resetting a few values if necessary.
    """
    if isinstance(states[result], LambdaType):
        st = states[result](s)
    else:
        st = states[result]
        st.reset(s)
    return st, s


def loadLevel(s, levelSelected):
    """ Returns a game state loaded with the level given by levelSelected"""
    level = glob.levelDict[levelSelected]
    return G.Game(s, level)


def winLevel(s):
    """ Get's called when a level is won.
    Goes to the next cutscene and then level if any
    else go to highscores cutscenes and reset level progress
    """
    glob.LEVEL += 1
    if glob.LEVEL > glob.Levels.lastLevel:
        glob.Levels.lastLevel = glob.LEVEL
        glob.saveSettings()
    # destroy game to reconstruct (score is kept)
    states[glob.gameString] = \
        lambda s: loadLevel(s, glob.levelChoices[glob.LEVEL])

    if glob.LEVEL > len(glob.levelDict.keys()):  # Won the game
        glob.LEVEL = 1
        return YW.YouWin(s)
    return cut.Cut(s, glob.LEVEL)


def setResolution(result, s):
    splitIndex = result.index('x')
    glob.Screen.WIDTH = int(result[:splitIndex].strip())
    glob.Screen.HEIGHT = int(result[splitIndex + 1:].strip())
    display.set_mode([glob.Screen.WIDTH, glob.Screen.HEIGHT])
    return M.Menu(s, glob.settingsString, M.SETTINGS_CHOICES)


def setFlags(args):
    glob.DEBUG = args['debug']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Rock and Brawl',
                                     version='0.3')
    parser.add_argument('-d', '--debug',
                        help='run in debug mode', action="store_true")
    args = parser.parse_args()
    main(**vars(args))
