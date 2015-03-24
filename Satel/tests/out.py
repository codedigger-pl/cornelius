#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from Satel.integra import Out

class OutTest(unittest.TestCase):
    """Testing Satel Out class"""

    def setUp(self):
        super(OutTest, self).setUp()
        self.out = Out('Some name')

    def test_name__initial(self):
        """Testing initial value"""
        self.assertEqual('Some name', self.out.name, 'Invalid initial value')

    def test_name__changing_value(self):
        """Testing changing out name"""
        new_name = 'Another name'
        self.out.name = new_name
        self.assertEqual(self.out.name, new_name, 'Failed to change out name')

    def test_active__changing(self):
        """Testing changing active state"""
        self.out.active = True
        self.assertEqual(self.out.active, True, 'Failed to change active state')
        self.out.active = False
        self.assertEqual(self.out.active, False, 'Failed to change active state')

    def test_active__invalid_value(self):
        """Testing parsing invalid value to active state"""
        try:
            self.out.active = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass
