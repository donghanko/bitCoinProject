import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
#from pybithumb import WebSocketManager

from pyupbit import WebSocketManager
class OverViewWorker(QThread):
    data24Sent = pyqtSignal(int, float ,float, int, float, int, float,int)
    dataMidSent = pyqtSignal(int, float, float)

    def __init__(self, ticker="BTC"):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        #wm = WebSocketManager("ticker", [f"KRW-{self.ticker}"])
        wm = WebSocketManager("ticker", [f"KRW-{self.ticker}"])
        while self.alive:
            data = wm.get()

            self.data24Sent.emit(int(data['trade_price']),
                                 float(data['signed_change_rate']*100),
                                 float(data['acc_trade_volume_24h']),
                                 int(data['high_price']),
                                 float(data['acc_trade_price_24h']),
                                 int(data['low_price']),
                                 float(data['trade_volume']),
                                 int(data['prev_closing_price']))
        wm.terminate()

    def close(self):
        self.alive = False


class OverviewWidget(QWidget):
    def __init__(self, parent=None, ticker="BTC"):
        super().__init__(parent)
        uic.loadUi("C:\\Users\\dhko23\\PycharmProjects\\uifile\\overview.ui", self)

        self.ticker = ticker
        self.ovw = OverViewWorker(ticker)
        self.ovw.data24Sent.connect(self.fill24Data)
        self.ovw.start()

    def closeEvent(self, event):
        self.ovw.close()

    def fill24Data(self, currPrice,chgRate,volume, highPrice, value, lowPrice,volumePower, PrevClosePrice):
        self.label_1.setText(f"{currPrice:,}")
        self.label_2.setText(f"{chgRate:+.2f}%")
        self.label_4.setText(f"{volume:,.2f} {self.ticker}")
        self.label_6.setText(f"{highPrice:,}")
        self.label_8.setText(f"{value/100000000:,.1f} 억")
        self.label_10.setText(f"{lowPrice:,}")
        self.label_12.setText(f"{volumePower:.2f}%")
        self.label_14.setText(f"{PrevClosePrice:,}")

        # ----------------- 추 가 ------------------
        self.__updateStyle()
        # ------------------------------------------

    def fillMidData(self, currPrice, chgRate, volumePower):
        self.label_1.setText(f"{currPrice:,}")
        self.label_2.setText(f"{chgRate:+.2f}%")
        self.label_12.setText(f"{volumePower:.2f}%")
        # ----------------- 추 가 ------------------
        self.__updateStyle()
        # ------------------------------------------

    # ----------------- 추 가 ------------------
    def __updateStyle(self):
        if '-' in self.label_2.text():
            self.label_1.setStyleSheet("color:blue;")
            self.label_2.setStyleSheet("background-color:blue;color:white")
        else:
            self.label_1.setStyleSheet("color:red;")
            self.label_2.setStyleSheet("background-color:red;color:white")
    # ------------------------------------------


if __name__ == "__main__":

    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ob = OverviewWidget()
    ob.show()
    exit(app.exec_())