#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flake8 import main
import unittest


class Flake8Test(unittest.TestCase):
    """All PEP8 and similar tests"""

    def setUp(self):
        """ Setting up tests

        :return: none
        """
        super(Flake8Test, self).setUp()

    def test_myself(self):
        """Testing this file"""
        self.assertEqual(main.check_file('other/PEP8.py', ignore=('E501', )), 0, 'Errors or warnings in PEP8 test file')

    def test_main_py(self):
        """Testing main.py file"""
        self.assertEqual(main.check_file('../main.py', ignore=('E501', )), 0, '(FLAKE8) Errors or warnings while testing main.py')

    def tearDown(self):
        """ Tearing down

        :return: none
        """
        super(Flake8Test, self).tearDown()
