#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import serial
from time import sleep
from PyQt4 import QtCore
from warnings import warn


def rotate_left(data):
    """ Rotating bits to the left with carriage.

    :param data: 2 bytes
    :return: rotated data
    """
    if data > 0xFFFF:
        raise TypeError('Data can not be larger than 2 bytes (16 bits)')
    # moving bits left with cutting to two bytes
    result = ((data << 1) & 0b1111111111111111)
    # moving oldest bit to first bit
    result = result | ((data & 0b1000000000000000) >> 15)
    return result


def high_byte(data):
    """ Returning highest byte.

    :param data: 2 bytes
    :return: highest byte from data
    """
    if data > 0xFFFF:
        raise TypeError('Data can not be larger than 2 bytes (16 bits)')

    return (data & 0xff00) // 256


def low_byte(data):
    """ Returning lowest byte.

    :param data: 2 bytes
    :return: lowest byte from data
    """
    if data > 0xFFFF:
        raise TypeError('Data can not be larger than 2 bytes (16 bits)')

    return data & 0xff


def calculate_crc(data):
    """ __calculateCRC
    Calculating CRC according to Satel docs.

    :param data: data to calculate
    :return: calculated crc
    """
    crc = 0x147A
    for d in data:
        crc = rotate_left(crc)                  # rotating byte
        crc = crc ^ 0xffff                      # XOR
        crc = crc + high_byte(crc) + d          # according to doc
        crc = crc & 0b1111111111111111          # cutting to 2 bytes

    # converting to bytearray
    inStr = hex(crc)[2:]
    if (len(inStr) % 2) == 1:
        inStr = '0' + inStr
    return bytearray.fromhex(inStr)


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

    def __init__(self, ipAddress=None, port=7094):
        """ Class initialization

        :param ipAdress: (str) - ip address
        :param port:  (str, int) - connection port
        :return: none
        """
        super(EthernetDataReader, self).__init__()
        self.socket = None

        self.ipAddress = ipAddress
        self.port = int(port)

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

        :return: (bool) connection was established
        """
        # checking valid configuration
        if self.ipAddress is None or self.port is None:
            return False

        # trying establish connection
        proto = socket.getprotobyname('tcp')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)
        self.socket.settimeout(2)
        try:
            self.socket.connect((self.ipAddress, self.port))
            return True
        except Exception as e:
            print('Problem with connecting to Integra system at', str(self.ipAddress) + ':' + str(self.port))
            print(e)
            return False

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
        warn('This method is deprecated. Use rotate_left instead.', DeprecationWarning)
        return rotate_left(data)

    def __hi(self, data):
        warn('This method is deprecated. Use high_byte instead.', DeprecationWarning)
        return high_byte(data)

    def __lo(self, data):
        warn('This method is deprecated. Use low_byte instead.', DeprecationWarning)
        return low_byte(data)

    def __calculateCRC(self, data):
        warn('This method is deprecated. Use calculate_crc instead.', DeprecationWarning)
        return calculate_crc(data)

    def setTime(self, time):
        """Setting time between reading data from CA"""
        warn('This method is deprecated. Use time directly.', DeprecationWarning)
        self.time = time

    def assignCA(self, CA):
        """Assigning alarm system"""
        warn('This method is deprecated. Use CA directly.', DeprecationWarning)
        self.CA = CA

    def assignPort(self, port):
        """Assigning communication port"""
        warn('This method is deprecated. Use port directly.', DeprecationWarning)
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
        if (data[0] != 0xfe) | (data[1] != 0xfe):
            return False

        # checking tail
        if (data[-1] != 0x0d) | (data[-2] != 0xfe):
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
        crc = calculate_crc(data[2:-4])
        if(data[-3] != crc[1]):
            return False
        if(data[-4] != crc[0]):
            return False

        return True

    def buildFrame(self, data):
        """ buildFrame
        Building frame data according to Satel datasheet.

        :param data: data to build
        :return: (bytearray) frame ready to send
        """
        w_data = bytearray()

        # frame header
        w_data.append(0xFE)
        w_data.append(0xFE)

        # adding data to frame
        if not isinstance(data, (list, tuple)):
            r_data = [data, ]
        else:
            r_data = data

        w_data.extend(r_data)
        # adding CRC
        w_data.extend(calculate_crc(r_data))

        # adding tail
        w_data.append(0xFE)
        w_data.append(0x0D)

        return w_data

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
        """This method will be removed after tests"""
        warn('Do not use this method', Warning)
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
