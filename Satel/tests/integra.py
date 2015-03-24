import unittest
from random import randint

from Satel.integra import Integra, Integra128, Integra24, Integra256Plus, Integra32, Integra64


class DefaultIntegraTests(unittest.TestCase):
    """Default test class"""
    def setUp(self):
        super(DefaultIntegraTests, self).setUp()
        self.integra = Integra()

    def test_initializing(self):
        self.assertNotEqual(self.integra, False, 'Initializing error')

    def test_count(self):
        detectorsCount = randint(1, 256)
        outsCount = randint(1, 256)
        zonesCount = randint(1, 32)
        c = Integra(detectorsNumber=detectorsCount, outsNumber=outsCount, zonesNumber=zonesCount)
        self.assertEqual(detectorsCount, len(c.getDetectors()), 'Invalid detectors count')
        self.assertEqual(outsCount, len(c.getOuts()), 'Invalid outs count')
        self.assertEqual(zonesCount, len(c.getZones()), 'Invalid zones count')

    def testCzujek(self):
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignAlarmByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getDetector(2).getAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(13).getAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(127).getAlarm(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignActiveByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getDetector(2).getActive(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(13).getActive(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(127).getActive(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignAlarmMemoryByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getDetector(2).getAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(13).getAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(127).getAlarmMemory(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignTamperByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getDetector(2).getTamper(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(13).getTamper(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(127).getTamper(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignTamperMemoryByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getDetector(2).getTamperMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(13).getTamperMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(127).getTamperMemory(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignOutsByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getOut(2).getActive(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getOut(13).getActive(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getOut(127).getActive(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignZoneArmedByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(2).getArmed(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(13).getArmed(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(31).getArmed(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignZoneCode1ByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(2).getCode1(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(13).getCode1(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(31).getCode1(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignZoneEntryTimeByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(2).getEntryTime(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(13).getEntryTime(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(31).getEntryTime(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignZoneExitTimeByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(2).getExitTime(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(13).getExitTime(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(31).getExitTime(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignZoneAlarmByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(2).getAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(13).getAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(31).getAlarm(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignZoneAlarmMemoryByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(2).getAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(13).getAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(31).getAlarmMemory(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignZoneFireAlarmByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(2).getFireAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(13).getFireAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(31).getFireAlarm(), "Blad zapisu w bitach")
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
        c = Integra(detectorsNumber=128, outsNumber=128, zonesNumber=32)
        c.assignZoneFireAlarmMemoryByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(2).getFireAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(13).getFireAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(31).getFireAlarmMemory(), "Blad zapisu w bitach")
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

    def test_elements_count(self):
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

    def test_elements_count(self):
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

    def test_elements_count(self):
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

    def test_elements_count(self):
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

    def test_elements_count(self):
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
