import unittest
from random import randint

from Satel.integra import Integra, Integra128, Integra24, Integra256Plus, Integra32, Integra64


class DefaultIntegraTests(unittest.TestCase):
    """Default test class"""
    def testInicjalizacjaOK(self):
        c=Integra()
        self.assertNotEqual(c, False, "Blad inicjalizacji")

    def testInicjalizacjaCzujek(self):
        detectorsCount=randint(1,256)
        outsCount=randint(1, 256)
        zonesCount=randint(1,32)
        c=Integra(detectorsCount, outsCount, zonesCount)
        self.assertEqual(detectorsCount, len(c.getDetectors()), "Niewlasciwa ilosc elementow")
        self.assertEqual(outsCount, len(c.getOuts()), 'Bad outs count')
        self.assertEqual(zonesCount, len(c.getZones()), 'Bad zones count')

    def testCzujek(self):
        c=Integra(128,128,32)
        for i in c.getDetectors():
            self.assertEqual(False,i.alarm,"Niewlasciwy stan")
            self.assertEqual(False,i.active,"Niewlasciwy stan")
            self.assertEqual(False,i.tamper,"Niewlasciwy stan")
            self.assertEqual(False,i.tamperMemory,"Niewlasciwy stan")
            i.setActive()
            i.setAlarm()
            i.setTamper()
            i.setTamperMemory()
            self.assertEqual(True,i.alarm,"Niewlasciwy stan")
            self.assertEqual(True,i.active,"Niewlasciwy stan")
            self.assertEqual(True,i.tamper,"Niewlasciwy stan")
            self.assertEqual(True,i.tamperMemory,"Niewlasciwy stan")

    def testAssignAlarmByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignAlarmByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getDetector(3-1).getAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(14-1).getAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(128-1).getAlarm(), "Blad zapisu w bitach")
        for i in range(len(c.getDetectors())):
            if i==2: continue
            elif i==13: continue
            elif i==127: continue
            else: self.assertEqual(False,c.getDetector(i).getAlarm(),"Blad zapisu w bitach w "+str(i))

    def testAssignActiveByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignActiveByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getDetector(3-1).getActive(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(14-1).getActive(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(128-1).getActive(), "Blad zapisu w bitach")
        for i in range(len(c.getDetectors())):
            if i==2: continue
            elif i==13: continue
            elif i==127: continue
            else: self.assertEqual(False,c.getDetector(i).getActive(),"Blad zapisu w bitach w "+str(i))

    def testAssignAlarmMemoryByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignAlarmMemoryByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getDetector(3-1).getAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(14-1).getAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(128-1).getAlarmMemory(), "Blad zapisu w bitach")
        for i in range(len(c.getDetectors())):
            if i==2: continue
            elif i==13: continue
            elif i==127: continue
            else: self.assertEqual(False,c.getDetector(i).getAlarmMemory(),"Blad zapisu w bitach w "+str(i))

    def testAssignTamperByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignTamperByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getDetector(3-1).getTamper(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(14-1).getTamper(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(128-1).getTamper(), "Blad zapisu w bitach")
        for i in range(len(c.getDetectors())):
            if i==2: continue
            elif i==13: continue
            elif i==127: continue
            else: self.assertEqual(False,c.getDetector(i).getTamper(),"Blad zapisu w bitach w "+str(i))

    def testAssignTamperMemoryByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignTamperMemoryByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getDetector(3-1).getTamperMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(14-1).getTamperMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getDetector(128-1).getTamperMemory(), "Blad zapisu w bitach")
        for i in range(len(c.getDetectors())):
            if i==2: continue
            elif i==13: continue
            elif i==127: continue
            else: self.assertEqual(False,c.getDetector(i).getTamperMemory(),"Blad zapisu w bitach w "+str(i))

    def testAssignOutsByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignOutsByBits(0b00100000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001)
        self.assertEqual(True, c.getOut(3-1).getActive(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getOut(14-1).getActive(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getOut(128-1).getActive(), "Blad zapisu w bitach")
        for i in range(len(c.getOuts())):
            if i==2: continue
            elif i==13: continue
            elif i==127: continue
            else: self.assertEqual(False,c.getOut(i).getActive(),"Blad zapisu w bitach w "+str(i))

    def testZoneArmedByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignZoneArmedByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(3-1).getArmed(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(14-1).getArmed(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(32-1).getArmed(), "Blad zapisu w bitach")
        for i in range(len(c.getZones())):
            if i==2: continue
            elif i==13: continue
            elif i==31: continue
            else: self.assertEqual(False,c.getZone(i).getArmed(),"Blad zapisu w bitach w "+str(i))

    def testZoneCode1ByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignZoneCode1ByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(3-1).getCode1(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(14-1).getCode1(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(32-1).getCode1(), "Blad zapisu w bitach")
        for i in range(len(c.getZones())):
            if i==2: continue
            elif i==13: continue
            elif i==31: continue
            else: self.assertEqual(False,c.getZone(i).getCode1(),"Blad zapisu w bitach w "+str(i))

    def testZoneEntryTimeByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignZoneEntryTimeByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(3-1).getEntryTime(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(14-1).getEntryTime(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(32-1).getEntryTime(), "Blad zapisu w bitach")
        for i in range(len(c.getZones())):
            if i==2: continue
            elif i==13: continue
            elif i==31: continue
            else: self.assertEqual(False,c.getZone(i).getEntryTime(),"Blad zapisu w bitach w "+str(i))

    def testZoneExitTimeByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignZoneExitTimeByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(3-1).getExitTime(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(14-1).getExitTime(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(32-1).getExitTime(), "Blad zapisu w bitach")
        for i in range(len(c.getZones())):
            if i==2: continue
            elif i==13: continue
            elif i==31: continue
            else: self.assertEqual(False,c.getZone(i).getExitTime(),"Blad zapisu w bitach w "+str(i))

    def testZoneAlarmByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignZoneAlarmByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(3-1).getAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(14-1).getAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(32-1).getAlarm(), "Blad zapisu w bitach")
        for i in range(len(c.getZones())):
            if i==2: continue
            elif i==13: continue
            elif i==31: continue
            else: self.assertEqual(False,c.getZone(i).getAlarm(),"Blad zapisu w bitach w "+str(i))

    def testZoneAlarmMemoryByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignZoneAlarmMemoryByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(3-1).getAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(14-1).getAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(32-1).getAlarmMemory(), "Blad zapisu w bitach")
        for i in range(len(c.getZones())):
            if i==2: continue
            elif i==13: continue
            elif i==31: continue
            else: self.assertEqual(False,c.getZone(i).getAlarmMemory(),"Blad zapisu w bitach w "+str(i))

    def testZoneFireAlarmByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignZoneFireAlarmByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(3-1).getFireAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(14-1).getFireAlarm(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(32-1).getFireAlarm(), "Blad zapisu w bitach")
        for i in range(len(c.getZones())):
            if i==2: continue
            elif i==13: continue
            elif i==31: continue
            else: self.assertEqual(False,c.getZone(i).getFireAlarm(),"Blad zapisu w bitach w "+str(i))

    def testZoneFireAlarmMemoryByBits(self):
        c=Integra(128,128,32)
        #Przyklad z instrukcji...
        c.assignZoneFireAlarmMemoryByBits(0b00100000000001000000000000000001)
        self.assertEqual(True, c.getZone(3-1).getFireAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(14-1).getFireAlarmMemory(), "Blad zapisu w bitach")
        self.assertEqual(True, c.getZone(32-1).getFireAlarmMemory(), "Blad zapisu w bitach")
        for i in range(len(c.getZones())):
            if i==2: continue
            elif i==13: continue
            elif i==31: continue
            else: self.assertEqual(False,c.getZone(i).getFireAlarmMemory(),"Blad zapisu w bitach w "+str(i))

class Integra24Test(unittest.TestCase):
    """Testing Integra24 class"""

    def testInitialization(self):
        ca=Integra24()
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
        ca=Integra32()
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
        ca=Integra64()
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
        ca=Integra128()
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
        ca=Integra256Plus()
        self.assertEqual(256,
                         len(ca.getDetectors()),
                         'Bad detectors number in Integra256 class')
        self.assertEqual(256,
                         len(ca.getOuts()),
                         'Bad outs number in Integra256 class')
        self.assertEqual(32,
                         len(ca.getZones()),
                         'Bad zones number in Integra256 class')