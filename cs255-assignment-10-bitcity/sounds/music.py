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

# Guitar Trax
G_DICT = {
    1: mixer.Sound("sounds/audioprac2.ogg"),
    2: mixer.Sound("sounds/audioprac2.ogg"),
    3: mixer.Sound("sounds/audioprac2.ogg")
}

# Drum Trax
D_DICT = {
    1: mixer.Sound("sounds/audioprac1.ogg"),
    2: mixer.Sound("sounds/audioprac1.ogg"),
    3: mixer.Sound("sounds/audioprac1.ogg")
}

# Audio Level Tuples for each player
PLYR_VOL_DICT = {
    0: (0.7, 0.6),
    1: (0.4, 0.9)
}

# Voiceovers
VO_DICT = {
    1: mixer.Sound("sounds/intro.ogg")
}

# Sound FX
HITSOUND = mixer.Sound("sounds/thud.ogg")

# Music Channels
G_CHNL = mixer.Channel(1)
D_CHNL = mixer.Channel(2)

# Sound Effect Channels
FX_CHNL = mixer.Channel(6)

# Constant to know which levels to return to after state changes
PLYR = 0


def theVolume():
    me = float(glob.Volume.VOLUME) / 100
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
    setmusic()


def nextMusic(playerid):
    """
    Changes the music depending on the player onscreen.
    """
    PLYR = playerid
    FX_CHNL.set_volume(theVolume())
    G_CHNL.set_volume(PLYR_VOL_DICT[PLYR][0] * theVolume())
    D_CHNL.set_volume(PLYR_VOL_DICT[PLYR][1] * theVolume())


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


def hitFX():
    FX_CHNL.play(HITSOUND, 1)


def voiceOver():
    D_CHNL.set_volume(0.8 * theVolume())
    D_CHNL.play(VO_DICT[glob.LEVEL], 0)