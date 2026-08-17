from scipy.stats import levy_stable
import numpy as np

Cg = 1.78


def geometric_power(signal):

    eps = 1e-12

    return np.exp(np.mean(np.log(np.abs(signal) + eps)))


def verify_gsnr(signal, noise):

    S0 = geometric_power(signal)
    N0 = geometric_power(noise)

    return 20 * np.log10(S0 / N0)


def generate_alpha_noise(signal, alpha, target_gsnr=15, beta=0):

    gamma = 1.0

    for _ in range(12):

        noise = levy_stable.rvs(
            alpha, beta, scale=gamma, size=signal.shape, random_state=42,
        )

        current = verify_gsnr(signal, noise)

        gamma *= 10 ** ((current - target_gsnr) / 20)

    noise = levy_stable.rvs(
        alpha, beta, scale=gamma, size=signal.shape, random_state=42
    )

    return noise, gamma
