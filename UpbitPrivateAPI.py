import time
import pyupbit
import ccxt
import sys
import plotly.graph_objs as go

my_upbit_key = 'DGmkiH2yFLoixeB0bGRw1mrpRHffMCR4tL19SEH9'
my_upbit_secret_key = 'IJEJOWBx3EQuAYXYZtQL9r1h8xGdIaMnHcHAF5fS'

my_biance_key = 'anzz0WxSYAAUasSogiBW0z0bGYMXq44b4I20fhmVB2qJulaL2NmWEGy4zJzH4PPc'
my_binance_secret_key = 'fvo2VZTmQx35J0KcbnZRzM8zcaxyrHVecF12kSNRBC1Zw2mQnY9iBElwnSJnOpb6'

start_time = time.time()
tickers = pyupbit.get_tickers(fiat='KRW')

binance = ccxt.binance({
'apiKey' : my_biance_key,
    'secret':my_binance_secret_key,
})


balance = binance.fetch_balance()
print(balance.keys())
print(balance['XRP'])
print(time.time()-start_time)

"""
upbit = pyupbit.Upbit(my_upbit_key,my_upbit_secret_key)
print(upbit.get_balances())
"""
