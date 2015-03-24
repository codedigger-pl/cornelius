#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from Satel import dataReader


class DataReaderTest(unittest.TestCase):
    """Testing interface"""
    def setUp(self):
        self.reader = dataReader.DataReader()

    def test_read(self):
        self.assertRaises(NotImplementedError, self.reader.read)

    def test_write(self):
        self.assertRaises(NotImplementedError, self.reader.write, bytearray())

    def test_connect(self):
        self.assertRaises(NotImplementedError, self.reader.connect)

    def test_close_connection(self):
        self.assertRaises(NotImplementedError, self.reader.close_connection)


class FunctionsTest(unittest.TestCase):

    def test_crc(self):
        data = []
        data.append(0xe0)
        self.assertEqual(bytearray.fromhex(hex(0xd8c2)[2:]), dataReader.calculate_crc(data), 'Error in CRC counting')

        data.append(0x12)
        self.assertEqual(bytearray.fromhex(hex(0x4eda)[2:]), dataReader.calculate_crc(data), 'Error in CRC counting')

        data.append(0x34)
        self.assertEqual(bytearray.fromhex(hex(0x62e1)[2:]), dataReader.calculate_crc(data), 'Error in CRC counting')

        data.append(0xff)
        self.assertEqual(bytearray.fromhex(hex(0x3b76)[2:]), dataReader.calculate_crc(data), 'Error in CRC counting')

        data.append(0xff)
        self.assertEqual(bytearray.fromhex(hex(0x8a9b)[2:]), dataReader.calculate_crc(data), 'Error in CRC counting')
