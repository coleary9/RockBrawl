# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>

import pygame
from pygame.locals import *
from pygame import display, sprite

from actors import player as PL
import enemySpawner as ES
from levels import tmxParser as tmxP, tile as TI
from sounds import music as M
from states import state
import glob
import aiAnalyzer as AI
import camera as CA
from layers import layer as LA, dynamicGroup as DG, hud

# Some globals for now. Ideally these should go somewhere better.
playerHeight = 75
playerWidth = 50
# Only actors are rigged up to update with layers at the moment.
# Update this if layers are changed.
ACTORS_INDEX = 2

# Key stuff should get its own class for configuration.
keyNumbers = {K_0: 0,
              K_1: 1,
              K_2: 2,
              K_3: 3,
              K_4: 4,
              K_5: 5,
              K_6: 6,
              K_7: 7,
              K_8: 8,
              K_9: 9}


class Game(state.State):

    """The state representing the gameplay. (Everything that's not a menu.)"""

    def __init__(self, s, level):
        """
        Constructor. Initialize pygame and add all in-game things
        to the list of objects,
        """
        super(Game, self).__init__(s)
        self.name = glob.gameString

        self.tiles, self.mapObjects, self.mapWidth, self.mapHeight = \
            tmxP.load(level)
        self.nodes = AI.genNodes(self.tiles, self.mapWidth)

        self.startXPosition = 0
        self.startYPosition = 0

        self.initializeObjects()
        self.camera = CA.Camera(s, self.startXPosition, self.startYPosition)
        self.updateTiles(self.tiles, self.tilesGroup, self.camera.pos)

    def initializeObjects(self):
        """Initialize dynamic objects in the game."""

        self.tilesGroup = DG.DynamicGroup()

        # Init all objects.
        self.playerGroup = DG.DynamicGroup()  # make a group for the player
        self.itemsGroup = sprite.Group()
        self.checkpoints = []
        self.removedTiles = {}

        # attacks
        self.attackGroup = DG.DynamicGroup()
        self.enemyAttackGroup = DG.DynamicGroup()
        self.enemiesGroup = DG.EnemiesGroup()
        self.enemySpawners = []

        # Init and Loads map objects: enemys spawners and player coordinates
        self.loadMapObjects(self.mapObjects)

        self.player = PL.Player(
            self.startXPosition, self.startYPosition, playerWidth,
            playerHeight, self.enemiesGroup)
        self.playerGroup.add(self.player)
        self.enemiesGroup.addPlayerReference(self.player)

        self.layers = [LA.BackgroundLayer(self.mapWidth),
                       LA.Layer([self.tilesGroup]),  # Tiles layer
                       LA.Layer([self.enemiesGroup,
                                 self.playerGroup,
                                 self.attackGroup,
                                 self.enemyAttackGroup]),  # Actors layer
                       LA.Layer([hud.Hud(self.s, self.player)])]  # Hud layer

    def draw(self):
        """Perform all graphical tasks for this frame."""

        # Draw each layer in order, from back to front.
        for layer in self.layers:
            layer.draw(self.camera)

        # Display the new frame.
        display.flip()

    def update(self, dt):
        """Perform all calculations for the amount of time that has passed."""
        super(Game, self).update(dt)

        # reset boolean
        reset = False

        # check for Death
        if self.player.health <= 0:
            reset = self.respawnPlayer()
        # Gets the current player position
        pos = self.player.pos()
        self.collideWithTiles(self.playerGroup, pos)
        self.collideWithTiles(self.enemiesGroup, pos)
        self.collideWithTiles(self.attackGroup, pos)
        self.collideWithTiles(self.enemyAttackGroup, pos)
        # Enemies colliding with players.

        self.checkAtts(dt)  # checks ALL Attacks

        # Update each actor
        self.layers[ACTORS_INDEX].update(dt)

        self.updateTiles(self.tiles, self.tilesGroup, self.camera.pos)

        for enemySpawner in reversed(self.enemySpawners):
            if enemySpawner.update(pos):
                self.enemySpawners.remove(enemySpawner)

        # Updates the camera's position, offset, and effects.
        self.camera.update(dt, self.player.pos(), self.player.intox)

        # Check for checkpoints
        for checkpoint in self.checkpoints:
            if pos[0] > checkpoint[0] > self.startXPosition:
                self.startXPosition = checkpoint[0]
                self.startYPosition = checkpoint[1]

        return reset  # to reset dts on player death

    def respawnPlayer(self):
        """
        Respawns the player at the proper checkpoint and reinits all
        necessary objects.
        """
        playerChoice = 0
        for x in range(len(self.player.players)):
            if x == self.player.playernum:
                playerChoice = self.player.playernum
                break

        self.tiles = dict(self.tiles, **self.removedTiles)
        self.initializeObjects()
        while playerChoice > 0:
            self.player.switchPlayer()
            playerChoice -= 1
        glob.SCORE = glob.previousLevelScore
        return True  # To reset

    def updateTiles(self, tiles, group, pos):
        """
        Only tiles on the screen are updated and drawn.
        This method decides which tiles are on the screen.
        """
        if not self.camera.tileChanged():
            if not self.player.body.checkForceTileChanged():
                return
        group.empty()
        topLeft = TI.getTileIndex((pos[0] - glob.Screen.WIDTH * 0.5
                                   - 2 * glob.tileSize,
                                   pos[1] - glob.Screen.HEIGHT
                                   - 2 * glob.tileSize))
        bottomRight = TI.getTileIndex((pos[0] + glob.Screen.WIDTH * 0.5
                                       + 2 * glob.tileSize,
                                       pos[1] + glob.Screen.HEIGHT * 0.5
                                       + 2 * glob.tileSize))
        for yMult in xrange(topLeft[1] * self.mapWidth,
                            bottomRight[1] * (self.mapWidth + 1),
                            self.mapWidth):
            for x in xrange(topLeft[0], bottomRight[0] + 1):
                key = yMult + x
                if key in tiles:
                    group.add(tiles[key])

    def collide(self, keysGroup, valuesGroup, playerPos):
        """Uses pygame collision to collide two sprite groups."""
        collDict = sprite.groupcollide(
            keysGroup, valuesGroup, False, False)
        for collided in collDict.keys():
            for collider in collDict[collided]:
                collided.setCollided(collider)

    def collideWithTiles(self, group, playerPos):
        """
        More efficient collision for tiles.
        Since tiles are staticly placed, we can quite easily
        define a pseudo-spatial hash instead of using pygame's
        collision, which is O(n*m) if you try to collide everything
        with everything.

        It might be worth it to define a similar thing for GameObjects.
        This would be more difficult and more computationally intensive
        since GameObjects would have to move to different buckets and
        be members of multiple buckets.
        """
        for spr in group:
            if TI.collideTiles(
                spr,
                self.tiles,
                spr.body.rect,
                self.mapWidth,
                    self.removedTiles):
                self.updateTiles(self.tiles, self.tilesGroup, playerPos)

    def attCollide(self, attackGroup, victimGroup):
        """
        Uses pygame collision to collide two sprite groups.
        Then hits the victim group with each collided attack.
        """
        if len(attackGroup) > 0:
            collDict = sprite.groupcollide(
                attackGroup,
                victimGroup,
                False,
                False)
            for atk in collDict.keys():
                for victim in collDict[atk]:
                    victim.hit(atk)

    def checkAtts(self, dt):
        """Handles all attack checks for this update."""
        # updating enemy attacks
        for enemy in self.enemiesGroup:
            enemy.handleAttacks(self.enemyAttackGroup)

        # Attack object collisions
        self.attCollide(self.attackGroup, self.enemiesGroup)
        self.attCollide(self.enemyAttackGroup, self.playerGroup)

    def processActions(self, keys, dt):
        """
        Processes anything related to changing states (e.g win, pause, etc)
        """
        # Take care of "global" key preccess (e.g Escape)
        result = super(Game, self).processKeys(keys, dt)

        if result != state.standardString:
            return result

        result = self.processKeys(keys, dt)
        if self.player.win:
            M.stopMusic()
            glob.previousLevelScore = glob.SCORE
            glob.newScore = True
            return glob.youWinString

        return result

    def processKeys(self, keys, dt):
        """Process key input."""
        # Processes keys related to player
        self.player.processAction(keys, dt, self.attackGroup)

        if keys[glob.mappedKeys["pause"]]:
            M.stopMusic()
            glob.isPaused = True
            return glob.menuString

        if glob.DEBUG and keys[glob.mappedKeys["god mode"]]:
            # Quick "god mode" to test out a remote checkpoint.
            # CTRL + a number key.
            for key in keyNumbers:
                if keys[key]:
                    num = keyNumbers[key]
                    if num is not None and num < len(self.checkpoints):
                        checkpoint = self.checkpoints[num]
                        self.startXPosition = checkpoint[0]
                        self.startYPosition = checkpoint[1]
                        self.respawnPlayer()

    def reset(self, s):
        super(Game, self).reset(s)
        self.player.body.forceTileChanged = True
        self.player.reloadSprite()
        for enemy in self.enemiesGroup:
            enemy.reloadSprite()
        for layer in self.layers:
            layer.reset()
        M.initMusic()

    def loadMapObjects(self, objectDict):
        """Loads objects from the tiled map into memory."""
        for prop in objectDict.keys():
            if prop == "playerStart":
                for item in objectDict[prop]:
                    if self.startXPosition == 0:
                        self.startXPosition = item[0]
                        self.startYPosition = item[1]
            elif "Spawn" in prop:
                for item in objectDict[prop]:
                    if prop == "BSpawn" or prop == "FSpawn":
                        count = 1
                    else:
                        count = 5

                    # objectDict[prop] = collection of enemy spawner (x,y)
                    self.enemySpawners.append(
                        ES.EnemySpawner(count,
                                        prop,
                                        item[0],
                                        item[1],
                                        self.enemiesGroup,
                                        self.nodes,
                                        self.mapWidth,
                                        self.mapHeight))
            elif prop == "checkpoint":
                for item in objectDict[prop]:
                    self.checkpoints.append((item[0], item[1]))

if __name__ == "__main__":
    main()
