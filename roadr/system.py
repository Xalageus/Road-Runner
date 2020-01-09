import pygame
from pygame.locals import *
import os
from roadr.printer import printer
from roadr.player import player
from roadr.tilesys import tile_system
from roadr.map import mapRead
from roadr.assets import asset_system

FPS = 60
DIS_WIDTH = 360
DIS_HEIGHT = 512
MAX_JOY = 2

class system():
    def __init__(self, debug_mode):
        self.printer = printer(debug_mode)
        self.printer.printInfo(0, None)

        pygame.init()
        self.printer.printDebugInfo(1, pygame.get_sdl_version(), None)
        pygame.display.set_caption("Road Runner")
        self.screen = pygame.display.set_mode(size=(DIS_WIDTH, DIS_HEIGHT))
        self.clock = pygame.time.Clock()

        self.assets = None
        self.player = None
        self.tilesys = None
        self._running = True
        self.debug_mode = debug_mode
        self.inputCount = 0
        self.js = [0] * MAX_JOY
        self.j0HLeft = False
        self.j0HRight = False
        self.j0A0Left = False
        self.j0A0Right = False
        self.mapRead = mapRead()
        self.timeMod = 0
        self.nextFPSReport = 0
        self.j0B0 = False

        self.getAssets()
        self.gameInit()

    def getAssets(self):
        self.assets = asset_system()
        self.assets.mergePaths()

    def gameInit(self):
        self.tilesys = tile_system(self.assets.tiles, DIS_WIDTH, DIS_HEIGHT, self.debug_mode)
        map = self.mapRead.readMap(self.assets.maps[0])
        self.tilesys.setTiles(map)
        self.player = player(self.assets.objs[0], DIS_WIDTH / 2, DIS_HEIGHT * 0.8)

        self.draw()
        self.joystickInit()

    def joystickInit(self):
        joyCount = pygame.joystick.get_count()
        self.printer.printDebugInfo(0, joyCount, None)
        curJoy = 0
        i = 0
        while i < joyCount:
            if curJoy < MAX_JOY:
                self.js = pygame.joystick.Joystick(i)
                self.js.init()
                self.joystickReport(self.js)
                curJoy += 1

            i += 1

        if curJoy == 0:
            self.printer.printInfo(1, None)

    def joystickReinit(self):
        self.printer.printDebugInfo(16, None, None)
        pygame.joystick.quit()
        self.js = [0] * MAX_JOY
        pygame.joystick.init()
        self.joystickInit()

    def joystickReport(self, joystick):
        if self.debug_mode:
            self.printer.printDebugInfo(3, joystick.get_name(), None)
            self.printer.printDebugInfo(7, joystick.get_numhats(), None)
            self.printer.printDebugInfo(8, joystick.get_numaxes(), None)

    def fpsReport(self):
        if self.debug_mode:
            if pygame.time.get_ticks() > self.nextFPSReport:
                self.printer.printDebugInfo(11, self.clock.get_fps(), FPS)
                self.nextFPSReport = pygame.time.get_ticks() + 5000

    def draw(self):
        self.screen.fill((240, 60, 51))

        for tile in self.tilesys.tiles:
            if tile is not 0:
                self.screen.blit(tile.image, (tile.xPos, tile.yPos))
        self.screen.blit(self.player.image, (self.player.xPos, self.player.yPos))
        pygame.display.flip()

    def joyHold(self):
        if self.j0HLeft:
            self.player.moveLeft(self.timeMod)
            self.draw()
        elif self.j0HRight:
            self.player.moveRight(self.timeMod)
            self.draw()
        elif self.j0A0Left:
            self.player.moveLeftAxis(self.js.get_axis(0), self.timeMod)
            self.draw()
        elif self.j0A0Right:
            self.player.moveRightAxis(self.js.get_axis(0), self.timeMod)
            self.draw()
            
        if self.j0B0:
            self.tilesys.scroll(0.1, self.timeMod)
            self.draw()

    def compEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.printer.printDebugInfo(4, None, None)
                self._running = False
            elif event.type == pygame.JOYBUTTONUP:
                self.printer.printDebugInfo(2, self.inputCount, None)
                if not self.js.get_button(0):
                    self.j0B0 = False
                self.inputCount += 1
            elif event.type == pygame.JOYBUTTONDOWN:
                self.printer.printDebugInfo(5, self.inputCount, None)
                if self.js.get_button(0):
                    self.printer.printDebugInfo(13, None, None)
                    self.j0B0 = True
                self.inputCount += 1
            elif event.type == pygame.JOYHATMOTION:
                self.printer.printDebugInfo(6, self.inputCount, None)
                if self.js.get_hat(0)[0] < 0:
                    self.j0HLeft = True
                    self.j0HRight = False
                elif self.js.get_hat(0)[0] > 0:
                    self.j0HRight = True
                    self.j0HLeft = False
                else:
                    self.j0HLeft = False
                    self.j0HRight = False
                self.inputCount += 1
            elif event.type == pygame.JOYAXISMOTION:
                if self.js.get_axis(0) < -0.2:
                    self.printer.printDebugInfo(10, self.inputCount, self.js.get_axis(0))
                    self.j0A0Left = True
                    self.j0A0Right = False
                elif self.js.get_axis(0) > 0.2:
                    self.printer.printDebugInfo(10, self.inputCount, self.js.get_axis(0))
                    self.j0A0Right = True
                    self.j0A0Left = False
                else:
                    self.printer.printDebugInfo(9, self.inputCount, None)
                    self.j0A0Left = False
                    self.j0A0Right = False
                self.inputCount += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    if self.debug_mode:
                        self.printer.printDebugInfo(15, None, None)
                        self.tilesys.resetTiles()
                        self.draw()
                elif event.key == pygame.K_F2:
                    if self.debug_mode:
                        self.joystickReinit()

    def mainLoop(self):
        while self._running:
            self.compEvents()
            self.joyHold()
            self.fpsReport()
            self.timeMod = self.clock.get_time()
            self.clock.tick(FPS)