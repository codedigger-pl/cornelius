# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MapEditor.ui'
#
# Created: Mon Nov 10 19:39:15 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MapEditor(object):
    def setupUi(self, MapEditor):
        MapEditor.setObjectName(_fromUtf8("MapEditor"))
        MapEditor.resize(945, 808)
        self.gridLayout_2 = QtGui.QGridLayout(MapEditor)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.widget = QtGui.QWidget(MapEditor)
        self.widget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.comboBox = QtGui.QComboBox(self.widget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.verticalLayout.addWidget(self.comboBox)
        self.treeWidget = QtGui.QTreeWidget(self.widget)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout.addWidget(self.treeWidget)
        self.pushButton = QtGui.QPushButton(self.widget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.widget)
        self.widget_2 = QtGui.QWidget(MapEditor)
        self.widget_2.setMaximumSize(QtCore.QSize(20, 16777215))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.line_2 = QtGui.QFrame(self.widget_2)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_2.addWidget(self.line_2)
        self.btnPanelSwitch = QtGui.QToolButton(self.widget_2)
        self.btnPanelSwitch.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.btnPanelSwitch.setArrowType(QtCore.Qt.LeftArrow)
        self.btnPanelSwitch.setObjectName(_fromUtf8("btnPanelSwitch"))
        self.verticalLayout_2.addWidget(self.btnPanelSwitch)
        self.line = QtGui.QFrame(self.widget_2)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.widget_2)
        self.graphicsView = QtGui.QGraphicsView(MapEditor)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.graphicsView)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(MapEditor)
        QtCore.QMetaObject.connectSlotsByName(MapEditor)

    def retranslateUi(self, MapEditor):
        MapEditor.setWindowTitle(QtGui.QApplication.translate("MapEditor", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MapEditor", "Dodaj podkład graficzny", None, QtGui.QApplication.UnicodeUTF8))
        self.btnPanelSwitch.setText(QtGui.QApplication.translate("MapEditor", "...", None, QtGui.QApplication.UnicodeUTF8))

