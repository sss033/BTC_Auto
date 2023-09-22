# REST API
#import requests

# url = "https://api.upbit.com/v1/market/all"
# resp = requests.get(url)
# data = resp.json()

# krw_tickers = []

# for coin in data:
#     ticker = coin['market']

#     if ticker.startswith("KRW"):
#         krw_tickers.append(ticker)

# print(krw_tickers)
# print(len(krw_tickers))

import pyupbit  

# tickers = pyupbit.get_tickers(fiat="KRW")  #종목 조회
# print(tickers)
# print(len(tickers))

# df = pyupbit.get_ohlcv("KRW-BTC" , "week")  #시세 캔들 조회
# print(df)

# tickers = ["KRW-BTC" , "KRW-XRP"]
# price = pyupbit.get_current_price(tickers)  #현재가 조회
# for k, v in price.items():
#     print(k, v)

# krw_tickers = pyupbit.get_tickers(fiat="KRW")  #모든종목 현재가 조회
# prices = pyupbit.get_current_price(krw_tickers)
# for k, v in prices.items():
#     print(k, v)

import pprint

# orderbooks = pyupbit.get_orderbook("KRW-BTC")  #호가정보 조회
# pprint.pprint(orderbooks)

f = open("upbit.txt")  #잔고 조회
lines = f.readlines()
access = lines[0].strip()
secret = lines[1].strip()
f.close()

upbit = pyupbit.Upbit(access, secret)
balance = upbit.get_balance("KRW")
print(balance)