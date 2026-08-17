import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import levy_stable
import wfdb

record = wfdb.rdrecord("sub01_snr06dB_l1_c0_fecg1")

fecg = wfdb.rdrecord("sub01_snr06dB_l1_c0_fecg1").p_signal

mecg = wfdb.rdrecord("sub01_snr06dB_l1_c0_mecg").p_signal

noise1 = wfdb.rdrecord("sub01_snr06dB_l1_c0_noise1").p_signal

noise2 = wfdb.rdrecord("sub01_snr06dB_l1_c0_noise2").p_signal


print(fecg.shape)
print(mecg.shape)
print(noise1.shape)
print(noise2.shape)

def geometric_power(signal):
    eps = 1e-12
    return np.exp(np.mean(np.log(np.abs(signal) + eps)))


def alpha_stable_noise(signal, alpha, gsnr_db=15, beta=0, seed=42):

    rng = np.random.default_rng(seed)

    Cg = 1.78

    S0 = geometric_power(signal)

    gamma = S0 / (Cg * (10 ** (gsnr_db / 20)))

    noise = levy_stable.rvs(
        alpha=alpha, beta=beta, loc=0, scale=gamma, size=signal.shape, random_state=rng
    )

    return noise, gamma


fecg_abd = fecg[:, :32]
mecg_abd = mecg[:, :32]

d_clean = fecg_abd + 0.2 * mecg_abd

noise14, gamma14 = alpha_stable_noise(d_clean, alpha=1.4, gsnr_db=15)

print("Gamma:", gamma14)
print("shape of d_clean : ",d_clean.shape)
print("Shape of noise : ", noise14.shape)

alphas = [2.0, 1.8, 1.6, 1.4]

plt.figure(figsize=(14, 10))

for i, a in enumerate(alphas):

    noise, g = alpha_stable_noise(d_clean, a, 15)

    plt.subplot(4, 1, i + 1)
    plt.plot(noise[:2000, 0])
    plt.title(f"alpha={a}, gamma={g:.5f}")

plt.tight_layout()
plt.show()

# ch = 2

# plt.figure(figsize=(14, 8))

# plt.subplot(3, 1, 1)
# plt.plot(d_clean[:, ch])
# plt.title("Clean Abdominal Signal")

# plt.subplot(3, 1, 2)
# plt.plot(noise14[:, ch])
# plt.title("Alpha-stable Noise (alpha=1.4)")

# plt.subplot(3, 1, 3)
# plt.plot((d_clean + noise14)[:, ch])
# plt.title("Noisy Abdominal Signal")

# plt.tight_layout()
# plt.show()
