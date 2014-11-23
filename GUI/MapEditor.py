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
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from QtD.MapEditor import Ui_MapEditor
from db import db
from statics import statics

class MapEditor(Ui_MapEditor, QtGui.QWidget):
  """Map editor panel
  It is QWidget, used as the same as simple map in cornelius system. It allow
  adding, deleting and modifying maps in system"""

  # private class variables
  detectors=[]
  outs=[]
  zones=[]

  class __MoveablePoint(QtGui.QLabel):
    """Private class

    Moveable point on map. It can move by mouse. Base class for other
    map editor elements"""

    # Signals from class
    hasBeenDeleted=pyqtSignal()

    def __init__(self, element=None):
      QtGui.QLabel.__init__(self)
      self.isMouseKeyHolding=False
      self.element=element
      self.__offset=0

      self.session=statics.dbSession

    def mousePressEvent(self, event):
      """Start moving"""
      if event.buttons() == QtCore.Qt.LeftButton:
        self.isMouseKeyHolding=True
        self.__offset=event.pos()

    def mouseReleaseEvent(self, event):
      """Stop moving and eventualy deleting element from database. Deleting is
      made by moving element out of the map."""

      self.isMouseKeyHolding=False

      # if we are connected with database
      if self.element:
        self.element.pointX=self.geometry().x()/self.parent().width()*1000
        self.element.pointY=self.geometry().y()/self.parent().height()*1000
        self.session.commit()

        # check, if element is out of range. If yes, delete it.
        if self.element.pointX < 0 or \
           self.element.pointY < 0 or \
           self.element.pointX > 1000 or \
           self.element.pointY > 1000:
          self.session.delete(self.element)
          self.session.commit()

          self.hasBeenDeleted.emit()

    def mouseMoveEvent(self, event):
      """Moving element, while mouse LeftButton is pressed"""
      if self.isMouseKeyHolding:
        self.move(self.mapToParent(event.pos()-self.__offset))


  class __DetectorPoint(__MoveablePoint):
    """ Private class
    Moveable detector point on map"""

    def paintEvent(self, event):
      """Redefinition paint event: paintint circle"""
      QtGui.QLabel.paintEvent(self, event)
      qp = QtGui.QPainter()
      qp.begin(self)

      qp.setRenderHint(QtGui.QPainter.Antialiasing)
      qp.setPen(QtCore.Qt.black)
      qp.setBrush(QtCore.Qt.Dense5Pattern)

      qp.setBrush(QtCore.Qt.blue)
      qp.drawEllipse(0,0,10,10)

      qp.end()

  class __OutPoint(__MoveablePoint):
    """ Private class
    Moveable out point on map"""

    def paintEvent(self, event):
      """Redefinition point event: paint rect"""
      QtGui.QLabel.paintEvent(self, event)
      qp = QtGui.QPainter()
      qp.begin(self)

      qp.setRenderHint(QtGui.QPainter.Antialiasing)
      qp.setPen(QtCore.Qt.black)
      qp.setBrush(QtCore.Qt.Dense5Pattern)

      qp.setBrush(QtCore.Qt.blue)
      qp.drawRect(0, 0, 10, 10)

      qp.end()

  class __ZonePoint(__MoveablePoint):
    """ Private class
    Moveable zone corner point on map"""

    # signals from class
    pointAdded=pyqtSignal()

    def paintEvent(self, event):
      """Redefinition point event: paint rect"""
      QtGui.QLabel.paintEvent(self, event)
      qp = QtGui.QPainter()
      qp.begin(self)

      qp.setRenderHint(QtGui.QPainter.Antialiasing)
      qp.setPen(QtCore.Qt.black)
      qp.setBrush(QtCore.Qt.Dense5Pattern)

      qp.setBrush(QtCore.Qt.yellow)
      qp.drawEllipse(0, 0, 6, 6)

      qp.end()

    def mouseDoubleClickEvent(self, event):
      prevNumber=self.element.pointNumber

      nextZonePoints=self.session.query(db.ZonePoint).\
                                  filter(db.ZonePoint.zoneID == self.element.zoneID).\
                                  filter(db.ZonePoint.pointNumber >= self.element.pointNumber).\
                                  all()
      for zonePoint in nextZonePoints: zonePoint.pointNumber+=1

      newZonePoint=db.ZonePoint()
      newZonePoint.pointX=self.element.pointX
      newZonePoint.pointY=self.element.pointY
      newZonePoint.zoneID=self.element.zoneID
      newZonePoint.pointNumber=prevNumber

      self.session.add(newZonePoint)
      self.session.commit()

      self.pointAdded.emit()

  class __ZoneArea(QtGui.QWidget):
    def __init__(self, element=None):
      QtGui.QWidget.__init__(self)
      self.isMouseKeyHolding=False
      self.element=element
      self.__offset=0
      self.points={}
      self.session=statics.dbSession

