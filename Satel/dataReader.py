#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import socket
from PyQt4 import QtCore
from time import sleep


class DataReader(QtCore.QObject):
    """ DataReader

    Interface for all classes for communication. Need implementation for read, write connect and disconnect methods.
    """

    def read(self):
        """Reading from device"""
        raise NotImplementedError('Method not implemented: read')

    def write(self, data):
        """Writing to device"""
        raise NotImplementedError('Method not implemented: write')

    def connect(self):
        """Connecting to device"""
        raise NotImplementedError('Method not implemented: connect')

    def close_connection(self):
        """Disconnecting from device"""
        raise NotImplementedError('Method not implemented: disconnect')


class RS232DataReader(DataReader):
    """ RS232DataReader

    Class for communication with Integra by RS port.
    TODO: finish it this class
    """

    def __init__(self, port):
        """Initializing class"""
        super(RS232DataReader, self).__init__()
        self.port = serial.Serial(port, 19200, timeout=2)

    def read(self):
        """Reading from port"""
        return self.port.read()

    def write(self, data):
        """Writing to port"""
        self.port.write(data)


class EthernetDataReader(DataReader):
    """ Ethernet Reader

    Read data from ethernet port
    """

    def __init__(self, ipAddress, port):
        """ Class initialization

        :param ipAdress: (str) - ip address
        :param port:  (str, int) - connection port
        :return: none
        """
        super(EthernetDataReader, self).__init__()
        self.socket = None

        self.ipAddress = ipAddress
        self.port = port

    def read(self):
        """ Reading data from port.
        Before read, socket should be available (use connect method).

        :return: read bytearray
        """
        if self.socket is not None:
            try:
                dane = self.socket.recv(2048)
                return dane
            except:
                return bytearray()
        return None

    def write(self, data):
        """ write
        Sending data to port

        :param data: data to send
        :return: none
        """
        if self.socket is not None:
            self.socket.send(data)

    def connect(self):
        """ connect
        Connecting to port (setting up socket). Set ipAddress and port before connect.

        :return: none
        """
        proto = socket.getprotobyname('tcp')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)
        try:
            self.socket.connect((self.ipAdress, self.port))
        except Exception as e:
            print('Problem with connecting to Integra system at', str(self.ipAdress) + ':' + str(self.port))
            print(e)

    def close_connection(self):
        """ close_connection
        Closing connection to ethernet port.

        :return: none
        """
        self.socket.close()


