from sys import argv
from roadr.system import system

def main():
    DEBUG = False
    DEBUG_QUIET_TILE_SYS = True
    OPENGL = True
    
    for arg in argv:
        if arg == "-d":
            DEBUG = True
        elif arg == "-dvts":
            DEBUG_QUIET_TILE_SYS = False
        elif arg == "-s":
            OPENGL = False

    sys = system(DEBUG, DEBUG_QUIET_TILE_SYS, OPENGL)
    sys.mainLoop()
    
if __name__ == "__main__":
    main()