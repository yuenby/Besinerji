import sys
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication

class AnaSayfa(QMainWindow)
    def __init__ (self):
        super(AnaSayfa, self).__init__()
        self.initUI()

        
app = QApplication(sys.argv)

