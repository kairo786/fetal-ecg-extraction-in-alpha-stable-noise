import wfdb
import numpy as np

base = "sub01_snr06dB_l1_c0"

files = {
    "FECG": base + "_fecg1",
    "MECG": base + "_mecg",
    "Noise1": base + "_noise1",
    "Noise2": base + "_noise2",
}

for name, path in files.items():

    record = wfdb.rdrecord(path)
    x = record.p_signal

    print("\n-----------------------")
    print(name)
    print("-----------------------")

    print("Shape       :", x.shape)
    print("Sampling Hz :", record.fs)
    print("Channels    :", record.n_sig)

    print("Min         :", np.min(x))
    print("Max         :", np.max(x))
    print("Mean        :", np.mean(x))
    print("Std         :", np.std(x))
