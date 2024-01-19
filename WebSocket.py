import asyncio
"""

async def make_americano():
    print("Americano Start")
    await asyncio.sleep(5)
    print("Americano End")
    return "Americano"

async def make_latte():
    print("Latte Start")
    await asyncio.sleep(3)
    print("Latte End")
    return "Latte"
async def main():
    coro1 = make_americano()
    coro2 = make_latte()
    result = await asyncio.gather(
        coro1,
        coro2
    )
    print(result)

print("Main Start")
asyncio.run(main())
print("Main End")
"""

"""
multiprocessing

import time

import multiprocessing as mp

def worker():
    proc = mp.current_process()
    print(proc.name)
    print(proc.pid)
    time.sleep(5)
    print("SubProcess End")


if __name__ == "__main__":
    proc = mp.current_process()
    print(proc.name)
    print(proc.pid)

    p = mp.Process(name="Subprocess", target=worker)

    p.start()

    print("MainProcess End")
"""

"""
import websockets
import asyncio
import json
import time
async def bithumb_ws_client():
    uri = "wss://pubwss.bithumb.com/pub/ws"

    async with websockets.connect(uri) as websocket:
        greeting = await websocket.recv()
        print(greeting)

        subscribe_fmt = {
            "type":"ticker",
            "symbols":["BTC_KRW"],
            "tickTypes":["1H"]
        }

        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            print(data)
async def main():
    await bithumb_ws_client()


asyncio.run(main())
"""

import multiprocessing as mp
import websockets
import asyncio
import json
import sys
import datetime
from PyQt5.QtWidgets import*
from PyQt5.QtCore import *

async def bithumb_ws_client(q):
    uri = "wss://pubwss.bithumb.com/pub/ws"

    async with websockets.connect(uri,ping_interval=None) as websocket:
        subscribe_fmt = {
            "type": "ticker",
            "symbols": ["BTC_KRW"],
            "tickTypes": ["1H"]
        }

        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        while True:
            data = await websocket.recv()
            data = json.loads(data)
            print(data)
            q.put(data)

async def main(q):
    await bithumb_ws_client(q)

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
        self.setGeometry(200,200,400,200)
        self.setWindowTitle("Bithumb Websocket with PyQt")

        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()

        self.label = QLabel("Bitcoin: ",self)
        self.label.move(10,10)

        self.line_edit = QLineEdit(" ",self)
        self.line_edit.resize(150,30)
        self.line_edit.move(100,10)

    @pyqtSlot(dict)
    def print_data(self,data):
        content = data.get('content')
        if content is not None:
            current_price = int(content.get("closePrice"))
            self.line_edit.setText(format(current_price,",d"))
        now = datetime.datetime.now()
        self.statusBar().showMessage(str(now))

if __name__=="__main__":
    q = mp.Queue()
    p = mp.Process(name="Producer",target=producer,args=(q,),daemon=True)
    p.start()

    app = QApplication(sys.argv)
    mywindow = MyWindow(q)
    mywindow.show()
    app.exec_()