import pygame
from pygame.locals import *
from roadr.road import road
from roadr.printer import printer

TILES = 180
WIDTH = 10
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

        self.speedY = 0.2
        self.draws = 1
        self.row = 0
        self.rowCount = 0
        self.lastRow = 0.0
        self.initial = True
        self.lowestYPos = 0.0

    def drawTile(self, tile, tilePos, j):
        item = str.split(tile, ".")

        flip = False
        if item[1] == str(1):
            flip = True

        if item[0] is not "#":
            if self.initial:
                self.tiles[tilePos] = road(self.tileFiles[int(item[0])].filename, DEF_TILE_WIDTH * j, DEF_TILE_HEIGHT * self.row, flip)
            else:
                self.tiles[tilePos] = road(self.tileFiles[int(item[0])].filename, DEF_TILE_WIDTH * j, self.lowestYPos - DEF_TILE_HEIGHT, flip)

    def setTiles(self, map):
        self.map = map

        self.row = HEIGHT
        tilePos = 0
        while tilePos < TILES:
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
        speed = self.speedY * (abs(mod) * time)
        self.lowestYPos = 32.0

        nredraw = False
        i = 0

        for tile in self.tiles:
            if tile is not 0:
                tile.yPos = tile.yPos + speed

                if tile.yPos < self.lowestYPos:
                    self.lowestYPos = tile.yPos

                if tile.yPos > self.disHeight:
                    nredraw = True
                    self.destroyTile(i)

            i += 1

        if not self.debug_quiet:
            self.printer.printDebugInfo(24, self.lowestYPos, None)

        if nredraw:
            self.drawRow(self.map)

    def destroyTile(self, tile):
        if not self.debug_quiet:
            self.printer.printDebugInfo(25, tile, None)
        self.tiles[tile] = 0

    def destroyTiles(self):
        self.tiles = [0] * TILES

    def resetTiles(self):
        self.draws = 1
        self.row = 0
        self.rowCount = 0
        self.lastRow = 0.0
        self.initial = True
        self.destroyTiles()
        self.setTiles(self.map)

    def debugScroll(self, mod, time, up):
        speed = self.speedY * (abs(mod) * time)

        for tile in self.tiles:
            if tile is not 0:
                if up:
                    tile.yPos = tile.yPos + speed
                else:
                    tile.yPos = tile.yPos - speed