# Why move whole zone? But, maybe somebody someday want to do this.
# After little fixing should work
#     def mousePressEvent(self, event):
#       """Start moving"""
#       if event.buttons() == QtCore.Qt.LeftButton:
#         self.isMouseKeyHolding=True
#         self.__offset=event.pos()
#         for zonePoint in self.points: zonePoint.mousePressEvent(event)
#
#     def mouseReleaseEvent(self, event):
#       """Stop moving and eventualy deleting element from database. Deleting is
#       made by moving element out of the map."""
#       self.isMouseKeyHolding=False
#
#       session=db.Session()
#       session.add(self.element)
#       self.points=[]
#       self.element.pointX=self.geometry().x()/self.parent().width()*1000
#       self.element.pointY=self.geometry().y()/self.parent().height()*1000
#
#       # check, if element is out of range. If yes, delete it.
#       if self.element.pointX < 0 or \
#          self.element.pointY < 0 or \
#          self.element.pointX > 1000 or \
#          self.element.pointY > 1000: session.delete(self.element)
#
#       session.commit()
#       session.close()
#
#     def mouseMoveEvent(self, event):
#       """Moving element, while mouse LeftButton is pressed"""
#       if self.isMouseKeyHolding:
# #         self.move(self.mapToParent(event.pos()-self.__offset))
#         for zonePoint in self.points:
#           zonePoint.mouseMoveEvent(event)
#         self.update()

    def paintEvent(self, event):
      """Redefinition point event: paint rect"""
      QtGui.QWidget.paintEvent(self, event)
      qp = QtGui.QPainter()
      qp.begin(self)

      qp.setRenderHint(QtGui.QPainter.Antialiasing)
      qp.setPen(QtCore.Qt.black)
      brush=QtGui.QBrush(QtCore.Qt.SolidPattern)
      brush.setColor(QtGui.QColor(0,0,255,100))
      qp.setBrush(brush)

      points=[]
      for point in self.points:
        points.append(QtCore.QPoint(self.points[point].x()+3,
                                    self.points[point].y()+3))

      qp.drawPolygon(*points)

      qp.end()

      self.parent().update()

    def changedPointsNumber(self):
      """Deleting whole zone, if there is less than 3 corners"""
      if len(self.element.points) < 3:
        for point in self.element.points: self.session.delete(point)
        self.session.delete(self.element)
        self.session.commit()

#---------------------------------------------------------------------- __init__
  def __init__(self):

    self.session=statics.dbSession

    super(MapEditor, self).__init__()
    self.setupUi(self)

    # connecting buttons actions
    self.btnPanelSwitch.clicked.connect(self.showHidePanel)
    self.btnMapAdd.clicked.connect(self.mapAddButtonClicked)
    self.btnMapDelete.clicked.connect(self.mapDeleteButtonClicked)
    self.btnLoadGraphic.clicked.connect(self.loadGraphicButtonClicked)
    self.cmbMaps.currentIndexChanged.connect(self.mapChanged)

    self.systemList.itemDoubleClicked.connect(self.systemListDbClicked)

    self.lblGraphic.resizeEvent=self.resizeMapGraphic

    self.loadData()

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
      newMap=db.Map()
      newMap.name=dialog.textValue()
      self.session.add(newMap)
      self.session.commit()
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
      deleteMap=self.session.\
                  query(db.Map).\
                  filter(db.Map.id==self.cmbMaps.itemData(self.cmbMaps.currentIndex(),
                                                          role=QtCore.Qt.UserRole)).\
                  one()
      self.session.delete(deleteMap)
      self.session.commit()

      self.loadData()

