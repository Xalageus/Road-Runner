from xml.etree import ElementTree
import os
from roadr.printer import printer

class asset_file():
    def __init__(self, name, id, filename):
        self.name = name
        self.id = id
        self.filename = filename

class asset_system():
    def __init__(self, debug_mode):
        self.printer = printer(debug_mode)
        self.maps = [0] * 1000
        self.objs = [0] * 1000
        self.tiles = [0] * 1000
        self.assetDir = os.path.dirname(os.path.realpath(__file__)) + "\\assets"
        self.map_path = None
        self.obj_path = None
        self.tile_path = None
        
        self.parseDef(self.assetDir + "\\assets.xml")
        
        self.maps = self.trim(self.maps)
        self.objs = self.trim(self.objs)
        self.tiles = self.trim(self.tiles)

    def parseDef(self, file):
        root = ElementTree.parse(file).getroot()
        self.map_path = root.find("maps/path").text
        self.obj_path = root.find("objs/path").text
        self.tile_path = root.find("tiles/path").text

        for tag in root.findall("maps/map"):
            self.maps[int(tag.find("id").text)] = asset_file(tag.find("name").text, tag.find("id").text, tag.find("file").text)

        self.printer.printDebugInfo(18, len(root.findall("maps/map")), None)

        for tag in root.findall("objs/obj"):
            self.objs[int(tag.find("id").text)] = asset_file(tag.find("name").text, tag.find("id").text, tag.find("file").text)

        self.printer.printDebugInfo(19, len(root.findall("objs/obj")), None)

        for tag in root.findall("tiles/tile"):
            self.tiles[int(tag.find("id").text)] = asset_file(tag.find("name").text, tag.find("id").text, tag.find("file").text)

        self.printer.printDebugInfo(20, len(root.findall("tiles/tile")), None)

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

    def mergePaths(self):
        for asset in self.maps:
            asset.filename = self.assetDir + "\\" + self.map_path + "\\" + asset.filename

        for asset in self.objs:
            asset.filename = self.assetDir + "\\" + self.obj_path + "\\" + asset.filename
        
        for asset in self.tiles:
            asset.filename = self.assetDir + "\\" + self.tile_path + "\\" + asset.filename