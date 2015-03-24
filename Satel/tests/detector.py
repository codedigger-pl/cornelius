#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from Satel.integra import Detector


class DetectorTest(unittest.TestCase):
    """Testing detector from Satel.integra module"""

    def setUp(self):
        super(DetectorTest, self).setUp()
        self.detector = Detector(name='Some name')

    def test_detector_name__from_initial(self):
        """Testing initial value"""
        self.assertEqual(self.detector.name, 'Some name', 'Incorrect initial value')

    def test_detector_name__changing(self):
        """Testing changing detector name"""
        new_name = 'Another name'
        self.detector.name = new_name
        self.assertEqual(self.detector.name, new_name, 'Failed to changed detector name')

    def test_detector_active__changing(self):
        """Testing changing detector active state"""
        self.detector.active = True
        self.assertEqual(self.detector.active, True, 'Failed to change active state')
        self.detector.active = False
        self.assertEqual(self.detector.active, False, 'Failed to change active state')

    def test_detector_active__invalid_value(self):
        """Testing invalid value parsed to active state"""
        try:
            self.detector.active = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass

    def test_detector_alarm__changing(self):
        """Testing changing detector alarm state"""
        self.detector.alarm = True
        self.assertEqual(self.detector.alarm, True, 'Failed to change alarm state')
        self.detector.alarm = False
        self.assertEqual(self.detector.alarm, False, 'Failed to change alarm state')

    def test_detector_alarm__invalid_value(self):
        """Testing invalid value parsed to alarm state"""
        try:
            self.detector.alarm = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass

    def test_detector_alarm_memory__changing(self):
        """Testing changing detector alarm_memory state"""
        self.detector.alarm_memory = True
        self.assertEqual(self.detector.alarm_memory, True, 'Failed to change alarm_memory state')
        self.detector.alarm_memory = False
        self.assertEqual(self.detector.alarm_memory, False, 'Failed to change alarm_memory state')

    def test_detector_alarm_memory__invalid_value(self):
        """Testing invalid value parsed to alarm_memory state"""
        try:
            self.detector.alarm_memory = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass

    def test_detector_tamper__changing(self):
        """Testing changing detector tamper state"""
        self.detector.tamper = True
        self.assertEqual(self.detector.tamper, True, 'Failed to change tamper state')
        self.detector.tamper = False
        self.assertEqual(self.detector.tamper, False, 'Failed to change tamper state')

    def test_detector_tamper__invalid_value(self):
        """Testing invalid value parsed to tamper state"""
        try:
            self.detector.tamper = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass

    def test_detector_tamper_memory__changing(self):
        """Testing changing detector tamper_memory state"""
        self.detector.tamper_memory = True
        self.assertEqual(self.detector.tamper_memory, True, 'Failed to change tamper_memory state')
        self.detector.tamper_memory = False
        self.assertEqual(self.detector.tamper_memory, False, 'Failed to change tamper_memory state')

    def test_detector_tamper_memory__invalid_value(self):
        """Testing invalid value parsed to active state"""
        try:
            self.detector.tamper_memory = 'Invalid'
            self.fail('No exception was thrown')
        except TypeError:
            pass
