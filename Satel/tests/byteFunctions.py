#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from Satel.byteFunctions import high_byte, low_byte, rotate_left


class FunctionsTest(unittest.TestCase):

    def test_hi_normal(self):
        """Checking counting highest byte"""
        for i in range(0xFFFF):
            self.assertEqual(i // 256, high_byte(i), 'Error while counting hi byte')

    def test_hi_exception(self):
        """Checking, if with to large data exception is throw"""
        try:
            high_byte(0xFFFFF)
            self.fail('Not an exception was thrown')
        except TypeError as e:
            self.assertEqual(type(e), TypeError, 'Invalid exception type')

    def test_lo_normal(self):
        """Checking counting lowest byte"""
        for i in range(0xFFFF):
            self.assertEqual(i & 0x00FF, low_byte(i), 'Error while counting lo byte')

    def test_lo_exception(self):
        """Checking exception"""
        try:
            low_byte(0xFFFFF)
            self.fail('Not an exception was thrown')
        except TypeError as e:
            self.assertEqual(type(e), TypeError, 'Invalid exception type')

    def test_rl_normal(self):
        """Checking rotating bits in byte"""
        test = 0b1100001100011101
        self.assertEqual(0b1000011000111011, rotate_left(test), 'Error while rotating bits')

        test = 0b0111000011011100
        self.assertEqual(0b1110000110111000, rotate_left(test), 'Error while rotating bits')

        test = 0b0000000000000000
        self.assertEqual(0b0000000000000000, rotate_left(test), 'Error while rotating bits')

        test = 0b1111111111111111
        self.assertEqual(0b1111111111111111, rotate_left(test), 'Error while rotating bits')

    def test_rl_exception(self):
        """Checking exception"""
        try:
            rotate_left(0xFFFFF)
            self.fail('Not an exception was thrown')
        except Exception as e:
            self.assertEqual(type(e), TypeError, 'Invalid exception type')
