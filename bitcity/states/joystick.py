# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import state
import glob
from images import movingBackground as MB
from pygame import key
from pygame import display
from pygame import Rect
from pygame import joystick
import pygame.draw
from pygame.locals import *
import os
import joystickFunction as joy
from images import gameImage as GI


class joystick(state.State):

    def __init__(self, s):
        super(joystick, self).__init__(s)
        self.background = MB.MovingBackground(s)
        self.title = "Controller Settings"
        self.subHeading = "which peripheral do you want to use"
        self.keyboard = False
        # keyboard menu settings
        self.chooseKeyboard = "Keyboard"
        self.chooseController = "Controller"
        self.chooseButtons = "choose Buttons"
        self.mainChoices = (self.chooseKeyboard,
                            self.chooseController,
                            glob.settingsString)

        # controller menu settings
        self.controllerChoices = (self.chooseButtons,
                                  glob.keySettings,
                                  glob.settingsString)
        # genereal choices tuple
        self.choices = self.mainChoices

        self.controller = False  # true if mapping to controller

        self.buttonIntake = False  # true if we are currently button intaking

        # will be greater than 0 if editing a specific key,
        # is index of glob.typesOfAttacks
        self.keyChoice = 0

        # position for menu selection
        self.pos = 0

        pygame.event.clear()
        # clears the event queue to make sure input is clean

        # name of key to be mapped to be blitted to screen since tab and shift
        # don't have ascii values
        self.keyInput = ''
        # actual key value of key to be changed
        self.keyChange = ''

# draws the menus needed but also handles what menu you are in and general
# functionality n the joystick module
    def draw(self):
        self.background.draw()
        self.blitToScreen(self.title, 0)

# if the user is trying to change the settings of controller
        if self.controller:
            if self.buttonIntake:
              # if the user is in the key changing mod don't give any options
              # but to change that specific key
                if self.keyChoice > 0 and glob.joystick:
                    self.controllerMap(self.keyChoice)
                    self.choices = ()
              # else list the keys you can change
                else:
                    self.choices = (
                        glob.typesOfAttacks[3:] + [glob.settingsString])
                    self.blitToScreen(
                        "what button do you want to change",
                        self.s.get_height() * .2)
        # prints the main menu for chooses for the keyboard interface
            else:
                self.controllerSetup()
                self.choices = self.controllerChoices

# if the user is trying to change the settings of a keyboard
        elif self.keyboard:
        # if the user chooses to try and change the buttons
            if self.buttonIntake:
              # if the user is in the key changing mod don't give any options
              # but to change that specific key
                if self.keyChoice > 0:
                    self.keyboardMap(self.keyChoice)
                    self.choices = ()
              # else list the keys you can change
                else:
                    self.choices = (
                        glob.typesOfAttacks[3:] + [glob.settingsString])
                    self.blitToScreen(
                        "what key do you want to change",
                        self.s.get_height() * .2)
        # prints the main menu for chooses for the keyboard interface
            else:
                self.choices = self.controllerChoices

        else:
            # just asks what peripheal you wan to use if you haven't specified
            self.blitToScreen(self.subHeading, self.s.get_height() * .2)

      # prints any menu choices if there are any
        for i in range(len(self.choices)):
            # i+6/15 makes it look pretty

            # if more than 8 menu items are split in half
            if(len(self.choices)) >= 8:
                if i < len(self.choices) / 2:
                    self.blitToScreen(
                        self.choices[i],
                        self.s.get_height() * (i + 5) / 15,
                        i, .25)
                else:
                    self.blitToScreen(
                        self.choices[i],
                        self.s.get_height() * (i - (
                            len(self.choices) / 2 - 4) + 1) / 15,
                        i, .75)

            # if less than 8 menu items can just go in the center
            else:
                self.blitToScreen(
                    self.choices[i],
                    self.s.get_height() * (i + 5) / 15,
                    i)
        display.flip()

# handles the printing to the screen and the logistics of changing what a key
# is mapped to process
    def keyboardMap(self, keyInt):
        self.blitToScreen("press a key for", self.s.get_height() * .2, 10)

        self.blitToScreen(
            glob.typesOfAttacks[keyInt],
            self.s.get_height() * .3,
            10)

        self.blitToScreen(
            "you choose: " + self.keyInput,
            self.s.get_height() * .6,
            10)

        if self.keyInput != '':
            self.blitToScreen(
                "press enter if you want this key",
                self.s.get_height() * .7,
                10)

    def controllerMap(self, keyInt):
        self.blitToScreen("press a key for", self.s.get_height() * .2, 10)

        self.blitToScreen(
            glob.typesOfAttacks[keyInt],
            self.s.get_height() * .3,
            10)

        for f in glob.joystickKeys:
            if f():
                self.keyInput = glob.typesOfAttacks[glob.joystickKeys.index(f)]

        self.blitToScreen(
            "you choose to switch keys with: " + self.keyInput,
            self.s.get_height() * .6,
            10)

        if self.keyInput != '':
            self.blitToScreen(
                "press enter if you want this key",
                self.s.get_height() * .7,
                10)

