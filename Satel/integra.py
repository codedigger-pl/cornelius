#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from warnings import warn


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


class Detector(QtCore.QObject):
    """Detectors in system. This is should be base class for all detectors in
    any systems. Currently here is only Integra system, so this is not used in
    this way."""

    # Qt signals
    hasChanged = QtCore.pyqtSignal()

    def __init__(self, name=""):
        """ Initializing class

        :param name: string with detector's name
        :return: none
        """
        super(Detector, self).__init__()

        self.name = name
        self.active = False
        self.alarm = False
        self.alarmMemory = False
        self.tamper = False
        self.tamperMemory = False

    def setName(self, name):
        """
        :param name: (str) new detector name
        :return: none
        """
        self.name = name
        self.hasChanged.emit()

    def setAlarm(self):
        """ Setting detector to alarm state

        :return: none
        """
        self.alarm = True
        self.hasChanged.emit()

    def setAlarmMemory(self):
        """ Setting detector to alarm memory state
        :return: none
        """
        self.alarmMemory = True
        self.hasChanged.emit()

    def setActive(self):
        """ Setting detector to active state.

        :return: none
        """
        self.active = True
        self.hasChanged.emit()

    def setTamper(self):
        """ Setting detector to tamper (sabotage) state

        :return: none
        """
        self.tamper = True
        self.hasChanged.emit()

    def setTamperMemory(self):
        """ Setting detector to tamper memory state.

        :return: none
        """
        self.tamperMemory = True
        self.hasChanged.emit()

    def clearAlarm(self):
        """ Clearing alarm state from detector.

        :return: none
        """
        self.alarm = False
        self.hasChanged.emit()

    def clearAlarmMemory(self):
        """ Clearing alarm memory state from detector.

        :return: none
        """
        self.alarmMemory = False
        self.hasChanged.emit()

    def clearActive(self):
        """ Clearing active state from detector.

        :return: none
        """
        self.active = False
        self.hasChanged.emit()

    def clearTamper(self):
        """ Clearing tamper state from detector.

        :return: none
        """
        self.tamper = False
        self.hasChanged.emit()

    def clearTamperMemory(self):
        """ Clearing tamper memory state from detector.

        :return: none
        """
        self.tamperMemory = False
        self.hasChanged.emit()

    """Functions for get data from class attributes"""
    # According to new functions in Python3, setting, clearing and getting methods will be changed
    def getActive(self):
        return self.active

    def getName(self):
        return self.name

    def getAlarm(self):
        return self.alarm

    def getAlarmMemory(self):
        return self.alarmMemory

    def getTamper(self):
        return self.tamper

    def getTamperMemory(self):
        return self.tamperMemory


class Out(QtCore.QObject):
    """Base class for any out in system. This is should be base class for all
    out in any system. Currently here is only Integra, so this is not used in
    this way."""

    # Qt signals
    hasChanged = QtCore.pyqtSignal()

    def __init__(self, name=""):
        """ Initializing class.

        :param name: out name
        :return: none
        """
        super(Out, self).__init__()

        self.name = name
        self.active = False

    def setName(self, name):
        """ Changes out name.

        :param name: new name
        :return:
        """
        self.name = name
        self.hasChanged.emit()

    def setActive(self):
        """ Setting out to active state.

        :return:
        """
        self.active = True
        self.hasChanged.emit()

    def clearActive(self):
        """ Clearing active state.

        :return:
        """
        self.active = False
        self.hasChanged.emit()

    """Function returns class attributes"""
    def getActive(self):
        return self.active

    def getName(self):
        return self.name


