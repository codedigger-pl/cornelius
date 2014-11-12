# -*- coding: utf-8 -*-

###############################################################################
# MapEditor.py
#
# author: Paweł Surowiec (codedigger)
# creation date: 10.11.2014
# version: 0.0.1
#
# Module contains MapEditor panel allowing user adding, modifying and deleting
# maps from system. It is based on QWidget class, can be used enywhere. In
# Cornelius system it used as map (almost fullscreen).
#
# Calling this module directly, it will call application window with this
# widget as central widget.
###############################################################################

MAPEDITOR_PY_VERSION=(0,0,1)

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot
from QtD.MapEditor import Ui_MapEditor
from db import db

class MapEditor(Ui_MapEditor, QtGui.QWidget):
  """Map editor panel
  It is QWidget, used as the same as simple map in cornelius system. It allow
  adding, deleting and modifying maps in system"""

  # private class variables
  detectors=[]
  outs=[]
  zones=[]

  #private class classes
  class __MoveablePoint(QtGui.QLabel):
    """Moveable point on map. It can move by mouse. Base class for other
    map editor elements"""
    def __init__(self, element):
      QtGui.QLabel.__init__(self)
      self.isMouseKeyHolding=False
      self.element=element
      self.__offset=0

    def mousePressEvent(self, event):
      """Start moving"""
      if event.buttons() == QtCore.Qt.LeftButton:
        self.isMouseKeyHolding=True
        self.__offset=event.pos()

    def mouseReleaseEvent(self, event):
      """Stop moving"""
      self.isMouseKeyHolding=False

      session=db.Session()
      session.add(self.element)
      self.element.pointX=self.geometry().x()/self.parent().width()*1000
      self.element.pointY=self.geometry().y()/self.parent().height()*1000
      print(self.element.pointX)
      print(self.element.pointY)
      session.commit()
      session.close()

    def mouseMoveEvent(self, event):
      """Moving element, while mouse LeftButton is pressed"""
      if self.isMouseKeyHolding:
        self.move(self.mapToParent(event.pos()-self.__offset))

  class __DetectorPoint(__MoveablePoint):
    def paintEvent(self, event):
      QtGui.QLabel.paintEvent(self, event)
      qp = QtGui.QPainter()
      qp.begin(self)

      qp.setRenderHint(QtGui.QPainter.Antialiasing)
      qp.setPen(QtCore.Qt.black)
      qp.setBrush(QtCore.Qt.Dense5Pattern)

      qp.setBrush(QtCore.Qt.blue)
      qp.drawEllipse(0,0,10,10)

      qp.end()

#---------------------------------------------------------------------- __init__
  def __init__(self):
    super(MapEditor, self).__init__()
    self.setupUi(self)

    # connecting buttons actions
    self.btnPanelSwitch.clicked.connect(self.showHidePanel)
    self.btnMapAdd.clicked.connect(self.mapAddButtonClicked)
    self.btnMapDelete.clicked.connect(self.mapDeleteButtonClicked)
    self.btnLoadGraphic.clicked.connect(self.loadGraphicButtonClicked)
    self.cmbMaps.currentIndexChanged.connect(self.mapChanged)

    self.systemList.itemDoubleClicked.connect(self.systemListDbClicked)

#     self.lblGraphic.paintEvent=self.repaintMapGraphic
    self.lblGraphic.resizeEvent=self.resizeMapGraphic

    self.loadData()

#     test.raise_()
#     detector=QtGui.QLabel(self)
#     detector.setText('det')
#     detector.setGeometry(250, 100, 30, 30)

#----------------------------------------------------------------- showHidePanel
  @pyqtSlot()
  def showHidePanel(self):
    """Showing or hiding left panel"""
    if self.panelContainer.isVisible():
      self.panelContainer.hide()
      self.btnPanelSwitch.setArrowType(QtCore.Qt.RightArrow)
    else:
      self.panelContainer.show()
      self.btnPanelSwitch.setArrowType(QtCore.Qt.LeftArrow)

#----------------------------------------------------------- mapAddButtonClicked
  @pyqtSlot()
  def mapAddButtonClicked(self):
    """Adding maps to database"""

    #creating dialog
    dialog=QtGui.QInputDialog(self)
    dialog.setLabelText('Podaj nazwę mapy')
    dialog.setWindowTitle('Nowa mapa')

    if dialog.exec_():
      session=db.Session()
      newMap=db.Map()
      newMap.name=dialog.textValue()
      session.add(newMap)
      session.commit()
      session.close()
      self.loadData()

