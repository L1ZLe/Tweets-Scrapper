import requests
import datetime
import pandas as pd
import numpy as np

def gget_binance_data_by_requests(ticker='ETHUSDT', interval='4h', start='2020-01-01 00:00:00', end='2023-07-01 00:00:00'):
  """
  interval: str tick interval - 4h/1h/1d ...
  """
  columns = ['open_time','open', 'high', 'low', 'close', 'volume','close_time', 'qav','num_trades','taker_base_vol','taker_quote_vol', 'ignore']
  usecols=['open', 'high', 'low', 'close', 'volume', 'qav','num_trades','taker_base_vol','taker_quote_vol']
  start = int(datetime.datetime.timestamp(pd.to_datetime(start))*1000)
  end_u = int(datetime.datetime.timestamp(pd.to_datetime(end))*1000)
  df = pd.DataFrame()
  print(f'Downloading {interval} {ticker} ohlc-data ...', end=' ')
  while True:
    url = f'https://www.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit=1000&startTime={start}#&endTime={end_u}'
    data = pd.DataFrame(requests.get(url, headers={'Cache-Control': 'no-cache', "Pragma": "no-cache"}).json(), columns=columns, dtype=np.float64)    
    start = int(data.open_time.tolist()[-1])+1
    data.index = [pd.to_datetime(x, unit='ms').strftime('%Y-%m-%d %H:%M:%S') for x in data.open_time]
    data = data[usecols]
    df = pd.concat([df, data], axis=0)
    if end in data.index.tolist():
      break
  print('Done.')
  df.index = pd.to_datetime(df.index)
  df = df.loc[:end]
  df.to_csv(f'{ticker}_price.csv')
  print("Data saved to csv file")
  return df[['open', 'high', 'low', 'close']]