class Zone(QtCore.QObject):
    """Base class for any alarm zone in system. This is should be base class for all
    zones in any system. Currently here is only Integra, so this is not used in
    this way."""

    # Qt signals
    hasChanged = QtCore.pyqtSignal()

    def __init__(self, name):
        """ Class initialization.

        :param name: zone name
        :return:
        """
        super(Zone, self).__init__()

        self.name = name
        self.armed = False
        self.code1 = False
        self.entryTime = False
        self.exitTime = False
        self.alarm = False
        self.alarmMemory = False
        self.fireAlarm = False
        self.fireAlarmMemory = False

    def setName(self, name):
        """ Setting new name to zone.

        :param name: new name
        :return:
        """
        self.name = name
        self.hasChanged.emit()

    def setArmed(self):
        """ Setting zone to armed state.

        :return: none
        """
        self.armed = True
        self.hasChanged.emit()

    def setCode1(self):
        """ Setting zone to state after first password.

        :return: none
        """
        self.code1 = True
        self.hasChanged.emit()

    def setEntryTime(self):
        """ Setting zone to entry time state.

        :return: none
        """
        self.entryTime = True
        self.hasChanged.emit()

    def setExitTime(self):
        """ Setting zone to exit time state.

        :return: none
        """
        self.exitTime = True
        self.hasChanged.emit()

    def setAlarm(self):
        """ Setting zone to alarm state
        :return: none
        """
        self.alarm = True
        self.hasChanged.emit()

    def setAlarmMemory(self):
        """ Setting zone to alarm memory state.

        :return: none
        """
        self.alarmMemory = True
        self.hasChanged.emit()

    def setFireAlarm(self):
        """ Setting zone to fire alarm state.

        :return: none
        """
        self.fireAlarm = True
        self.hasChanged.emit()

    def setFireAlarmMemory(self):
        """ Setting zone to fire memory state.

        :return: none
        """
        self.fireAlarmMemory = True
        self.hasChanged.emit()

    def clearArmed(self):
        """ Clearing armed state.

        :return: none
        """
        self.armed = False
        self.hasChanged.emit()

    def clearCode1(self):
        """ Clearing after first password state.

        :return: none
        """
        self.code1 = False
        self.hasChanged.emit()

    def clearEntryTime(self):
        """ Clearing entry time state.

        :return: none
        """
        self.entryTime = False
        self.hasChanged.emit()

    def clearExitTime(self):
        """ Clearing exit time state.

        :return: none
        """
        self.exitTime = False
        self.hasChanged.emit()

    def clearAlarm(self):
        """ Clearing alarm state.

        :return: none
        """
        self.alarm = False
        self.hasChanged.emit()

    def clearAlarmMemory(self):
        """ Clearing alarm memory state.

        :return: none
        """
        self.alarmMemory = False
        self.hasChanged.emit()

    def clearFireAlarm(self):
        """ Clearing fire alarm state.

        :return: none
        """
        self.fireAlarm = False
        self.hasChanged.emit()

    def clearFireAlarmMemory(self):
        """ Clearing fire alarm memory state.

        :return: none
        """
        self.alarmMemory = False
        self.hasChanged.emit()

    """Function return class attributes"""
    def getName(self):
        return self.name

    def getArmed(self):
        return self.armed

    def getCode1(self):
        return self.code1

    def getEntryTime(self):
        return self.entryTime

    def getExitTime(self):
        return self.exitTime

    def getAlarm(self):
        return self.alarm

    def getAlarmMemory(self):
        return self.alarmMemory

    def getFireAlarm(self):
        return self.fireAlarm

    def getFireAlarmMemory(self):
        return self.fireAlarmMemory

# TODO: delete after tests
# Thread change randomly some attributes in system
from time import sleep
import random


class Thread(QtCore.QThread):

    def __init__(self, integra):
        super(Thread, self).__init__()
        self.integra = integra

    def run(self):
        while True:
            self.integra.assignAlarmByBits(random.randint(0, 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111))
            self.integra.assignActiveByBits(random.randint(0, 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111))
            self.integra.assignAlarmMemoryByBits(random.randint(0, 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111))
            self.integra.assignTamperByBits(random.randint(0, 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111))
            self.integra.assignTamperMemoryByBits(random.randint(0, 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111))
            self.integra.assignOutsByBits(random.randint(0, 0b11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111))
            self.integra.assignZoneAlarmByBits(random.randint(0, 0b11111111111111111111111111111111))
            self.integra.assignZoneArmedByBits(random.randint(0, 0b11111111111111111111111111111111))
            self.integra.assignZoneCode1ByBits(random.randint(0, 0b11111111111111111111111111111111))
            sleep(120)