#-------------------------------------------------------------------- mapChanged
  @pyqtSlot()
  def mapChanged(self):
    if self.cmbMaps.count() != 0:

      # getting current selected map from database
      currMap=self.session.query(db.Map).\
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

      # have to hide main graphic map. Adding elements to visible label as
      # parent don't work. Strange thing...
      self.lblGraphic.setVisible(False)

      # clearing old data
      for detector in self.detectors:
        detector.deleteLater()
        detector=None
      self.detectors=[]

      for out in self.outs:
        out.deleteLater()
        out=None
      self.outs=[]

      for zone in self.zones:
        for zonePoint in zone.points:
          zone.points[zonePoint].deleteLater()
          zone.points[zonePoint]=None
        zone.deleteLater()
        zone=None
      self.zones=[]


      self.lblGraphic.update()


      #adding detectors to map
      for detector in currMap.detectors:
        detectorPoint=self.__DetectorPoint(detector)
        detectorPoint.setParent(self.lblGraphic)
        detectorPoint.move(detector.pointX*self.lblGraphic.width()/1000,
                           detector.pointY*self.lblGraphic.height()/1000)
        self.detectors.append(detectorPoint)

      # edding outs to map
      for out in currMap.outs:
        outPoint=self.__OutPoint(out)
        outPoint.setParent(self.lblGraphic)
        outPoint.move(out.pointX*self.lblGraphic.width()/1000,
                      out.pointY*self.lblGraphic.height()/1000)
        self.outs.append(outPoint)

      # adding zones to map
      for zone in currMap.zones:
        zoneArea=self.__ZoneArea(zone)
        zoneArea.setParent(self.lblGraphic)
        zoneArea.setGeometry(0, 0, self.lblGraphic.width(), self.lblGraphic.height())
        zoneArea.lower()
        for zonePoint in zone.points:
          zonePointG=self.__ZonePoint(zonePoint)
          zonePointG.setParent(self.lblGraphic)
          zonePointG.move(zonePoint.pointX*self.lblGraphic.width()/1000,
                          zonePoint.pointY*self.lblGraphic.height()/1000)
          zoneArea.points[zonePoint.pointNumber]=zonePointG
          zonePointG.hasBeenDeleted.connect(zoneArea.changedPointsNumber)
          zonePointG.hasBeenDeleted.connect(self.mapChanged)
          zonePointG.pointAdded.connect(self.mapChanged)

        self.zones.append(zoneArea)


      # restoring main graphic
      self.lblGraphic.setVisible(True)

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
      dbMap=self.session.query(db.Map).\
                    filter(db.Map.id==self.cmbMaps.itemData(self.cmbMaps.currentIndex(),
                                                            role=QtCore.Qt.UserRole)).\
                    one()
      self.session.add(dbMap)

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
      self.session.commit()