# deals with setting up and changing the buttons for a controller
    def controllerSetup(self):
        pygame.joystick.init()
        if glob.joystick:
            self.blitToScreen(
                "Joystick attached!",
                self.s.get_height() * .2,
                10)
            return

        if pygame.joystick.get_count() < 1:
            self.blitT / \
                Screen("hook up joystick", self.s.get_height() * .2, 10)
        else:
            if glob.joystick is False:
                glob.Joystick = pygame.joystick.Joystick(0)

                # removes problem with virtual box being stupid
                if "VirtualBox" in glob.Joystick.get_name():
                    if pygame.joystick.get_count() > 2:
                        glob.Joystick = pygame.joystick.Joystick(1)
                    else:
                        self.blitToScreen(
                            "hook up joystick",
                            self.s.get_height() * .2,
                            10)
                        return

                self.blitToScreen(
                    "Joystick attached!",
                    self.s.get_height() * .2,
                    10)

                glob.Joystick.init()
                glob.joystick = True
                # maps joystickkeys to keyboard keys
                glob.joystickKeys = [joy.a, joy.b, joy.c, joy.d, joy.e, joy.f,
                                     joy.g, joy.h, joy.i, joy.j, joy.k, joy.l]
            else:
                self.blitToScreen(
                    "hook up joystick",
                    self.s.get_height() * .2,
                    10)

# takes what to print and at what height, always blits to center
# of the screen
# i aka the number position of the menu item for slection reasons sets to 100
# if not specified to make sure it cna't be slected if not specified
    def blitToScreen(self, toPrint, height, i=100, widthCoefficent=.5):
        col = glob.FONT_COLOR
        backCol = glob.SELECTED_FONT_COLOR
        if i == self.pos:
            backCol, col = col, backCol
        image = glob.FONT.render(toPrint, True, col)
        rect = image.get_rect()
        rect.x = widthCoefficent * (self.s.get_width() - image.get_width())
        rect.y = 20 + height
        if i == self.pos:
            pygame.draw.rect(self.s, backCol, rect)
        self.s.blit(image, rect)

    def update(self, dt):
        super(joystick, self).update(dt)
        self.background.update(dt)

    def incMenu(self, amount):
        """Steps by the passed amount in the menu."""
        self.pos += amount
        if self.pos < 0:
            self.pos = len(self.choices) - 1
        elif self.pos > len(self.choices) - 1:
            self.pos = 0

    def processSelc(self):
        if self.choices[self.pos] == self.chooseKeyboard:
            self.keyboard = True
        elif self.choices[self.pos] == self.chooseController:
            self.controller = True
        elif self.choices[self.pos] == self.chooseButtons:
            self.buttonIntake = True
        elif self.choices[self.pos] in glob.typesOfAttacks:
            self.keyChoice = self.pos + 3
        else:
            return self.choices[self.pos]

    def processKeys(self, keys, dt):
        result = super(joystick, self).processKeys(keys, dt)
        if result != state.standardString:
            return result
        # this elif statement deals with the phsical intake of what
        # key the user is pressing for a key change
        elif self.buttonIntake and self.keyboard:
            for key in pygame.event.get():
                if key.type == KEYDOWN:
                    if key.unicode.isalnum():
                        self.keyInput = key.unicode
                        self.keyChange = ord(key.unicode)
            if keys[K_TAB]:
                self.keyChange = K_TAB
                self.keyInput = "tab"
            if keys[K_UP]:
                self.keyChange = K_UP
                self.keyInput = "up key"
            if keys[K_DOWN]:
                self.keyChange = K_DOWN
                self.keyInput = "down key"
            if keys[K_RIGHT]:
                self.keyChange = K_RIGHT
                self.keyInput = "right key"
            if keys[K_LEFT]:
                self.keyChange = K_LEFT
                self.keyInput = "left key"
            if keys[K_RSHIFT]:
                self.keyChange = K_RSHIFT
                self.keyInput = "Right Shift"
            if keys[K_LSHIFT]:
                self.keyChange = K_LSHIFT
                self.keyInput = "Left shift"
            pygame.event.clear()

        if keys[glob.mappedKeys["up"]]:
            self.timeAlive = 0
            self.incMenu(-1)
        elif keys[glob.mappedKeys["down"]]:
            self.timeAlive = 0
            self.incMenu(1)
        # next two handles left and right for long menus with two columns

        elif len(self.choices) >= 8 and keys[glob.mappedKeys["right"]]:
            self.timeAlive = 0
            self.incMenu(len(self.choices) / 2)

        elif len(self.choices) >= 8 and keys[glob.mappedKeys["left"]]:
            self.timeAlive = 0
            self.incMenu(-(len(self.choices) / 2))

        elif keys[glob.mappedKeys["select"]]:
            self.timeAlive = 0
            if self.keyChange != '' and self.keyChoice > 0 and self.keyboard:
                glob.Keys.currentKeys[self.keyChoice] = self.keyChange
                glob.mappedKeys = dict(
                    zip(glob.typesOfAttacks, glob.Keys.currentKeys))
                self.keyChoice = 0
                self.keyChange = ''
                self.keyInput = ''
            if self.buttonIntake and self.keyChoice > 0 and self.controller:
                tempFunc = glob.joystickKeys[
                    glob.typesOfAttacks.index(self.keyInput)]
                switchFunc = glob.joystickKeys[self.keyChoice]
                glob.joystickKeys[self.keyChoice] = tempFunc
                glob.joystickKeys[
                    glob.typesOfAttacks.index(
                        self.keyInput)] = switchFunc
                self.keyChoice = 0
                self.keyChange = ''
                self.keyInput = ''

            elif len(self.choices) != 0:
                return self.processSelc()
