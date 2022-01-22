from typing import *

import h5py
import numpy as np


class Hdf5Client:
    def __init__(self, exchange: str):
        self.hf = h5py.File(f"data/{exchange}.h5", 'a')
        self.hf.flush()

    def create_dataset(self, symbol: str):
        if symbol not in self.hf.keys():
            self.hf.create_dataset(symbol, (0, 6), maxshape=(None, 6), dtype="float64")
            self.hf.flush()

    def write_data(self, symbol: str, data: List[Tuple]):

        data_array = np.array(data)

        self.hf[symbol].resize(self.hf[symbol].shape[0] + data_array.shape[0], axis=0)
        self.hf[symbol][-data_array.shape[0]:] = data_array

        self.hf.flush()