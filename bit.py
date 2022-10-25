import python_bitbankcc
import json
import numpy as np
import time

def get_price(public, pair='btc_jpy', candle_type='1hour', date='20220101'):
    chart = []
    """
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
        chart.append(i)

    return chart


# marketの場合、価格の指定は気にしなくてもいい。数量の設定に注意！！
if __name__ == '__main__':
    api_key = ''  # bitbankからAPIキーを発行する
    api_select = ''
    public = python_bitbankcc.public()
    private = python_bitbankcc.private(api_key=api_key, api_secret=api_select)
    while True:
        try:
            chart = get_price(public)
            print('取引中…')

        except Exception as e:
            print('取引失敗')
            print(e)
