#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from warnings import warn

from .byteFunctions import change_byte


class Detector(QtCore.QObject):
    """Detectors in system. This is should be base class for all detectors in
    any systems. Currently here is only Integra system, so this is not used in
    this way."""

    # Qt signals
    hasChanged = QtCore.pyqtSignal()
    name_changed = QtCore.pyqtSignal()
    active_changed = QtCore.pyqtSignal()
    alarm_changed = QtCore.pyqtSignal()
    alarm_memory_changed = QtCore.pyqtSignal()
    tamper_changed = QtCore.pyqtSignal()
    tamper_memory_changed = QtCore.pyqtSignal()

    def __init__(self, name=''):
        """ Initializing class

        :param name: string with detector's name
        :return: none
        """
        super(Detector, self).__init__()

        self._name = name
        self._active = False
        self._alarm = False
        self._alarm_memory = False
        self._tamper = False
        self._tamper_memory = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if self._name != val:
            self._name = str(val)
            self.name_changed.emit()

        self.hasChanged.emit()

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._active != val:
            self._active = val
            self.active_changed.emit()

        self.hasChanged.emit()

    @property
    def alarm(self):
        return self._alarm

    @alarm.setter
    def alarm(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._alarm != val:
            self._alarm = val
            self.alarm_changed.emit()

        self.hasChanged.emit()

    @property
    def alarm_memory(self):
        return self._alarm_memory

    @alarm_memory.setter
    def alarm_memory(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._alarm_memory != val:
            self._alarm_memory = val
            self.alarm_memory_changed.emit()

        self.hasChanged.emit()

    @property
    def tamper(self):
        return self._tamper

    @tamper.setter
    def tamper(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._tamper != val:
            self._tamper = val
            self.tamper_changed.emit()

        self.hasChanged.emit()

    @property
    def tamper_memory(self):
        return self._tamper_memory

    @tamper_memory.setter
    def tamper_memory(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._tamper_memory != val:
            self._tamper_memory = val
            self.tamper_memory_changed.emit()

        self.hasChanged.emit()

    def setName(self, name):  # pragma: no cover
        """
        :param name: (str) new detector name
        :return: none
        """
        warn('This method is deprecated. Use name directly.', DeprecationWarning)
        self._name = name
        self.hasChanged.emit()

    def setAlarm(self):  # pragma: no cover
        """ Setting detector to alarm state

        :return: none
        """
        warn('This method is deprecated. Use alarm directly.', DeprecationWarning)
        self._alarm = True
        self.hasChanged.emit()

    def setAlarmMemory(self):  # pragma: no cover
        """ Setting detector to alarm memory state
        :return: none
        """
        warn('This method is deprecated. Use alarm_memory directly.', DeprecationWarning)
        self._alarm_memory = True
        self.hasChanged.emit()

    def setActive(self):  # pragma: no cover
        """ Setting detector to active state.

        :return: none
        """
        warn('This method is deprecated. Use active directly.', DeprecationWarning)
        self._active = True
        self.hasChanged.emit()

    def setTamper(self):  # pragma: no cover
        """ Setting detector to tamper (sabotage) state

        :return: none
        """
        warn('This method is deprecated. Use tamper directly.', DeprecationWarning)
        self._tamper = True
        self.hasChanged.emit()

    def setTamperMemory(self):  # pragma: no cover
        """ Setting detector to tamper memory state.

        :return: none
        """
        warn('This method is deprecated. Use tamper_memory directly.', DeprecationWarning)
        self._tamper_memory = True
        self.hasChanged.emit()

    def clearAlarm(self):  # pragma: no cover
        """ Clearing alarm state from detector.

        :return: none
        """
        warn('This method is deprecated. Use alarm directly.', DeprecationWarning)
        self._alarm = False
        self.hasChanged.emit()

    def clearAlarmMemory(self):  # pragma: no cover
        """ Clearing alarm memory state from detector.

        :return: none
        """
        warn('This method is deprecated. Use alarm_memory directly.', DeprecationWarning)
        self._alarm_memory = False
        self.hasChanged.emit()

    def clearActive(self):  # pragma: no cover
        """ Clearing active state from detector.

        :return: none
        """
        warn('This method is deprecated. Use active directly.', DeprecationWarning)
        self._active = False
        self.hasChanged.emit()

    def clearTamper(self):  # pragma: no cover
        """ Clearing tamper state from detector.

        :return: none
        """
        warn('This method is deprecated. Use tamper directly.', DeprecationWarning)
        self._tamper = False
        self.hasChanged.emit()

    def clearTamperMemory(self):  # pragma: no cover
        """ Clearing tamper memory state from detector.

        :return: none
        """
        warn('This method is deprecated. Use tamper_memory directly.', DeprecationWarning)
        self._tamper_memory = False
        self.hasChanged.emit()

    """Functions for get data from class attributes"""
    # According to new functions in Python3, setting, clearing and getting methods will be changed
    def getActive(self):  # pragma: no cover
        warn('This method is deprecated. Use active directly.', DeprecationWarning)
        return self._active

    def getName(self):  # pragma: no cover
        warn('This method is deprecated. Use name directly.', DeprecationWarning)
        return self._name

    def getAlarm(self):  # pragma: no cover
        warn('This method is deprecated. Use alarm directly.', DeprecationWarning)
        return self._alarm

    def getAlarmMemory(self):  # pragma: no cover
        warn('This method is deprecated. Use alarm_memory directly.', DeprecationWarning)
        return self._alarm_memory

    def getTamper(self):  # pragma: no cover
        warn('This method is deprecated. Use tamper directly.', DeprecationWarning)
        return self._tamper

    def getTamperMemory(self):  # pragma: no cover
        warn('This method is deprecated. Use tamper_memory directly.', DeprecationWarning)
        return self._tamper_memory


class Out(QtCore.QObject):
    """Base class for any out in system. This is should be base class for all
    out in any system. Currently here is only Integra, so this is not used in
    this way."""

    # Qt signals
    hasChanged = QtCore.pyqtSignal()
    name_changed = QtCore.pyqtSignal()
    active_changed = QtCore.pyqtSignal()

    def __init__(self, name=''):
        """ Initializing class.

        :param name: out name
        :return: none
        """
        super(Out, self).__init__()

        self._name = name
        self._active = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if self._name != val:
            self._name = val
            self.name_changed.emit()

        self.hasChanged.emit()

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._active != val:
            self._active = val
            self.active_changed.emit()

        self.hasChanged.emit()

    def setName(self, name):  # pragma: no cover
        """ Changes out name.

        :param name: new name
        :return:
        """
        warn('This method is deprecated. Use name directly.', DeprecationWarning)
        self._name = name
        self.hasChanged.emit()

    def setActive(self):  # pragma: no cover
        """ Setting out to active state.

        :return:
        """
        warn('This method is deprecated. Use active directly.', DeprecationWarning)
        self._active = True
        self.hasChanged.emit()

    def clearActive(self):  # pragma: no cover
        """ Clearing active state.

        :return:
        """
        warn('This method is deprecated. Use active directly.', DeprecationWarning)
        self._active = False
        self.hasChanged.emit()

    """Function returns class attributes"""
    def getActive(self):  # pragma: no cover
        warn('This method is deprecated. Use active directly.', DeprecationWarning)
        return self._active

    def getName(self):  # pragma: no cover
        warn('This method is deprecated. Use name directly.', DeprecationWarning)
        return self._name


class Zone(QtCore.QObject):
    """Base class for any alarm zone in system. This is should be base class for all
    zones in any system. Currently here is only Integra, so this is not used in
    this way."""

    # Qt signals
    hasChanged = QtCore.pyqtSignal()
    name_changed = QtCore.pyqtSignal()
    armed_changed = QtCore.pyqtSignal()
    first_code_changed = QtCore.pyqtSignal()
    entry_time_changed = QtCore.pyqtSignal()
    exit_time_changed = QtCore.pyqtSignal()
    alarm_changed = QtCore.pyqtSignal()
    alarm_memory_changed = QtCore.pyqtSignal()
    fire_alarm_changed = QtCore.pyqtSignal()
    fire_alarm_memory_changed = QtCore.pyqtSignal()

    def __init__(self, name=''):
        """ Class initialization.

        :param name: zone name
        :return:
        """
        super(Zone, self).__init__()

        self._name = name
        self._armed = False
        self._first_code = False
        self._entry_time = False
        self._exit_time = False
        self._alarm = False
        self._alarm_memory = False
        self._fire_alarm = False
        self._fire_alarm_memory = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if self._name != val:
            self._name = val
            self.name_changed.emit()

        self.hasChanged.emit()

    @property
    def armed(self):
        return self._armed

    @armed.setter
    def armed(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._armed != val:
            self._armed = val
            self.armed_changed.emit()

        self.hasChanged.emit()

    @property
    def first_code(self):
        return self._first_code

    @first_code.setter
    def first_code(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._first_code != val:
            self._first_code = val
            self.first_code_changed.emit()

        self.hasChanged.emit()

    @property
    def entry_time(self):
        return self._entry_time

    @entry_time.setter
    def entry_time(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._entry_time != val:
            self._entry_time = val
            self.entry_time_changed.emit()

        self.hasChanged.emit()

    @property
    def exit_time(self):
        return self._exit_time

    @exit_time.setter
    def exit_time(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._exit_time != val:
            self._exit_time = val
            self.exit_time_changed.emit()

        self.hasChanged.emit()

    @property
    def alarm(self):
        return self._alarm

    @alarm.setter
    def alarm(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._alarm != val:
            self._alarm = val
            self.alarm_changed.emit()

        self.hasChanged.emit()

    @property
    def alarm_memory(self):
        return self._alarm_memory

    @alarm_memory.setter
    def alarm_memory(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._alarm_memory != val:
            self._alarm_memory = val
            self.alarm_memory_changed.emit()

        self.hasChanged.emit()

    @property
    def fire_alarm(self):
        return self._fire_alarm

    @fire_alarm.setter
    def fire_alarm(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._fire_alarm != val:
            self._fire_alarm = val
            self.fire_alarm_changed.emit()

        self.hasChanged.emit()

    @property
    def fire_alarm_memory(self):
        return self._fire_alarm_memory

    @fire_alarm_memory.setter
    def fire_alarm_memory(self, val):
        if not isinstance(val, bool):
            raise TypeError('Value should be a boolean value only')

        if self._fire_alarm_memory != val:
            self._fire_alarm_memory = val
            self.fire_alarm_memory_changed.emit()

        self.hasChanged.emit()

    def setName(self, name):  # pragma: no cover
        """ Setting new name to zone.

        :param name: new name
        :return:
        """
        warn('This method is deprecated. Use name directly.', DeprecationWarning)
        self._name = name
        self.hasChanged.emit()

    def setArmed(self):  # pragma: no cover
        """ Setting zone to armed state.

        :return: none
        """
        warn('This method is deprecated. Use armed directly.', DeprecationWarning)
        self._armed = True
        self.hasChanged.emit()

    def setCode1(self):  # pragma: no cover
        """ Setting zone to state after first password.

        :return: none
        """
        warn('This method is deprecated. Use first_code directly.', DeprecationWarning)
        self._first_code = True
        self.hasChanged.emit()

    def setEntryTime(self):  # pragma: no cover
        """ Setting zone to entry time state.

        :return: none
        """
        warn('This method is deprecated. Use entry_time directly.', DeprecationWarning)
        self._entry_time = True
        self.hasChanged.emit()

    def setExitTime(self):  # pragma: no cover
        """ Setting zone to exit time state.

        :return: none
        """
        warn('This method is deprecated. Use exit_time directly.', DeprecationWarning)
        self._exit_time = True
        self.hasChanged.emit()

    def setAlarm(self):  # pragma: no cover
        """ Setting zone to alarm state
        :return: none
        """
        warn('This method is deprecated. Use alarm directly.', DeprecationWarning)
        self._alarm = True
        self.hasChanged.emit()

    def setAlarmMemory(self):  # pragma: no cover
        """ Setting zone to alarm memory state.

        :return: none
        """
        warn('This method is deprecated. Use alarm_memory directly.', DeprecationWarning)
        self._alarm_memory = True
        self.hasChanged.emit()

    def setFireAlarm(self):  # pragma: no cover
        """ Setting zone to fire alarm state.

        :return: none
        """
        warn('This method is deprecated. Use fire_alarm directly.', DeprecationWarning)
        self._fire_alarm = True
        self.hasChanged.emit()

    def setFireAlarmMemory(self):  # pragma: no cover
        """ Setting zone to fire memory state.

        :return: none
        """
        warn('This method is deprecated. Use fire_alarm_memory directly.', DeprecationWarning)
        self._fire_alarm_memory = True
        self.hasChanged.emit()

    def clearArmed(self):  # pragma: no cover
        """ Clearing armed state.

        :return: none
        """
        warn('This method is deprecated. Use armed directly.', DeprecationWarning)
        self._armed = False
        self.hasChanged.emit()

    def clearCode1(self):  # pragma: no cover
        """ Clearing after first password state.

        :return: none
        """
        warn('This method is deprecated. Use first_code directly.', DeprecationWarning)
        self._first_code = False
        self.hasChanged.emit()

    def clearEntryTime(self):  # pragma: no cover
        """ Clearing entry time state.

        :return: none
        """
        warn('This method is deprecated. Use entry_time directly.', DeprecationWarning)
        self._entry_time = False
        self.hasChanged.emit()

    def clearExitTime(self):  # pragma: no cover
        """ Clearing exit time state.

        :return: none
        """
        warn('This method is deprecated. Use exit_time directly.', DeprecationWarning)
        self._exit_time = False
        self.hasChanged.emit()

    def clearAlarm(self):  # pragma: no cover
        """ Clearing alarm state.

        :return: none
        """
        warn('This method is deprecated. Use alarm directly.', DeprecationWarning)
        self._alarm = False
        self.hasChanged.emit()

    def clearAlarmMemory(self):  # pragma: no cover
        """ Clearing alarm memory state.

        :return: none
        """
        warn('This method is deprecated. Use alarm_memory directly.', DeprecationWarning)
        self._alarm_memory = False
        self.hasChanged.emit()

    def clearFireAlarm(self):  # pragma: no cover
        """ Clearing fire alarm state.

        :return: none
        """
        warn('This method is deprecated. Use fire_alarm directly.', DeprecationWarning)
        self._fire_alarm = False
        self.hasChanged.emit()

    def clearFireAlarmMemory(self):  # pragma: no cover
        """ Clearing fire alarm memory state.

        :return: none
        """
        warn('This method is deprecated. Use fire_alarm_memory directly.', DeprecationWarning)
        self._alarm_memory = False
        self.hasChanged.emit()

    """Function return class attributes"""
    def getName(self):  # pragma: no cover
        warn('This method is deprecated. Use name directly.', DeprecationWarning)
        return self._name

    def getArmed(self):  # pragma: no cover
        warn('This method is deprecated. Use armed directly.', DeprecationWarning)
        return self._armed

    def getCode1(self):  # pragma: no cover
        warn('This method is deprecated. Use first_code directly.', DeprecationWarning)
        return self._first_code

    def getEntryTime(self):  # pragma: no cover
        warn('This method is deprecated. Use entry_time directly.', DeprecationWarning)
        return self._entry_time

    def getExitTime(self):  # pragma: no cover
        warn('This method is deprecated. Use exit_time directly.', DeprecationWarning)
        return self._exit_time

    def getAlarm(self):  # pragma: no cover
        warn('This method is deprecated. Use alarm directly.', DeprecationWarning)
        return self._alarm

    def getAlarmMemory(self):  # pragma: no cover
        warn('This method is deprecated. Use alarm_memory directly.', DeprecationWarning)
        return self._alarm_memory

    def getFireAlarm(self):  # pragma: no cover
        warn('This method is deprecated. Use fire_alarm directly.', DeprecationWarning)
        return self._fire_alarm

    def getFireAlarmMemory(self):  # pragma: no cover
        warn('This method is deprecated. Use fire_alarm_memory directly.', DeprecationWarning)
        return self._fire_alarm_memory

# TODO: delete after tests
# Thread change randomly some attributes in system
from time import sleep
import random


class Thread(QtCore.QThread):  # pragma: no cover

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
            0x00: self.assignActiveByBits,
            0x01: self.assignTamperByBits,
            0x02: self.assignAlarmByBits,
            0x03: self.assignTamperByBits,
            0x04: self.assignAlarmMemoryByBits,
            0x05: self.assignTamperMemoryByBits,
            0x09: self.assignZoneArmedByBits,
            0x0A: self.assignZoneArmedByBits,
            0x0D: self.assignZoneCode1ByBits,
            0x0E: self.assignZoneEntryTimeByBits,
            0x0F: self.assignZoneExitTimeByBits,
            0x10: self.assignZoneExitTimeByBits,
            0x13: self.assignZoneAlarmByBits,
            0x14: self.assignZoneFireAlarmByBits,
            0x15: self.assignZoneAlarmMemoryByBits,
            0x16: self.assignZoneFireAlarmMemoryByBits,
            0x17: self.assignOutsByBits,
            0x28: self.assignTamperByBits,
            0x29: self.assignTamperMemoryByBits, }

        # TODO: delete after tests. Starts testing thread
        # self.th=Thread(self)
        # self.th.start()

    """Returns class attributes"""
    def getName(self):
        warn('This method is deprecated. Use name directly.', DeprecationWarning)
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
