import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.uic import loadUi
from threading import *

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi("main.ui", self)
        self.setWindowTitle("Paper Based Keyboard")
        # self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set the central widget of the Window.
        # self.setCentralWidget(button)
        self.launch.clicked.connect(self.thread)
        self.redetect.clicked.connect(self.thread1)

    def thread(self):
        t1 = Thread(target=self.OpenProject)
        t1.start()

    def OpenProject(self):
        ret = os.system('QwertyLayout.py')
        if ret:
            exit()

    def thread1(self):
        t2 = Thread(target=self.Redetect)
        t2.start()

    def Redetect(self):
        f = open("keyboard.txt","w+")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
