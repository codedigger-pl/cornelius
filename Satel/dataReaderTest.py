'''
Created on 30 cze 2014

@author: codedigger
'''

import unittest
from Satel import dataReader


class Test(unittest.TestCase):

    def testHi(self):
        reader=dataReader.DataParser()
        for i in range(0xffff):
            self.assertEqual(i//256, reader.testHi(i), "Błąd wydzielenia wysokiego bajtu")

    def testRl(self):
        reader=dataReader.DataParser()
        test=0b1100001100011101
        self.assertEqual(0b1000011000111011, reader.testRl(test), "Błąd przesunięcia bitowego")
        test=0b0111000011011100
        self.assertEqual(0b1110000110111000, reader.testRl(test), "Błąd przesunięcia bitowego")
        test=0b0000000000000000
        self.assertEqual(0b0000000000000000, reader.testRl(test), "Błąd przesunięcia bitowego")
        test=0b1111111111111111
        self.assertEqual(0b1111111111111111, reader.testRl(test), "Błąd przesunięcia bitowego")

    def testCRC(self):
        reader=dataReader.DataParser()
        data=[]
        data.append(0xe0)
        d=bytearray()
        self.assertEqual(bytearray.fromhex(hex(0xd8c2)[2:]), reader.testCRC(data), "Błąd liczenia sumy CRC")
        data.append(0x12)
        self.assertEqual(bytearray.fromhex(hex(0x4eda)[2:]), reader.testCRC(data), "Błąd liczenia sumy CRC")
        data.append(0x34)
        self.assertEqual(bytearray.fromhex(hex(0x62e1)[2:]), reader.testCRC(data), "Błąd liczenia sumy CRC")
        data.append(0xff)
        self.assertEqual(bytearray.fromhex(hex(0x3b76)[2:]), reader.testCRC(data), "Błąd liczenia sumy CRC")
        data.append(0xff)
        self.assertEqual(bytearray.fromhex(hex(0x8a9b)[2:]), reader.testCRC(data), "Błąd liczenia sumy CRC")

    def testCheckFrame(self):
        reader=dataReader.DataParser()
        data=[0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D]
        self.assertTrue(reader.checkFrame(data), "Błąd sprawdzania ramki")
        data=[0xFE, 0xFE, 0x1C, 0xD7, 0xFE, 0xF0, 0xFE, 0x0D]
        self.assertTrue(reader.checkFrame(data), "Błąd sprawdzania ramki")
        data=[0xFE, 0xFE, 0xe0, 0x12, 0x34, 0xff, 0xff, 0x8a, 0x9b, 0xfe, 0x0d]
        self.assertTrue(reader.checkFrame(data), "Błąd sprawdzania ramki")


if __name__ == '__main__':
    unittest.main()