from roadr.__init__ import __version__

class printer():
    def __init__(self, debug):
        self.PRINT_DEBUG = debug

    def tupToStr(self, tup):
        string = ""
        count = 0

        for t in tup:
            string += str(t)

            if count < (len(tup) - 1):
                string += "."

            count += 1

        return string

    def printDebugInfo(self, msg, arg, argTwo):
        if(self.PRINT_DEBUG):
            if msg == 0:
                print("[Debug SYS] # of controllers: " + str(arg))
            if msg == 1:
                print("[Debug SYS] SDL version: " + str(self.tupToStr(arg)))
            if msg == 2:
                print("[Debug SYS] Received JOYBUTTONUP input " + str(arg))
            if msg == 3:
                print("[Debug SYS] Joystick '" + str(arg) + "' connected")
            if msg == 4:
                print("[Debug SYS] Received QUIT")
            if msg == 5:
                print("[Debug SYS] Received JOYBUTTONDOWN input " + str(arg))
            if msg == 6:
                print("[Debug SYS] Received JOYHATMOTION input " + str(arg))
            if msg == 7:
                print("[Debug SYS] # of Hats: " + str(arg))
            if msg == 8:
                print("[Debug SYS] # of Axes: " + str(arg))
            if msg == 9:
                print("[Debug SYS] Received JOYAXISMOTION (in deadzone) input " + str(arg))
            if msg == 10:
                print("[Debug SYS] Received JOYAXISMOTION input " + str(arg) + " (" + str(argTwo) + ")")
            if msg == 11:
                print("[Debug SYS] FPS: " + str(arg) + " / " + str(argTwo))
            if msg == 12:
                print("[Debug TILESYS] Tiles loaded: " + str(arg) + " / " + str(argTwo))
            if msg == 13:
                print("[Debug SYS] Received Button 0")
            if msg == 14:
                print("[Debug SYS] Released Button 0")
            if msg == 15:
                print("[Debug SYS] Resetting tiles to original state...")
            if msg == 16:
                print("[Debug SYS] Re-initializing controllers...")
            if msg == 17:
                print("[Debug SYS] # of Buttons: " + str(arg))

    def printInfo(self, msg, arg):
        if msg == 0:
            print("Starting up roadr " + __version__ + " ...")
        if msg == 1:
            print("No controllers detected!")