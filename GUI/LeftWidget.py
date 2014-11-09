'''
Created on 4 cze 2014

@author: codedigger
'''

from PyQt4 import QtGui

'''
Rodzic->bez pix
Dziecko->z pix
'''

class Item(QtGui.QTreeWidgetItem):
  def __init__(self, name, mapa=0):
    super(Item, self).__init__()
    self.name=name
    self.hMap=False
    #self.pix=QtGui.QPixmap()
    #if mapa: self.setMap(mapa)
    #else: self.mapa=0
    self.setMap(mapa)
    
    #if pix!="": self.setPix(pix)
    self.setName(name)
    #self.hasPixmap=False
  def setName(self, name): 
    self.setText(0, name)
    self.name=name
  '''def setPix(self, pix):
    #print("Dodawanie grafiki: "+pix)
    self.pix=QtGui.QPixmap(pix)
    self.hasPixmap=True
  def getPix(self): return self.pix
  def hasPix(self):
    if self.pix.height()==0: return False
    return True
    #return False'''
  def setMap(self, mapa):
    if mapa!=0:
      self.hMap=True
      self.mapa=mapa
  def getMap(self): return self.mapa
  def hasMap(self): return self.hMap

class LeftWidget(QtGui.QTreeWidget):
  def __init__(self):
    super(LeftWidget, self).__init__()
    self.setMaximumWidth(200)
    self.setMinimumWidth(100)
    self.setAnimated(True)
    self.setExpandsOnDoubleClick(False)

'''
class LeftW(QtGui.QDockWidget):
  def __init__(self):
    super(LeftW, self).__init__()
    self.lj=QtGui.QHBoxLayout()
    self.setLayout(self.lj)
    self.lj.addWidget(LeftWidget())'''

'''
  def addMenu(self, name):
    self.item=Item()
    self.item.setName(name)
    self.item.setText(0, name)
  def addItem(self, name, pix):
    self.item=Item()
    self.item.setName(name)
    self.item.setText(0, name)
    self.item.setPix(pix)
'''