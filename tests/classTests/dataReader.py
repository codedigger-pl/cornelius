#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from socketserver import TCPServer, BaseRequestHandler
from time import sleep
from threading import Thread
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
        try:
            self.reader = dataReader.DataParser()
        except:
            self.reader = None

    def test_creation(self):
        self.assertNotEqual(self.reader, None, 'Class not initialized')

    def test_check_frame(self):
        data = [0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D]
        self.assertTrue(self.reader.checkFrame(data), 'Error while frame validation')
        data = [0xFE, 0xFE, 0x1C, 0xD7, 0xFE, 0xF0, 0xFE, 0x0D]
        self.assertTrue(self.reader.checkFrame(data), 'Error while frame validation')
        data = [0xFE, 0xFE, 0xe0, 0x12, 0x34, 0xff, 0xff, 0x8a, 0x9b, 0xfe, 0x0d]
        self.assertTrue(self.reader.checkFrame(data), 'Error while frame validation')

    def test_check_frame__frame_to_short(self):
        """Testing too short frame data"""
        data = [0XFE, 0xFE, 0xFE, 0x0D]
        self.assertFalse(self.reader.checkFrame(data), 'Checking frame (too short) passes true')

    def test_check_frame__no_data(self):
        """Testing check_frame with no data"""
        self.assertFalse(self.reader.checkFrame(None), 'Checking frame with no data passes true')

    def test_check_frame__bad_header(self):
        """Testing check_frame with bad header"""
        data = [0xFE, 0xFD, 0x09, 0xD7, 0xEB, 0xFE, 0x0D]
        self.assertFalse(self.reader.checkFrame(data), 'Checking frame with bad header passes true')

    def test_check_frame__bad_tail(self):
        """Testing check_frame with bad header"""
        data = [0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0E]
        self.assertFalse(self.reader.checkFrame(data), 'Checking frame with bad tail passes true')

    def test_check_frame__bad_hi_crc(self):
        """Testing check_frame with bad header"""
        data = [0xFE, 0xFE, 0x09, 0xD8, 0xEB, 0xFE, 0x0D]
        self.assertFalse(self.reader.checkFrame(data), 'Checking frame with bad high byte in crc passes true')

    def test_check_frame__bad_lo_crc(self):
        """Testing check_frame with bad header"""
        data = [0xFE, 0xFE, 0x09, 0xD7, 0xEC, 0xFE, 0x0D]
        self.assertFalse(self.reader.checkFrame(data), 'Checking frame with bad lo byte in crc passes true')

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

    def test_build_frame__with_one_byte(self):
        self.assertEqual(self.reader.buildFrame(0x09),
                         bytearray([0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D]),
                         'Invalid frame was build')


class EthernetDataReaderTest(unittest.TestCase):
    """Testing EthernetDataReader class"""
    def setUp(self):
        self.ip_address = '192.168.0.11'
        self.port = 7094
        self.reader = dataReader.EthernetDataReader(ipAddress=self.ip_address, port=self.port)

    def test_initializing(self):
        """Testing class initializing"""
        self.assertEqual(self.reader.ipAddress, self.ip_address, 'Bad ip address while class creation')
        self.assertEqual(self.reader.port, self.port, 'Bad port while class creation')

    def test_read__without_connection(self):
        """Testing read without connection"""
        self.assertEqual(self.reader.read(), None, 'While reading without connection get data other than None')

    def test_read__some_data(self):
        """Testing read some data from socket"""
        class ServerHandler(BaseRequestHandler):
            """Server request handler"""

            def handle(self):
                self.request.sendall(self.server.some_data)

        class ServerThread(Thread):
            """Server thread"""
            def __init__(self):
                super(ServerThread, self).__init__()
                self.server = TCPServer(('127.0.0.1', 7901), ServerHandler, False)
                self.server.allow_reuse_address = True
                self.server.server_bind()
                self.server.server_activate()

                self.server.some_data = bytearray([0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D])

            def run(self):
                # creating server socket
                self.server.serve_forever()

        server = ServerThread()
        server.start()

        reader = dataReader.EthernetDataReader(ipAddress='127.0.0.1', port=7901)
        reader.connect()
        read_data = reader.read()
        reader.close_connection()
        sleep(0.5)  # wait to finish closing connection
        server.server.shutdown()
        server.join()

        self.assertEqual(read_data, server.server.some_data, 'Read data not the same')

    def test_write__without_connection(self):
        """Testing write without connection - we shouldn't get any errors"""
        self.reader.write(bytearray())
        self.assertTrue(True, True)

    def test_write__some_data(self):
        """Testing write to some created port"""

        class ServerHandler(BaseRequestHandler):
            """Server request handler"""

            def handle(self):
                self.server.rec_data = self.request.recv(2048)

        class ServerThread(Thread):
            """Server thread"""
            def __init__(self):
                super(ServerThread, self).__init__()
                self.server = TCPServer(('127.0.0.1', 7900), ServerHandler, False)
                self.server.allow_reuse_address = True
                self.server.server_bind()
                self.server.server_activate()

                self.server.rec_data = None

            def run(self):
                # creating server socket
                self.server.serve_forever()

        server = ServerThread()
        server.start()

        some_data = bytearray([0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D])

        # creating class with valid configuration
        reader = dataReader.EthernetDataReader(ipAddress='127.0.0.1', port=7900)
        reader.connect()
        reader.write(some_data)
        reader.close_connection()
        sleep(0.5)  # wait to finish closing connection
        server.server.shutdown()
        server.join()

        self.assertEqual(some_data, server.server.rec_data, 'Written data not the same')

    def test_connect__without_valid_configuration(self):
        """Trying to connect without configuration"""
        reader = dataReader.EthernetDataReader()
        self.assertFalse(reader.connect(), 'Connecting without configuration passes true')

    def test_connect__to_missing_host(self):
        """Trying to connect to missing host. In your network can't be host with below ip address"""
        self.reader.ipAddress = '192.168.0.254'
        self.assertFalse(self.reader.connect(), 'Connection to missing host established')
