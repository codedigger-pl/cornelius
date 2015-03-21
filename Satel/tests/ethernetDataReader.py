#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from socketserver import TCPServer, BaseRequestHandler
from time import sleep
from threading import Thread

from Satel.dataReader import EthernetDataReader


class EthernetDataReaderTest(unittest.TestCase):
    """Testing EthernetDataReader class"""
    def setUp(self):
        self.ip_address = '192.168.0.11'
        self.port = 7094
        self.reader = EthernetDataReader(ipAddress=self.ip_address, port=self.port)

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

        reader = EthernetDataReader(ipAddress='127.0.0.1', port=7901)
        reader.connect()
        read_data = reader.read()
        reader.close_connection()
        sleep(0.5)  # wait to finish closing connection
        server.server.shutdown()
        server.join()

        self.assertEqual(read_data, server.server.some_data, 'Read data not the same')

    def test_read__lost_connection(self):
        """Testing read some data from socket"""
        class ServerHandler(BaseRequestHandler):
            """Server request handler"""

            def handle(self):
                sleep(3)

        class ServerThread(Thread):
            """Server thread"""
            def __init__(self):
                super(ServerThread, self).__init__()
                self.server = TCPServer(('127.0.0.1', 7901), ServerHandler, False)
                self.server.allow_reuse_address = True
                self.server.server_bind()
                self.server.server_activate()

            def run(self):
                # creating server socket
                self.server.serve_forever()

        server = ServerThread()
        server.start()

        reader = EthernetDataReader(ipAddress='127.0.0.1', port=7901)
        reader.connect()
        read_data = reader.read()
        server.server.shutdown()
        sleep(0.5)  # wait to finish closing connection
        reader.close_connection()
        server.join()

        self.assertEqual(read_data, bytearray(), 'Read data on lost connection not empty')

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
        reader = EthernetDataReader(ipAddress='127.0.0.1', port=7900)
        reader.connect()
        reader.write(some_data)
        reader.close_connection()
        sleep(0.5)  # wait to finish closing connection
        server.server.shutdown()
        server.join()

        self.assertEqual(some_data, server.server.rec_data, 'Written data not the same')

    def test_connect__without_valid_configuration(self):
        """Trying to connect without configuration"""
        reader = EthernetDataReader()
        self.assertFalse(reader.connect(), 'Connecting without configuration passes true')

    def test_connect__to_missing_host(self):
        """Trying to connect to missing host. In your network can't be host with below ip address"""
        self.reader.ipAddress = '192.168.0.254'
        self.assertFalse(self.reader.connect(), 'Connection to missing host established')