class Integra(QtCore.QObject):
    """Base class for Satel Integra alarm system"""

    # Qt signals
    hasDetectorsChanged = QtCore.pyqtSignal()
    hasZonesChanged = QtCore.pyqtSignal()
    hasZonesAlarmChanged = QtCore.pyqtSignal(Zone)
    hasOutsChanged = QtCore.pyqtSignal()

    def __init__(self, name='Integra', detectorsNumber=0, outsNumber=0, zonesNumber=0):
        """ Initializing class.

        :param name: system name
        :param detectorsNumber: detector's count
        :param outsNumber: out's count
        :param zonesNumber: zone's count
        :return: none
        """
        super(Integra, self).__init__()

        self.__detectors = []
        self.__outs = []
        self.__zones = []
        self.name = name
        for i in range(detectorsNumber):
            self.__detectors.append(Detector('Detector ' + str(i)))
        for i in range(outsNumber):
            self.__outs.append(Out('Out ' + str(i)))
        for i in range(zonesNumber):
            self.__zones.append(Zone('Zone ' + str(i)))

        # registered functions
        self.registered_functions = {
            0x00: self.CA.assignActiveByBits,
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
            0x29: self.CA.assignTamperMemoryByBits, }

        # TODO: delete after tests. Starts testing thread
        # self.th=Thread(self)
        # self.th.start()

    """Returns class attributes"""
    def getName(self):
        return self.name

    def getDetectors(self):
        return self.__detectors

    def getDetector(self, i):
        return self.__detectors[i]

    def getOuts(self):
        return self.__outs

    def getOut(self, i):
        return self.__outs[i]

    def getZones(self):
        return self.__zones

    def getZone(self, i):
        return self.__zones[i]

    """Adding elements to class"""
    def addDetector(self, detector):
        self.__detectors.append(detector)

    def addOut(self, out):
        self.__outs.append(out)

    def addZone(self, zone):
        self.__zones.append(zone)

    """Setting elements to class"""
    def setDetector(self, index, detector):
        self.__detectors[index] = detector

    def setOut(self, index, out):
        self.__outs[index] = out

    def setZone(self, index, zone):
        self.__zones[index] = zone

    def __checkBit(self, what, position):
        """Checks, if bit in given position is set. Rather only for testing.

        input:
          what - int with bits
          position - int with position to check
        output: boolean, True if bit is set, False otherwise"""
        position = 0b1 << (128 - position)
        if what & position:
            return True
        return False

    def changeByte(self, byte):
        """Changing bytes to human readable.
        View input numbers from CA: 8,7,6,5,4,3,2,1 16,15,14,13,12,11,10,9
        View input numbers from system: 1,2,3,4,5,6,7,8 9,10,11,12,13,14,15,16
        Data from CA: 0101 1001
        Data, which we can use: 1010 1001

        input: byte - int with single byte from CA
        output: useful data"""
        warn('This method is deprecated. Use change_byte from module instead.', DeprecationWarning)
        return change_byte(byte)

    def assignStateByBits(self, function, data):
        """Assign CA state with state from data. Depends on what bit is set in
        data, call function.
        EXPERIMENTAL - don't use it.

        input:
          function: what function to use
          data: int with bits.
        output: none"""
        pass

    def assignAlarmByBits(self, data):
        """Assign alarm state of detectors with data.

        input: data - int with bits - current detectors state
        output: none"""
        """Przypisanie odpowiednich wartosci w tablicach wg. otrzymanych bajtow.
        Bajty powinny byc juz w "ludzkiej" postaci"""
        if len(self.getDetectors()) == 0:
            return

        position = 1
        position = position << (len(self.getDetectors()) - 1)
        for i in self.getDetectors():
            if(position & data):
                i.setAlarm()
            else:
                i.clearAlarm()
            position = position >> 1
        self.hasDetectorsChanged.emit()

    def assignActiveByBits(self, data):
        """Assign active state of detectors depends on data.

        input: data - int with bits - current detectors state
        output: none"""
        if len(self.getDetectors()) == 0:
            return

        position = 1
        position = position << (len(self.getDetectors()) - 1)
        for i in self.getDetectors():
            if(position & data):
                i.setActive()
            else:
                i.clearActive()
            position = position >> 1
        self.hasDetectorsChanged.emit()

    def assignAlarmMemoryByBits(self, data):
        """Assign alarm memory state of detectors depends on data.

        input: data - int with bits - current detectors state
        output: none"""
        if len(self.getDetectors()) == 0:
            return

        position = 1
        position = position << (len(self.getDetectors()) - 1)
        for i in self.getDetectors():
            if(position & data):
                i.setAlarmMemory()
            else:
                i.clearAlarmMemory()
            position = position >> 1
        self.hasDetectorsChanged.emit()

    def assignTamperByBits(self, data):
        """Assign alarm tamper state of detectors depends on data.

        input: data - int with bits - current detectors state
        output: none"""
        if len(self.getDetectors()) == 0:
            return

        position = 1
        position = position << (len(self.getDetectors()) - 1)
        for i in self.getDetectors():
            if(position & data):
                i.setTamper()
            else:
                i.clearTamper()
            position = position >> 1
        self.hasDetectorsChanged.emit()

    def assignTamperMemoryByBits(self, data):
        """Assign alarm tamper memory state of detectors depends on data.

        input: data - int with bits - current detectors state
        output: none"""
        if len(self.getDetectors()) == 0:
            return

        position = 1
        position = position << (len(self.getDetectors()) - 1)
        for i in self.getDetectors():
            if(position & data):
                i.setTamperMemory()
            else:
                i.clearTamperMemory()
            position = position >> 1
        self.hasDetectorsChanged.emit()

    def assignOutsByBits(self, data):
        """Assign state of out depends on data.

        input: data - int with bits - current out state
        output: none"""
        if len(self.getOuts()) == 0:
            return

        position = 1
        position = position << (len(self.getOuts()) - 1)
        for i in self.getOuts():
            if(position & data):
                i.setActive()
            else:
                i.clearActive()
            position = position >> 1
        self.hasOutsChanged.emit()

    def assignZoneArmedByBits(self, data):
        """Assign armed state of zone depends on data.

        input: data - int with bits - current zones state
        output: none"""
        if len(self.getZones()) == 0:
            return

        position = 1
        position = position << (len(self.getZones()) - 1)
        for i in self.getZones():
            if(position & data):
                i.setArmed()
            else:
                i.clearArmed()
            position = position >> 1
        self.hasZonesChanged.emit()

    def assignZoneCode1ByBits(self, data):
        """Assign 1st code state of zone depends on data.

        input: data - int with bits - current zones state
        output: none"""
        if len(self.getZones()) == 0:
            return

        position = 1
        position = position << (len(self.getZones()) - 1)
        for i in self.getZones():
            if(position & data):
                i.setCode1()
            else:
                i.clearCode1()
            position = position >> 1
        self.hasZonesChanged.emit()

    def assignZoneEntryTimeByBits(self, data):
        """Assign entry time state of zone depends on data.

        input: data - int with bits - current zones state
        output: none"""
        if len(self.getZones()) == 0:
            return

        position = 1
        position = position << (len(self.getZones()) - 1)
        for i in self.getZones():
            if(position & data):
                i.setEntryTime()
            else:
                i.clearEntryTime()
            position = position >> 1
        self.hasZonesChanged.emit()

    def assignZoneExitTimeByBits(self, data):
        """Assign exit time state of zone depends on data.

        input: data - int with bits - current zones state
        output: none"""
        if len(self.getZones()) == 0:
            return

        position = 1
        position = position << (len(self.getZones()) - 1)
        for i in self.getZones():
            if(position & data):
                i.setExitTime()
            else:
                i.clearExitTime()
            position = position >> 1
        self.hasZonesChanged.emit()

    def assignZoneAlarmByBits(self, data):
        """Assign alarm state of zone depends on data.

        input: data - int with bits - current zones state
        output: none"""
        if len(self.getZones()) == 0:
            return

        position = 1
        position = position << (len(self.getZones()) - 1)
        for i in self.getZones():
            if(position & data):
                if not i.getAlarm():
                    self.hasZonesAlarmChanged.emit(i)
                i.setAlarm()
            else:
                i.clearAlarm()
            position = position >> 1
        self.hasZonesChanged.emit()

    def assignZoneAlarmMemoryByBits(self, data):
        """Assign alarm memory state of zone depends on data.

        input: data - int with bits - current zones state
        output: none"""
        if len(self.getZones()) == 0:
            return

        position = 1
        position = position << (len(self.getZones()) - 1)
        for i in self.getZones():
            if(position & data):
                i.setAlarmMemory()
            else:
                i.clearAlarmMemory()
            position = position >> 1
        self.hasZonesChanged.emit()

    def assignZoneFireAlarmByBits(self, data):
        """Assign fire alarm state of zone depends on data.

        input: data - int with bits - current zones state
        output: none"""
        if len(self.getZones()) == 0:
            return

        position = 1
        position = position << (len(self.getZones()) - 1)
        for i in self.getZones():
            if(position & data):
                i.setFireAlarm()
            else:
                i.clearFireAlarm()
            position = position >> 1
        self.hasZonesChanged.emit()

    def assignZoneFireAlarmMemoryByBits(self, data):
        """Assign fire alarm memory state of zone depends on data.

        input: data - int with bits - current zones state
        output: none"""
        if len(self.getZones()) == 0:
            return

        position = 1
        position = position << (len(self.getZones()) - 1)
        for i in self.getZones():
            if(position & data):
                i.setFireAlarmMemory()
            else:
                i.clearFireAlarmMemory()
            position = position >> 1
        self.hasZonesChanged.emit()


