'''
Created on 30 cze 2014

@author: Paweł Surowiec
'''

from PyQt4 import QtCore
import serial
import socket
from time import sleep

#===============================================================================
# DataReader
# Klasa podstawowa dla klas realizujących odczyt danych
#===============================================================================
class DataReader(QtCore.QObject):

    def read(self):
        raise NameError('Niezdefiniowana metoda "read"')

    def write(self, data):
        raise NameError('Niezdefiniowana metoda "write"')

    def connect(self):
        raise NameError('Niezdefiniowana metoda "connect"')


class RS232DataReader(DataReader):

    def __init__(self, port):
        super(RS232DataReader, self).__init__()
        self.port=serial.Serial(port, 19200, timeout=2)

    def read(self):
        return self.port.read()

    def write(self, data):
        self.port.write(data)


class EthernetDataReader(DataReader):

    def __init__(self, ipAdress, port):
        super(EthernetDataReader, self).__init__()
        self.ipAdress=ipAdress
        self.port=port
        self.socket=None

    def read(self):
        if self.socket is not None:
            try:
                dane=self.socket.recv(2048)
                # print('<< '+str(dane))
                return dane
            except:
                return bytearray()

    def write(self, data):
        #     data=bytearray()
        #     data.extend([0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D])
        if self.socket is not None:
            #       try:
            # print('>> '+str(data))
            self.socket.send(data)
        #       except:
        #         print('Wysyłanie nieudane')
        #         pass

    def connect(self):
        proto = socket.getprotobyname('tcp')
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)
        try:
            self.socket.connect((self.ipAdress, self.port))
        except Exception as e:
            print('Problem with connecting to Integra at', str(self.ipAdress) + ':' + str(self.port))
            print(e)

    def close_connection(self):
        self.socket.close()


