#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from Satel.dataReader import DataParser


class DataParserTest(unittest.TestCase):

    def setUp(self):
        try:
            self.parser = DataParser()
        except:
            self.parser = None

    def test_creation(self):
        self.assertNotEqual(self.parser, None, 'Class not initialized')

    def test_check_frame(self):
        data = [0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D]
        self.assertTrue(self.parser.checkFrame(data), 'Error while frame validation')
        data = [0xFE, 0xFE, 0x1C, 0xD7, 0xFE, 0xF0, 0xFE, 0x0D]
        self.assertTrue(self.parser.checkFrame(data), 'Error while frame validation')
        data = [0xFE, 0xFE, 0xe0, 0x12, 0x34, 0xff, 0xff, 0x8a, 0x9b, 0xfe, 0x0d]
        self.assertTrue(self.parser.checkFrame(data), 'Error while frame validation')

    def test_check_frame__frame_to_short(self):
        """Testing too short frame data"""
        data = [0XFE, 0xFE, 0xFE, 0x0D]
        self.assertFalse(self.parser.checkFrame(data), 'Checking frame (too short) passes true')

    def test_check_frame__no_data(self):
        """Testing check_frame with no data"""
        self.assertFalse(self.parser.checkFrame(None), 'Checking frame with no data passes true')

    def test_check_frame__bad_header(self):
        """Testing check_frame with bad header"""
        data = [0xFE, 0xFD, 0x09, 0xD7, 0xEB, 0xFE, 0x0D]
        self.assertFalse(self.parser.checkFrame(data), 'Checking frame with bad header passes true')

    def test_check_frame__bad_tail(self):
        """Testing check_frame with bad header"""
        data = [0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0E]
        self.assertFalse(self.parser.checkFrame(data), 'Checking frame with bad tail passes true')

    def test_check_frame__bad_hi_crc(self):
        """Testing check_frame with bad header"""
        data = [0xFE, 0xFE, 0x09, 0xD8, 0xEB, 0xFE, 0x0D]
        self.assertFalse(self.parser.checkFrame(data), 'Checking frame with bad high byte in crc passes true')

    def test_check_frame__bad_lo_crc(self):
        """Testing check_frame with bad header"""
        data = [0xFE, 0xFE, 0x09, 0xD7, 0xEC, 0xFE, 0x0D]
        self.assertFalse(self.parser.checkFrame(data), 'Checking frame with bad lo byte in crc passes true')

    def test_build_frame(self):
        """Testing correct frame building"""
        self.assertEqual(self.parser.buildFrame([0x09]),
                         bytearray([0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D]),
                         'Invalid frame was build')
        # self.assertEqual(self.reader.buildFrame([0x1C]),
        #                  bytearray([0xFE, 0xFE, 0x1C, 0xD7, 0xFE, 0xF0, 0xFE, 0x0D]),
        #                  'Invalid frame was build')
        self.assertEqual(self.parser.buildFrame([0xe0, 0x12, 0x34, 0xff, 0xff]),
                         bytearray([0xFE, 0xFE, 0xe0, 0x12, 0x34, 0xff, 0xff, 0x8a, 0x9b, 0xfe, 0x0d]),
                         'Invalid frame was build')

    def test_build_frame__with_one_byte(self):
        self.assertEqual(self.parser.buildFrame(0x09),
                         bytearray([0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D]),
                         'Invalid frame was build')

    def test_add_function(self):
        """Testing correct add function to list"""
        func = lambda x: x + x
        self.parser.add_function(function_code=0x00, function_body=func)
        self.assertEqual(func, self.parser._functions[0x00])

    def test_add_function__code_to_large(self):
        """Testing for exception"""
        func = lambda x: x + x
        try:
            self.parser.add_function(function_code=0xFFF, function_body=func)
            self.fail('No exception was thrown')
        except Exception as e:
            self.assertEqual(type(e), TypeError, 'Invalid exception thrown')

    def test_parseData(self):
        """Testing parsing data"""
        # First byte in param is function code. Rest are params to correct function.
        def func(some_value):
            if some_value == 0b00011001:
                return True
            else:
                return False

        self.parser.add_function(function_code=0x00, function_body=func)
        self.assertEqual(self.parser.parseData(bytearray([0x00, 0b10011000])),
                         True,
                         'Data passed to function incorrect')

    def test_parseData__with_invalid_func_code(self):
        """Testing call invalid (unregistered) function code. This should print only message"""
        self.parser.parseData(bytearray([0x12, ]))

    def test_parseData__catching_7F(self):
        self.parser.add_function(function_code=0x7F, function_body=self.parser.parse7FResponse)
        self.parser.parseData(bytearray([0x7F, 0xFF, 0b00000001, 0, 0, 0, 0, 0xFF]))
        self.assertTrue([0x00, ] in self.parser.tasks, 'Error while catching 7F response in parseData function')

    def test_parser7FResponse(self):
        """testing request for 0x00, 0x01, 0x06, 0x07, 0x0D. 0x19, 0x1D functions"""
        # we have 39 base functions -> 39 bits: 0b00000000 00000000 00000000 00000000 0000000
        # testing functions will be on bits: 0b11000011 00100000 10000000 00100010 0000000
        # in bytearray: [0b11000011,  0b00100000,  0b10000000, 0b00100010, 0b0000000]
        # according to Satel documentation, in response we have two additional bytes - we don't need them right now
        test_works = bytearray([0xFF, 0b11000011, 0b00100000, 0b10000000, 0b00100010, 0b00000000, 0xFF])
        self.parser.parse7FResponse(test_works)
        self.assertTrue([0x00, ] in self.parser.tasks, 'Task 0x00 not in tasks list')
        self.assertTrue([0x01, ] in self.parser.tasks, 'Task 0x01 not in tasks list')
        self.assertTrue([0x06, ] in self.parser.tasks, 'Task 0x06 not in tasks list')
        self.assertTrue([0x07, ] in self.parser.tasks, 'Task 0x07 not in tasks list')
        self.assertTrue([0x0D, ] in self.parser.tasks, 'Task 0x0D not in tasks list')
        self.assertTrue([0x19, ] in self.parser.tasks, 'Task 0x19 not in tasks list')
        self.assertTrue([0x1D, ] in self.parser.tasks, 'Task 0x1D not in tasks list')
