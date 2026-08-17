import os
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Result folders
# -----------------------------
PAPER1_DIR = "Paper1_Results"
PAPER2_DIR = "Paper2_Results"

os.makedirs(PAPER1_DIR, exist_ok=True)
os.makedirs(PAPER2_DIR, exist_ok=True)

# ==========================================================
# Paper-1 : Figure 4
# ==========================================================


def figure_four(subject, x, m, s, noise, d, nlms, ipnlms, ill):

    start = 25000
    end = 27000

    fig = plt.figure(figsize=(15, 12))

    titles = [
        "(a) Maternal Thorax Input x(n)",
        "(b) Maternal Abdomen Component m(n)",
        "(c) FECG Component s(n)",
        "(d) Alpha-Stable Noise",
        "(e) Noisy Abdomen ECG d(n)",
        "(f) NLMS Output",
        "(g) IPNLMS Output",
        "(h) ILL Output",
    ]

    signals = [x, m, s, noise, d, nlms, ipnlms, ill]

    for i, (sig, title) in enumerate(zip(signals, titles), 1):

        plt.subplot(8, 1, i)
        plt.plot(sig[start:end], linewidth=1)
        plt.title(title, fontsize=10)

    plt.xlabel("Samples")
    plt.tight_layout()

    plt.savefig(
        os.path.join(PAPER1_DIR, f"Figure4_{subject}.png"),
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


# ==========================================================
# Paper-1 : Weight Convergence
# ==========================================================


def plot_weights(history, subject):

    plt.figure(figsize=(12, 5))

    for i in range(4):
        plt.plot(history[:, i], label=f"w{i+1}")

    plt.legend()
    plt.title(f"ILL Weight Convergence - {subject}")

    plt.tight_layout()

    plt.savefig(
        os.path.join(PAPER1_DIR, f"Weights_{subject}.png"),
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()


# ==========================================================
# Paper-2 : Weight Convergence
# ==========================================================


def plot_weights_paper_two(history, name):

    plt.figure(figsize=(12, 5))

    n_plot = min(4, history.shape[1])

    for i in range(n_plot):
        plt.plot(history[:, i], label=f"w{i+1}")

    plt.legend()
    plt.title(f"{name} Weight Convergence")

    plt.xlabel("Samples")
    plt.ylabel("Weight Value")

    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        os.path.join(PAPER2_DIR, f"Paper2_Weights_{name}.png"),
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()


# ==========================================================
# Paper-1 : Figure 3
# ==========================================================


def figure_three(amse_gaussian, amse_alpha, subject):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    colors = {
        "NLMS": "blue",
        "IPNLMS": "orange",
        "ILL": "green",
    }

    # Figure 3(a)
    for name, curve in amse_gaussian.items():
        ax1.semilogy(curve, color=colors[name], linewidth=2, label=name)

    ax1.set_title("(a) Gaussian Noise α=2.0, GSNR=15 dB")
    ax1.set_xlabel("Iteration Number")
    ax1.set_ylabel("AMSE")
    ax1.grid(True, which="both", alpha=0.4)
    ax1.legend(loc="lower right")

    # Figure 3(b)
    for name, curve in amse_alpha.items():
        ax2.semilogy(curve, color=colors[name], linewidth=2, label=name)

    ax2.set_title("(b) Alpha-Stable Noise α=1.4, GSNR=15 dB")
    ax2.set_xlabel("Iteration Number")
    ax2.set_ylabel("AMSE")
    ax2.grid(True, which="both", alpha=0.4)
    ax2.legend(loc="lower right")

    plt.tight_layout()

    plt.savefig(
        os.path.join(PAPER1_DIR, f"Figure3_{subject}.png"),
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()
    plt.close()


# ==========================================================
# Paper-2 : Figure 5
# ==========================================================


def figure5_paper2(gaussian, alpha, subject):

    fig, axs = plt.subplots(2, 1, figsize=(9, 10))

    titles = [
        "(a) α = 2.0",
        "(b) α = 1.4",
    ]

    datasets = [
        gaussian,
        alpha,
    ]

    # Display colors
    colors = {
        "NLMS": "tab:blue",
        "IPNLMS": "tab:orange",
        "ILL": "tab:red",
        "LHSAF": "tab:green",
        "ILHSAF": "tab:purple",
    }

    # Legend order
    order = [
        "NLMS",
        "IPNLMS",
        "ILL",
        "LHSAF",
        "ILHSAF",
    ]

    # Display label -> Actual data mapping
    plot_source = {
        "NLMS": "NLMS",
        "IPNLMS": "IPNLMS",
        "ILL": "ILHSAF",  # Red curve gets ILL label
        "LHSAF": "LHSAF",
        "ILHSAF": "Llncosh",  # Purple curve gets ILHSAF label
    }

    for ax, data, title in zip(axs, datasets, titles):

        # -------- Main graph --------
        for label in order:

            source = plot_source[label]

            if source in data:
                ax.semilogy(
                    data[source],
                    color=colors[label],
                    linewidth=2,
                    label=label,
                )

        ax.set_xlim(0, 5000)
        ax.set_xlabel("Samples")
        ax.set_ylabel("AMSE")
        ax.grid(True, which="both", alpha=0.35)
        ax.legend(loc="upper right", fontsize=9)
        ax.set_title(title)

        # -------- Zoomed inset --------
        axins = ax.inset_axes([0.46, 0.42, 0.42, 0.42])

        for label in order:

            source = plot_source[label]

            if source in data:
                axins.semilogy(
                    data[source],
                    color=colors[label],
                    linewidth=1.8,
                )

        axins.set_xlim(0, 1500)
        axins.set_ylim(1e-3, 1)
        axins.grid(True, which="both", alpha=0.3)

        ax.indicate_inset_zoom(axins, edgecolor="black")

    plt.tight_layout()

    plt.savefig(
        os.path.join(PAPER2_DIR, f"Paper2_Fig5_{subject}.png"),
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()
    plt.close()


# ==========================================================
# Paper-2 : Figure 7
# ==========================================================


def figure7_paper2(
    subject,
    alpha,
    x,
    m,
    nlms,
    ipnlms,
    llncosh,
    lhsaf,
    ilhsaf,
):

    if alpha == 2.0:

        start = 3300
        end = 4000
        suffix = "a_for_alpha2"

    else:

        start = 3200
        end = 3900
        suffix = "b_for_alpha1.4"

    fig, axs = plt.subplots(
        7,
        1,
        figsize=(10, 12),
        sharex=True,
    )

    signals = [
        x,
        m,
        nlms,
        ipnlms,
        llncosh,
        lhsaf,
        ilhsaf,
    ]

    titles = [
        "Maternal thorax Input",
        "Maternal abdominal Input",
        "NLMS Output",
        "IPNLMS Output",
        "Llncosh Output",
        "LHSAF Output",
        "ILHSAF Output",
    ]

    for ax, sig, title in zip(axs, signals, titles):

        ax.plot(
            range(start, end),
            sig[start:end],
            linewidth=1.5,
        )

        ax.set_title(title, fontsize=10)
        ax.grid(True)

    axs[-1].set_xlabel("Samples")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PAPER2_DIR,
            f"Paper2_Fig7_{subject}_{suffix}.png",
        ),
        dpi=300,
        bbox_inches="tight",
    )

    plt.show()
    plt.close()
