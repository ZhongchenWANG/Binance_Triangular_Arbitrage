#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from binance.client import Client
import pandas as pd
import requests
from datetime import datetime
import time


# In[ ]:


api=[]
with open("./api_key.txt", encoding="utf-16",errors='ignore') as f:  
    data = f.readlines()
    api.extend(data)
api[0] = api[0][:-1]


# In[ ]:


client = Client(api[0], api[1])


# In[ ]:


client.API_URL = 'https://testnet.binance.vision/api'


# In[ ]:


symbol_1 = ["BNBUSDT","CAKEUSDT","CAKEBNB"]
symbol_2 = ["BTCUSDT","CAKEUSDT","CAKEBTC"]


# In[ ]:


print('\nThere are two defaul pairs for checking the triangular arbitrage opportunity:\n1. BNB/USDT, CAKE/USDT and CAKE/BNB pairs\n2. BTC/USDT, CAKE/USDT and CAKE/BTC pairs')


# In[ ]:


profit = input('\nPlease input the profit margin:(Input 0 for default setting 0.1%)\n')
if profit == '0':
    profit = 0.001
else:
    profit = float(profit)


# In[ ]:


def Triangular_Arbitrage_check(symbol):
    # get latest price from Binance API
    bnb_usdt_price = float(client.get_symbol_ticker(symbol=symbol[0])['price'])
    cake_usdt = float(requests.get('https://api.binance.com/api/v3/avgPrice?symbol='+symbol[1]).json()['price'])
    cake_bnb = float(requests.get('https://api.binance.com/api/v3/avgPrice?symbol='+symbol[2]).json()['price'])
    bnb_usdt_arb = cake_usdt/cake_bnb
    if abs(bnb_usdt_price-bnb_usdt_arb)>=profit:
        print('Alert, there is the price different up to:', abs(bnb_usdt_price-bnb_usdt_arb),'and now is:',
              datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'(GMT+8).')
    else:
        print('There is no Triangular Arbitrage.')


# In[ ]:


times = input('\nPlease input the number of times you want to check for the Triangular Arbitrage method:\n')


# In[ ]:


print('\033[1m\nStart checking!\033[0m\n')
for i in range(int(times)):
    print('Now check the profit for BNB/USDT, CAKE/USDT and CAKE/BNB pairs:\n')
    Triangular_Arbitrage_check(symbol_1)
    print('\nNow check the profit for BTC/USDT, CAKE/USDT and CAKE/BTC pairs:\n')
    Triangular_Arbitrage_check(symbol_2)
    print('\n\n')
    time.sleep(10)
print('\033[1mFinish checking!\n\033[0m')

