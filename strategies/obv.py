
import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)

def backtest(df: pd.DataFrame, ma_period: int):

    df["obv"]= (np.sign(df["close"].diff()) * df["volume"]).fillna(0).cumsum()      # fill N/A as 0, cumulative sum of volume data
    df["obv_ma"] = round(df["obv"].rolling(window=ma_period).mean(), 2)             # Moving average: averaging the last x data

    df["signal"] = np.where(df["obv"] > df["obv_ma"], 1, -1)
    df["close_change"] = df["close"].pct_change()
    df["signal_shift"] = df["signal"].shift(1)

    df["pnl"] = df["close"].pct_change() * df["signal"].shift(1)

    # The reason for shift is that signal is calculated only at the end of each period T. So PnL = (Close_T+1 -Close_T)*signal
    # Without shift, it would have been (Close_T -Close_T-1)*signal

    return df["pnl"].sum()
    print(df[1:50])