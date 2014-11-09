# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import datetime

class EventType:
  """Alarm types generated in system"""
  BreakIn='Alarm włamaniowy'
  Attack='Kod pod przymusem'
  Panic='Napad'


class Event(QtGui.QListWidgetItem):
  """Events generated in system"""
  #-------------------------------------------------------------------- __init__
  def __init__(self,
               alarmType=EventType.BreakIn,
               zone='',
               detectors=[]):
    super(Event, self).__init__()
    self.date=datetime.datetime.now()
    self.alarmType=alarmType
    self.zone=zone
    self.detectors=detectors

  #------------------------------------------------------------------------ data
  def data(self, role):
    """ Returns custom text, when display in other widget. For other functions
    return default QListWidgetItem value

    inputs:
      role: integer - which role data to return
    output: data for selected role"""
    if role==QtCore.Qt.DisplayRole:
      return '%s: %s z %s' % (self.date.strftime('%Y-%m-%d, %H:%M:%S'),
                              self.alarmType,
                              self.zone)
    else: return QtGui.QListWidgetItem.data(self, role)
