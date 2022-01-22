import h5py


class Hdf5Client:
    def __init__(self, exchange: str):
        self.hf = h5py.File(f"data/{exchange}.h5", 'a')
        self.hf.flush()

    def create_dataset(self, symbol: str):
        if symbol not in self.hf.keys():
            self.hf.create_dataset(symbol, (0, 6), maxshape=(None, 6), dtype="float64")
            self.hf.flush()