# -*- coding: utf-8 -*-

###############################################################################
# SystemEditor.py
#
# author: Paweł Surowiec (codedigger)
# creation date: 09.11.2014
# version: 0.0.1
#
# Module contains GUI element. SystemEditor can add, modify and delete
# integrated systems from Cornelius system.
#
# Call this module directly to invoke module
###############################################################################

SYSTEMEDITOR_PY_VERSION=(0,0,1)

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from QtD.SystemEditor import Ui_SystemEditor
from GUI.DlgSystemAdd import DlgSystemAdd
from db import db

class SystemEditor(Ui_SystemEditor, QtGui.QDialog):
  """GUI element allowing adding, modyfing and deleting integrated systems
  from Cornelius System.
  Some additional data are saved in data() at QtCore.Qt.UserRole position"""

  # current selected system
  selectedSystem=None

  def __init__(self):
    """Base initialization"""
    super(SystemEditor, self).__init__()
    self.setupUi(self)

    # connecting buttonn click singals
    self.btnAddSystem.clicked.connect(self.addSystemClicked)
    self.btnDelSystem.clicked.connect(self.delSystemClicked)
    self.btnSaveChanges.clicked.connect(self.saveChangesClicked)

    # connecting system choice click signal
    self.lstSystems.clicked.connect(self.selectSystemClicked)

    # connecting detectors, outs and zones choice signals
    self.cmbDetectors.currentIndexChanged.connect(self.selectedDetectorChanged)
    self.cmbOuts.currentIndexChanged.connect(self.selectedOutChanged)
    self.cmbZones.currentIndexChanged.connect(self.selectedZoneChanged)

    # connecting changing data
    self.txtSystemName.editingFinished.connect(
      lambda: self.selectedSystem.__setattr__('name',
                                              self.txtSystemName.text()))

    self.txtIPAddress.editingFinished.connect(
      lambda: self.selectedSystem.__setattr__('IP',
                                              self.txtIPAddress.text()))

    self.txtIntegrationPort.editingFinished.connect(
      lambda: self.selectedSystem.__setattr__('port',
                                              self.txtIntegrationPort.text()))

    # these are more complex. Putting it in lambda looks really ugly
    self.txtDetectorName.editingFinished.connect(self.detectorNameChanged)
    self.txtOutName.editingFinished.connect(self.outNameChanged)
    self.txtZoneName.editingFinished.connect(self.zoneNameChanged)

    # opening database session
    self.session=db.Session()

    # load default data
    self.loadSystems()

  def done(self, *args, **kwargs):
    """Before closing dialog"""
    #TODO: is this safe method?
    self.session.close()
    return QtGui.QDialog.done(self, *args, **kwargs)

  def loadSystems(self):
    """Load all saved systems from database. System ID's are saved in data()
    at QtCore.Qt.UserRole position"""
    self.lstSystems.clear()
    systems=self.session.query(db.Integra.id, db.Integra.name).all()
    for (ID, systemName) in systems:
      item=QtGui.QListWidgetItem(systemName)
      item.setData(QtCore.Qt.UserRole, ID)
      self.lstSystems.addItem(item)


  @pyqtSlot()
  def addSystemClicked(self):
    """Action after clicking "Add" button"""
    dlgSystemAdd=DlgSystemAdd()
    if dlgSystemAdd.exec_():

      # adding new system to db. To get id of new system, commiting
      system=db.Integra()
      system.name=dlgSystemAdd.newSystem.getName()
      self.session.add(system)
      self.session.commit()

      # adding detectors to database
      for detector in dlgSystemAdd.newSystem.getDetectors():
        dbDetector=db.Detector()
        dbDetector.name=detector.getName()
        dbDetector.system=system.id
        self.session.add(dbDetector)

      # adding outs to database
      for out in dlgSystemAdd.newSystem.getOuts():
        dbOut=db.Out()
        dbOut.name=out.getName()
        dbOut.system=system.id
        self.session.add(dbOut)

      # adding zones to database
      for zone in dlgSystemAdd.newSystem.getZones():
        dbZone=db.Zone()
        dbZone.name=zone.getName()
        dbZone.system=system.id
        self.session.add(dbZone)

      # commiting session
      self.session.commit()
      self.loadSystems()

  @pyqtSlot()
  def delSystemClicked(self):
    """Action after clicking "Delete" button"""
    # getting selected system ID
    try:
      currID=self.lstSystems.currentItem().data(QtCore.Qt.UserRole)

      # getting system from database and deleting it
      system=self.session.query(db.Integra).filter(db.Integra.id==currID).one()
      if system:
        self.session.delete(system)
        self.session.commit()

      # refreshing list
      self.loadSystems()
    except: pass

  @pyqtSlot()
  def saveChangesClicked(self):
    """Action after clicking "Save changes" button"""
    self.session.commit()
    self.loadSystems()
    self.refreshSystemData()

  @pyqtSlot(int)
  def selectedDetectorChanged(self, index):
    """Setting data from selected detector. Reads additional data (whole
    Detector class) from data() at position UserRole"""
    selDetector=self.cmbDetectors.itemData(index, role=QtCore.Qt.UserRole)
    # this function is called also after clean() method. This is workaround,
    # when list is cleared
    if selDetector: self.txtDetectorName.setText(selDetector.name)

  @pyqtSlot(int)
  def selectedOutChanged(self, index):
    """Setting data from selected out. Reads additional data (whole
    Detector class) from data() at position UserRole"""
    selOut=self.cmbOuts.itemData(index, role=QtCore.Qt.UserRole)
    # this function is called also after clean() method. This is workaround,
    # when list is cleared
    if selOut: self.txtOutName.setText(selOut.name)

  @pyqtSlot(int)
  def selectedZoneChanged(self, index):
    """Setting data from selected zone. Reads additional data (whole
    Detector class) from data() at position UserRole"""
    selZone=self.cmbZones.itemData(index, role=QtCore.Qt.UserRole)
    # this function is called also after clean() method. This is workaround,
    # when list is cleared
    if selZone: self.txtZoneName.setText(selZone.name)

  @pyqtSlot()
  def selectSystemClicked(self):
    """Action after clicking on item in system list. Load detailes about
    selected system and stores additional data in userData"""
    # getting ID selected system
    currID=self.lstSystems.currentItem().data(QtCore.Qt.UserRole)

    # getting system from database
    currSystem=self.session.query(db.Integra).filter(db.Integra.id==currID).one()

    # saving current edited system
    self.selectedSystem=currSystem

    self.refreshSystemData()
