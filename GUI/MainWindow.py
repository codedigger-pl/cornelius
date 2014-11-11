# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from GUI.CentralWidget import CentralWidget, Map
from GUI.LeftWidget import LeftWidget, Item
from Satel import integra, dataReader
from GUI.LoginWindow import LoginWindow
from GUI.UsersList import UsersList
from GUI.Event import Event, EventType
from GUI.EventList import EventList
from GUI.SystemEditor import SystemEditor
from GUI.DlgUserPasswordChange import DlgUserPasswordChange
from GUI.MapEditor import MapEditor


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

    self.centralny=CentralWidget()
    self.lewyDock=QtGui.QDockWidget()
    self.lewyDock.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
    self.lewy=LeftWidget()
    self.lewyDock.setWidget(self.lewy)

#     self.userDock=QtGui.QDockWidget()
#     self.userDock.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
#     self.userDockContent=Ui_UsersList()
#     self.userDockContent.setupUi(self.userDock)

    #Tworzenie mapek dla tablicy synoptycznej
    self.lewyK836Map=Map(QtGui.QPixmap("../gfx/img/32WOG-logo.png"))
    for i in range(128):
      self.lewyK836Map.addDetector(self.CA.getDetector(i), QtCore.QPoint(10+10*i, 10))
      self.lewyK836Map.addOut(self.CA.getOut(i), QtCore.QPoint(5+10*i, 20))
    self.lewyK836Map.addZone(self.CA.getZone(0), [QtCore.QPoint(200,200),
                                                  QtCore.QPoint(200,400),
                                                  QtCore.QPoint(400,200)])

    self.lewyAll=Item("Wszystkie obiekty")
    self.lewyAll.setIcon(0, self.__ikona)
    self.lewy.addTopLevelItem(self.lewyAll)
    self.lewy.addTopLevelItem(Item(""))

    self.lewyK836=Item("K-836",self.lewyK836Map)
    self.lewyK836.setIcon(0, self.__ikona)
    self.lewyK836_B27=Item("Budynek 27")
    self.lewyK836_B27_Kasa=Item("Kasa")
    self.lewyK836_B27_ZKMRJ=Item("ZKMRJ")
    self.lewyK836_B27_KT=Item("Kanc. JW3391")
    self.lewyK836_B27_WL=Item("Węzeł Łączności")
    self.lewyK836_B27.addChild(self.lewyK836_B27_Kasa)
    self.lewyK836_B27.addChild(self.lewyK836_B27_KT)
    self.lewyK836_B27.addChild(self.lewyK836_B27_ZKMRJ)
    self.lewyK836_B27.addChild(self.lewyK836_B27_WL)
    self.lewyK836.addChild(self.lewyK836_B27)
    self.lewyK836_B74=Item("Budynek 74")
    self.lewyK836_B74_KT=Item("Kanc. JW5371")
    self.lewyK836_B74.addChild(self.lewyK836_B74_KT)
    self.lewyK836.addChild(self.lewyK836_B74)
    self.lewyK836_B105=Item("Budynek 105")
    self.lewyK836_B105_parter=Item("Parter")
    self.lewyK836_B105_1p=Item("1 piętro")
    self.lewyK836_B105_2p=Item("2 piętro")
    self.lewyK836_B105_3p=Item("3 piętro")
    self.lewyK836_B105.addChild(self.lewyK836_B105_parter)
    self.lewyK836_B105.addChild(self.lewyK836_B105_1p)
    self.lewyK836_B105.addChild(self.lewyK836_B105_2p)
    self.lewyK836_B105.addChild(self.lewyK836_B105_3p)
    self.lewyK836.addChild(self.lewyK836_B105)
    self.lewyK836_B108=Item("Budynek 108")
    self.lewyK836_B108_parter=Item("Parter")
    self.lewyK836_B108_1p=Item("1 piętro")
    self.lewyK836_B108_2p=Item("2 piętro")
    self.lewyK836_B108_3p=Item("3 piętro")
    self.lewyK836_B108.addChild(self.lewyK836_B108_parter)
    self.lewyK836_B108.addChild(self.lewyK836_B108_1p)
    self.lewyK836_B108.addChild(self.lewyK836_B108_2p)
    self.lewyK836_B108.addChild(self.lewyK836_B108_3p)
    self.lewyK836.addChild(self.lewyK836_B108)
    self.lewy.addTopLevelItem(self.lewyK836)

    self.lewyK845=Item("K-845")
    self.lewyK845_B3=Item("Budynek 3")
    self.lewyK845_B4=Item("Budynek 4")
    self.lewyK845_B5=Item("Budynek 5")
    self.lewyK845.addChild(self.lewyK845_B3)
    self.lewyK845.addChild(self.lewyK845_B4)
    self.lewyK845.addChild(self.lewyK845_B5)
    self.lewy.addTopLevelItem(self.lewyK845)

    self.lewy.expandAll()

    #Dodawanie obsługi dwukliku
    self.lewy.itemDoubleClicked.connect(self.lewyClicked)

    # TODO: Autoscrolling - niby działa.
    self.dolnyLayout=QtGui.QHBoxLayout()

    self.dolnyL=QtGui.QTextBrowser()
    self.dolnyLFont=QtGui.QFont()
    self.dolnyLFont.setPointSize(8)
    self.dolnyL.setFont(self.dolnyLFont)
    self.appendInfo("Początek zdarzeń")

    self.eventList=EventList()
