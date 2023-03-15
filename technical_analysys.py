import pandas as pd
import ta

class Technical:
    def __init__(self) -> None:
        pass

    def macd(self, price):
        close = pd.Series(price)
        macd = ta.trend.MACD(close)
        signal = macd.macd_diff()
        if signal.iloc[-1]>0 and signal.iloc[-2]<0:
            return 'buy'
        elif signal.iloc[-1]<0 and signal.iloc[-2]>0:
            return 'sell'
        else:
            return 'fail'
        
    def rsi(self, price):
        close = pd.Series(price)
        rsi = ta.momentum.RSIIndicator(close)
        
