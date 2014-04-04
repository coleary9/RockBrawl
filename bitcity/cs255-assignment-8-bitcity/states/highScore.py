# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>
from pygame import key
from pygame import display
from pygame import Rect
import pygame.draw

from pygame.locals import *
import os
from images import movingBackground as MB
import state
import glob

STANDARD_HIGH_SCORES = """1000:BIT
900:CIT
800:YST
700:UDI
600:0S
500:AAA
400:BBB
300:CCC
200:DDD
100:EEE"""

# class for both displaying highScores and for taking them in


class HighScore(state.State):

    def __init__(self, s):
        super(HighScore, self).__init__(s)
        self.background = MB.MovingBackground(s)
        self.title = "High Scores"
        self.name = ""
        self.nameDone = not glob.newScore
        self.hasError = False
        pygame.event.clear()
# clears the event file to make sure input is clean

    def draw(self):
        self.background.draw()

        highscores = self.parseHighScores()
        if glob.newScore and not glob.isPaused:
            if self.hasError:
                self.error()
            glob.previousLevelScore = 0
            self.drawInput()
            highscores = self.addScore(highscores, self.name)
            self.toFile(highscores)
 # not else cuz above can change newScore
        else:
            self.showHighScores(highscores)
            glob.SCORE = 0  # clears out highScore to play again
        display.flip()

    def addScore(self, highscores, newName):
        newList = highscores
        # causes lsit only to be updated if new name is>3
        if (not self.nameDone):
            return newList
        for i in range(len(highscores)):
            item = highscores[len(highscores) - i - 1]
            if glob.SCORE > int(item[0]):
                newList[(len(highscores) - i - 1)] = [str(glob.SCORE), newName]
                if i != 0:
                    newList[len(highscores) - i] = item
            else:
                break
        glob.newScore = False
        self.nameDone = False
        return newList

    def toFile(self, highscore):
        highscorefile = glob.getFile('highscores.txt')
        if os.path.isfile(highscorefile):
            f = open(highscorefile, 'w')
            for i in range(len(highscore)):
                f.write(highscore[i][0])
                f.write(":")
                f.write(highscore[i][1])
                f.write("\n")
            f.close()

    def parseHighScores(self):
        # find highscores.txt, create score array
        highscorefile = 'highscores.txt'
        if os.path.isfile(highscorefile):
            f = open(highscorefile, 'r')
            lines = f.readlines()
            scores = []
            for line in lines:
                scores.append(line.strip().split(':'))
            f.close()
            return scores
        else:
            # create nonexistant highscores.txt file
            f = open("highscores.txt", 'w')
            f.write(STANDARD_HIGH_SCORES)
            f.close()
            return self.parseHighScores()

    def showHighScores(self, scores):
        # showing scores
        self.blitToScreen(self.title, 0, .5 * self.s.get_width())
        for i in range(len(scores)):
            name = scores[i][1]
            score = scores[i][0]  # get name and score from score array
            # names
            nameimage = glob.FONT.render(name, True, glob.FONT_COLOR)
            namerect = nameimage.get_rect()
            namerect.left, namerect.y = 40, 100 + \
                (i * (namerect.height + self.s.get_height() / 50))
            self.s.blit(nameimage, namerect)

            # scores
            scoreimage = glob.FONT.render(score, True, glob.FONT_COLOR)
            scorerect = scoreimage.get_rect()
            scorerect.right, scorerect.y = (
                self.s.get_width() - 40), namerect.y
            self.s.blit(scoreimage, scorerect)

    def drawInput(self):
        self.blitToScreen(self.title, 0, .5 * self.s.get_width())
        self.blitToScreen("NEW HIGHSCORE:    INPUT NAME",
                          self.s.get_height() * .25, self.s.get_width() * .5)
        if (not self.nameDone and len(self.name) < 10):
            self.blitToScreen(
                self.name,
                self.s.get_height() * .25 + 50,
                self.s.get_width() * .5)
        else:
            glob.newScore = False
            self.nameDone = True

# blits to screen a message taking the height and width to blit to, adds
# 20 to height so it isn't off the screen
# half of image over so that the center is blitted at where you want
    def blitToScreen(self, toPrint, height, width):
        image = glob.FONT.render(toPrint, True, glob.FONT_COLOR)
        rect = image.get_rect()
        rect.x = width - (.5 * image.get_width())  # for centering reasons
        rect.y = 20 + height
        self.s.blit(image, rect)

    def update(self, dt):
        super(HighScore, self).update(dt)
        self.background.update(dt)

    def error(self):
        self.blitToScreen("enter characters!", self.s.get_height() * .8,
                          .5 * self.s.get_width())

    def processKeys(self, keys, dt):

        result = super(HighScore, self).processKeys(keys, dt)
        if result != state.standardString:
            return result
        elif keys[glob.mappedKeys["select"]]:
            if glob.isPaused:
                return glob.menuString

            if glob.newScore and len(self.name) > 0:
                self.nameDone = True
                self.timeAlive = 0
                return None
            elif glob.newScore:
                self.hasError = True
                return None
            # stops enter from caring over from enter name
            elif self.timeAlive > 150:
                return glob.menuString
        elif keys[K_BACKSPACE]:
            self.name = self.name[:-1]
            pygame.event.clear()
        for key in pygame.event.get():
            if key.type == KEYDOWN:
                if key.unicode.isalpha():
                    self.name += key.unicode

        return None