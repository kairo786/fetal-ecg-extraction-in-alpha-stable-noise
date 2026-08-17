import wfdb
import matplotlib.pyplot as plt

# Read mECG signal
mecg = wfdb.rdrecord("sub01_snr06dB_l1_c0_mecg").p_signal

print("mECG Shape:", mecg.shape)

# Plot Channel 33 and 34
fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# Channel 33 (index 32)
axes[0].plot(mecg[:, 32], linewidth=0.8)
axes[0].set_title("mECG - Channel 33")
axes[0].set_ylabel("Amplitude")
axes[0].grid(True)

# Channel 34 (index 33)
axes[1].plot(mecg[:, 33], linewidth=0.8)
axes[1].set_title("mECG - Channel 34")
axes[1].set_xlabel("Sample")
axes[1].set_ylabel("Amplitude")
axes[1].grid(True)

plt.suptitle("mECG Signals (Channels 33 & 34)", fontsize=14)
plt.tight_layout()
plt.show()