class Integra24(Integra):
    """Base Satel Integra24 class"""

    def __init__(self):
        """Class initialization with specification from Satel website.

        input: none
        output: none"""
        Integra.__init__(self, name='Integra 24', detectorsNumber=24, outsNumber=20, zonesNumber=4)


class Integra32(Integra):
    """Base Satel Integra32 class"""

    def __init__(self):
        """Class initialization with specifications from Satel.

        input: none
        output: none"""
        Integra.__init__(self, name='Integra 32', detectorsNumber=32, outsNumber=32, zonesNumber=16)


class Integra64(Integra):
    """Base Satel Integra64 class"""

    def __init__(self):
        """Class initialization with specifications from Satel.

        input: none
        output: none"""
        Integra.__init__(self, name='Integra 64', detectorsNumber=64, outsNumber=64, zonesNumber=32)


class Integra64Plus(Integra64):
    """Base Satel Integra 64 Plus class. Currently the same as Integra64"""
    pass


class Integra128(Integra):
    """Base Satel Integra128 class"""

    def __init__(self):
        """Class initialization with specifications from Satel.

        input: none
        output: none"""
        Integra.__init__(self, name='Integra 128', detectorsNumber=128, outsNumber=128, zonesNumber=32)


class Integra128Plus(Integra128):
    """Base Satel Integra128 Plus class. Currently tha same as Integra128 class"""
    pass


