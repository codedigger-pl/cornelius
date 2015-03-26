#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from Satel.integra import Zone


class ZoneTest(unittest.TestCase):
    """Testing Satel.Zone class"""

    def setUp(self):
        super(ZoneTest, self).setUp()
        self.zone = Zone('Some name')

    def test_name__initial(self):
        """Testing initial value"""
        self.assertEqual('Some name', self.zone.name, 'Invalid initial value')

    def test_name__changing_value(self):
        """Testing changing out name"""
        new_name = 'Another name'
        self.zone.name = new_name
        self.assertEqual(self.zone.name, new_name, 'Failed to change zone name')

    def test_armed__changing(self):
        """Testing changing active state"""
        self.zone.armed = True
        self.assertEqual(self.zone.armed, True, 'Failed to change armed state')
        self.zone.armed = False
        self.assertEqual(self.zone.armed, False, 'Failed to change armed state')

    def test_armed__invalid_value(self):
        """Testing parsing invalid value to armed state"""
        try:
            self.zone.armed = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass

    def test_first_code__changing(self):
        """Testing changing first_code state"""
        self.zone.first_code = True
        self.assertEqual(self.zone.first_code, True, 'Failed to change first_code state')
        self.zone.first_code = False
        self.assertEqual(self.zone.first_code, False, 'Failed to change first_code state')

    def test_first_code__invalid_value(self):
        """Testing parsing invalid value to first_code state"""
        try:
            self.zone.first_code = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass

    def test_entry_time__changing(self):
        """Testing changing entry_time state"""
        self.zone.entry_time = True
        self.assertEqual(self.zone.entry_time, True, 'Failed to change entry_time state')
        self.zone.entry_time = False
        self.assertEqual(self.zone.entry_time, False, 'Failed to change entry_time state')

    def test_entry_time__invalid_value(self):
        """Testing parsing invalid value to entry_time state"""
        try:
            self.zone.entry_time = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass

    def test_exit_time__changing(self):
        """Testing changing exit_time state"""
        self.zone.exit_time = True
        self.assertEqual(self.zone.exit_time, True, 'Failed to change exit_time state')
        self.zone.exit_time = False
        self.assertEqual(self.zone.exit_time, False, 'Failed to change exit_time state')

    def test_exit_time__invalid_value(self):
        """Testing parsing invalid value to exit_time state"""
        try:
            self.zone.exit_time = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass

    def test_alarm__changing(self):
        """Testing changing alarm state"""
        self.zone.alarm = True
        self.assertEqual(self.zone.alarm, True, 'Failed to change alarm state')
        self.zone.alarm = False
        self.assertEqual(self.zone.alarm, False, 'Failed to change alarm state')

    def test_alarm__invalid_value(self):
        """Testing parsing invalid value to alarm state"""
        try:
            self.zone.alarm = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass

    def test_alarm_memory__changing(self):
        """Testing changing alarm_memory state"""
        self.zone.alarm_memory = True
        self.assertEqual(self.zone.alarm_memory, True, 'Failed to change alarm_memory state')
        self.zone.alarm_memory = False
        self.assertEqual(self.zone.alarm_memory, False, 'Failed to change alarm_memory state')

    def test_alarm_memory__invalid_value(self):
        """Testing parsing invalid value to alarm_memory state"""
        try:
            self.zone.alarm_memory = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass

    def test_fire_alarm__changing(self):
        """Testing changing fire_alarm state"""
        self.zone.fire_alarm = True
        self.assertEqual(self.zone.fire_alarm, True, 'Failed to change fire_alarm state')
        self.zone.fire_alarm = False
        self.assertEqual(self.zone.fire_alarm, False, 'Failed to change fire_alarm state')

    def test_fire_alarm__invalid_value(self):
        """Testing parsing invalid value to fire_alarm state"""
        try:
            self.zone.fire_alarm = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass

    def test_fire_alarm_memory__changing(self):
        """Testing changing fire_alarm_memory state"""
        self.zone.fire_alarm_memory = True
        self.assertEqual(self.zone.fire_alarm_memory, True, 'Failed to change fire_alarm_memory state')
        self.zone.fire_alarm_memory = False
        self.assertEqual(self.zone.fire_alarm_memory, False, 'Failed to change fire_alarm_memory state')

    def test_fire_alarm_memory__invalid_value(self):
        """Testing parsing invalid value to fire_alarm_memory state"""
        try:
            self.zone.fire_alarm_memory = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass
