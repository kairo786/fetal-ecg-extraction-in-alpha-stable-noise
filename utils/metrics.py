import numpy as np


def rmse(true, pred):

    return np.sqrt(np.mean((true - pred) ** 2))


def prd(true, pred):

    return 100 * np.sqrt(np.sum((true - pred) ** 2) / np.sum(true**2))


def geometric_power(signal):

    eps = 1e-12

    return np.exp(np.mean(np.log(np.abs(signal) + eps)))


def snr(true, pred):
    # S0 = geometric_power(true);
    # N0 = geometric_power(true-pred);
    # noise = true - pred
    noise = pred -true
    return 10 * np.log10(np.sum(true**2) / np.sum(noise**2))
    # return 20 * np.log10(S0 / N0)


def amse(true, pred):

    return np.mean((true - pred) ** 2)


def amse_curve(target, estimate):

    err = (target - estimate) ** 2

    return np.cumsum(err) / np.arange(1, len(err) + 1)
