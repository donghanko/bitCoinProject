import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pyupbit import WebSocketManager

try:
    uic_directory = os.mkdir("C:\\Users\\dhko23\\Downloads\\")
except:
    uic_directory = "C:\\Users\\dhko23\\Downloads\\"




"""
class MySignal(QObject):
    signal1 = pyqtSignal()
    def run(self):
        self.signal1.emit()
class MyWindow(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,200,300,400)
        self.setWindowTitle("BitCoin Live Price")
        self.setWindowIcon(QIcon("C:\\Users\\dhko23\\Pictures\\bitcoin.png"))      #Window ICON
        self. setupUi(self)
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.inquiry)
        mysignal = MySignal()
        mysignal.signal1.connect(self.signal1_emitted)
        mysignal.run()

    @pyqtSlot()
    def signal1_emitted(self):
        print("signal emitted")

    def inquiry(self):
        cur_time = QTime.currentTime()
        str_time = cur_time.toString("hh:mm:ss")
        self.statusBar().showMessage(str_time)
        price = pykorbit.get_current_price("BTC")
        self.lineEdit.setText(f"{int(price // 1e6)}" + "," + f"{int((price // 1e3) % 1000):03d}" + "," + f"{int(price % 1000):03d}")

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
"""

