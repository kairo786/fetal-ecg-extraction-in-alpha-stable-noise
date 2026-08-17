import numpy as np


def align_reference(x, m):

    corr = np.correlate(m, x, mode="full")

    delay = np.argmax(corr) - (len(x) - 1)

    x_aligned = np.roll(x, delay)

    return x_aligned, delay
