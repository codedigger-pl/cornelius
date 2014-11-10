# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
from QtD.DlgAlarmConfirmation import Ui_DlgAlarmConfirmation
from statics import statics
from db import db

class DlgAlarmConfirmation(QtGui.QDialog, Ui_DlgAlarmConfirmation):

  def __init__(self, event):
    super(QtGui.QDialog, self).__init__()
    self.setupUi(self)
    self.btnAlarmConfirm.clicked.connect(self.alarmConfirmAction)

    self.event=event
    self.lblAlarmSource.setText(event.zone)
    self.lblAlarmType.setText(event.alarmType)

  def __getDBAlarmReason(self):
    """Return appropriate event reason readed from database"""
    reason=None
    if self.rdbBreakIn.isChecked(): reason=db.AlarmReasons.breakeIn
    elif self.rdbFalseAlarm.isChecked(): reason=db.AlarmReasons.falseAlarm
    elif self.rdbSystemCheck.isChecked(): reason=db.AlarmReasons.systemCheck
    elif self.rdbSystemError.isChecked(): reason=db.AlarmReasons.systemError
    elif self.rdbUserError.isChecked(): reason=db.AlarmReasons.userError
    return reason

  def __getDBAlarmAction(self):
    actions=[]
    if self.chbCallAdmin.isChecked(): actions.append(db.AlarmActions.notifiedAdministrator)
    if self.chbCallGroup.isChecked(): actions.append(db.AlarmActions.notifiedGroup)
    if self.chbCallKO.isChecked(): actions.append(db.AlarmActions.notifiedKO)
    if self.chbCallOD.isChecked(): actions.append(db.AlarmActions.notifiedOD)
    if self.chbSentPatrol.isChecked(): actions.append(db.AlarmActions.sentPatrol)
    return actions

  @pyqtSlot()
  def alarmConfirmAction(self):
    session=db.Session()
    session.add(statics.currentLogedUser)
    alarmEvent=db.AlarmEvent()
    alarmEvent.confirmUserID=statics.currentLogedUser.id
    alarmEvent.date=self.event.date
    alarmEvent.zoneName=self.event.zone
    alarmEvent.alarmType=self.event.alarmType
    alarmEvent.detectors=[]
    alarmEvent.comment=self.txtAlarmDescription.toPlainText()
    alarmEvent.reasonID=self.__getDBAlarmReason()
    alarmEvent.actions=self.__getDBAlarmAction()
    session.add(alarmEvent)
    session.commit()
    session.close()
    self.done(1)