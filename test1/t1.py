import ccxt

# 获取所有交易所列表
import inline as inline
import matplotlib

exchange_list = ccxt.exchanges

# 初始化交易所
binance_exchange = ccxt.binance({
    'timeout': 15000,
    'enableRateLimit': True,
         'proxies': {'https': "http://127.0.0.1:10809", 'http': "http://127.0.0.1:10809"}
})


# print('交易所当前时间：', binance_exchange.iso8601(binance_exchange.milliseconds()))

# 加载市场数据
binance_markets = binance_exchange.load_markets()

# 支持的交易对
# print(list(binance_markets.keys()))

symbol = 'BTC/USDT'

btc_usdt_market = binance_markets[symbol]

# print(btc_usdt_market)

# 获取单个交易对ticker数据
ticker_data = binance_exchange.fetchTicker(symbol)
print(ticker_data)
print('Ticker时刻：', ticker_data['datetime'])
print('Ticker价格：', ticker_data['last'])

# 获取多个交易对ticker数据
tickers_data = binance_exchange.fetchTickers(['BTC/USDT', 'ETH/USDT'])

binance_exchange.fetch_order_book(symbol)

# 获取上一次访问交易所的时间
binance_exchange.last_response_headers['Date']

print(binance_exchange.last_response_headers['Date'])

orderbook = binance_exchange.fetch_order_book(symbol)

# 最高买价
bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None

# 最低卖价
ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None

# 价差
spread = (ask - bid) if (bid and ask) else None

# 市场行情
print ('买价：{:.2f}, 卖价：{:.2f}, 价差：{:.2f}'.format(bid, ask, spread))


import pandas as pd

if binance_exchange.has['fetchOHLCV']:
    kline_data = pd.DataFrame(binance_exchange.fetch_ohlcv(symbol, timeframe='1m'))
    kline_data.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Vol']
    kline_data['Datetime'] = kline_data['Datetime'].apply(binance_exchange.iso8601)

print(kline_data.head())
kline_data.tail()
kline_data.shape

if binance_exchange.has['fetchOrders']:
    since = binance_exchange.parse8601('2021-05-06T00:00:00Z')
    end = binance_exchange.milliseconds() - 60 * 1000  # 前一分钟
    all_kline_data = []
    while since < end:
        symbol = 'BTC/USDT'
        kline_data = binance_exchange.fetch_ohlcv(symbol, since=since, timeframe='1m')
        print(binance_exchange.iso8601(since))
        if len(kline_data):
            # 更新获取时间
            since = kline_data[len(kline_data) - 1][0]
            all_kline_data += kline_data
        else:
            break

all_kline_data_df = pd.DataFrame(all_kline_data)
all_kline_data_df.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Vol']
all_kline_data_df['Datetime'] = all_kline_data_df['Datetime'].apply(binance_exchange.iso8601)

all_kline_data_df.shape
all_kline_data_df.head()
all_kline_data_df.tail()
all_kline_data_df[all_kline_data_df['Datetime'].duplicated()]

all_kline_data_df.drop_duplicates(subset=['Datetime'], inplace=True)
all_kline_data_df['Datetime'] = pd.to_datetime(all_kline_data_df['Datetime'] )
all_kline_data_df.set_index('Datetime', inplace=True)

import matplotlib.pyplot as plt

all_kline_data_df['Open'].plot(figsize=(15, 8))