#     # displaying base data
#     self.txtSystemName.setText(currSystem.name)
#     self.txtIPAddress.setText(currSystem.IP)
#     self.txtIntegrationPort.setText(currSystem.port)
#
#     # displaying detectors
#     self.cmbDetectors.clear()
#     for detector in currSystem.detectors:
#       self.cmbDetectors.addItem(detector.name, userData=detector)
#
#     # displaying outs
#     self.cmbOuts.clear()
#     for out in currSystem.outs:
#       self.cmbOuts.addItem(out.name, userData=out)
#
#     # displaying zones
#     self.cmbZones.clear()
#     for zone in currSystem.zones:
#       self.cmbZones.addItem(zone.name, userData=zone)

  @pyqtSlot()
  def detectorNameChanged(self):
    currDetector=self.cmbDetectors.itemData(self.cmbDetectors.currentIndex(),
                                            role=QtCore.Qt.UserRole)
    currDetector.name=self.txtDetectorName.text()

  @pyqtSlot()
  def outNameChanged(self):
    currOut=self.cmbOuts.itemData(self.cmbOuts.currentIndex(),
                                  role=QtCore.Qt.UserRole)
    currOut.name=self.txtDetectorName.text()

  @pyqtSlot()
  def zoneNameChanged(self):
    currZone=self.cmbZones.itemData(self.cmbZones.currentIndex(),
                                    role=QtCore.Qt.UserRole)
    currZone.name=self.txtDetectorName.text()

  def refreshSystemData(self):
    """Refreshing saved data from self.selectedSystem"""
    # displaying base data
    self.txtSystemName.setText(self.selectedSystem.name)
    self.txtIPAddress.setText(self.selectedSystem.IP)
    self.txtIntegrationPort.setText(self.selectedSystem.port)

    # displaying detectors
    self.cmbDetectors.clear()
    for detector in self.selectedSystem.detectors:
      self.cmbDetectors.addItem(detector.name, userData=detector)

    # displaying outs
    self.cmbOuts.clear()
    for out in self.selectedSystem.outs:
      self.cmbOuts.addItem(out.name, userData=out)

    # displaying zones
    self.cmbZones.clear()
    for zone in self.selectedSystem.zones:
      self.cmbZones.addItem(zone.name, userData=zone)


# Running SystemEditor like a application
if __name__=='__main__':
  import sys
  app = QtGui.QApplication(sys.argv)
  SystemEditor().exec_()
  sys.exit(app.exec_())