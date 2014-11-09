'''
Created on 4 cze 2014

@author: codedigger
'''

from PyQt4 import QtGui, QtCore
import random
from Satel import integra
from time import sleep

#TODO: zamiast QLabale, ścieżka do obrazka oraz zastosowanie drawImage lub DrawPicture
class Map(QtGui.QLabel):
  def __init__(self, pixmap):
    '''
    pixmap: podkłąd graficzny QtGui.QPixmap()
    '''
    super(Map, self).__init__()
    self.setScaledContents(True)
    self.setPixmap(pixmap.scaled(self.width(), self.width(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation))
    self.detectors=[]
    self.zones=[]
    self.outs=[]
    self.statusbar=None
    self.pixmap=pixmap

  def addDetector(self, detector, point):
    self.detectors.append([detector, point])
    self.detectors[-1][0].hasChanged.connect(self.update)
  def addZone(self, zone, point):
    self.zones.append([zone, point])
    self.zones[-1][0].hasChanged.connect(self.update)
  def addOut(self, out, point):
    self.outs.append([out, point])
    self.outs[-1][0].hasChanged.connect(self.update)

  def paintEvent(self, e):
    super(Map, self).paintEvent(e)
    qp = QtGui.QPainter()
    qp.begin(self)
    self.drawElements(qp)
    qp.end()

  def mouseMoveEvent(self, e):
    if self.statusbar!=None: self.statusbar.showMessage("Pozycja kursora: "+str(e.x())+", "+str(e.y()))

  def mouseMoveEventCon(self, statusbar):
    self.statusbar=statusbar

  def drawElements(self, qp):
    qp.setRenderHint(QtGui.QPainter.Antialiasing)
    qp.setPen(QtCore.Qt.black)
    qp.setBrush(QtCore.Qt.Dense5Pattern)
    for detector, point in self.detectors:
      qp.setBrush(QtCore.Qt.gray)
      # Kolejność pokazywania stanu czuki:
      # Alarm > Tamper > TamperMemory > AlarmMemory > Active
      if detector.getAlarm(): qp.setBrush(QtCore.Qt.red)
      elif detector.getTamper(): qp.setBrush(QtCore.Qt.yellow)
      elif detector.getTamperMemory(): qp.setBrush(QtCore.Qt.darkYellow)
      elif detector.getAlarmMemory(): qp.setBrush(QtCore.Qt.darkRed)
      elif detector.getActive(): qp.setBrush(QtCore.Qt.green)
      qp.drawEllipse(point, 5, 5)
    for out, point in self.outs:
      qp.setBrush(QtCore.Qt.gray)
      # Kolejność pokazywania stanu czuki:
      # Alarm > Tamper > TamperMemory > AlarmMemory > Active
      if out.getActive():
        qp.setBrush(QtCore.Qt.red)
      qp.drawRect(point.x(), point.y(), 10, 10)

    for zone, points in self.zones:
      polygon=QtGui.QPolygon()
      for i in points: polygon.append(i)
      brush=QtGui.QBrush(QtCore.Qt.SolidPattern)
      brush.setColor(QtGui.QColor(160,160,164,100))
      if zone.getAlarm(): brush.setColor(QtGui.QColor(255,0,0,180))
      elif zone.getArmed(): brush.setColor(QtGui.QColor(0,255,0,100))
      elif zone.getCode1(): brush.setColor(QtGui.QColor(50,200,0,100))
      elif zone.getEntryTime(): brush.setColor(QtGui.QColor(100,200,0,100))
      elif zone.getExitTime(): brush.setColor(QtGui.QColor(160,255,164,100))
      elif zone.getAlarmMemory(): brush.setColor(QtGui.QColor(255,50,50,100))
      qp.setBrush(brush)
      qp.drawPolygon(polygon)

class CentralWidget(QtGui.QTabWidget):
  def __init__(self):
    super(CentralWidget, self).__init__()
    self.setTabsClosable(True)
    self.setMovable(True)
    self.tabCloseRequested.connect(self.closeTab)
    self.tabs=[]
    
    #self.CA.hasZonesChanged.connect(self.signalAlarm)
  """def addPix(self, name, pixmap):
    #Dodanie nowej zakładki wraz z podkładem
    mapa=Map(pixmap)
    mapa.setGeometry(self.geometry())
    '''for i in range(1, 128):
      mapa.addDetector(self.CA.getDetector(i), QtCore.QPoint(10+10*i,10))
      '''#mapa.addDetector(self.CA.getDetector(5), QtCore.QPoint(50, 50))
    self.tabs.append(mapa)
    self.addTab(mapa, name)"""
  def closeTab(self, index):
    #if self.count()>1: self.removeTab(index)
    self.removeTab(index)