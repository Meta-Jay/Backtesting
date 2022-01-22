

import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)

def backtest(df: pd.DataFrame, min_point: int, min_diff_points: int, rounding_nb: float, take_profit: float, stop_loss: float)
    # Backtest with support_resistance: Long, if level breaks up the resistance and Short if breaks down the support