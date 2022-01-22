import datetime
from ctypes import *

import pandas as pd


TF_EQUIV = {"1m": "1Min", "5m": "5Min", "15m": "15Min", "30m": "30Min", "1h": "1H", "4h": "4H", "12h": "12H", "1d": "D"}

STRAT_PARAMS = {
    "obv": {
        "ma_period": {"name": "MA Period", "type": int},
    },
    "ichimoku": {
        "kijun": {"name": "Kijun Period", "type": int},
        "tenkan": {"name": "Tenkan Period", "type": int},
    },
    "sup_res": {
        "min_points": {"name": "Min. Points", "type": int},
        "min_diff_points": {"name": "Min. Difference between Points", "type": int},
        "rounding_nb": {"name": "Rounding Number", "type": float},
        "take_profit": {"name": "Take Profit %", "type": float},
        "stop_loss": {"name": "Stop Loss %", "type": float},
    },
    "sma": {
        "slow_ma": {"name": "Slow MA Period", "type": int},
        "fast_ma": {"name": "Fast MA Period", "type": int},
    },
    "psar": {
        "initial_acc": {"name": "Initial Acceleration", "type": float},
        "acc_increment": {"name": "Acceleration Increment", "type": float},
        "max_acc": {"name": "Max. Acceleration", "type": float},
    },
}


def ms_to_dt(ms: int) -> datetime.datetime:
    return datetime.datetime.utcfromtimestamp(ms / 1000)


def resample_timeframe(data: pd.DataFrame, tf: str) -> pd.DataFrame:
    return data.resample(TF_EQUIV[tf]).agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    )


def get_library():
    lib = CDLL("backtestingCpp/build/libbacktestingCpp.dll", winmode=0)

    # SMA

    lib.Sma_new.restype = c_void_p
    lib.Sma_new.argtypes = [c_char_p, c_char_p, c_char_p, c_longlong, c_longlong]
    lib.Sma_execute_backtest.restype = c_void_p
    lib.Sma_execute_backtest.argtypes = [c_void_p, c_int, c_int]

    lib.Sma_get_pnl.restype = c_double
    lib.Sma_get_pnl.argtypes = [c_void_p]
    lib.Sma_get_max_dd.restype = c_double
    lib.Sma_get_max_dd.argtypes = [c_void_p]

    # PSAR

    lib.Psar_new.restype = c_void_p
    lib.Psar_new.argtypes = [c_char_p, c_char_p, c_char_p, c_longlong, c_longlong]
    lib.Psar_execute_backtest.restype = c_void_p
    lib.Psar_execute_backtest.argtypes = [c_void_p, c_double, c_double, c_double]

    lib.Psar_get_pnl.restype = c_double
    lib.Psar_get_pnl.argtypes = [c_void_p]
    lib.Psar_get_max_dd.restype = c_double
    lib.Psar_get_max_dd.argtypes = [c_void_p]

    return lib
