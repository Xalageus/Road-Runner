from roadr.system import system

DEBUG = True

def main():
    sys = system(DEBUG)
    sys.mainLoop()
    
if __name__ == "__main__":
    main()