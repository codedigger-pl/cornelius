# -*- coding: utf-8 -*-

###############################################################################
# DlgSystemAdd.py
#
# author: Paweł Surowiec (codedigger)
# creation date: 12.05.2014
# version: 0.0.1
#
# Module contains simple dialog allowing adding integrated systems to Cornelius
# system. Integrated systems are located in SYSTEMS variable.
#
# Calling this module directly, it will call this dialog for tests
###############################################################################

DLGSYSTEMADD_PY_VERSION=(0,0,1)

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from QtD.DlgSystemAdd import Ui_DlgSystemAdd
from Satel.integra import Integra24, Integra32, Integra64, Integra64Plus,     \
                            Integra128, Integra128Plus, Integra256Plus

SYSTEMS=(('Satel Integra 24', Integra24),
         ('Satel Integra 32', Integra32),
         ('Satel Integra 64', Integra64),
         ('Satel Integra 64Plus', Integra64Plus),
         ('Satel Integra 128', Integra128),
         ('Satel Integra 128PLUS', Integra128Plus),
         ('Satel Integra 256PLUS', Integra256Plus))

class DlgSystemAdd(Ui_DlgSystemAdd, QtGui.QDialog):
  """Dialog allowing adding systems do Cornelius system"""
  newSystem=None

  def __init__(self):
    """Base inicjalization"""
    super(DlgSystemAdd, self).__init__()
    self.setupUi(self)
    self.btnAdd.clicked.connect(self.addButtonClicked)

    for s in SYSTEMS: self.cmbSystems.addItem(s[0], userData=s[1])

  @pyqtSlot()
  def addButtonClicked(self):
    self.newSystem=self.cmbSystems.itemData(self.cmbSystems.currentIndex(),
                                            role=QtCore.Qt.UserRole)()
    self.done(1)

if __name__=='__main__':
  import sys
  app = QtGui.QApplication(sys.argv)
  DlgSystemAdd().exec_()
  sys.exit(app.exec_())