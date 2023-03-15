from argparse import ArgumentParser
from datetime import datetime
import python_bitbankcc
import json
# import numpy as np
import pandas as pd
import ta
from technical_analysys import Technical
import time

def order(private, order_side):
    private.order(
		pair='btc_jpy', # ペア
		price=None, # 価格 (成行注文の場合は None にする)
		amount='0.0001', # 注文枚数
		side=order_side, # 注文サイド (buy|sell)
		order_type='market', # 注文タイプ (limit|market|stop|stop_limit)
		# 以降は任意の引数
		# False, # post_only 注文、デフォは False, None も可能で Falseと同じ挙動
		# '151594' # trigger_price 逆指値などのトリガー価格
	)

def get_price(public, pair='btc_jpy', candle_type='4hour', date='20230215'):
    chart = []
    """
    candle_typeで指定できる期間: 1min, 5min, 15min, 30min, 1hour, 4hour, 8hour, 12hour, 1day, 1week, 1month

    [bitbankのAPIからビットコインの価格を取得する]
    読み込むデータの構造
    {
      "success": 0,
      "data": {
        "candlestick": [
          {
            "type": "string",
            "ohlcv": [
              [
                "string"[始値, 高値, 安値, 終値, 出来高, UnixTimeのミリ秒]
              ]
            ]
          }
        ]
      }
    }
    """

    val = public.get_candlestick(
        pair,
        candle_type,
        date
    )
    for i in val['candlestick'][0]['ohlcv']:
        chart.append(int(i[3]))

    return chart


# marketの場合、価格の指定は気にしなくてもいい。数量の設定に注意！！
if __name__ == '__main__':
    perser = ArgumentParser()
    perser.add_argument('api_key', help='bitbank api key')
    perser.add_argument('secret_key', help='bitbank secret key')
    args = perser.parse_args()

    api_key = args.api_key  # bitbankからAPIキーを発行する
    secret_key = args.secret_key
    public = python_bitbankcc.public()
    private = python_bitbankcc.private(api_key=api_key, api_secret=secret_key)
    
    analysys = Technical()
    while True:
        try:
            day = datetime.now()
            year = day.strftime('%Y')
            chart = get_price(public=public, date=year)
            signal = analysys.macd(chart)
            if signal == 'buy':
                order(private, signal)
            elif signal == 'sell':
                order(private, signal)
            print('取引中…')
        except Exception as e:
            print('取引失敗')
            print(e)
        time.sleep(14400)
