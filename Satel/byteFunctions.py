#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def change_byte(byte):
    """Changing bytes to human readable.
    View input numbers from CA: 8,7,6,5,4,3,2,1 16,15,14,13,12,11,10,9
    View input numbers from system: 1,2,3,4,5,6,7,8 9,10,11,12,13,14,15,16
    Data from CA: 0101 1001
    Data, which we can use: 1010 1001

    input: byte - int with single byte from CA
    output: useful data"""

    result = 0b00000000
    for i in range(8):
        # some magic here
        if byte & (0b10000000 >> i):
            result = result | (0b1 << i)
    return result


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
