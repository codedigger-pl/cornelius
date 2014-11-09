# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DlgAlarmConfirmation.ui'
#
# Created: Sun Oct 26 16:50:15 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DlgAlarmConfirmation(object):
    def setupUi(self, DlgAlarmConfirmation):
        DlgAlarmConfirmation.setObjectName(_fromUtf8("DlgAlarmConfirmation"))
        DlgAlarmConfirmation.resize(636, 406)
        self.lblAlarmSource = QtGui.QLabel(DlgAlarmConfirmation)
        self.lblAlarmSource.setGeometry(QtCore.QRect(10, 20, 621, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lblAlarmSource.setFont(font)
        self.lblAlarmSource.setAlignment(QtCore.Qt.AlignCenter)
        self.lblAlarmSource.setObjectName(_fromUtf8("lblAlarmSource"))
        self.label1 = QtGui.QLabel(DlgAlarmConfirmation)
        self.label1.setGeometry(QtCore.QRect(14, 257, 231, 16))
        self.label1.setObjectName(_fromUtf8("label1"))
        self.groupBox1 = QtGui.QGroupBox(DlgAlarmConfirmation)
        self.groupBox1.setGeometry(QtCore.QRect(10, 80, 281, 181))
        self.groupBox1.setObjectName(_fromUtf8("groupBox1"))
        self.rdbSystemCheck = QtGui.QRadioButton(self.groupBox1)
        self.rdbSystemCheck.setGeometry(QtCore.QRect(20, 30, 251, 21))
        self.rdbSystemCheck.setObjectName(_fromUtf8("rdbSystemCheck"))
        self.rdbFalseAlarm = QtGui.QRadioButton(self.groupBox1)
        self.rdbFalseAlarm.setGeometry(QtCore.QRect(20, 60, 161, 21))
        self.rdbFalseAlarm.setObjectName(_fromUtf8("rdbFalseAlarm"))
        self.rdbBreakIn = QtGui.QRadioButton(self.groupBox1)
        self.rdbBreakIn.setGeometry(QtCore.QRect(20, 120, 171, 21))
        self.rdbBreakIn.setChecked(True)
        self.rdbBreakIn.setObjectName(_fromUtf8("rdbBreakIn"))
        self.rdbUserError = QtGui.QRadioButton(self.groupBox1)
        self.rdbUserError.setGeometry(QtCore.QRect(20, 90, 141, 21))
        self.rdbUserError.setObjectName(_fromUtf8("rdbUserError"))
        self.rdbSystemError = QtGui.QRadioButton(self.groupBox1)
        self.rdbSystemError.setGeometry(QtCore.QRect(20, 150, 151, 21))
        self.rdbSystemError.setObjectName(_fromUtf8("rdbSystemError"))
        self.groupBox2 = QtGui.QGroupBox(DlgAlarmConfirmation)
        self.groupBox2.setGeometry(QtCore.QRect(300, 80, 331, 181))
        self.groupBox2.setObjectName(_fromUtf8("groupBox2"))
        self.chbSentPatrol = QtGui.QCheckBox(self.groupBox2)
        self.chbSentPatrol.setGeometry(QtCore.QRect(20, 30, 301, 21))
        self.chbSentPatrol.setObjectName(_fromUtf8("chbSentPatrol"))
        self.chbCallGroup = QtGui.QCheckBox(self.groupBox2)
        self.chbCallGroup.setGeometry(QtCore.QRect(20, 60, 301, 21))
        self.chbCallGroup.setObjectName(_fromUtf8("chbCallGroup"))
        self.chbCallOD = QtGui.QCheckBox(self.groupBox2)
        self.chbCallOD.setGeometry(QtCore.QRect(20, 90, 261, 21))
        self.chbCallOD.setObjectName(_fromUtf8("chbCallOD"))
        self.chbCallAdmin = QtGui.QCheckBox(self.groupBox2)
        self.chbCallAdmin.setGeometry(QtCore.QRect(20, 120, 301, 21))
        self.chbCallAdmin.setObjectName(_fromUtf8("chbCallAdmin"))
        self.chbCallKO = QtGui.QCheckBox(self.groupBox2)
        self.chbCallKO.setGeometry(QtCore.QRect(20, 150, 301, 21))
        self.chbCallKO.setObjectName(_fromUtf8("chbCallKO"))
        self.btnAlarmConfirm = QtGui.QPushButton(DlgAlarmConfirmation)
        self.btnAlarmConfirm.setGeometry(QtCore.QRect(500, 370, 131, 31))
        self.btnAlarmConfirm.setObjectName(_fromUtf8("btnAlarmConfirm"))
        self.lblAlarmType = QtGui.QLabel(DlgAlarmConfirmation)
        self.lblAlarmType.setGeometry(QtCore.QRect(10, 50, 621, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lblAlarmType.setFont(font)
        self.lblAlarmType.setAlignment(QtCore.Qt.AlignCenter)
        self.lblAlarmType.setObjectName(_fromUtf8("lblAlarmType"))
        self.txtAlarmDescription = QtGui.QPlainTextEdit(DlgAlarmConfirmation)
        self.txtAlarmDescription.setGeometry(QtCore.QRect(10, 280, 621, 81))
        self.txtAlarmDescription.setObjectName(_fromUtf8("txtAlarmDescription"))

        self.retranslateUi(DlgAlarmConfirmation)
        QtCore.QMetaObject.connectSlotsByName(DlgAlarmConfirmation)

    def retranslateUi(self, DlgAlarmConfirmation):
        DlgAlarmConfirmation.setWindowTitle(_translate("DlgAlarmConfirmation", "Potwierdź alarm", None))
        self.lblAlarmSource.setText(_translate("DlgAlarmConfirmation", "Strefa alarmu", None))
        self.label1.setText(_translate("DlgAlarmConfirmation", "Komentarz dotyczący alarmu:", None))
        self.groupBox1.setTitle(_translate("DlgAlarmConfirmation", "Przyczyna alarmu", None))
        self.rdbSystemCheck.setText(_translate("DlgAlarmConfirmation", "Sprawdzenie działania systemu", None))
        self.rdbFalseAlarm.setText(_translate("DlgAlarmConfirmation", "Fałszywy alarm", None))
        self.rdbBreakIn.setText(_translate("DlgAlarmConfirmation", "Włamanie do strefy", None))
        self.rdbUserError.setText(_translate("DlgAlarmConfirmation", "Błąd użytkownika", None))
        self.rdbSystemError.setText(_translate("DlgAlarmConfirmation", "Błąd systemu", None))
        self.groupBox2.setTitle(_translate("DlgAlarmConfirmation", "Podjęte działania", None))
        self.chbSentPatrol.setText(_translate("DlgAlarmConfirmation", "Wysłanie patrolu", None))
        self.chbCallGroup.setText(_translate("DlgAlarmConfirmation", "Wezwanie grupy interwencyjnej", None))
        self.chbCallOD.setText(_translate("DlgAlarmConfirmation", "Powiadomienie Oficera Dyżurnego", None))
        self.chbCallAdmin.setText(_translate("DlgAlarmConfirmation", "Powiadomienie Administratora", None))
        self.chbCallKO.setText(_translate("DlgAlarmConfirmation", "Powiadomienie Komendanta Ochrony", None))
        self.btnAlarmConfirm.setText(_translate("DlgAlarmConfirmation", "Potwierdź alarm", None))
        self.lblAlarmType.setText(_translate("DlgAlarmConfirmation", "Typ alarmu", None))

