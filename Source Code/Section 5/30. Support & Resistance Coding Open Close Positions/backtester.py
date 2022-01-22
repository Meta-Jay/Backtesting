from database import Hdf5Client

from utils import resample_timeframe
import strategies.obv
import strategies.ichimoku
import strategies.support_resistance


def run(exchange: str, symbol: str, strategy: str, tf: str, from_time: int, to_time: int):

    if strategy == "obv":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)

        print(strategies.obv.backtest(data, 9))

    elif strategy == "ichimoku":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)

        print(strategies.ichimoku.backtest(data, tenkan_period=9, kijun_period=26))

    elif strategy == "sup_res":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)

        print(strategies.support_resistance.backtest(data, min_points=3, min_diff_points=7, rounding_nb=400,
                                                     take_profit=3, stop_loss=3))
