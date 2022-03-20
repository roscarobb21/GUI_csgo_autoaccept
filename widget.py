# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
from time import sleep

from worker import Worker
from datetime import datetime
from PySide6.QtWidgets import QApplication,QSystemTrayIcon, QWidget, QPushButton, QTextBrowser, QProgressBar, QSystemTrayIcon, QComboBox
from PySide6 import QtGui, QtCore
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from configparser import ConfigParser


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.firstStart = False
        self.resolutionIndex = 0
        self.aspectIndex = 0
        self.resArray = [['1280x1024','1024x768', '800x600'], ['1920x1080']]
        self.aspectArray = ['4:3', '16:9']
        self.resolutionBox = 0
        self.aspectBox = 1
        self.startBtn = 0
        self.closeBtn = 0
        self.logText = 0
        self.progress = 0
        self.w = 0
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def getButtons(self):
        self.startBtn = self.findChild(QPushButton, "startBtn")
        self.closeBtn = self.findChild(QPushButton, "closeBtn")
        self.logText  = self.findChild(QTextBrowser, "logText")

        self.startBtn.clicked.connect(self.acceptbtn_press)
        self.closeBtn.clicked.connect(self.closebtn_press)

        # Set Disabled the closeBtn first
        self.closeBtn.setEnabled(False)

    def getComboBoxes(self):
        self.resolutionBox = self.findChild(QComboBox, "resolutionBox")
        self.aspectBox = self.findChild(QComboBox, "aspectBox")
        for i in self.aspectArray:
            self.aspectBox.addItem(i)
        for i in self.resArray[self.aspectBox.currentIndex()]:
            self.resolutionBox.addItem(i)
        self.resolutionBox.textActivated.connect(self.resClick)
        self.aspectBox.textActivated.connect(self.aspectClick)


    def acceptbtn_press(self):
        self.w = Worker()
        self.w.setLog(self.logText)
        self.w.readConfig()
        # self.w.setProgress(self.progress)
        self.w.start()
        # Accept Button pressed, set close enabled and accept disabled
        self.startBtn.setEnabled(False)
        self.closeBtn.setEnabled(True)

        # disable also combo boxes
        self.resolutionBox.setEnabled(False)
        self.aspectBox.setEnabled(False)

        if(not self.firstStart):
            self.logText.append("Info: roscaroberto21@gmail.com ")
            self.logText.append("----------------------------------------")
        self.firstStart = True
        self.logText.append("Start on : "+ str(datetime.now().time()) + " " + str(datetime.now().date()))


    def closebtn_press(self):
        self.w.restart()
        self.w.stop()
        #Close Button pressed, set close disabled and accept enabled
        self.startBtn.setEnabled(True)
        self.closeBtn.setEnabled(False)

        # enable res and aspect combo boxes
        self.resolutionBox.setEnabled(True)
        self.aspectBox.setEnabled(True)

        self.logText.append("Closed on : "+ str(datetime.now().time()) + " " + str(datetime.now().date()))
        self.logText.append("----------------------------------------")
        self.w.stop()

    def waitForAccept(self):
        return 0
    def getlogText(self):
        return self.logText

    def resClick(self):
        self.writeConfig(self.resolutionBox.currentIndex(), self.aspectBox.currentIndex())

    def aspectClick(self):
        self.changeResValues(self.aspectBox.currentIndex())
        self.writeConfig(self.resolutionBox.currentIndex(), self.aspectBox.currentIndex())

    def changeResValues(self, index):
        self.resolutionBox.clear()
        for i in self.resArray[index]:
            self.resolutionBox.addItem(i)
        self.writeConfig(self.resolutionBox.currentIndex(), self.aspectBox.currentIndex())

    def readConfig(self):
        config = ConfigParser()
        config.read('config.ini')
        resVal = int(config.get('res', 'resolution'))
        aspectVal = int(config.get('aspect', 'aspect'))
        self.aspectBox.setCurrentIndex(aspectVal)
        self.changeResValues(aspectVal)
        self.resolutionBox.setCurrentIndex(resVal)

    def writeConfig(self, resVal, aspectVal):
        config = ConfigParser()
        config.read('config.ini')
        config.set('res', 'resolution', str(resVal))
        config.set('aspect', 'aspect', str(aspectVal))
        cfgfile = open('config.ini', 'w')
        config.write(cfgfile)
        cfgfile.close()


if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.setWindowTitle("CS:GO Auto Accept")
    widget.setFixedSize(450, 200)
    trayIcon = QSystemTrayIcon()
    trayIcon.setIcon(QtGui.QIcon('title.png'))
    widget.setWindowIcon(QtGui.QIcon('title.png'))
    widget.show()
    widget.getButtons()
    widget.getComboBoxes()
    widget.readConfig()
    sys.exit(app.exec())

