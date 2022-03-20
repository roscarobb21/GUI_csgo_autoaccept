from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QTextEdit
from time import sleep
import psutil
import warnings
import pyautogui
from pywinauto.application import Application
from configparser import ConfigParser

class Worker(QtCore.QThread):

    def setLog(self, logText):
        self.pid = 0
        self.logText = logText
        self.skip = False
        self.first = True

    def setProgress(self, progress):
        self.progress = progress

    def run(self):
        print("WORKER " + str(self.aspectVal))
        self.getCSGOPID()
        while (self.pid == 0 and not self.skip):
            sleep(2)
            if(self.first):
                self.logText.append("Open CS:GO first")
                self.first = False
            self.getCSGOPID()
        self.wait_for_accept()

    def wait_for_accept(self):
        warnings.simplefilter("ignore")
        self.logText.append("CS:GO process found, pid="+ str(self.pid))
        self.logText.append("Waiting for accept button.")
        app=Application().connect(process=self.pid)
        app_dialog = app.top_window()
        while True:
            app_dialog.restore()
            #acceptButton = pyautogui.locateOnScreen("./elements/acceptbtn.png", confidence=0.89)
            acceptButton = pyautogui.locateOnScreen("./elements/" + self.aspectFolder[self.aspectVal] + "/" + self.resArray[self.aspectVal][self.resVal] + "_acceptbtn.png", confidence=0.89)
            print(" PATH IS " + "./elements/" + self.aspectFolder[self.aspectVal] + "/" + self.resArray[self.aspectVal][self.resVal] + "_acceptbtn.png")
            playButtonDown = pyautogui.locateOnScreen("./elements/" + self.aspectFolder[self.aspectVal] + "/" + self.resArray[self.aspectVal][self.resVal] + "_playDown.png", confidence=0.89)
            playButtonUp = pyautogui.locateOnScreen("./elements/" + self.aspectFolder[self.aspectVal] + "/" + self.resArray[self.aspectVal][self.resVal] + "_play.png", confidence=0.89)
            acButton = pyautogui.locateOnScreen("./elements/" + self.aspectFolder[self.aspectVal] + "/" + self.resArray[self.aspectVal][self.resVal] + "_ac.png", confidence=0.89)
            notAcButton = pyautogui.locateOnScreen("./elements/" + self.aspectFolder[self.aspectVal] + "/" + self.resArray[self.aspectVal][self.resVal] + "_notac.png", confidence=0.89)
            if(acceptButton):
                pyautogui.doubleClick(acceptButton)
                self.logText.append("Match found and accepted! DoubleClick!")
                #break
            elif (playButtonDown or playButtonUp):
                self.logText.append("Still in menu or waiting for accept!")
            elif (not playButtonDown and not playButtonUp and not acceptButton and not acButton and not notAcButton):
                self.logText.append("Match started!")
                break
            sleep(2)

    def restart(self):
        self.skip = False
        self.first = True

    def readConfig(self):
        config = ConfigParser()
        config.read('config.ini')
        self.resVal = int(config.get('res', 'resolution'))
        self.aspectVal = int(config.get('aspect', 'aspect'))
        self.resArray = [['1280x1024','1024x768', '800x600'], ['1920x1080']]
        self.aspectArray = ['4:3', '16:9']
        self.aspectFolder = ['43' ,  '169']

    def stop(self):
        print("Thread stoped working!")
        self.terminate()

    def getCSGOPID(self):
        process_name = "csgo"
        self.pid = 0
        for proc in psutil.process_iter():
            if process_name in proc.name():
               self.pid = proc.pid


