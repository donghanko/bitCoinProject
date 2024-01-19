from UpbitPrivateAPI import my_upbit_key,my_upbit_secret_key


url = "wss://api.upbit.com/websocket/v1"
"""
First Model

import websockets
import asyncio
import json

async def upbit_ws_client():
    url = "wss://api.upbit.com/websocket/v1"

    async with websockets.connect(url) as websocket:
        subscribe_fmt =[
            {"ticket":"test"},
            {
                "type":'ticker',
                "codes":["KRW-BTC"],
                "isOnlyRealtime":True
            },
            {"format":"SIMPLE"}
        ]

        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            print(data)

async def main():
    await upbit_ws_client()

asyncio.run(main())
"""

import multiprocessing as mp
import websockets
import asyncio
import json
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
async def upbit_ws_client(q):
    uri = url

    async with websockets.connect(uri) as websocket:
        subscribe_fmt = [
            {"ticket": "test"},
            {
                "type": 'ticker',
                "codes": ["KRW-BTC"],
                "isOnlyRealtime": True
            },
            {"format": "SIMPLE"}
        ]

        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            print(data)
            q.put(data)

async def main(q):
    await upbit_ws_client(q)

def producer(q):
    asyncio.run(main(q))

class Consumer(QThread):
    poped = pyqtSignal(dict)

    def __init__(self,q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            if not self.q.empty():
                data = q.get()
                self.poped.emit(data)

class MyWindow(QMainWindow):
    def __init__(self,q):
        super().__init__()
        self.setGeometry(200, 200, 400, 200)
        self.setWindowTitle("Bithumb Websocket with PyQt")

        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()

        self.label = QLabel("Bitcoin: ", self)
        self.label.move(10, 10)

        self.line_edit = QLineEdit(" ", self)
        self.line_edit.resize(150, 30)
        self.line_edit.move(100, 10)

    @pyqtSlot(dict)
    def print_data(self, data):
        content = int(data.get('tp'))

        self.line_edit.setText(format(content, ",d"))
        now = datetime.datetime.now()
        self.statusBar().showMessage(str(now))


if __name__ == "__main__":
    q = mp.Queue()
    p = mp.Process(name="Producer", target=producer, args=(q,), daemon=True)
    p.start()

    app = QApplication(sys.argv)
    mywindow = MyWindow(q)
    mywindow.show()
    app.exec_()