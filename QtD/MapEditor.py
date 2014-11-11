# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MapEditor.ui'
#
# Created: Tue Nov 11 20:22:16 2014
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
        self.panelContainer = QtGui.QWidget(MapEditor)
        self.panelContainer.setMaximumSize(QtCore.QSize(200, 16777215))
        self.panelContainer.setObjectName(_fromUtf8("panelContainer"))
        self.gridLayout = QtGui.QGridLayout(self.panelContainer)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cmbMaps = QtGui.QComboBox(self.panelContainer)
        self.cmbMaps.setObjectName(_fromUtf8("cmbMaps"))
        self.verticalLayout.addWidget(self.cmbMaps)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnMapAdd = QtGui.QPushButton(self.panelContainer)
        self.btnMapAdd.setObjectName(_fromUtf8("btnMapAdd"))
        self.horizontalLayout_2.addWidget(self.btnMapAdd)
        self.btnMapDelete = QtGui.QPushButton(self.panelContainer)
        self.btnMapDelete.setObjectName(_fromUtf8("btnMapDelete"))
        self.horizontalLayout_2.addWidget(self.btnMapDelete)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.systemList = QtGui.QTreeWidget(self.panelContainer)
        self.systemList.setAlternatingRowColors(True)
        self.systemList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.systemList.setRootIsDecorated(True)
        self.systemList.setObjectName(_fromUtf8("systemList"))
        self.systemList.header().setVisible(False)
        self.verticalLayout.addWidget(self.systemList)
        self.btnLoadGraphic = QtGui.QPushButton(self.panelContainer)
        self.btnLoadGraphic.setObjectName(_fromUtf8("btnLoadGraphic"))
        self.verticalLayout.addWidget(self.btnLoadGraphic)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.panelContainer)
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
        self.lblGraphic = QtGui.QLabel(MapEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblGraphic.sizePolicy().hasHeightForWidth())
        self.lblGraphic.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lblGraphic.setFont(font)
        self.lblGraphic.setAcceptDrops(True)
        self.lblGraphic.setScaledContents(True)
        self.lblGraphic.setAlignment(QtCore.Qt.AlignCenter)
        self.lblGraphic.setObjectName(_fromUtf8("lblGraphic"))
        self.horizontalLayout.addWidget(self.lblGraphic)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(MapEditor)
        QtCore.QMetaObject.connectSlotsByName(MapEditor)

    def retranslateUi(self, MapEditor):
        MapEditor.setWindowTitle(QtGui.QApplication.translate("MapEditor", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMapAdd.setText(QtGui.QApplication.translate("MapEditor", "Dodaj mapę", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMapDelete.setText(QtGui.QApplication.translate("MapEditor", "Usuń mapę", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoadGraphic.setText(QtGui.QApplication.translate("MapEditor", "Dodaj podkład graficzny", None, QtGui.QApplication.UnicodeUTF8))
        self.btnPanelSwitch.setText(QtGui.QApplication.translate("MapEditor", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.lblGraphic.setText(QtGui.QApplication.translate("MapEditor", "<html><head/><body><p>Kliknij</p><p><span style=\" font-weight:600;\">&quot;Dodaj podkład graficzny&quot;</span></p><p>aby załadować grafikę</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

