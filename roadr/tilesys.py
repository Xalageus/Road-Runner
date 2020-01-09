import pygame
from pygame.locals import *
from roadr.road import road
from roadr.printer import printer

TILES = 200
WIDTH = 5
HEIGHT = 12
DEF_TILE_WIDTH = 36
DEF_TILE_HEIGHT = 32

class tile_system():
    def __init__(self, tileFiles, disWidth, disHeight, debug_mode):
        self.tiles = [0] * TILES
        self.tileFiles = tileFiles
        self.disWidth = disWidth
        self.disHeight = disHeight
        self.map = None
        self.printer = printer(debug_mode)

        self.speedY = 0.2

    def setTiles(self, map):
        self.map = map

        tile = 0
        i = 0
        for row in map:
            j = 0
            for data in row:
                item = str.split(data, ".")

                flip = False
                if item[1] == str(1):
                    flip = True

                if item[0] is not "#":
                    self.tiles[tile] = road(self.tileFiles[int(item[0])].filename, DEF_TILE_WIDTH * j, DEF_TILE_HEIGHT * i, flip)
                    tile += 1
                j += 1
            i += 1

        self.printer.printDebugInfo(12, tile, TILES)

    def scroll(self, mod, time):
        for tile in self.tiles:
            if tile is not 0:
                tile.yPos = tile.yPos + (self.speedY * (abs(mod) * time))

    def resetTiles(self):
        self.setTiles(self.map)