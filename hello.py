import pyupbit  #베스트 케이 값 구하기
import numpy as np
import pprint


def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-BTC", count=60)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror


for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    pprint.pprint("%.1f %f" % (k, ror))