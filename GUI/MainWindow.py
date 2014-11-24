# -*- coding: utf-8 -*-

###############################################################################
# MainWindow.py
#
# author: Paweł Surowiec (codedigger)
# creation date: ?
# version: 0.0.1
#
# Module contains main widgets. Running this module directly will run base
# system.
#
###############################################################################

MAINWINDOW_PY_VERSION=(0,0,1)

from PyQt4 import QtGui, QtCore
from GUI.CentralWidget import CentralWidget, Map
from Satel import integra, dataReader
from GUI.LoginWindow import LoginWindow
from GUI.UsersList import UsersList
from GUI.EventList import EventList
from GUI.SystemEditor import SystemEditor
from GUI.DlgUserPasswordChange import DlgUserPasswordChange
from GUI.MapEditor import MapEditor
from GUI.MapExplorer import MapExplorer
from statics import statics
from db import db


class MainWidget(QtGui.QWidget):
  def __init__(self):
    super(MainWidget, self).__init__()

    self.__ikona=QtGui.QIcon("../gfx/img/32WOG-logo.png")

    self.CAReader=dataReader.EthernetDataReader('192.168.0.10', 7094)
    self.CAParser=dataReader.DataParser()
    self.CA=integra.Integra128()
#     self.CAReader.connect()
    self.CAParser.assignPort(self.CAReader)
    self.CAParser.assignCA(self.CA)
    self.CAParser.start()
    self.CA.hasZonesAlarmChanged.connect(self.signalAlarm)

    vLayout=QtGui.QVBoxLayout()
    hLayout=QtGui.QHBoxLayout()

    self.centralWidget=CentralWidget()

    self.downLayout=QtGui.QHBoxLayout()

    self.downL=QtGui.QTextBrowser()
    self.downLFont=QtGui.QFont()
    self.downLFont.setPointSize(8)
    self.downL.setFont(self.downLFont)
    self.appendInfo("Początek zdarzeń")

    self.eventList=EventList()
#     self.eventList.itemDoubleClicked.connect(self.eventListDblClick)

    self.downLayout.addWidget(self.downL)
    self.downLayout.addWidget(self.eventList)

    self.down=QtGui.QWidget()
    self.down.setMinimumHeight(50)
    self.down.setMaximumHeight(100)
    self.down.setLayout(self.downLayout)

#     self.gornyPaleta=QtGui.QPalette(QtGui.QColor(255,20,20))
#     self.gorny=QtGui.QPushButton("Potwierdzanie zdarzeń")
#     self.gorny.setPalette(self.gornyPaleta)
#     self.gorny.setMaximumHeight(100)
#     self.gorny.setMinimumHeight(50)

    wc=QtGui.QWidget()

    hLayout.addWidget(self.centralWidget)

    wc.setLayout(hLayout)

    vLayout.addWidget(wc)
    vLayout.addWidget(self.down)

    self.setLayout(vLayout)

  def appendInfo(self, info): self.downL.append(info)

  def appendEvent(self, event):
    self.eventList.addItem(event)

  def signalAlarm(self):
    for i in self.CA.getZones():
      if i.getAlarm(): self.appendEvent("Alarm włamaniowy z strefy "+i.getName())

class MainWindow(QtGui.QMainWindow):
  def __init__(self, *args, **kwargs):
    QtGui.QMainWindow.__init__(self, *args, **kwargs)

    self.dbSession=statics.dbSession

    self.blueSkin=self.__createBlueSkin()
    self.redSkin=self.__createRedSkin()

    self.setPalette(self.blueSkin)

    self.menubar = self.menuBar()

    self.statusBar().showMessage("Gotowy")

    self.actionExit = QtGui.QAction("&Zakończ", self)
    self.actionExit.setShortcut("Ctrl+Q")
    self.actionExit.setStatusTip("Zakończ program")
    self.actionExit.triggered.connect(QtGui.qApp.quit)

    self.actionFullScreen=QtGui.QAction("Pełny ekran", self)
    self.actionFullScreen.setStatusTip("Przełącz na pełny ekran")
    self.actionFullScreen.setShortcut("Ctrl+F")
    self.actionFullScreen.triggered.connect(self.switchFullScreen)

    # Dialog allowing user change his password
    self.actionUserPasswordChange=QtGui.QAction('Zmień hasło', self)
    self.actionUserPasswordChange.triggered.connect(
      lambda: DlgUserPasswordChange().exec_())

    self.actionLegenda=QtGui.QAction("Pokaż legendę", self)
    self.actionLegenda.triggered.connect(self.showLegend)

    self.actionMapy=QtGui.QAction("Pokaż mapy", self)
    self.actionMapy.setShortcut("Ctrl+W")
    self.actionMapy.triggered.connect(
      lambda: self.mapExplorerDock.show() )

    self.actionUsersList=QtGui.QAction('Lista użytkowników', self)
    self.actionUsersList.triggered.connect(
      lambda: self.userDock.show() or\
              self.userDock.loadData() ) #self.showUsersList)

    # Dialog allowing adding, deleting and modifying integrated systems
    self.actionSystemList=QtGui.QAction('Lista systemów', self)
    self.actionSystemList.triggered.connect(
      lambda: SystemEditor().exec_() )

    # Action allowing adding, deleting and modifying system maps
    self.actionMapEditor=QtGui.QAction('Edytor map', self)
    self.actionMapEditor.triggered.connect(
      lambda: self.mainWidget.centralWidget.addTab(MapEditor(), 'Edytor map'))

    fileMenu=self.menubar.addMenu("&Plik")
    fileMenu.addAction(self.actionExit)

    windowMenu=self.menubar.addMenu("Ekran")
    windowMenu.addAction(self.actionFullScreen)

    toolsMenu=self.menubar.addMenu("Narzędzia")
    toolsMenu.addAction(self.actionLegenda)
    toolsMenu.addAction(self.actionMapy)
    toolsMenu.addAction(self.actionUserPasswordChange)

    # don't nedd now. But in future?
