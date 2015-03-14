#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from Satel import dataReader


class FunctionsTest(unittest.TestCase):

    def test_hi_normal(self):
        """Checking counting highest byte"""
        for i in range(0xFFFF):
            self.assertEqual(i // 256, dataReader.high_byte(i), 'Error while counting hi byte')

    def test_hi_exception(self):
        """Checking, if with to large data exception is throw"""
        try:
            dataReader.high_byte(0xFFFFF)
            self.fail('Not an exception was thrown')
        except TypeError as e:
            self.assertEqual(type(e), TypeError, 'Invalid exception type')

    def test_lo_normal(self):
        """Checking counting lowest byte"""
        for i in range(0xFFFF):
            self.assertEqual(i & 0x00FF, dataReader.low_byte(i), 'Error while counting lo byte')

    def test_lo_exception(self):
        """Checking exception"""
        try:
            dataReader.low_byte(0xFFFFF)
            self.fail('Not an exception was thrown')
        except TypeError as e:
            self.assertEqual(type(e), TypeError, 'Invalid exception type')

    def test_rl_normal(self):
        """Checking rotating bits in byte"""
        test = 0b1100001100011101
        self.assertEqual(0b1000011000111011, dataReader.rotate_left(test), 'Error while rotating bits')

        test = 0b0111000011011100
        self.assertEqual(0b1110000110111000, dataReader.rotate_left(test), 'Error while rotating bits')

        test = 0b0000000000000000
        self.assertEqual(0b0000000000000000, dataReader.rotate_left(test), 'Error while rotating bits')

        test = 0b1111111111111111
        self.assertEqual(0b1111111111111111, dataReader.rotate_left(test), 'Error while rotating bits')

    def test_rl_exception(self):
        """Checking exception"""
        try:
            dataReader.rotate_left(0xFFFFF)
            self.fail('Not an exception was thrown')
        except TypeError as e:
            self.assertEqual(type(e), TypeError, 'Invalid exception type')

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


class DataParserTest(unittest.TestCase):

    def setUp(self):
        self.reader = dataReader.DataParser()

    def test_check_frame(self):
        data = [0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D]
        self.assertTrue(self.reader.checkFrame(data), 'Error while frame validation')
        data = [0xFE, 0xFE, 0x1C, 0xD7, 0xFE, 0xF0, 0xFE, 0x0D]
        self.assertTrue(self.reader.checkFrame(data), 'Error while frame validation')
        data = [0xFE, 0xFE, 0xe0, 0x12, 0x34, 0xff, 0xff, 0x8a, 0x9b, 0xfe, 0x0d]
        self.assertTrue(self.reader.checkFrame(data), 'Error while frame validation')

    def test_build_frame(self):
        """Testing correct frame building"""
        self.assertEqual(self.reader.buildFrame([0x09]),
                         bytearray([0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D]),
                         'Invalid frame was build')
        # self.assertEqual(self.reader.buildFrame([0x1C]),
        #                  bytearray([0xFE, 0xFE, 0x1C, 0xD7, 0xFE, 0xF0, 0xFE, 0x0D]),
        #                  'Invalid frame was build')
        self.assertEqual(self.reader.buildFrame([0xe0, 0x12, 0x34, 0xff, 0xff]),
                         bytearray([0xFE, 0xFE, 0xe0, 0x12, 0x34, 0xff, 0xff, 0x8a, 0x9b, 0xfe, 0x0d]),
                         'Invalid frame was build')