class DataParser(QtCore.QThread):
    """ DataParser

    Class for parsing data from alarm system.
    """

    def __init__(self):
        """Initializing class"""
        super(DataParser, self).__init__()

        self.CA = None
        self.port = None
        self.time = 60
        self.tasks = []

    def __rl(self, data):
        """Rotating bit left"""
        # moving bits left with cutting to two bytes
        result = ((data << 1) & 0b1111111111111111)
        # moving oldest bit to first bit
        result = result | ((data & 0b1000000000000000) >> 15)
        return result

    def __hi(self, data):
        """Returning high byte from data"""
        return (data & 0xff00) // 256

    def __lo(self, data):
        """Returning low byte from data"""
        return data[0] & 0xff

    def __calculateCRC(self, data):
        """ __calculateCRC
        Calculating CRC according to Satel docs.

        :param data: data to calculate
        :return: calculated crc
        """
        crc = 0x147A
        for d in data:
            crc = self.__rl(crc)                # rotating byte
            crc = crc ^ 0xffff                  # XOR
            crc = crc + self.__hi(crc) + d      # according to doc
            crc = crc & 0b1111111111111111      # cutting to 2 bytes

        # converting to bytearray
        inStr = hex(crc)[2:]
        if (len(inStr) % 2) == 1:
            inStr = '0' + inStr
        return bytearray.fromhex(inStr)

    # TODO: move to root or delete after tests
    def testHi(self, data):
        return self.__hi(data)

    # TODO: move to root or delete after tests
    def testRl(self, data):
        return self.__rl(data)

    # TODO: move to root or delete after tests
    def testCRC(self, data):
        return self.__calculateCRC(data)

    def setTime(self, time):
        """Setting time between reading data from CA"""
        self.time = time

    def assignCA(self, CA):
        """Assigning alarm system"""
        self.CA = CA

    def assignPort(self, port):
        """Assigning communication port"""
        self.port = port

    def checkFrame(self, data):
        """ checkFrame
        Validating frame according to Satel datasheet.

        :param data: (bytearray) validating frame
        :return: (bool)
        """
        # no data?
        if data is None:
            return False

        # checking minimal length
        if len(data) < 7:
            return False

        # checking header
        if (data[0] != 0xfe) & (data[1] != 0xfe):
            return False

        # checking tail
        if (data[-1] != 0x0d) & (data[-2] != 0xfe):
            return False

        # changing FE F0 to single FE value
        tmp = data[:]
        data = []
        for i in range(len(tmp)):
            if (tmp[i] == 0xf0) & (tmp[i - 1] == 0xfe):
                pass
            else:
                data.append(tmp[i])

        # calculating CRC value
        crc = self.__calculateCRC(data[2:-4])
        if(data[-3] != crc[1]):
            print("LO CRC Error:", hex(data[-3]), ", should be:", hex(self.__lo(crc)))
            return False
        if(data[-4] != crc[0]):
            print("HI CRC Error:", hex(data[-4]), ", should be:", hex(self.__hi(crc)))
            return False

        return True

    def buildFrame(self, data):
        """ buildFrame
        Building frame data according to Satel datasheet.

        :param data: data to build
        :return: (bytearray) frame ready to send
        """
        dane = bytearray()

        # frame header
        dane.append(0xFE)
        dane.append(0xFE)

        # adding data to frame
        if type(data) is list:
            dane.extend(data)
        else:
            dane.append(data)

        # adding CRC
        dane.extend(self.__calculateCRC(data))

        # adding tail
        dane.append(0xFE)
        dane.append(0x0D)

        return dane

    def parseData(self, data):
        """ parseData
        Parsing data and invoking correct functions.

        :param data: data from system
        :return:
        """
        # functions list with theirs codes
        functions = {0x00: self.CA.assignActiveByBits,
                     0x01: self.CA.assignTamperByBits,
                     0x02: self.CA.assignAlarmByBits,
                     0x03: self.CA.assignTamperByBits,
                     0x04: self.CA.assignAlarmMemoryByBits,
                     0x05: self.CA.assignTamperMemoryByBits,
                     0x09: self.CA.assignZoneArmedByBits,
                     0x0A: self.CA.assignZoneArmedByBits,
                     0x0D: self.CA.assignZoneCode1ByBits,
                     0x0E: self.CA.assignZoneEntryTimeByBits,
                     0x0F: self.CA.assignZoneExitTimeByBits,
                     0x10: self.CA.assignZoneExitTimeByBits,
                     0x13: self.CA.assignZoneAlarmByBits,
                     0x14: self.CA.assignZoneFireAlarmByBits,
                     0x15: self.CA.assignZoneAlarmMemoryByBits,
                     0x16: self.CA.assignZoneFireAlarmMemoryByBits,
                     0x17: self.CA.assignOutsByBits,
                     0x28: self.CA.assignTamperByBits,
                     0x29: self.CA.assignTamperMemoryByBits,
                     0x7F: self.parse7FResponse,
                     }

        correct_data = 0
        for d in data[1:]:
            correct_data = correct_data << 8
            correct_data += self.CA.changeByte(d)

        try:
            if data[0] == 0x7F:
                self.parse7FResponse(data[1:])
            else:
                function = functions[data[0]]
                function(correct_data)
        except Exception as e:
            print('Error while calling function', data[0])
            print(e)

    def parse7FResponse(self, data):
        """Parsing 7F response"""
        mask = 0b1000000000000000000000000000000000000000
        f_data = 0
        task = 0
        for i in data[1:-1]:
            f_data = (f_data << 8) + self.CA.changeByte(i)
        for i in range(39):
            if f_data & mask:
                self.tasks.append([task, ])
            mask = mask >> 1
            task += 1

    def startConnection(self):
        self.sleep(self.time)

    def run(self):
        """Thread loop function"""

        # adding requests for data
        while(True):
            self.tasks.append([0x00, ])
            self.tasks.append([0x17, ])
            self.tasks.append([0x01, ])
            self.tasks.append([0x02, ])
            self.tasks.append([0x03, ])
            self.tasks.append([0x04, ])
            self.tasks.append([0x05, ])
            self.tasks.append([0x09, ])
            self.tasks.append([0x0A, ])
            self.tasks.append([0x0D, ])
            self.tasks.append([0x0E, ])
            self.tasks.append([0x0F, ])
            self.tasks.append([0x10, ])
            self.tasks.append([0x13, ])
            self.tasks.append([0x14, ])
            self.tasks.append([0x15, ])
            self.tasks.append([0x16, ])
            self.tasks.append([0x28, ])
            self.tasks.append([0x29, ])

            # Opening port for connection
            try:
                self.port.connect()

                # Writing and receiving new data from CA
                for task in self.tasks:
                    self.port.write(self.buildFrame(task))
                    r_data = self.port.read()
                    if self.checkFrame(r_data):
                        self.parseData(r_data[2:-4])

                # Closing port
                self.port.close_connection()

            except Exception as e:
                print('Connection trouble')
                print(e)

            # Clearing tasks
            self.tasks = []

            sleep(0.5)