#     self.eventList.itemDoubleClicked.connect(self.eventListDblClick)

    self.dolnyLayout.addWidget(self.dolnyL)
    self.dolnyLayout.addWidget(self.eventList)

    self.dolny=QtGui.QWidget()
    self.dolny.setMinimumHeight(50)
    self.dolny.setMaximumHeight(100)
    self.dolny.setLayout(self.dolnyLayout)

    self.gornyPaleta=QtGui.QPalette(QtGui.QColor(255,20,20))
    self.gorny=QtGui.QPushButton("Potwierdzanie zdarzeń")
    self.gorny.setPalette(self.gornyPaleta)
    self.gorny.setMaximumHeight(100)
    self.gorny.setMinimumHeight(50)

    wc=QtGui.QWidget()

    hLayout.addWidget(self.centralny)

    wc.setLayout(hLayout)

    vLayout.addWidget(wc)
    vLayout.addWidget(self.dolny)

    self.setLayout(vLayout)

  def lewyClicked(self, item, index):
    if item.hasMap():
      self.appendInfo(">>> Wstawianie mapy "+item.name)
      self.centralny.addTab(item.getMap(), item.name)
      self.centralny.setCurrentIndex(self.centralny.count()-1)

  def appendInfo(self, info): self.dolnyL.append(info)

  def appendEvent(self, event):
    self.eventList.addItem(event)

  def signalAlarm(self):
    for i in self.CA.getZones():
      if i.getAlarm(): self.appendEvent("Alarm włamaniowy z strefy "+i.getName())

