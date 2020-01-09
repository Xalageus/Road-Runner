import pygame
from pygame.locals import *
from roadr.road import road
from roadr.printer import printer

#Max num of tiles to draw including off screen
TILES = 180
#Max tiles left to right
WIDTH = 10
#Tile pos to start drawing from (bottom most)
HEIGHT = 15
DEF_TILE_WIDTH = 36
DEF_TILE_HEIGHT = 32

class tile_system():
    def __init__(self, tileFiles, disWidth, disHeight, debug_mode, debug_quiet):
        self.tiles = [0] * TILES
        self.tileFiles = tileFiles
        self.disWidth = disWidth
        self.disHeight = disHeight
        self.map = None
        self.printer = printer(debug_mode)
        self.debug_quiet = debug_quiet
        self.tileObjs = [0] * len(tileFiles)

        self.speedY = 0.2
        #Current row (from bottom to top) to draw at
        self.row = 0
        #Current num of rows read from map and drawn 
        self.rowCount = 0
        self.initial = True
        self.lowestYPos = 0.0

    def initTileObjs(self):
        i = 0
        for tileF in self.tileFiles:
            self.tileObjs[i] = road(tileF.filename, 0, 0, False)
            i += 1

    def drawTile(self, tile, tilePos, j):
        """Create a tile to be drawn"""
        item = str.split(tile, ".")

        flip = False
        if item[1] == str(1):
            flip = True

        if item[0] is not "#":

            if self.initial:
                #Only on setTiles()
                self.tiles[tilePos] = self.tileObjs[int(item[0])].copy(DEF_TILE_WIDTH * j, DEF_TILE_HEIGHT * self.row, flip)
            else:
                #Use last known lowest yPos (top most tile) minus the default tile height
                self.tiles[tilePos] =self.tileObjs[int(item[0])].copy(DEF_TILE_WIDTH * j, self.lowestYPos - DEF_TILE_HEIGHT, flip)

    def setTiles(self, map):
        """Setup the initial tiles to be drawn"""
        self.map = map
        self.initTileObjs()

        self.row = HEIGHT
        tilePos = 0
        while tilePos < TILES:
            #Tile pos to draw at
            j = 0
            for data in map[self.rowCount]:
                self.drawTile(data, tilePos, j)
                tilePos += 1
                j += 1
            self.rowCount += 1
            self.row -= 1

        self.printer.printDebugInfo(12, tilePos, TILES)
        self.initial = False

    def findEmpty(self):
        """Get a list of empty (0) spots in tile array"""
        empty = [-1] * WIDTH
        i = 0
        count = 0
        while i < TILES and count < WIDTH:
            if self.tiles[i] == 0:
                empty[count] = i
                count += 1
            i += 1

        if empty[9] == -1:
            self.printer.printDebugInfo(28, WIDTH, None)

        return empty

    def drawRow(self, map):
        """Draw a row of tiles at last known lowest yPos minus the
        height of a tile"""
        tilePos = 0
        j = 0
        redraws = self.findEmpty()
        for data in map[self.rowCount]:
            if not self.debug_quiet:
                self.printer.printDebugInfo(26, redraws[tilePos], None)
            self.drawTile(data, redraws[tilePos], j)
            tilePos += 1
            j += 1
        self.rowCount += 1

    def scroll(self, mod, time):
        """Scroll the tiles and check for tiles that are no longer
        needed"""
        speed = self.speedY * (abs(mod) * time)
        self.lowestYPos = 32.0

        #Draw new row?
        newRow = False
        i = 0

        #Set new tile yPos for every tile, check for lowest yPos to
        #record and check for tiles that have gone off screen
        for tile in self.tiles:
            if tile is not 0:
                tile.yPos = tile.yPos + speed

                if tile.yPos < self.lowestYPos:
                    self.lowestYPos = tile.yPos

                if tile.yPos > self.disHeight:
                    newRow = True
                    self.destroyTile(i)

            i += 1

        if not self.debug_quiet:
            self.printer.printDebugInfo(24, self.lowestYPos, None)

        if newRow:
            self.drawRow(self.map)

    def destroyTile(self, tile):
        """Destroy a tile. Sets to '0'"""
        if not self.debug_quiet:
            self.printer.printDebugInfo(25, tile, None)
        self.tiles[tile] = 0

    def destroyTiles(self):
        """Destroy all tiles at once"""
        self.tiles = [0] * TILES

    def resetTiles(self):
        """Reset tile system"""
        self.row = 0
        self.rowCount = 0
        self.initial = True
        self.destroyTiles()
        self.setTiles(self.map)

    def debugScroll(self, mod, time, up):
        """Manually scroll tiles without drawing new ones or removing
        any"""
        speed = self.speedY * (abs(mod) * time)

        for tile in self.tiles:
            if tile is not 0:
                if up:
                    tile.yPos = tile.yPos + speed
                else:
                    tile.yPos = tile.yPos - speed