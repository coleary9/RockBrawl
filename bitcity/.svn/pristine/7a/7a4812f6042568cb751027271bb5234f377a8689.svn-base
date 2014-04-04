# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import pygame
from pygame import mixer

import glob

mixer.init()  # Mixer initialization

menuGuit = glob.getFile("sounds/cleanguit.ogg")
menuDrum = glob.getFile("sounds/cleandrum.ogg")
guitarTraxFile = glob.getFile("sounds/audioprac2.ogg")
drumTraxFile = glob.getFile("sounds/audioprac1.ogg")
lowGuit = glob.getFile("sounds/lowguit.ogg")
lowDrum = glob.getFile("sounds/lowdrum.ogg")
psychGuit = glob.getFile("sounds/psychguitar.ogg")
psychDrum = glob.getFile("sounds/psychdrum.ogg")
slohvyGuit = glob.getFile("sounds/slohvyguit.ogg")
slohvyDrum = glob.getFile("sounds/slohvydrum.ogg")
bossGuit = glob.getFile("sounds/hvyguit.ogg")
bossDrum = glob.getFile("sounds/hvydrum.ogg")


introFile = glob.getFile("sounds/intro.ogg")
thudFile = glob.getFile("sounds/thud.ogg")
enemyHit = glob.getFile("sounds/body_impact_1_with_grunt_.ogg")
drinkSound = glob.getFile("sounds/human_swallow_gulp.ogg")
specGuit = glob.getFile("sounds/guitarjamatk.ogg")

# Guitar Trax
G_DICT = {
    0: mixer.Sound(menuGuit),
    1: mixer.Sound(guitarTraxFile),
    2: mixer.Sound(lowGuit),
    3: mixer.Sound(psychGuit),
    4: mixer.Sound(slohvyGuit),
    5: mixer.Sound(bossGuit)
}

# Drum Trax
D_DICT = {
    0: mixer.Sound(menuDrum),
    1: mixer.Sound(drumTraxFile),
    2: mixer.Sound(lowDrum),
    3: mixer.Sound(psychDrum),
    4: mixer.Sound(slohvyDrum),
    5: mixer.Sound(bossDrum)
}

# Audio Level Tuples for each player
PLYR_VOL_DICT = {
    0: (0.7, 0.6),
    1: (0.4, 0.9),
    2: (0.0, 0.9)  # TODO
}

# Voiceovers
VO_DICT = {
    1: mixer.Sound(introFile)
}

# Sound FX
ENEMYHIT = mixer.Sound(enemyHit)
DRINKSOUND = mixer.Sound(drinkSound)
SPECGUIT = mixer.Sound(specGuit)
PLYRHIT = {
    0: mixer.Sound(thudFile),
    1: mixer.Sound(thudFile),
    2: mixer.Sound(thudFile)
}

# Music Channels
G_CHNL = mixer.Channel(1)
D_CHNL = mixer.Channel(2)

# Sound Effect Channels
FX_CHNL = mixer.Channel(6)
FX_2_CHNL = mixer.Channel(7)

# Constant to know which levels to return to after state changes
PLYR = 0


def theVolume():
    me = float(glob.Settings.VOLUME) / 100
    return me


def setmusic():
    """
    Sets up the music channels on init.
    """
    G_CHNL.set_volume(PLYR_VOL_DICT[PLYR][0] * theVolume())
    D_CHNL.set_volume(PLYR_VOL_DICT[PLYR][1] * theVolume())
    G_CHNL.play(G_DICT[glob.LEVEL], -1)
    D_CHNL.play(D_DICT[glob.LEVEL], -1)


def initMusic():
    """
    Initialize Music based on what stage we are on.
    Currently assumed that we use the first player.
    """
    FX_CHNL.set_volume(theVolume())
    FX_2_CHNL.set_volume(theVolume())
    setmusic()


def nextMusic(playerid):
    """
    Changes the music depending on the player onscreen.
    """
    PLYR = playerid
    FX_CHNL.set_volume(theVolume())
    G_CHNL.set_volume(PLYR_VOL_DICT[PLYR][0] * theVolume())
    D_CHNL.set_volume(PLYR_VOL_DICT[PLYR][1] * theVolume())


def menuMusic():
    """
    Plays the music in the menu
    """
    G_CHNL.set_volume(theVolume() * .6)
    D_CHNL.set_volume(theVolume())
    G_CHNL.play(G_DICT[0], -1)
    D_CHNL.play(D_DICT[0], -1)


def pauseMusic():
    """
    Pauses the music.
    """
    G_CHNL.pause()
    D_CHNL.pause()


def unpauseMusic():
    """
    Resumes the music from where it left off.
    """
    nextMusic(PLYR)
    G_CHNL.unpause()
    D_CHNL.unpause()


def stopMusic():
    """
    Completely stops all audio channels.
    """
    G_CHNL.stop()
    D_CHNL.stop()
    FX_CHNL.stop()


def enemyHitFX():
    FX_CHNL.play(ENEMYHIT, 0)


def drinkFX():
    FX_CHNL.play(DRINKSOUND, 0)


def playerHit():
    FX_CHNL.play(PLYRHIT[PLYR], 0)


def specGuit():
    FX_2_CHNL.play(SPECGUIT, 0)
    G_CHNL.set_volume(PLYR_VOL_DICT[PLYR][0] * theVolume() * .70)
    D_CHNL.set_volume(PLYR_VOL_DICT[PLYR][1] * theVolume() * .70)


def voiceOver():
    D_CHNL.set_volume(0.8 * theVolume())
    D_CHNL.play(VO_DICT[glob.LEVEL], 0)
