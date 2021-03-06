import csv
from roadr.printer import printer
    
class mapRead():
    def __init__(self, debug_mode):
        self.printer = printer(debug_mode)
        self.map = [0] * 1024

    def trim(self, arr):
        count = 0

        for item in arr:
            if item != 0:
                count += 1

        newArr = [0] * count
        i = 0

        while i < count:
            newArr[i] = arr[i]
            i += 1

        return newArr

    def readMap(self, mapFile):
        with open(mapFile.filename, newline='\n') as csvfile:
            rawMap = csv.reader(csvfile, delimiter=',')

            i = 0
            for row in rawMap:
                self.map[i] = row
                i += 1

            self.printer.printDebugInfo(21, mapFile.name, None)

            return self.trim(self.map)