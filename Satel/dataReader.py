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
  def read(self): raise NameError('Niezdefiniowana metoda "read"')
  def write(self, data): raise NameError('Niezdefiniowana metoda "write"')
  def connect(self): raise NameError('Niezdefiniowana metoda "connect"')

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
        print('<< '+str(dane))
        return dane
      except:
        return bytearray()

  def write(self, data):
#     data=bytearray()
#     data.extend([0xFE, 0xFE, 0x09, 0xD7, 0xEB, 0xFE, 0x0D])
    if self.socket is not None:
#       try:
        print('>> '+str(data))
        self.socket.send(data)
#       except:
#         print('Wysyłanie nieudane')
#         pass

  def connect(self):
    proto=socket.getprotobyname('tcp')
    self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)
    try:
      self.socket.connect((self.ipAdress, self.port))
    except:
      print(socket)

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

  def setTime(self, time): self.time=time

  def assignCA(self, CA): self.CA=CA
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
    #TODO: zmiana FE F0 na FE, też trochę po chamsku - można to wstawić przy odczycie
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
      dane=dane<<8
      dane+=d

    try:
      functions[data[0]](dane)
    except: pass

#
#
#     # 00 - naruszenie wejść
#     if data[0]==0x00:
#       dane=0
#       for d in data[1:]:
#         dane=dane<<8
# #         dane+=self.CA.changeByte(d)
#         dane+=d
#       self.CA.assignActiveByBits(dane)
#
#     # 01: tamper wejść
#     elif data[0]==0x01:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignTamperByBits(dane)
#
#     # 02: alarm wejść
#     elif data[0]==0x02:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignAlarmByBits(dane)
#
#     # 03: tamper alarm
#     elif data[0]==0x03:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignTamperByBits(dane)
#
#     # 04: pamięć alarmu wejścia
#     elif data[0]==0x04:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignAlarmMemoryByBits(dane)
#
#
#     # 05: tamper memory alarm
#     elif data[0]==0x05:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignTamperMemoryByBits(dane)
#
#     # 06: obejście strefy
#     elif data[0]==0x06:
#       pass
#
#     # 07: brak naruszenia trefy
#     elif data[0]==0x07:
#       pass
#
#     # 08: zbyt długie naruszenie
#     elif data[0]==0x08:
#       pass
#
#     # 09: uzbrojenie strefy (supresed)
#     elif data[0]==0x09:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignZoneArmedByBits(dane)
#
#     # 0A: uzbrojenie strefy
#     elif data[0]==0x0A:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignZoneArmedByBits(dane)
#
#     # 0B: uzbrojenie strefy mode 2
#     elif data[0]==0x0B:
#       pass
#
#     # 0C: uzbrojenie strefy mode 3
#     elif data[0]==0x0C:
#       pass
#
#     # 0D: podanie pierszego hasła
#     elif data[0]==0x0D:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignZoneCode1ByBits(dane)
#
#     # 0E: czas na wejście
#     elif data[0]==0x0E:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignZoneEntryTimeByBits(dane)
#
#     # 0F: czas na wyjście pow. 10s
#     elif data[0]==0x0F:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignZoneExitTimeByBits(dane)
#
#     # 10: czas na wyjście poniżej 10s
#     elif data[0]==0x10:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignZoneExitTimeByBits(dane)
#
#     # 11: strefa zablokowana
#     elif data[0]==0x11:
#       pass
#
#     # 12: strefa zablokowana dla strażnika
#     elif data[0]==0x12:
#       pass
#
#     # 13: alarm strefy
#     elif data[0]==0x13:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignZoneAlarmByBits(dane)
#
#     # 14: alarm p.poż
#     elif data[0]==0x14:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignZoneFireAlarmByBits(dane)
#
#     # 15: pamięc alarmu
#     elif data[0]==0x15:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignZoneAlarmMemoryByBits(dane)
#
#     # 16: pamięć alarmu p.poż
#     elif data[0]==0x16:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignZoneFireAlarmMemoryByBits(dane)
#
#     # 17: stan wyjść
#     elif data[0]==0x17:
#       dane=0
#       for d in data[1:]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignOutsByBits(dane)
#
#     # 18: otwarcie drzwi
#     elif data[0]==0x18:
#       pass
#
#     # 19: zbyt długo otwarte drzwi
#     elif data[0]==0x19:
#       pass
#
#     # 1A: RTC oraz status
#     elif data[0]==0x1A:
#       pass
#
#     # 1B: awarie cz.1
#     elif data[0]==0x1B:
#       pass
#
#     # 1C: awarie cz.2
#     elif data[0]==0x1C:
#       pass
#
#     # 1D: awarie cz.3
#     elif data[0]==0x1D:
#       pass
#
#     # 1E: awarie cz.4
#     elif data[0]==0x1E:
#       pass
#
#     # 1F: awarie cz.5
#     elif data[0]==0x1F:
#       pass
#
#     # 20: pamięć awarii cz.1
#     elif data[0]==0x20:
#       pass
#
#     # 21: pamięć awarii cz.2
#     elif data[0]==0x21:
#       pass
#
#     # 22: pamięć awarii cz.3
#     elif data[0]==0x22:
#       pass
#
#     # 23: pamięć awarii cz.4
#     elif data[0]==0x23:
#       pass
#
#     # 24: pamięć awarii cz.5:
#     elif data[0]==0x24:
#       pass
#
#     # 25: strefy z naruszonym wejściem
#     elif data[0]==0x25:
#       pass
#
#     # 26: wejście wyizolowane (?)
#     elif data[0]==0x26:
#       pass
#
#     # 27: strefy z weryfikowanym alarmem
#     elif data[0]==0x27:
#       pass
#
#     # 28: wejśćie zamaskowane
#     elif data[0]==0x28:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignTamperByBits(dane)
#
#     # 29: pamięć zamaskowanych wejść
#     elif data[0]==0x29:
#       dane=0
#       for d in data[1:-1]:
#         dane=dane<<8
#         dane+=self.CA.changeByte(d)
#       self.CA.assignTamperMemoryByBits(dane)
#
#     # 2A: strefa uzbrojona mode 1
#     elif data[0]==0x2A:
#       pass
#
#     # 2B: strefy z ostrzeżeniami
#     elif data[0]==0x2B:
#       pass
#
#     # 2C: awarie cz.6
#     elif data[0]==0x2C:
#       pass
#
#     # 2D: awarie cz.7
#     elif data[0]==0x2D:
#       pass
#
#     # 2E: pamięć awarii cz.6
#     elif data[0]==0x2E:
#       pass
#
#     # 2F: pamięć awarii cz.7
#     elif data[0]==0x2F:
#       pass
#
#     # 7C: wersja modułów INT-RS oraz ETHM
#     elif data[0]==0x7C:
#       pass
#
#     # 7D: temperatura stref
#     elif data[0]==0x7D:
#       pass
#
#     # 7E: wersja centrali
#     elif data[0]==0x7E:
#       pass
#
#     # 7F: pobranie zmian
#     elif data[0]==0x7F:
#       maska=0b1000000000000000000000000000000000000000
#       dane=0
#       zadanie=0
#       for i in data[1:-1]: dane=(dane<<8)+self.CA.changeByte(i)
#       for i in range(39):
# #         if dane&maska: self.zadania.append([zadanie])
#         maska=maska>>1
#         zadanie+=1
#       pass
#
#     # nieudokumentowana odpowiedź
#     else: pass

  def parse7FResponse(self, data):
    maska=0b1000000000000000000000000000000000000000
    dane=0
    zadanie=0
    for i in data[1:-1]: dane=(dane<<8)+self.CA.changeByte(i)
    for i in range(39):
      if dane&maska: self.zadania.append([zadanie, ])
      maska=maska>>1
      zadanie+=1

  def startConnection(self):
    self.sleep(self.time)

  def run(self):
    # Odczyt zmian w CA
    '''
    dane=[]
    self.port.write(self.buildFrame(0x7F))
    while self.checkFrame(dane)==False:
      i=self.port.read()
      if len(dane)>1:
        if (i==0xF0)&(dane[-1]==0xFE): pass
        elif (i==0xFE)&(dane[-1]==0xFE): dane=[0xFE, 0xFE]
        #elif (i==0x0D)&&(dane[-1]==0xFE): pass
      else: dane.append(i)
    self.parseData(dane)
    '''

    # Odczyt danych oraz ich interpretacja
    # to jest w wątku, ciekawe, jak się zachowa, kiedy dane (self.zadania) zmieną
    # się poza wątkiem :)
    while(True):
      self.zadania.insert(0, [0x7F])
      self.zadania.append([0x00])
      self.zadania.append([0x17])
      for z in self.zadania:
        self.port.write(self.buildFrame(z))
        dane=self.port.read()
        if self.checkFrame(dane): self.parseData(dane[2:-4])

  #       while self.checkFrame(dane)==False:
  #         i=self.port.read()
  #         if len(dane)>1:
  #           if (i==0xF0)&(dane[-1]==0xFE): pass
  #           elif (i==0xFE)&(dane[-1]==0xFE): dane=[0xFE, 0xFE]
  #         #elif (i==0x0D)&&(dane[-1]==0xFE): pass
  #         else: dane.append(i)
  #       self.parseData(dane)
  #       dane=[]
      self.zadania=[]
      sleep(0.5)