#----------------------------------------------------------- systemListDbClicked
  @pyqtSlot(int, int)
  def systemListDbClicked(self, element, _):
    data=element.data(0, QtCore.Qt.UserRole)
    self.session.add(data)

    # we got Detector type?
    if type(data) == db.Detector:

      # creating detectorPoint with data from given variable
      detectorPoint=db.DetectorPoint()
      detectorPoint.detector=data
      detectorPoint.detectorID=data.id
      detectorPoint.pointX=10
      detectorPoint.pointY=10
      detectorPoint.map=self.cmbMaps.itemData(self.cmbMaps.currentIndex(),
                                              role=QtCore.Qt.UserRole)
      self.session.add(detectorPoint)
      self.session.commit()
      self.session.close()

      self.mapChanged()

    elif type(data) == db.Out:

      # creating outPoint with data from given variable
      outPoint=db.OutPoint()
      outPoint.detector=data
      outPoint.detectorID=data.id
      outPoint.pointX=10
      outPoint.pointY=10
      outPoint.map=self.cmbMaps.itemData(self.cmbMaps.currentIndex(),
                                         role=QtCore.Qt.UserRole)
      self.session.add(outPoint)
      self.session.commit()
      self.session.close()

      self.mapChanged()

    elif type(data) == db.Zone:

      # creating zoneArea with data from given variable
      zoneArea=db.ZoneArea()
      zoneArea.map=self.cmbMaps.itemData(self.cmbMaps.currentIndex(),
                                         role=QtCore.Qt.UserRole)
      self.session.add(zoneArea)

      self.session.commit()

      zonePoint1=db.ZonePoint()
      zonePoint1.pointX=10
      zonePoint1.pointY=10
      zonePoint1.pointNumber=0
      zonePoint1.zoneID=zoneArea.id
      self.session.add(zonePoint1)

      zonePoint2=db.ZonePoint()
      zonePoint2.pointX=10
      zonePoint2.pointY=100
      zonePoint2.pointNumber=1
      zonePoint2.zoneID=zoneArea.id
      self.session.add(zonePoint2)

      zonePoint3=db.ZonePoint()
      zonePoint3.pointX=100
      zonePoint3.pointY=100
      zonePoint3.pointNumber=2
      zonePoint3.zoneID=zoneArea.id
      self.session.add(zonePoint3)

      zonePoint4=db.ZonePoint()
      zonePoint4.pointX=100
      zonePoint4.pointY=10
      zonePoint4.pointNumber=3
      zonePoint4.zoneID=zoneArea.id
      self.session.add(zonePoint4)

      self.session.commit()

      self.mapChanged()

#------------------------------------------------------------- repaintMapGraphic
  def repaintMapGraphic(self, event):
    """Rewrited paint event from GtGui.QLabel. Painting any detector, out and
    zone on the map. Given points are proportial to 1000.
    Example: 10 is 10/1000=1/100=1% of pixels"""
    #TODO: delete later
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
    for zone in self.zones:
      zone.setGeometry(0, 0, self.lblGraphic.width(), self.lblGraphic.height())
    self.replaceAllElements()

#------------------------------------------------------------ replaceAllElements
  def replaceAllElements(self):
    """Wfter resizing window (lblGrapgic), replace all elements to their
    coordinates"""

    # replacing all detectors
    for detector in self.detectors:
      # little lazy fixing...
#       try:
#         self.session.add(detector.element)
#       except: qDebug('DB: trying add prevously added detector '+str(detector.element)+' ')

      detector.move(int(detector.element.pointX*self.lblGraphic.width()/1000),
                    int(detector.element.pointY*self.lblGraphic.height()/1000))

    for out in self.outs:
#       try:
#         self.session.add(out.element)
#       except: pass
      out.move(int(out.element.pointX*self.lblGraphic.width()/1000),
               int(out.element.pointY*self.lblGraphic.height()/1000))

    for zone in self.zones:
#       try:
#         self.session.add(zone.element)
#       except: qDebug('DB: Trying adding prevously added zone '+str(zone))

      for zonePoint in zone.points:
        zone.points[zonePoint].move(zone.points[zonePoint].element.pointX*self.lblGraphic.width()/1000,
                                    zone.points[zonePoint].element.pointY*self.lblGraphic.height()/1000)

#---------------------------------------------------------------------- loadData
  def loadData(self):
    """Loading all data from database into form"""

    # clearing previous data
    self.cmbMaps.clear()
    self.systemList.clear()

    # reading saved maps from database and add to map selector (ComboBox)
    for (mapID, mapName) in self.session.query(db.Map.id, db.Map.name).all():
      self.cmbMaps.addItem(mapName, userData=mapID)

    # reading integrated systems
    for integra in self.session.query(db.Integra).all():
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

#-------------------------------------------------------------- main entry point
if __name__=='__main__':
  import sys
  # creating new database session
  session=db.Session()
  statics.dbSession=session

  # starting application
  app = QtGui.QApplication(sys.argv)
  mw=QtGui.QMainWindow()
  mw.setCentralWidget(MapEditor())
  mw.show()
  exitCode=app.exec_()

  # closing session and quiting app
  session.close()
  sys.exit(exitCode)