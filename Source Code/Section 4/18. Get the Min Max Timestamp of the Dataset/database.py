from typing import *
import logging

import h5py
import numpy as np


logger = logging.getLogger()


class Hdf5Client:
    def __init__(self, exchange: str):
        self.hf = h5py.File(f"data/{exchange}.h5", 'a')
        self.hf.flush()

    def create_dataset(self, symbol: str):
        if symbol not in self.hf.keys():
            self.hf.create_dataset(symbol, (0, 6), maxshape=(None, 6), dtype="float64")
            self.hf.flush()

    def write_data(self, symbol: str, data: List[Tuple]):

        min_ts, max_ts = self.get_first_last_timestamp(symbol)

        if min_ts is None:
            min_ts = float("inf")
            max_ts = 0

        filtered_data = []

        for d in data:
            if d[0] < min_ts:
                filtered_data.append(d)
            elif d[0] > max_ts:
                filtered_data.append(d)

        if len(filtered_data) == 0:
            logger.warning("%s: No data to insert", symbol)
            return

        data_array = np.array(filtered_data)

        self.hf[symbol].resize(self.hf[symbol].shape[0] + data_array.shape[0], axis=0)
        self.hf[symbol][-data_array.shape[0]:] = data_array

        self.hf.flush()

    def get_first_last_timestamp(self, symbol: str) -> Union[Tuple[None, None], Tuple[float, float]]:

        existing_data = self.hf[symbol][:]

        if len(existing_data) == 0:
            return None, None

        first_ts = min(existing_data, key=lambda x: x[0])[0]
        last_ts = max(existing_data, key=lambda x: x[0])[0]

        return first_ts, last_ts






