import time
import pyupbit
import ccxt
import sys
import plotly.graph_objs as go

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