#-------------------------------------------------------- mapDeleteButtonClicked
  @pyqtSlot()
  def mapDeleteButtonClicked(self):
    """Deleting map from system"""

    # Creating confirmation dialog
    dialog=QtGui.QMessageBox(self)
    dialog.setWindowTitle('Usunięcie mapy')
    dialog.setText('Czy na pewno chcesz usunąć mapę "'+\
                   self.cmbMaps.currentText()+\
                   '" ?')
    dialog.setStandardButtons(QtGui.QMessageBox.No|QtGui.QMessageBox.Yes)

    # If confirmed
    if dialog.exec_()==QtGui.QMessageBox.Yes:
      session=db.Session()
      deleteMap=session.\
                  query(db.Map).\
                  filter(db.Map.id==self.cmbMaps.itemData(self.cmbMaps.currentIndex(),
                                                          role=QtCore.Qt.UserRole)).\
                  one()
      session.delete(deleteMap)
      session.commit()
      session.close()
      self.loadData()

#-------------------------------------------------------------------- mapChanged
  @pyqtSlot()
  def mapChanged(self):
    if self.cmbMaps.count() != 0:
      # clearing old data
      for detector in self.detectors:
        detector.delete()
      # creating session
      session=db.Session()

      # getting current selected map from database
      currMap=session.query(db.Map).\
              filter(db.Map.id==self.cmbMaps.itemData(self.cmbMaps.currentIndex(),
                                                      role=QtCore.Qt.UserRole)).\
              one()

      # load pixmap data from database
      pixmapData=QtCore.QByteArray().fromRawData(currMap.graphic)
      pixmap=QtGui.QPixmap()
      pixmap.loadFromData(pixmapData, format='PNG')

      # scaling pixmap to maximum container size
      if pixmap.height() > self.lblGraphic.height() or \
         pixmap.width() > self.lblGraphic.width():
        pixmap=pixmap.scaled(self.lblGraphic.width(),
                       self.lblGraphic.height(),
                       aspectRatioMode=QtCore.Qt.IgnoreAspectRatio,
                       transformMode=QtCore.Qt.SmoothTransformation)

      # setting pixmap
      self.lblGraphic.setPixmap(pixmap)

#       self.detectors=currMap.detectors
#       self.outs=currMap.outs
#       self.zones=currMap.zones

      # have to hide main graphic map. Adding elements to visible label as
      # parent don't work. Strange thing...
      self.lblGraphic.setVisible(False)

      #adding detectors to map
      for detector in currMap.detectors:
        detectorPoint=self.__DetectorPoint(detector)
        detectorPoint.setParent(self.lblGraphic)
        detectorPoint.move(detector.pointX*self.lblGraphic.width()/1000,
                           detector.pointY*self.lblGraphic.height()/1000)
        self.detectors.append(detectorPoint)

      # restoring main graphic
      self.lblGraphic.setVisible(True)

      session.close()

#------------------------------------------------------ loadGraphicButtonClicked
  def loadGraphicButtonClicked(self):
    fileName=(QtGui.QFileDialog.getOpenFileName(self,
                                                'Otwórz podkład mapy',
                                                '.',
                                                'Pliki graficzne (*.png *.jpg *.bmp)'));

    if fileName != '':
      pix=QtGui.QPixmap(fileName)

      # saving graphic in database
      #TODO: save scaled pixmap?
      session=db.Session()
      dbMap=session.query(db.Map).\
                    filter(db.Map.id==self.cmbMaps.itemData(self.cmbMaps.currentIndex(),
                                                            role=QtCore.Qt.UserRole)).\
                    one()
      session.add(dbMap)

      # if loaded pixmap is larger than image container
      if pix.height() > self.lblGraphic.height() or \
         pix.width() > self.lblGraphic.width():
        pix=pix.scaled(self.lblGraphic.width(),
                       self.lblGraphic.height(),
                       aspectRatioMode=QtCore.Qt.IgnoreAspectRatio,
                       transformMode=QtCore.Qt.SmoothTransformation)

      #load graphic into container
      self.lblGraphic.setPixmap(pix)

      # preparing pixmap to write to database
      byteArray=QtCore.QByteArray()
      buffer=QtCore.QBuffer(byteArray)
      buffer.open(QtCore.QIODevice.WriteOnly)
      pix.save(buffer, format='PNG')

      # saving graphic's data to databse
      dbMap.graphic=byteArray.data()
      session.commit()
      session.close()

