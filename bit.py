import ccxt
import json
import numpy as np
import talib
import requests
import time

def get_price(period):
    char = np.zeros(0)
    """[CoinGeckoのAPIからビットコインの価格を取得する関数]
    Arguments:
        ticker {[str]} -- [各仮想通貨のticker(例：bitcoin・ethereum・ripple…)]
    Returns:
        [DataFrame] -- [日付・価格・変化率のデータフレーム]
    """

    # APIから価格データを取得する
    url = 'https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc?periods=' \
          + str(period) + '&after=' + str(int(time.time() - 30*24*60*60))
    r = requests.get(url)
    r = json.loads(r.text)

    # jsonをデータフレームに変換
    # ここでのpriceは終値
    # 出来高加重平均価格　VW-MACDというのもある(priceの部分)
    for i in r['result'][str(period)]:
        char = np.append(char, i[4])

    return char

def order_buy(side, trade):
    """[ビットコインを注文する関数]
    Argument:
        [str]  -- [注文サイド(buy or sell))]
    Returns:
        [json] -- [注文内容]
    type:
        指値ならlimit、成行ならmarket
    """
    # priceは成り行き注文でも入れる
    order = trade.create_order(symbol='BTC/JPY',  # ペア
                               price='100',  # 価格
                               amount='0.0001',  # 注文枚数(bitcoin)
                               side=side,  # 注文サイド
                               type='market'  # 注文タイプ
                               )
    return order

def mac_d(price, trade):
    # 終値を持ってくる↑
    macd, macdsignal, macdhist = talib.MACD(price, fastperiod=24, slowperiod=52, signalperiod=18)
    # fast-> 期間の短い指数移動平均 slow-> 期間の長い指数移動平均 sig-> 移動平均を求める個数
    # MACD = slow - fast となる
    '''
    持ってくるデータの時間間隔(日足, 15分足とか)でもMACDの性能が変化する。詳しくは<https://www.higedura24.com/macd-parameter-point>
    get_price()から持ってくるデータを変えるとスマホで見ている15分足とか日足とかのMACDを表示できる。
    
    macd+macsignal<0なら下げ
    macd+macsignal>0なら上げ
    macd+macsignal==0ならデッドorゴールデンクロス
    '''
    # -> 上げ ->　クロス ->　下げ デッドクロス

    # print(macd)　確認用
    """
        for i in range(-10, 0):
        print(macd[i]-macdsignal[i])
    """
    # print(order_buy('buy', trade))　確認用

    if macd[-3] - macdsignal[-3] > 0 and macd[-2] - macdsignal[-2] >= 0 and macd[-1] - macdsignal[-1] < 0:
        try:
            print(order_buy('sell', trade))
        except Exception as e:
            print('売却失敗')
            print(e)
        # -> 下げ ->　クロス ->　上げ ゴールデンクロス
    elif macd[-3] - macdsignal[-3] < 0 and macd[-2] - macdsignal[-2] <= 0 and macd[-1] - macdsignal[-1] > 0:
        try:
            print(order_buy('buy', trade))
        except Exception as e:
            print('購入失敗')
            print(e)


API_KEY = ''  # bitbankからAPIキーを発行する
API_SECRET = ''
prv = ccxt.bitbank({
    'apiKey': API_KEY,
    'secret': API_SECRET})

# marketの場合、価格の指定は気にしなくてもいい。数量の設定に注意！！
# value = prv.order('btc_jpy', '100', '0.0001', 'sell', 'market')　確認用

# 14400秒 -> 4時間
# print(order_buy('buy', prv)) 確認用

if __name__ == '__main__':
    while True:
        try:
            chart = get_price(14400)
            mac_d(chart, prv)
            print('取引中…')
        except Exception as ee:
            print('取引失敗')
            print(ee)
        time.sleep(14400)

