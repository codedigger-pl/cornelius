# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MapExplorer.ui'
#
# Created: Mon Nov 24 20:28:01 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MapExplorer(object):
    def setupUi(self, MapExplorer):
        MapExplorer.setObjectName(_fromUtf8("MapExplorer"))
        MapExplorer.resize(193, 525)
        MapExplorer.setMinimumSize(QtCore.QSize(193, 525))
        MapExplorer.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lstMaps = QtGui.QTreeWidget(self.dockWidgetContents)
        self.lstMaps.setObjectName(_fromUtf8("lstMaps"))
        self.lstMaps.headerItem().setText(0, _fromUtf8("1"))
        self.lstMaps.header().setVisible(False)
        self.verticalLayout.addWidget(self.lstMaps)
        self.btnRefresh = QtGui.QPushButton(self.dockWidgetContents)
        self.btnRefresh.setObjectName(_fromUtf8("btnRefresh"))
        self.verticalLayout.addWidget(self.btnRefresh)
        MapExplorer.setWidget(self.dockWidgetContents)

        self.retranslateUi(MapExplorer)
        QtCore.QMetaObject.connectSlotsByName(MapExplorer)

    def retranslateUi(self, MapExplorer):
        MapExplorer.setWindowTitle(QtGui.QApplication.translate("MapExplorer", "Lista map", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefresh.setText(QtGui.QApplication.translate("MapExplorer", "Odśwież", None, QtGui.QApplication.UnicodeUTF8))

