from roadr.system import system

DEBUG = True
DEBUG_QUIET_TILE_SYS = True

def main():
    sys = system(DEBUG, DEBUG_QUIET_TILE_SYS)
    sys.mainLoop()
    
if __name__ == "__main__":
    main()