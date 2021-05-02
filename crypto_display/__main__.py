#!/usr/bin/python3

import sys
import requests
import threading
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

interval = 60000

currency = 'SGD'

coins = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'ADA': 'cardano',
    'DOGE': 'dogecoin'
}

last = {}
lcds = {}

colors = [
    QColor(255, 255, 255),
    QColor(0, 255, 0),
    QColor(255, 0, 0)
]

def main():
    global lcds, coins, currency

    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(480, 320)
    w.move(0, 0)
    w.setWindowTitle('Crypto')

    layout = QVBoxLayout(w)

    close = QPushButton()
    close.setText('Close')
    close.clicked.connect(app.quit)

    refresh = QPushButton()
    refresh.setText('Refresh')
    refresh.clicked.connect(data_load)

    display = QGridLayout(w)
    display.setColumnStretch(1, 1)

    row = 0

    for k in coins:
        print('Creating display for ' + k)

        lcd = QLCDNumber()
        lcd.setDigitCount(12)
        lcd.setSmallDecimalPoint(True)
        lcd.setSegmentStyle(QLCDNumber.Flat)

        label = QLabel()
        label.setText(k + ':' + currency)
        label.setFont(QFont('Arial', 20))

        display.addWidget(label, row, 0)
        display.addWidget(lcd, row, 1)

        lcds[k] = lcd
        row += 1


    layout.addLayout(display)
    layout.addWidget(refresh)
    layout.addWidget(close)

    data_load()

    timer = QTimer(w)
    timer.timeout.connect(data_load)
    timer.start(interval)

    w.showFullScreen()

    sys.exit(app.exec_())

def data_load():
    global coins, currency, last, lcds, colors

    query_ids = ''

    for k in coins:
        if not query_ids:
            query_ids = coins[k]
        else:
            query_ids = query_ids + '%2C' + coins[k]

    query = 'https://api.coingecko.com/api/v3/simple/price?vs_currencies=' + currency + '&ids=' + query_ids

    print('Calling CoinGecko API...')
    print(query)
    response = requests.get(query)
    print(response.text)

    data = response.json()

    for k in coins:
        value = data[coins[k]][currency.lower()]
        movement = 0 

        if k in last:
            if last[k] < value:
                movement = 1
            elif last[k] > value:
                movement = -1


        palette = lcds[k].palette()
        palette.setColor(palette.Background, colors[movement])
        lcds[k].setPalette(palette)

        lcds[k].display('{:.2f}'.format(value))

        last[k] = value

        print(k + ':' + str(movement) + ':{:.2f}'.format(value))

main()
