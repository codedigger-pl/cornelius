# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from external import vlc
from GUI.DlgAlarmConfirmation import DlgAlarmConfirmation
from statics import statics

class EventList(QtGui.QListWidget):
    """List of events to approve in system"""

    # Signals
    signal_emptyList=pyqtSignal()
    signal_newEvent=pyqtSignal()
    signal_notEmptyList=pyqtSignal()

    def __init__(self):
        super(EventList, self).__init__()

        # Adding sound support with VLC plugin.
        #TODO: error with 'bad main_data_begin pointer' - try to fix this
        self.vlcInstance=vlc.Instance('--input-repeat=-1')
        self.alarmPlayer=self.vlcInstance.media_player_new()
        self.alarmPlayer.set_media(self.vlcInstance.media_new(statics.sndAlarmPath))

        self.itemDoubleClicked.connect(self.dblClickAction)

    @pyqtSlot()
    def dblClickAction(self):
        """Showing alarm confirmations dialog after double click on event"""
        # print(self.item(self.currentRow()))
        # q = QtGui.QListWidgetItem()
        # q.da
        dialog=DlgAlarmConfirmation(self.item(self.currentRow()))
        ret=dialog.exec_()
        if ret==1: self.takeItem(self.currentRow())
        if self.count()==0:
            self.alarmPlayer.stop()
            self.signal_emptyList.emit()

    def appendEvent(self, event):
        """Appending event to event list

        input: event - Event from system
        output: none"""
        self.addItem(event)
        self.alarmPlayer.play()
        self.signal_newEvent.emit()
        if self.count() > 0:
            self.signal_notEmptyList.emit()

#----------------------------------------------------------------------- testing
if __name__=='__main__':
    """For testing - delete after finish"""
    from time import sleep
    instance=vlc.Instance()
    mediaplayer=instance.media_player_new()
    mediaplayer.set_media(instance.media_new('../gfx/snd/alarm.mp3'))
    mediaplayer.play()
    sleep(1000)