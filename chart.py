import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QLineSeries, QChart, QValueAxis, QDateTimeAxis
from PyQt5.QtCore import Qt, QDateTime
from collections import deque
# ----------------- 추 가 ------------------
import time
import pybithumb
from PyQt5.QtCore import QThread, pyqtSignal
import pyupbit

class PriceWorker(QThread):
    dataSent = pyqtSignal(float)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:
            data  = pyupbit.get_current_price(self.ticker)
            time.sleep(.1)
            self.dataSent.emit(data)

    def close(self):
        self.alive = False
# ------------------------------------------

class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker="KRW-BTC"):
        super().__init__(parent)
        uic.loadUi("C:\\Users\\dhko23\\PycharmProjects\\uifile\\chart.ui", self)
        self.ticker = ticker
        self.viewLimit = 600
        self.high = 0
        self.low = 0
        self.open_ = 0
        self.container = deque()

        self.priceData = QLineSeries()
        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)
        self.priceChart.legend().hide()

        axisX = QDateTimeAxis()
        axisX.setFormat("hh:mm:ss")
        axisX.setTickCount(4)
        dt = QDateTime.currentDateTime()
        axisX.setRange(dt, dt.addSecs(self.viewLimit))
        axisY = QValueAxis()


        self.priceChart.addAxis(axisX, Qt.AlignBottom)
        self.priceChart.addAxis(axisY, Qt.AlignRight)
        self.priceData.attachAxis(axisX)
        self.priceData.attachAxis(axisY)
        self.priceChart.layout().setContentsMargins(0, 0, 0, 0)

        self.priceView.setChart(self.priceChart)
        self.priceView.setRenderHints(QPainter.Antialiasing)

        # ----------------- 추 가 ------------------
        self.pw = PriceWorker(ticker)
        self.pw.dataSent.connect(self.appendData)
        self.pw.start()
        # ------------------------------------------

    def appendData(self, currPrice):
        if len(self.container)==0:
            self.high = self.low = self.open_ = currPrice

        if (currPrice>self.high):
            self.high = currPrice
        if (currPrice<self.low):
            self.low = currPrice
        self.container.append(currPrice)
        if len(self.priceData) == self.viewLimit :
            self.priceData.remove(0)
            self.container.popleft()
            self.open_ = self.container[0]

        dt = QDateTime.currentDateTime()
        self.priceData.append(dt.toMSecsSinceEpoch(), (currPrice-self.open_)/(self.high-self.low+1e-3)*100)
        self.__updateAxis()

    def __updateAxis(self):
        pvs = self.priceData.pointsVector()
        dtStart = QDateTime.fromMSecsSinceEpoch(int(pvs[0].x()))
        if len(self.priceData) == self.viewLimit :
            dtLast = QDateTime.fromMSecsSinceEpoch(int(pvs[-1].x()))
        else:
            dtLast = dtStart.addSecs(self.viewLimit)
        ax = self.priceChart.axisX()
        ax.setRange(dtStart, dtLast)

        ay = self.priceChart.axisY()
        dataY = [v.y() for v in pvs]
        ay.setRange(min(dataY), max(dataY))

if __name__ == "__main__":

    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    cw = ChartWidget()
    cw.show()
    exit(app.exec_())
