#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" main.py

Module contains main application. Run this script to run main program
"""

import sys
from PyQt4 import QtGui

from GUI.LoginWindow import LoginWindow
from GUI.MainWindow import MainWindow


# creating main application
app = QtGui.QApplication(sys.argv)

# TODO: done in some lazy way. Try to reconstruct this
loginCounts = 0

while loginCounts < 3:
    ret = LoginWindow().exec_()

    if ret == 1:
        wMain = MainWindow()
        wMain.showFullScreen()
        wMain.setWindowTitle('Tablica synoptyczna')
        # w.setWindowFlags(w.windowFlags()&~QtCore.Qt.WindowStaysOnTopHint)
        wMain.show()
        break

    elif ret == 2:
        # invalid login/password
        loginCounts += 1

    else:
        # user clicked "CANCEL" button or any other action different from "OK"
        loginCounts = 3

if loginCounts > 2:
    sys.exit(0)

sys.exit(app.exec_())
