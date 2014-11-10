# -*- coding: utf-8 -*-

###############################################################################
# db.py
#
# author: Paweł Surowiec (codedigger)
# creation date: 12.05.2014
# version: 0.0.1
#
# Module contains default classes for working with database - PostgreSQL. See
# settings.py in this package for configurations (connection, username, etc.).
# Rememeber to set db_createTables to False after first start.
#
# Calling this module directly, it will set db_createTables to True and reset
# all tables
###############################################################################

MAPEDITOR_PY_VERSION=(0,0,1)

from PyQt4 import QtCore, QtGui
from QtD.MapEditor import Ui_MapEditor
from db import db

class MapEditor(Ui_MapEditor, QtGui.QWidget):

  def __init__(self):
    super(MapEditor, self).__init__()
    self.setupUi(self)