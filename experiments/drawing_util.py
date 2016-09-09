import numpy as np

def get_data_from_file(filename):
    data = np.loadtxt(filename, skiprows=1, delimiter=",", usecols=range(1,5), unpack=True)
