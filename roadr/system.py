import pygame
from pygame.locals import *
import os
import time
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
    def __init__(self, debug_mode, debug_quiet_tile_sys, opengl, debug_quiet_controller_input):
        self.printer = printer(debug_mode)
        self.printer.printInfo(0, None)
        #TODO: Add opengl support
        pygame.init()
        self.printer.printDebugInfo(1, pygame.get_sdl_version(), None, None)
        #Set/init pygame modules
        pygame.display.set_caption("Road Runner")
        self.screen = pygame.display.set_mode(size=(DIS_WIDTH, DIS_HEIGHT), flags=DOUBLEBUF)
        self.screen.set_alpha(None)
        self.clock = pygame.time.Clock()

        #Init system vars
        self.assets = None
        self.player = None
        self.tilesys = None
        self._running = True
        self.debug_mode = debug_mode
        self.debug_quiet_tile_sys = debug_quiet_tile_sys
        self.debug_quiet_controller_input = debug_quiet_controller_input
        self.inputCount = 0
        self.js = [0] * MAX_JOY
        self.j0HLeft = False
        self.j0HRight = False
        self.j0A0Left = False
        self.j0A0Right = False
        self.j0A3Up = False
        self.j0A3Down = False
        self.mapRead = mapRead(debug_mode)
        self.timeMod = 0
        self.nextRegReport = 0
        self.j0B0 = False
        self.moveSpeed = 0
        self.loopTime = None
        self.times = [0] * FPS
        self.timesPos = 0
        self.fullTimes = False
        self.timesFirst = True

        #Finish init
        self.getAssets()
        self.gameInit()

    def getAssets(self):
        """Get asset file info and full paths to the files"""
        self.assets = asset_system(self.debug_mode)
        self.assets.mergePaths()

    def gameInit(self):
        """Init tile system and player, then call joystickInit"""
        self.tilesys = tile_system(self.assets.tiles, DIS_WIDTH, DIS_HEIGHT, self.debug_mode, self.debug_quiet_tile_sys)
        map = self.mapRead.readMap(self.assets.maps[0])
        self.tilesys.setTiles(map)
        self.player = player(self.assets.objs[0], DIS_WIDTH / 2, DIS_HEIGHT * 0.8)

        self.draw()
        self.joystickInit()

    def joystickInit(self):
        """Find ready controllers then init them"""
        #Currently only first joy is read
        joyCount = pygame.joystick.get_count()
        self.printer.printDebugInfo(0, joyCount, None, None)
        curJoy = 0
        i = 0
        while i < joyCount:
            #Only init controllers until we reach MAX_JOY
            if curJoy < MAX_JOY:
                self.js = pygame.joystick.Joystick(i)
                self.js.init()
                self.joystickReport(self.js)
                curJoy += 1

            i += 1

        if curJoy == 0:
            self.printer.printInfo(1, None)

    def joystickReinit(self):
        """Destroy controllers then re-init them"""
        self.printer.printDebugInfo(16, None, None, None)
        pygame.joystick.quit()
        self.js = [0] * MAX_JOY
        pygame.joystick.init()
        self.joystickInit()

    def joystickReport(self, joystick):
        """Print controller info"""
        if self.debug_mode:
            self.printer.printDebugInfo(3, joystick.get_name(), None, None)
            self.printer.printDebugInfo(7, joystick.get_numhats(), None, None)
            self.printer.printDebugInfo(8, joystick.get_numaxes(), None, None)
            self.printer.printDebugInfo(17, joystick.get_numbuttons(), None, None)

    def regReport(self):
        """In debug mode, print current fps, time since last tick and current movement speed"""
        if self.debug_mode:
            if pygame.time.get_ticks() > self.nextRegReport:
                self.printer.printDebugInfo(11, self.clock.get_fps(), FPS, None)
                self.printer.printDebugInfo(29, self.loopTime, None, None)
                self.printer.printDebugInfo(22, self.moveSpeed, None, None)
                self.nextRegReport = pygame.time.get_ticks() + 5000

    def draw(self):
        """Draw tiles, objs, HUD, menus to the screen"""
        self.screen.fill((240, 60, 51))

        for tile in self.tilesys.tiles:
            if tile is not 0:
                self.screen.blit(tile.image, (tile.xPos, tile.yPos))
        self.screen.blit(self.player.image, (self.player.xPos, self.player.yPos))
        pygame.display.flip()

    def joyHold(self):
        """Compute events when a button or axis is held down/outside of deadzone"""
        #Move player left or right (left/right HAT or left stick)
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
            
        #Move player forward (scroll screen) (Button 0)
        if self.j0B0:
            if self.moveSpeed < 1:
                self.moveSpeed += 0.01
            self.tilesys.scroll(self.moveSpeed, self.timeMod)
            self.draw()
        else:
            #Gradually slow down player when button is not held down
            if self.moveSpeed > 0:
                self.moveSpeed -= 0.002
            if self.moveSpeed < 0:
                self.moveSpeed = 0
            if self.moveSpeed is not 0:
                self.tilesys.scroll(self.moveSpeed, self.timeMod)
                self.draw()

        #If debug mode is enabled, allow player to scroll screen manually without
        #destroying or adding tiles (up/down right stick)
        if self.debug_mode:
            if self.j0A3Up:
                self.tilesys.debugScroll(self.js.get_axis(3), self.timeMod, True)
                self.moveSpeed = 0
                self.draw()
            elif self.j0A3Down:
                self.tilesys.debugScroll(self.js.get_axis(3), self.timeMod, False)
                self.moveSpeed = 0
                self.draw()

    def compEvents(self):
        """Compute pygame events including controller button UP/DOWN and axis changes"""
        #TODO: Clean this up/use switch statements instead of if, elif, ...
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.printer.printDebugInfo(4, None, None, None)
                self._running = False
            elif event.type == pygame.JOYBUTTONUP:
                if not self.debug_quiet_controller_input:
                    self.printer.printDebugInfo(2, self.inputCount, None, None)
                if not self.js.get_button(0):
                    self.j0B0 = False
                self.inputCount += 1
            elif event.type == pygame.JOYBUTTONDOWN:
                if not self.debug_quiet_controller_input:
                    self.printer.printDebugInfo(5, self.inputCount, None, None)
                if self.js.get_button(0):
                    if not self.debug_quiet_controller_input:
                        self.printer.printDebugInfo(13, None, None, None)
                    self.j0B0 = True
                self.inputCount += 1
            elif event.type == pygame.JOYHATMOTION:
                if not self.debug_quiet_controller_input:
                    self.printer.printDebugInfo(6, self.inputCount, None, None)
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
                    if not self.debug_quiet_controller_input:
                        self.printer.printDebugInfo(10, self.inputCount, self.js.get_axis(0), None)
                    self.j0A0Left = True
                    self.j0A0Right = False
                elif self.js.get_axis(0) > 0.2:
                    if not self.debug_quiet_controller_input:
                        self.printer.printDebugInfo(10, self.inputCount, self.js.get_axis(0), None)
                    self.j0A0Right = True
                    self.j0A0Left = False
                else:
                    if not self.debug_quiet_controller_input:
                        self.printer.printDebugInfo(9, self.inputCount, None, None)
                    self.j0A0Left = False
                    self.j0A0Right = False

                if self.js.get_axis(3) < -0.2:
                    if self.debug_mode:
                        if not self.debug_quiet_controller_input:
                            self.printer.printDebugInfo(23, self.inputCount, self.js.get_axis(3), None)
                        self.j0A3Up = True
                        self.j0A3Down = False
                elif self.js.get_axis(3) > 0.2:
                    if self.debug_mode:
                        if not self.debug_quiet_controller_input:
                            self.printer.printDebugInfo(23, self.inputCount, self.js.get_axis(3), None)
                        self.j0A3Down = True
                        self.j0A3Up = False
                else:
                    if self.debug_mode:
                        self.j0A3Up = False
                        self.j0A3Down = False
                self.inputCount += 1
            elif event.type == pygame.KEYDOWN:
                #In debug mode only, reset tile system on Keyboard F1 press
                if event.key == pygame.K_F1:
                    if self.debug_mode:
                        self.printer.printDebugInfo(15, None, None, None)
                        self.moveSpeed = 0
                        self.tilesys.resetTiles()
                        self.draw()
                #In debug mode only, reinit controllers on Keyboard F2 press
                elif event.key == pygame.K_F2:
                    if self.debug_mode:
                        self.joystickReinit()

    def mainLoop(self):
        while self._running:
            startTime = time.perf_counter_ns()
            self.compEvents()
            self.joyHold()
            self.regReport()
            endTime = time.perf_counter_ns()
            self.detectStutter(endTime - startTime)
            self.loopTime = self.clock.get_rawtime() #Get time in milliseconds since last tick (not including time used to lock the fps)
            self.timeMod = self.clock.tick(FPS)

    def detectStutter(self, deltaTime):
        if self.debug_mode:
            if self.timesFirst:
                self.times[self.timesPos] = deltaTime
                self.timesPos += 1
                self.timesFirst = False
            else:
                if self.fullTimes:
                    timesAvg = int(sum(self.times) / FPS)
                    if ((deltaTime + 1) / (timesAvg + 1)) > 10:
                        self.printer.printDebugInfo(30, deltaTime, FPS, timesAvg)
                if self.timesPos == FPS:
                    self.timesPos = 0
                    self.fullTimes = True
                self.times[self.timesPos] = deltaTime
                self.timesPos += 1