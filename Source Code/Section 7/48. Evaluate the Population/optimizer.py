import random
import typing

from utils import STRAT_PARAMS, resample_timeframe, get_library

from database import Hdf5Client
from models import BacktestResult

import strategies.obv
import strategies.ichimoku
import strategies.support_resistance


class Nsga2:
    def __init__(self, exchange: str, symbol: str, strategy: str, tf: str, from_time: int, to_time: int,
                 population_size: int):
        self.exchange = exchange
        self.symbol = symbol
        self.strategy = strategy
        self.tf = tf
        self.from_time = from_time
        self.to_time = to_time
        self.population_size = population_size

        self.params_data = STRAT_PARAMS[strategy]

        if self.strategy in ["obv", "ichimoku", "sup_res"]:
            h5_db = Hdf5Client(exchange)
            self.data = h5_db.get_data(symbol, from_time, to_time)
            self.data = resample_timeframe(self.data, tf)

        elif self.strategy in ["psar", "sma"]:

            self.lib = get_library()

            if self.strategy == "sma":
                self.obj = self.lib.Sma_new(exchange.encode(), symbol.encode(), tf.encode(), from_time, to_time)
            elif self.strategy == "psar":
                self.obj = self.lib.Psar_new(exchange.encode(), symbol.encode(), tf.encode(), from_time, to_time)

    def create_initial_population(self) -> typing.List[BacktestResult]:

        population = []

        while len(population) < self.population_size:
            backtest = BacktestResult()
            for p_code, p in self.params_data.items():
                if p["type"] == int:
                    backtest.parameters[p_code] = random.randint(p["min"], p["max"])
                elif p["type"] == float:
                    backtest.parameters[p_code] = round(random.uniform(p["min"], p["max"]), p["decimals"])

            if backtest not in population:
                population.append(backtest)

        return population

    def evaluate_population(self, population: typing.List[BacktestResult]) -> typing.List[BacktestResult]:

        if self.strategy == "obv":

            for bt in population:
                bt.pnl, bt.max_dd = strategies.obv.backtest(self.data, ma_period=bt.parameters["ma_period"])

            return population

        elif self.strategy == "ichimoku":

            for bt in population:
                bt.pnl, bt.max_dd = strategies.ichimoku.backtest(self.data, tenkan_period=bt.parameters["tenkan"],
                                                                 kijun_period=bt.parameters["kijun"])

            return population

        elif self.strategy == "sup_res":

            for bt in population:
                bt.pnl, bt.max_dd = strategies.support_resistance.backtest(self.data, min_points=bt.parameters["min_points"],
                                                                           min_diff_points=bt.parameters["min_diff_points"],
                                                                           rounding_nb=bt.parameters["rounding_nb"],
                                                                           take_profit=bt.parameters["take_profit"],
                                                                           stop_loss=bt.parameters["stop_loss"])

            return population

        elif self.strategy == "sma":

            for bt in population:
                self.lib.Sma_execute_backtest(self.obj, bt.parameters["slow_ma"], bt.parameters["fast_ma"])
                bt.pnl = self.lib.Sma_get_pnl(self.obj)
                bt.max_dd = self.lib.Sma_get_max_dd(self.obj)

            return population

        elif self.strategy == "psar":

            for bt in population:
                self.lib.Psar_execute_backtest(self.obj, bt.parameters["initial_acc"], bt.parameters["acc_increment"],
                                               bt.parameters["max_acc"])
                bt.pnl = self.lib.Psar_get_pnl(self.obj)
                bt.max_dd = self.lib.Psar_get_max_dd(self.obj)

            return population