class MainWindow(QtGui.QMainWindow):
  def __init__(self, *args, **kwargs):
    QtGui.QMainWindow.__init__(self, *args, **kwargs)

    self.blueSkin=self.__createBlueSkin()
    self.redSkin=self.__createRedSkin()

    self.setPalette(self.blueSkin)

    self.menubar = self.menuBar()
    self.isPokazPozycjeKursora=False

    self.statusBar().showMessage("Gotowy")

    self.actionExit = QtGui.QAction("&Zakończ", self)
    self.actionExit.setShortcut("Ctrl+Q")
    self.actionExit.setStatusTip("Zakończ program")
    self.actionExit.triggered.connect(QtGui.qApp.quit)

    self.actionFullScreen=QtGui.QAction("Pełny ekran", self)
    self.actionFullScreen.setStatusTip("Przełącz na pełny ekran")
    self.actionFullScreen.setShortcut("Ctrl+F")
    self.actionFullScreen.triggered.connect(self.switchFullScreen)

    self.actionPozycjaKursora=QtGui.QAction("Pokaż pozycję kursora", self)
    self.actionPozycjaKursora.setStatusTip("Pokaż pozycję kursora")
    self.actionPozycjaKursora.setShortcut("Ctrl+Shift+G")
    self.actionPozycjaKursora.setCheckable(True)
    self.actionPozycjaKursora.triggered.connect(self.pozycjaKursoraCon)

    # Dialog allowing user change his password
    self.actionUserPasswordChange=QtGui.QAction('Zmień hasło', self)
    self.actionUserPasswordChange.triggered.connect(
      lambda: DlgUserPasswordChange().exec_())

    self.actionLegenda=QtGui.QAction("Pokaż legendę", self)
    self.actionLegenda.triggered.connect(self.showLegend)

    self.actionMapy=QtGui.QAction("Pokaż mapy", self)
    self.actionMapy.setShortcut("Ctrl+W")
    self.actionMapy.triggered.connect(self.showMaps)

    self.actionUsersList=QtGui.QAction('Lista użytkowników', self)
    self.actionUsersList.triggered.connect(self.showUsersList)

    # Dialog allowing adding, deleting and modifying integrated systems
    self.actionSystemList=QtGui.QAction('Lista systemów', self)
    self.actionSystemList.triggered.connect(
      lambda: SystemEditor().exec_() )

    # Action allowing adding, deleting and modifying system maps
    self.actionMapEditor=QtGui.QAction('Edytor map', self)
    self.actionMapEditor.triggered.connect(
      lambda: self.mainWidget.centralny.addTab(MapEditor(), 'Edytor map'))

    fileMenu=self.menubar.addMenu("&Plik")
    fileMenu.addAction(self.actionExit)
    windowMenu=self.menubar.addMenu("Ekran")
    windowMenu.addAction(self.actionFullScreen)
    narzedziaMenu=self.menubar.addMenu("Narzędzia")
    narzedziaMenu.addAction(self.actionLegenda)
    narzedziaMenu.addAction(self.actionMapy)
    narzedziaMenu.addAction(self.actionUserPasswordChange)
    narzedziaSerwisMenu=narzedziaMenu.addMenu("Serwis")
    narzedziaSerwisMenu.addAction(self.actionPozycjaKursora)
    adminMenu=self.menubar.addMenu('Administracja')
    adminMenu.addAction(self.actionUsersList)
    adminMenu.addAction(self.actionSystemList)
    adminMenu.addAction(self.actionMapEditor)

    self.mainWidget=MainWidget()
    self.setCentralWidget(self.mainWidget)

    self.addDockWidget(QtCore.Qt.NoDockWidgetArea, self.mainWidget.lewyDock);
    self.mainWidget.lewyDock.setParent(self)
    self.mainWidget.lewyDock.close()

    self.userDock=UsersList()
    self.addDockWidget(QtCore.Qt.NoDockWidgetArea, self.userDock)
    self.userDock.setParent(self)
    self.userDock.close()

    # Automatic skin changing
    self.mainWidget.eventList.signal_emptyList.connect(
      lambda: self.setPalette(self.blueSkin))
    self.mainWidget.eventList.signal_notEmptyList.connect(
      lambda: self.setPalette(self.redSkin))

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

#TODO: dziwne, działa po kliknięciu. Ale to i lepiej :)
  def pozycjaKursoraCon(self):
    if self.isPokazPozycjeKursora:
      self.mainWidget.centralny.currentWidget().mouseMoveEventCon(None)
      self.isPokazPozycjeKursora=False
      self.mainWidget.appendInfo(">>> Wyłączono pokazywanie pozycji kursora")
    else:
      self.mainWidget.centralny.currentWidget().mouseMoveEventCon(self.statusBar())
      self.isPokazPozycjeKursora=True
      self.mainWidget.appendInfo(">>> Włączono pokazywanie pozycji kursora. Kliknij, aby zobaczyć")

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
    self.mainWidget.centralny.addTab(self.mapa, "Legenda")

  def showMaps(self):
    self.mainWidget.lewyDock.show()

  def showUsersList(self):
    self.userDock.show()
    self.userDock.loadData()

if __name__ == '__main__':
  import sys

  app = QtGui.QApplication(sys.argv)

#TODO: trochę po chamsku, ale działa
#nie mam pomysłu jak to poprawić...
  iloscProb=0
  while iloscProb<3:
    wynik=LoginWindow().exec_()
    if wynik==1:
      wMain=MainWindow()
      wMain.showFullScreen()
      wMain.setWindowTitle("Tablica synoptyczna")
      #w.setWindowFlags(w.windowFlags()&~QtCore.Qt.WindowStaysOnTopHint)
      wMain.show()
      break
    elif wynik==2: iloscProb+=1
    else: iloscProb=3
  if iloscProb>2: sys.exit(0)

  sys.exit(app.exec_())