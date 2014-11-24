# -*- coding: utf-8 -*-

###############################################################################
# MapExplorer.py
#
# author: Paweł Surowiec (codedigger)
# creation date: 23.11.2014
# version: 0.0.1
#
# Module contains MapExplorer panel. It is little DockWidget with list of maps
# created in system.
#
###############################################################################
from PyQt4 import QtGui, QtCore
from QtD.MapExplorer import Ui_MapExplorer
from statics import statics
from db import db

class Item(QtGui.QTreeWidgetItem):
  def __init__(self, name, mapa=0):
    super(Item, self).__init__()
    self.name=name
    self.hMap=False
    self.setMap(mapa)
    self.setName(name)

  def setName(self, name):
    self.setText(0, name)
    self.name=name

  def setMap(self, mapa):
    if mapa!=0:
      self.hMap=True
      self.mapa=mapa

  def getMap(self): return self.mapa
  def hasMap(self): return self.hMap

class MapExplorer(Ui_MapExplorer, QtGui.QDockWidget):
  """Show list of maps created in system"""

  def __init__(self):
    super(MapExplorer, self).__init__()
    self.setupUi(self)

    self.dbSession=statics.dbSession

    self.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)

    self.btnRefresh.clicked.connect(self.refreshMapList)
    self.refreshMapList()

  def refreshMapList(self):
    mapList=self.dbSession.query(db.Map).all()
    self.lstMaps.clear()
    for map_ in mapList:
      mapItem=QtGui.QTreeWidgetItem()
      mapItem.setText(0, map_.name)
      mapItem.setData(0, QtCore.Qt.UserRole, map_)
      self.lstMaps.addTopLevelItem(mapItem)