#     toolsServiceMenu=toolsMenu.addMenu("Serwis")

    adminMenu=self.menubar.addMenu('Administracja')
    adminMenu.addAction(self.actionUsersList)
    adminMenu.addAction(self.actionSystemList)
    adminMenu.addAction(self.actionMapEditor)

    self.mainWidget=MainWidget()
    self.setCentralWidget(self.mainWidget)

    self.userDock=UsersList()
    self.addDockWidget(QtCore.Qt.NoDockWidgetArea, self.userDock)
    self.userDock.setParent(self)
    self.userDock.close()

    self.mapExplorerDock=MapExplorer()
    self.addDockWidget(QtCore.Qt.NoDockWidgetArea, self.mapExplorerDock)
    self.mapExplorerDock.setParent(self)
    self.mapExplorerDock.close()
    self.mapExplorerDock.lstMaps.doubleClicked.connect(self.mapExplorerDblClicked)

    # Automatic skin changing
    self.mainWidget.eventList.signal_emptyList.connect(
      lambda: self.setPalette(self.blueSkin))
    self.mainWidget.eventList.signal_notEmptyList.connect(
      lambda: self.setPalette(self.redSkin))

    # All detectors, zones, etc
    # This is little crazy thing: here are connection betwen database ex.
    # detectors and real detectors from systems
    self.allSystems={}
    self.allDetectors={}
    self.allOuts={}
    self.allZones={}

    # Reading all Integra systems from database
    integraSystems=self.dbSession.query(db.Integra).all()
    for integraSystem in integraSystems:
      # creating system
      CA=integra.Integra(name=integraSystem.name,
                         detectorsNumber=0,
                         outsNumber=0,
                         zonesNumber=0)

      # add detectors from database to system
      for dbDetector in integraSystem.detectors:
        detector=integra.Detector(dbDetector.name)
        CA.addDetector(detector)

        # adding key dbDetector <-> systemDetector
        self.allDetectors[dbDetector]=detector

      # add outs from database to system
      for dbOut in integraSystem.outs:
        out=integra.Out(dbOut.name)
        CA.addOut(out)

        # adding key dbOut <-> systemOut
        self.allOuts[dbOut]=out

      # add zones from database to system
      for dbZone in integraSystem.zones:
        zone=integra.Zone(dbZone.name)
        CA.addZone(zone)

        # adding key dbZone <-> systemOut
        self.allZones[dbZone]=zone

      CAReader=dataReader.EthernetDataReader(integraSystem.IP,
                                             int(integraSystem.port))
      CAParser=dataReader.DataParser()
      CAParser.assignPort(CAReader)
      CAParser.assignCA(CA)
#       CAParser.start()

      self.allSystems[integraSystem]=CA

