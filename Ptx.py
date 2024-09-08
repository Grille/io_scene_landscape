import bpy
import struct
import io

from enum import Enum
from abc import ABC, abstractmethod
from io import BufferedReader, BufferedWriter

class PtxHead:

    def __init__(self):
        self.compression : int
        self.bitsPerPixel : int
        self.width : int
        self.height : int
        self.mipMapLevels : int


    def deserialize(self, reader : BufferedReader):
        read = struct.unpack('2B', reader.read(2))
        self.compression = read[0]
        self.bitsPerPixel = read[1]

        reader.read(2)

        read = struct.unpack('2I', reader.read(8))
        self.width = read[0]
        self.height = read[1]

        reader.read(4)


class PtxLevel:

    def __init__(self):
        self.data : bytes
    

    def deserialize(self, reader : BufferedReader):
        read = struct.unpack('2I', reader.read(8))
        size = read[0]
        synsize = read[1]

        if (synsize > 0):
            msg = "Files compressed by Synetic’s algorithm can't be decoded."
            raise Exception(msg)
        
        self.data = reader.read(size)
        

class PtxFile:
    def __init__(self):
        self.head : PtxHead = PtxHead()
        self.levels : list[PtxLevel] = []
        
    def deserialize(self, reader : BufferedReader):
        self.head.deserialize(reader)

        for i in range(1, self.head.mipMapLevels):
            level = PtxLevel()
            level.deserialize(reader)
            self.levels.append(level)