class Integra256Plus(Integra):
    """Base Satel Integra256 Plus class"""

    def __init__(self):
        """Class initialization with specifications from Satel.

        input: none
        output: none"""
        Integra.__init__(self, name='Integra 256', detectorsNumber=256, outsNumber=256, zonesNumber=32)


# ------------------------------------------------------------------ testing part
if __name__ == '__main__':
    """Run this file, to start class tests"""
    import unittest
    from random import randint

    class DefaultIntegraTests(unittest.TestCase):
        """Default test class"""
        def testInicjalizacjaOK(self):
            c = Integra()
            self.assertNotEqual(c, False, "Blad inicjalizacji")

        def testInicjalizacjaCzujek(self):
            detectorsCount = randint(1, 256)
            outsCount = randint(1, 256)
            zonesCount = randint(1, 32)
            c = Integra(detectorsCount, outsCount, zonesCount)
            self.assertEqual(detectorsCount, len(c.getDetectors()), "Niewlasciwa ilosc elementow")
            self.assertEqual(outsCount, len(c.getOuts()), 'Bad outs count')
            self.assertEqual(zonesCount, len(c.getZones()), 'Bad zones count')

        def testCzujek(self):
            c = Integra(128, 128, 32)
            for i in c.getDetectors():
                self.assertEqual(False, i.alarm, "Niewlasciwy stan")
                self.assertEqual(False, i.active, "Niewlasciwy stan")
                self.assertEqual(False, i.tamper, "Niewlasciwy stan")
                self.assertEqual(False, i.tamperMemory, "Niewlasciwy stan")
                i.setActive()
                i.setAlarm()
                i.setTamper()
                i.setTamperMemory()
                self.assertEqual(True, i.alarm, "Niewlasciwy stan")
                self.assertEqual(True, i.active, "Niewlasciwy stan")
                self.assertEqual(True, i.tamper, "Niewlasciwy stan")
                self.assertEqual(True, i.tamperMemory, "Niewlasciwy stan")

        def testAssignAlarmByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignAlarmByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
            self.assertEqual(True, c.getDetector(3 - 1).getAlarm(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getDetector(14 - 1).getAlarm(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getDetector(128 - 1).getAlarm(), "Blad zapisu w bitach")
            for i in range(len(c.getDetectors())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 127:
                    continue
                else:
                    self.assertEqual(False, c.getDetector(i).getAlarm(), "Blad zapisu w bitach w " + str(i))

        def testAssignActiveByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignActiveByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
            self.assertEqual(True, c.getDetector(3 - 1).getActive(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getDetector(14 - 1).getActive(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getDetector(128 - 1).getActive(), "Blad zapisu w bitach")
            for i in range(len(c.getDetectors())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 127:
                    continue
                else:
                    self.assertEqual(False, c.getDetector(i).getActive(), "Blad zapisu w bitach w " + str(i))

        def testAssignAlarmMemoryByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignAlarmMemoryByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
            self.assertEqual(True, c.getDetector(3 - 1).getAlarmMemory(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getDetector(14 - 1).getAlarmMemory(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getDetector(128 - 1).getAlarmMemory(), "Blad zapisu w bitach")
            for i in range(len(c.getDetectors())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 127:
                    continue
                else:
                    self.assertEqual(False, c.getDetector(i).getAlarmMemory(), "Blad zapisu w bitach w " + str(i))

        def testAssignTamperByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignTamperByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
            self.assertEqual(True, c.getDetector(3 - 1).getTamper(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getDetector(14 - 1).getTamper(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getDetector(128 - 1).getTamper(), "Blad zapisu w bitach")
            for i in range(len(c.getDetectors())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 127:
                    continue
                else:
                    self.assertEqual(False, c.getDetector(i).getTamper(), "Blad zapisu w bitach w " + str(i))

        def testAssignTamperMemoryByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignTamperMemoryByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
            self.assertEqual(True, c.getDetector(3 - 1).getTamperMemory(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getDetector(14 - 1).getTamperMemory(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getDetector(128 - 1).getTamperMemory(), "Blad zapisu w bitach")
            for i in range(len(c.getDetectors())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 127:
                    continue
                else:
                    self.assertEqual(False, c.getDetector(i).getTamperMemory(), "Blad zapisu w bitach w " + str(i))

        def testAssignOutsByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignOutsByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
            self.assertEqual(True, c.getOut(3 - 1).getActive(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getOut(14 - 1).getActive(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getOut(128 - 1).getActive(), "Blad zapisu w bitach")
            for i in range(len(c.getOuts())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 127:
                    continue
                else:
                    self.assertEqual(False, c.getOut(i).getActive(), "Blad zapisu w bitach w " + str(i))

        def testZoneArmedByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignZoneArmedByBits(0b00100000000001000000000000000001)
            self.assertEqual(True, c.getZone(3 - 1).getArmed(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(14 - 1).getArmed(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(32 - 1).getArmed(), "Blad zapisu w bitach")
            for i in range(len(c.getZones())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 31:
                    continue
                else:
                    self.assertEqual(False, c.getZone(i).getArmed(), "Blad zapisu w bitach w " + str(i))

        def testZoneCode1ByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignZoneCode1ByBits(0b00100000000001000000000000000001)
            self.assertEqual(True, c.getZone(3 - 1).getCode1(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(14 - 1).getCode1(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(32 - 1).getCode1(), "Blad zapisu w bitach")
            for i in range(len(c.getZones())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 31:
                    continue
                else:
                    self.assertEqual(False, c.getZone(i).getCode1(), "Blad zapisu w bitach w " + str(i))

        def testZoneEntryTimeByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignZoneEntryTimeByBits(0b00100000000001000000000000000001)
            self.assertEqual(True, c.getZone(3 - 1).getEntryTime(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(14 - 1).getEntryTime(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(32 - 1).getEntryTime(), "Blad zapisu w bitach")
            for i in range(len(c.getZones())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 31:
                    continue
                else:
                    self.assertEqual(False, c.getZone(i).getEntryTime(), "Blad zapisu w bitach w " + str(i))

        def testZoneExitTimeByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignZoneExitTimeByBits(0b00100000000001000000000000000001)
            self.assertEqual(True, c.getZone(3 - 1).getExitTime(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(14 - 1).getExitTime(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(32 - 1).getExitTime(), "Blad zapisu w bitach")
            for i in range(len(c.getZones())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 31:
                    continue
                else:
                    self.assertEqual(False, c.getZone(i).getExitTime(), "Blad zapisu w bitach w " + str(i))

        def testZoneAlarmByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignZoneAlarmByBits(0b00100000000001000000000000000001)
            self.assertEqual(True, c.getZone(3 - 1).getAlarm(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(14 - 1).getAlarm(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(32 - 1).getAlarm(), "Blad zapisu w bitach")
            for i in range(len(c.getZones())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 31:
                    continue
                else:
                    self.assertEqual(False, c.getZone(i).getAlarm(), "Blad zapisu w bitach w " + str(i))

        def testZoneAlarmMemoryByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignZoneAlarmMemoryByBits(0b00100000000001000000000000000001)
            self.assertEqual(True, c.getZone(3 - 1).getAlarmMemory(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(14 - 1).getAlarmMemory(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(32 - 1).getAlarmMemory(), "Blad zapisu w bitach")
            for i in range(len(c.getZones())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 31:
                    continue
                else:
                    self.assertEqual(False, c.getZone(i).getAlarmMemory(), "Blad zapisu w bitach w " + str(i))

        def testZoneFireAlarmByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignZoneFireAlarmByBits(0b00100000000001000000000000000001)
            self.assertEqual(True, c.getZone(3 - 1).getFireAlarm(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(14 - 1).getFireAlarm(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(32 - 1).getFireAlarm(), "Blad zapisu w bitach")
            for i in range(len(c.getZones())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 31:
                    continue
                else:
                    self.assertEqual(False, c.getZone(i).getFireAlarm(), "Blad zapisu w bitach w " + str(i))

        def testZoneFireAlarmMemoryByBits(self):
            c = Integra(128, 128, 32)
            # Przyklad z instrukcji...
            c.assignZoneFireAlarmMemoryByBits(0b00100000000001000000000000000001)
            self.assertEqual(True, c.getZone(3 - 1).getFireAlarmMemory(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(14 - 1).getFireAlarmMemory(), "Blad zapisu w bitach")
            self.assertEqual(True, c.getZone(32 - 1).getFireAlarmMemory(), "Blad zapisu w bitach")
            for i in range(len(c.getZones())):
                if i == 2:
                    continue
                elif i == 13:
                    continue
                elif i == 31:
                    continue
                else:
                    self.assertEqual(False, c.getZone(i).getFireAlarmMemory(), "Blad zapisu w bitach w " + str(i))

    class Integra24Test(unittest.TestCase):
        """Testing Integra24 class"""

        def testInitialization(self):
            ca = Integra24()
            self.assertEqual(24,
                             len(ca.getDetectors()),
                             'Bad detectors number in Integra24 class')
            self.assertEqual(20,
                             len(ca.getOuts()),
                             'Bad outs number in Integra24 class')
            self.assertEqual(4,
                             len(ca.getZones()),
                             'Bad zones number in Integra24 class')

    class Integra32Test(unittest.TestCase):
        """Testing Integra24 class"""

        def testInitialization(self):
            ca = Integra32()
            self.assertEqual(32,
                             len(ca.getDetectors()),
                             'Bad detectors number in Integra32 class')
            self.assertEqual(32,
                             len(ca.getOuts()),
                             'Bad outs number in Integra32 class')
            self.assertEqual(16,
                             len(ca.getZones()),
                             'Bad zones number in Integra32 class')

    class Integra64Test(unittest.TestCase):
        """Testing Integra24 class"""

        def testInitialization(self):
            ca = Integra64()
            self.assertEqual(64,
                             len(ca.getDetectors()),
                             'Bad detectors number in Integra64 class')
            self.assertEqual(64,
                             len(ca.getOuts()),
                             'Bad outs number in Integra64 class')
            self.assertEqual(32,
                             len(ca.getZones()),
                             'Bad zones number in Integra64 class')

    class Integra128Test(unittest.TestCase):
        """Testing Integra24 class"""

        def testInitialization(self):
            ca = Integra128()
            self.assertEqual(128,
                             len(ca.getDetectors()),
                             'Bad detectors number in Integra128 class')
            self.assertEqual(128,
                             len(ca.getOuts()),
                             'Bad outs number in Integra128 class')
            self.assertEqual(32,
                             len(ca.getZones()),
                             'Bad zones number in Integra128 class')

    class Integra256Test(unittest.TestCase):
        """Testing Integra24 class"""

        def testInitialization(self):
            ca = Integra256Plus()
            self.assertEqual(256,
                             len(ca.getDetectors()),
                             'Bad detectors number in Integra256 class')
            self.assertEqual(256,
                             len(ca.getOuts()),
                             'Bad outs number in Integra256 class')
            self.assertEqual(32,
                             len(ca.getZones()),
                             'Bad zones number in Integra256 class')

    unittest.main()