class DataParser(QtCore.QThread):

    def __init__(self):
        super(DataParser, self).__init__()
        self.CA=None
        self.port=None
        self.time=60
        self.zadania=[]

    def __rl(self, data):
        '''
        Obrót bitów w lewo z przepisaniem
        '''
        # przesunięcie bitów z obcięciem do 2 bajtów
        wynik=((data<<1)&0b1111111111111111)
        #przepisanie najstarszego bitu na pozycję 1
        wynik=wynik|((data&0b1000000000000000)>>15)
        return wynik

    def __hi(self, data):
        '''
        Wysoki bajt z danych
        '''
        return (data&0xff00)//256

    def __lo(self, data):
        return data[0]&0xff

    def __calculateCRC(self, data):
        '''
        Wyliczenie sumy kontrolnej
        data: [] z bajtami danych
        '''
        crc=0x147A
        for d in data:
            crc=self.__rl(crc)          # przesunięcie
            crc=crc^0xffff              # XOR
            crc=crc+self.__hi(crc)+d    # roszada
            crc=crc&0b1111111111111111  # obcięcie do 2 bajtów
        #     print(hex(crc))
        #     print(bytearray.fromhex(hex(crc)[2:]))
        #     ret=bytearray()
        #     ret=bytearray.fromhex(hex(crc)[2:])
        #     tmp=ret[0]
        #     ret[0]=ret[1]
        #     ret[1]=tmp
        #     return ret
        #     return crc
        inStr=hex(crc)[2:]
        if (len(inStr)%2)==1: inStr='0'+inStr
        return bytearray.fromhex(inStr)

    #TODO: po testach do usunięcia
    def testHi(self, data): return self.__hi(data)
    def testRl(self, data): return self.__rl(data)
    def testCRC(self, data): return self.__calculateCRC(data)

    def setTime(self, time):
        self.time=time

    def assignCA(self, CA):
        self.CA=CA

    def assignPort(self, port):
        #     self.port=serial.Serial(port, 19200, timeout=2)
        self.port=port

    def checkFrame(self, data):
        '''
        data: [] z bajtami danych - bajty synchronizacji, dane oraz crc
        '''
        # minimalna długość ramki:
        # synchronizacja (2): FE FE
        # cmd (1): bajt
        # dane (4): 4 bajty (albo 0 bajtów dla wysyłania)
        # crc (2)
        # koniec ramki (2)
        if data is None: return False
        if len(data)<2+1+0+2+2:
            #  print("Zła długość ramki")
            return False
        if (data[0]!=0xfe)&(data[1]!=0xfe):
            #  print("Błąd synchronizacji ramki")
            return False
        if (data[-1]!=0x0d)&(data[-2]!=0xfe):
            #  print("Błąd zakończenia ramki")
            return False
        #TODO: zmiana FE F0 na FE, - można to wstawić przy odczycie
        # danych z centrali
        tmp=data[:]
        data=[]
        for i in range(len(tmp)):
            if (tmp[i]==0xf0)&(tmp[i-1]==0xfe): pass
            else: data.append(tmp[i])

        crc=self.__calculateCRC(data[2:-4])
        #     if (data[-3]!=self.__lo(crc)): #zamienione
        if(data[-3]!=crc[1]):
            print("Błąd CRC(lo): "+hex(data[-3])+", wyliczone: "+hex(self.__lo(crc)))
            return False
        #     if (data[-4]!=self.__hi(crc)): #zamienione
        if(data[-4]!=crc[0]):
            print("Błąd CRC(hi)")
            return False
        return True

    def buildFrame(self, data):
        dane=bytearray()
        dane.append(0xFE)
        dane.append(0xFE)
        if type(data) is list: dane.extend(data)
        else: dane.append(data)
        #     crc=self.__calculateCRC(data)
        #     dane.extend(crc)
        dane.extend(self.__calculateCRC(data))
        dane.append(0xFE)
        dane.append(0x0D)
        return dane

    def parseData(self, data):
        '''
        Identyfikacja danych
        data: [] bajty, bez crc oraz synchronizacji ramek
        '''

        '''
        Dla potomnych - raczej niepotrzebne
          dane=0
          for d in data[1:-1]:
            dl=d&0x0f
            dh=d>>16
            dl=self.CA.changeByte(dl)
            dh=self.CA.changeByte(dh)
            dane=dane<<8+dh
            dane=dane<<8+dl
        '''

        functions={0x00: self.CA.assignActiveByBits,
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
                   0x7F: self.parse7FResponse, }

        dane=0
        for d in data[1:]:
            dane = dane<<8
            dane += self.CA.changeByte(d)

        try:
            if data[0] == 0x7F:
                self.parse7FResponse(data[1:])
            else:
                function = functions[data[0]]
                function(dane)
        except Exception as e:
            print('Error while calling function', data[0])
            print(e)

    def parse7FResponse(self, data):
        maska=0b1000000000000000000000000000000000000000
        dane=0
        zadanie=0
        for i in data[1:-1]:
            dane = (dane<<8)+self.CA.changeByte(i)
        for i in range(39):
            if dane&maska: self.zadania.append([zadanie, ])
            maska = maska>>1
            zadanie += 1

    def startConnection(self):
        self.sleep(self.time)

    def run(self):
        # Odczyt danych oraz ich interpretacja

        while(True):
            # self.zadania.insert(0, [0x7F])
            self.zadania.append([0x00, ])
            self.zadania.append([0x17, ])
            self.zadania.append([0x01, ])
            self.zadania.append([0x02, ])
            self.zadania.append([0x03, ])
            self.zadania.append([0x04, ])
            self.zadania.append([0x05, ])
            self.zadania.append([0x09, ])
            self.zadania.append([0x0A, ])
            self.zadania.append([0x0D, ])
            self.zadania.append([0x0E, ])
            self.zadania.append([0x0F, ])
            self.zadania.append([0x10, ])
            self.zadania.append([0x13, ])
            self.zadania.append([0x14, ])
            self.zadania.append([0x15, ])
            self.zadania.append([0x16, ])
            self.zadania.append([0x28, ])
            self.zadania.append([0x29, ])

            # Opening port for connection
            try:
                self.port.connect()
                # Writing and receiving new data from CA
                for z in self.zadania:
                    self.port.write(self.buildFrame(z))
                    dane=self.port.read()
                    if self.checkFrame(dane): self.parseData(dane[2:-4])
                # Closing port
                self.port.close_connection()
            except Exception as e:
                print('Connection trouble')
                print(e)

            # Clearing tasks
            self.zadania=[]

            sleep(0.5)