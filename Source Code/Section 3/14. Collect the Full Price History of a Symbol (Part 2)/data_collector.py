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

    while True:

        data = client.get_historical_data(symbol, start_time=int(most_recent_ts + 60000))

        if data is None:
            time.sleep(4)  # Pause in case an error occurs during the request
            continue

        if len(data) < 2:
            break

        data = data[:-1]

        if data[-1][0] > most_recent_ts:
            most_recent_ts = data[-1][0]

        logger.info("%s %s: Collected %s recent data from %s to %s", exchange, symbol, len(data),
                    ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))

        time.sleep(1.1)

    # Older data

    while True:

        data = client.get_historical_data(symbol, end_time=int(oldest_ts - 60000))

        if data is None:
            time.sleep(4)  # Pause in case an error occurs during the request
            continue

        if len(data) == 0:
            logger.info("%s %s: Stopped older data collection because no data was found before %s", exchange, symbol,
                        ms_to_dt(oldest_ts))
            break

        if data[0][0] < oldest_ts:
            oldest_ts = data[0][0]

        logger.info("%s %s: Collected %s older data from %s to %s", exchange, symbol, len(data),
                    ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))

        time.sleep(1.1)




