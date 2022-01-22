from typing import *
import logging

import time

from utils import *
from exchanges.binance import BinanceClient
from exchanges.ftx import FtxClient


logger = logging.getLogger()


def collect_all(client: Union[BinanceClient, FtxClient], exchange: str, symbol: str):

    oldest_ts, most_recent_ts = None, None

    # Initial Request

    if oldest_ts is None:
        data = client.get_historical_data(symbol, end_time=int(time.time() * 1000) - 60000)

        if len(data) == 0:
            logger.warning("%s %s: no initial data found", exchange, symbol)
            return
        else:
            logger.info("%s %s: Collected %s initial data from %s to %s", exchange, symbol, len(data),
                        ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))

        oldest_ts = data[0][0]
        most_recent_ts = data[-1][0]

    # Most recent data

    # Older data