#----------------------------------------------------------- systemListDbClicked
  @pyqtSlot(int, int)
  def systemListDbClicked(self, element, _):
    data=element.data(0, QtCore.Qt.UserRole)

    # we got Detector type?
    if type(data) == db.Detector:

      # creating session
      session=db.Session()
      session.add(data)

      # creating detectorPoint with data from given variable
      detectorPoint=db.DetectorPoint()
      detectorPoint.detector=data
      detectorPoint.detectorID=data.id
      detectorPoint.pointX=10
      detectorPoint.pointY=10
      detectorPoint.map=self.cmbMaps.itemData(self.cmbMaps.currentIndex(),
                                              role=QtCore.Qt.UserRole)
      session.add(detectorPoint)
      session.commit()
      session.close()

      self.mapChanged()

    elif type(data) == db.Out:

      # creating session
      session=db.Session()

      # creating outPoint with data from given variable
      outPoint=db.OutPoint()
      outPoint.detector=data
      outPoint.detectorID=data.id
      outPoint.pointX=10
      outPoint.pointY=10
      outPoint.map=self.cmbMaps.itemData(self.cmbMaps.currentIndex(),
                                         role=QtCore.Qt.UserRole)
      session.add(outPoint)
      session.commit()
      session.close()

      self.mapChanged()

    elif type(data) == db.Zone:

      # creating session
      session=db.Session()

      # creating zonePoint with data from given variable
      zonePoint=db.ZonePoint()
      zonePoint.detector=data
      zonePoint.detectorID=data.id
      zonePoint.pointX=10
      zonePoint.pointY=10
      zonePoint.map=self.cmbMaps.itemData(self.cmbMaps.currentIndex(),
                                          role=QtCore.Qt.UserRole)
      session.add(zonePoint)
      session.commit()
      session.close()

      self.mapChanged()

#------------------------------------------------------------- repaintMapGraphic
  def repaintMapGraphic(self, event):
    """Rewrited paint event from GtGui.QLabel. Painting any detector, out and
    zone on the map. Given points are proportial to 1000.
    Example: 10 is 10/1000=1/100=1% of pixels"""
    QtGui.QLabel.paintEvent(self.lblGraphic, event)
    qp = QtGui.QPainter()
    qp.begin(self.lblGraphic)

    qp.setRenderHint(QtGui.QPainter.Antialiasing)
    qp.setPen(QtCore.Qt.black)
    qp.setBrush(QtCore.Qt.Dense5Pattern)

    qp.setBrush(QtCore.Qt.blue)
    for detector in self.detectors:
      qp.drawEllipse(detector.pointX/1000*self.lblGraphic.width(),
                     detector.pointY/1000*self.lblGraphic.height(),
                     10,
                     10)

    qp.end()

#-------------------------------------------------------------- resizeMapGraphic
  def resizeMapGraphic(self, event):
    QtGui.QLabel.resizeEvent(self.lblGraphic, event)
    self.mapChanged()
#---------------------------------------------------------------------- loadData
  def loadData(self):
    """Loading all data from database into form"""
    session=db.Session()

    # clearing previous data
    self.cmbMaps.clear()
    self.systemList.clear()

    # reading saved maps from database and add to map selector (ComboBox)
    for (mapID, mapName) in session.query(db.Map.id, db.Map.name).all():
      self.cmbMaps.addItem(mapName, userData=mapID)

    # reading integrated systems
    for integra in session.query(db.Integra).all():
      systemItem=QtGui.QTreeWidgetItem(self.systemList, [integra.name])
      systemItem.setData(0, QtCore.Qt.UserRole, integra)

      detectorsList=QtGui.QTreeWidgetItem(systemItem, ['Wejścia'])
      outsList=QtGui.QTreeWidgetItem(systemItem, ['Wyjścia'])
      zonesList=QtGui.QTreeWidgetItem(systemItem, ['Strefy'])

      # adding detectors
      for detector in integra.detectors:
        detectorItem=QtGui.QTreeWidgetItem(detectorsList, [detector.name])
        detectorItem.setData(0, QtCore.Qt.UserRole, detector)

      # adding outs
      for out in integra.outs:
        outItem=QtGui.QTreeWidgetItem(outsList, [out.name])
        outItem.setData(0, QtCore.Qt.UserRole, out)

      # adding zones
      for zone in integra.zones:
        zoneItem=QtGui.QTreeWidgetItem(zonesList, [zone.name])
        zoneItem.setData(0, QtCore.Qt.UserRole, zone)

    session.close()

#-------------------------------------------------------------- main entry point
if __name__=='__main__':
  import sys
  app = QtGui.QApplication(sys.argv)
  mw=QtGui.QMainWindow()
  mw.setCentralWidget(MapEditor())
  mw.show()
  sys.exit(app.exec_())