from sys import argv
from roadr.system import system

def main():
    DEBUG = False
    DEBUG_QUIET_TILE_SYS = True
    DEBUG_QUIET_CONTROLLER_INPUT = True
    OPENGL = True
    
    for arg in argv:
        if arg == "-d":
            DEBUG = True
        elif arg == "-dvts":
            DEBUG_QUIET_TILE_SYS = False
        elif arg == "-s":
            OPENGL = False
        elif arg == "-dvci":
            DEBUG_QUIET_CONTROLLER_INPUT = False

    sys = system(DEBUG, DEBUG_QUIET_TILE_SYS, OPENGL, DEBUG_QUIET_CONTROLLER_INPUT)
    sys.mainLoop()
    
if __name__ == "__main__":
    main()