#     self.mainWidget.eventList.appendEvent(Event(alarmType=EventType.Panic,
#                                       zone='Strefa testowa'))

  def __createBlueSkin(self):
    palette = QtGui.QPalette()
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
    brush = QtGui.QBrush(QtGui.QColor(68, 69, 104))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
    brush = QtGui.QBrush(QtGui.QColor(102, 103, 156))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
    brush = QtGui.QBrush(QtGui.QColor(85, 86, 130))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
    brush = QtGui.QBrush(QtGui.QColor(34, 34, 52))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
    brush = QtGui.QBrush(QtGui.QColor(45, 46, 69))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(68, 69, 104))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
    brush = QtGui.QBrush(QtGui.QColor(34, 34, 52))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
    brush = QtGui.QBrush(QtGui.QColor(68, 69, 104))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
    brush = QtGui.QBrush(QtGui.QColor(102, 103, 156))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
    brush = QtGui.QBrush(QtGui.QColor(85, 86, 130))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
    brush = QtGui.QBrush(QtGui.QColor(34, 34, 52))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
    brush = QtGui.QBrush(QtGui.QColor(45, 46, 69))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(68, 69, 104))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
    brush = QtGui.QBrush(QtGui.QColor(34, 34, 52))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
    brush = QtGui.QBrush(QtGui.QColor(34, 34, 52))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
    brush = QtGui.QBrush(QtGui.QColor(68, 69, 104))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
    brush = QtGui.QBrush(QtGui.QColor(102, 103, 156))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
    brush = QtGui.QBrush(QtGui.QColor(85, 86, 130))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
    brush = QtGui.QBrush(QtGui.QColor(34, 34, 52))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
    brush = QtGui.QBrush(QtGui.QColor(45, 46, 69))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
    brush = QtGui.QBrush(QtGui.QColor(34, 34, 52))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
    brush = QtGui.QBrush(QtGui.QColor(34, 34, 52))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
    brush = QtGui.QBrush(QtGui.QColor(68, 69, 104))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(68, 69, 104))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
    brush = QtGui.QBrush(QtGui.QColor(68, 69, 104))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
    return palette

  def __createRedSkin(self):
    palette = QtGui.QPalette()
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
    brush = QtGui.QBrush(QtGui.QColor(112, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
    brush = QtGui.QBrush(QtGui.QColor(168, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
    brush = QtGui.QBrush(QtGui.QColor(140, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
    brush = QtGui.QBrush(QtGui.QColor(56, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
    brush = QtGui.QBrush(QtGui.QColor(74, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(112, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
    brush = QtGui.QBrush(QtGui.QColor(56, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
    brush = QtGui.QBrush(QtGui.QColor(112, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
    brush = QtGui.QBrush(QtGui.QColor(168, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
    brush = QtGui.QBrush(QtGui.QColor(140, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
    brush = QtGui.QBrush(QtGui.QColor(56, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
    brush = QtGui.QBrush(QtGui.QColor(74, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(112, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
    brush = QtGui.QBrush(QtGui.QColor(56, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
    brush = QtGui.QBrush(QtGui.QColor(56, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
    brush = QtGui.QBrush(QtGui.QColor(112, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
    brush = QtGui.QBrush(QtGui.QColor(168, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
    brush = QtGui.QBrush(QtGui.QColor(140, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
    brush = QtGui.QBrush(QtGui.QColor(56, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
    brush = QtGui.QBrush(QtGui.QColor(74, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
    brush = QtGui.QBrush(QtGui.QColor(56, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
    brush = QtGui.QBrush(QtGui.QColor(56, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
    brush = QtGui.QBrush(QtGui.QColor(112, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
    brush = QtGui.QBrush(QtGui.QColor(112, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
    brush = QtGui.QBrush(QtGui.QColor(112, 0, 1))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
    brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
    brush.setStyle(QtCore.Qt.SolidPattern)
    palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
    return palette


  def switchFullScreen(self):
    if self.isFullScreen(): self.showNormal()
    else: self.showFullScreen()

  def mapExplorerDblClicked(self, event):
    dbMap=self.mapExplorerDock.lstMaps.currentItem().data(0, QtCore.Qt.UserRole)

    self.mainWidget.appendInfo('>>> Wstawianie mapy '+dbMap.name)

    pixmapData=QtCore.QByteArray().fromRawData(dbMap.graphic)
    pixmap=QtGui.QPixmap()
    pixmap.loadFromData(pixmapData, format='PNG')

    gfxMap=Map(pixmap)
    self.mainWidget.centralWidget.addTab(gfxMap, dbMap.name)
    self.mainWidget.centralWidget.setCurrentIndex(self.mainWidget.centralWidget.count()-1)

    for detector in dbMap.detectors:
      gfxMap.addDetector(self.allDetectors[detector.detector],
                         QtCore.QPoint(detector.pointX/1000*gfxMap.width(),
                                       detector.pointY/1000*gfxMap.height()))

    for out in dbMap.outs:
      gfxMap.addOut(self.allOuts[out.out],
                    QtCore.QPoint(out.pointX/1000*gfxMap.width(),
                                  out.pointY/1000*gfxMap.height()))

    for zone in dbMap.zones:
      zonePoints={}
      for zonePoint in zone.points:
        zonePoints[zonePoint.pointNumber]=QtCore.QPoint(zonePoint.pointX/1000*gfxMap.width(),
                                                        zonePoint.pointY/1000*gfxMap.height())
      zonePoints_=[]
      for z in zonePoints: zonePoints_.append(zonePoints[z])
      gfxMap.addZone(self.allZones[zone.zone], zonePoints_)

  def showLegend(self):
    self.legendCA=integra.Integra()
    self.d1=self.legendCA.getDetector(2)
    self.d1.setActive()
    self.d2=self.legendCA.getDetector(3)
    self.d2.setAlarm()
    self.d3=self.legendCA.getDetector(4)
    self.d3.setAlarmMemory()
    self.d4=self.legendCA.getDetector(5)
    self.d4.setTamper()
    self.d5=self.legendCA.getDetector(6)
    self.d5.setTamperMemory()
    self.z1=self.legendCA.getZone(2)
    self.z1.setArmed()
    self.z2=self.legendCA.getZone(3)
    self.z2.setCode1()
    self.z3=self.legendCA.getZone(4)
    self.z3.setEntryTime()
    self.z4=self.legendCA.getZone(5)
    self.z4.setExitTime()
    self.z5=self.legendCA.getZone(6)
    self.z5.setAlarm()
    self.z6=self.legendCA.getZone(7)
    self.z6.setAlarmMemory()
    self.o1=self.legendCA.getOut(2)
    self.o1.setActive()
    self.mapa=Map(QtGui.QPixmap("../gfx/img/legenda.png"))
    self.mapa.addDetector(self.legendCA.getDetector(1), QtCore.QPoint(140,100))
    self.mapa.addDetector(self.d1, QtCore.QPoint(140,121))
    self.mapa.addDetector(self.d2, QtCore.QPoint(140,142))
    self.mapa.addDetector(self.d3, QtCore.QPoint(140,163))
    self.mapa.addDetector(self.d4, QtCore.QPoint(140,184))
    self.mapa.addDetector(self.d5, QtCore.QPoint(140,205))
    self.mapa.addZone(self.legendCA.getZone(1), [QtCore.QPoint(110,238),
                                                 QtCore.QPoint(140,238),
                                                 QtCore.QPoint(140,248),
                                                 QtCore.QPoint(110,248)])
    self.mapa.addZone(self.z1, [QtCore.QPoint(110,259),
                                QtCore.QPoint(140,259),
                                QtCore.QPoint(140,269),
                                QtCore.QPoint(110,269)])
    self.mapa.addZone(self.z2, [QtCore.QPoint(110,280),
                                QtCore.QPoint(140,280),
                                QtCore.QPoint(140,290),
                                QtCore.QPoint(110,290)])
    self.mapa.addZone(self.z3, [QtCore.QPoint(110,301),
                                QtCore.QPoint(140,301),
                                QtCore.QPoint(140,311),
                                QtCore.QPoint(110,311)])
    self.mapa.addZone(self.z4, [QtCore.QPoint(110,322),
                                QtCore.QPoint(140,322),
                                QtCore.QPoint(140,332),
                                QtCore.QPoint(110,332)])
    self.mapa.addZone(self.z5, [QtCore.QPoint(110,343),
                                QtCore.QPoint(140,343),
                                QtCore.QPoint(140,353),
                                QtCore.QPoint(110,353)])
    self.mapa.addZone(self.z6, [QtCore.QPoint(110,364),
                                QtCore.QPoint(140,364),
                                QtCore.QPoint(140,374),
                                QtCore.QPoint(110,374)])
    self.mapa.addOut(self.legendCA.getOut(1), QtCore.QPoint(135,405))
    self.mapa.addOut(self.o1, QtCore.QPoint(135,426))
    self.mainWidget.centralWidget.addTab(self.mapa, "Legenda")

if __name__ == '__main__':
  import sys

  app = QtGui.QApplication(sys.argv)

#TODO: done in some lazy way. Try to reconstruct this
  loginCounts=0
  while loginCounts<3:
    ret=LoginWindow().exec_()
    if ret==1:
      wMain=MainWindow()
      wMain.showFullScreen()
      wMain.setWindowTitle("Tablica synoptyczna")
      #w.setWindowFlags(w.windowFlags()&~QtCore.Qt.WindowStaysOnTopHint)
      wMain.show()
      break
    elif ret==2: loginCounts+=1
    else: loginCounts=3
  if loginCounts>2: sys.exit(0)

  sys.exit(app.exec_())