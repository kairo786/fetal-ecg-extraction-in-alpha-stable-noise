# import numpy as np
# import pandas as pd

# from utils.loader import load_subject
# from utils.noise import generate_alpha_noise
# from utils.filters import ill_filter, nlms_filter, ipnlms_filter
# from utils.metrics import rmse, prd, snr, amse
# from utils.plotting import figure_four, plot_weights ,figure_three
# from utils.metrics import amse_curve

# subjects = ["sub01", "sub03", "sub05", "sub07"]
# alphas = [2.0, 1.8, 1.6, 1.4]

# rows = []


# def choose_best_reference(mecg, abdomen_signal):

#     ref33 = mecg[:, 32]
#     ref34 = mecg[:, 33]

#     c33 = abs(np.corrcoef(ref33, abdomen_signal)[0, 1])
#     c34 = abs(np.corrcoef(ref34, abdomen_signal)[0, 1])

#     if c33 >= c34:
#         return ref33 - np.mean(ref33), 33, c33

#     return ref34 - np.mean(ref34), 34, c34


# for subject in subjects:

#     print("=" * 60)
#     print(subject.upper())
#     print("=" * 60)

#     data = load_subject(subject)

#     fecg = data["fecg"]
#     mecg = data["mecg"]

#     amse_gaussian={}
#     amse_alpha={}

#     # x, ref_channel, corr = choose_best_reference(mecg, m)

#     for alpha in alphas:

#         print(f"Alpha={alpha}")

#         channel_results = []

#         for ch in range(4):

#             s = fecg[:, ch]
#             m = mecg[:, ch]

#             x, ref_channel, corr = choose_best_reference(mecg, m)

#             clean = s + m

#             noise, _ = generate_alpha_noise(clean, alpha, 15)

#             d = clean + noise

#             algorithms = {
#                 "NLMS": nlms_filter(x, d), # y ,e,w,h
#                 "IPNLMS": ipnlms_filter(x, d),
#                 "ILL": ill_filter(x, d, m),
#             }

#             skip = 5000

#             # ideal = d - m
#             ideal = s + noise

#             for name, (y, e, w, h) in algorithms.items():

#                 channel_results.append(
#                     {
#                         "Subject": subject,
#                         "Alpha": alpha,
#                         "Channel": ch + 1,
#                         "Algorithm": name,
#                         "RMSE": rmse(s[skip:], e[skip:]),
#                         "PRD": prd(s[skip:], e[skip:]),
#                         "SNR": snr(s[skip:], e[skip:]),
#                         "AMSE": amse(s[skip:], e[skip:]),
#                     }
#                 )

#             if subject == "sub01" and alpha == 1.4 and ch == 0:

#                 figure_four(
#                     subject,
#                     x,
#                     m,
#                     s,
#                     noise,
#                     d,
#                     algorithms["NLMS"][1],
#                     algorithms["IPNLMS"][1],
#                     algorithms["ILL"][1],
#                 )

#                 plot_weights(algorithms["ILL"][3], subject)


#             if subject == "sub01" and ch == 0:

#                 if alpha == 2.0:

#                     amse_gaussian = {
#                   "NLMS": amse_curve(ideal, algorithms["NLMS"][1]),
#                   "IPNLMS": amse_curve(ideal, algorithms["IPNLMS"][1]),
#                   "ILL": amse_curve(ideal, algorithms["ILL"][1]),
#                     }

#                 if alpha == 1.4:

#                     amse_alpha = {
#                  "NLMS": amse_curve(ideal, algorithms["NLMS"][1]),
#                  "IPNLMS": amse_curve(ideal, algorithms["IPNLMS"][1]),
#                  "ILL": amse_curve(ideal, algorithms["ILL"][1]),
#                    }

#                 if subject=="sub01" and alpha==1.4 and ch==0:
#                   figure_three(amse_gaussian, amse_alpha, "sub01")

#         df_channel = pd.DataFrame(channel_results)

#         summary = df_channel.groupby("Algorithm")[["RMSE", "PRD", "SNR", "AMSE"]].mean()

#         print(summary)

#         for algo, row in summary.iterrows():

#             rows.append(
#                 {
#                     "Subject": subject,
#                     "Alpha": alpha,
#                     "Algorithm": algo,
#                     "RMSE": row["RMSE"],
#                     "PRD": row["PRD"],
#                     "SNR": row["SNR"],
#                     "AMSE": row["AMSE"],
#                 }
#             )

# final_table = pd.DataFrame(rows)

# print("\nFINAL TABLE")
# print(final_table)

# final_table.to_csv("Paper_TableII.csv", index=False)

# pivot = final_table.pivot_table(
#     index=["Subject", "Alpha"],
#     columns="Algorithm",
#     values=["RMSE", "PRD", "SNR", "AMSE"],
# )

# pivot.to_excel("Paper_TableII.xlsx")

# print("\nDone.")
# print("Generated:")
# print("Paper_TableII.csv")
# print("Paper_TableII.xlsx")
# print("Figure4_sub01.png")
# print("Weights_sub01.png")

import os
import numpy as np
import pandas as pd

from utils.loader import load_subject
from utils.noise import generate_alpha_noise
from utils.filters import ill_filter, nlms_filter, ipnlms_filter
from utils.metrics import rmse, prd, snr, amse, amse_curve
from utils.plotting import figure_four, plot_weights, figure_three

# ==========================================================
# Result Folder
# ==========================================================

PAPER1_DIR = "Paper1_Results"
os.makedirs(PAPER1_DIR, exist_ok=True)

subjects = ["sub01", "sub03", "sub05", "sub07"]
alphas = [2.0, 1.8, 1.6, 1.4]

rows = []


def choose_best_reference(mecg, abdomen_signal):

    ref33 = mecg[:, 32]
    ref34 = mecg[:, 33]

    c33 = abs(np.corrcoef(ref33, abdomen_signal)[0, 1])
    c34 = abs(np.corrcoef(ref34, abdomen_signal)[0, 1])

    if c33 >= c34:
        return ref33 - np.mean(ref33), 33, c33

    return ref34 - np.mean(ref34), 34, c34


for subject in subjects:

    print("=" * 60)
    print(subject.upper())
    print("=" * 60)

    data = load_subject(subject)

    fecg = data["fecg"]
    mecg = data["mecg"]

    amse_gaussian = {}
    amse_alpha = {}

    for alpha in alphas:

        print(f"Alpha={alpha}")

        channel_results = []

        for ch in range(4):

            s = fecg[:, ch]
            m = mecg[:, ch]

            x, ref_channel, corr = choose_best_reference(mecg, m)

            clean = s + m

            noise, _ = generate_alpha_noise(clean, alpha, 15)

            d = clean + noise

            algorithms = {
                "NLMS": nlms_filter(x, d),  # y,e,w,h
                "IPNLMS": ipnlms_filter(x, d),
                "ILL": ill_filter(x, d, m),
            }

            skip = 5000

            ideal = s + noise

            for name, (y, e, w, h) in algorithms.items():

                channel_results.append(
                    {
                        "Subject": subject,
                        "Alpha": alpha,
                        "Channel": ch + 1,
                        "Algorithm": name,
                        "RMSE": rmse(s[skip:], e[skip:]),
                        "PRD": prd(s[skip:], e[skip:]),
                        "SNR": snr(s[skip:], e[skip:]),
                        "AMSE": amse(s[skip:], e[skip:]),
                    }
                )

            # -----------------------------
            # Paper Figure 4 + Weights
            # -----------------------------
            if subject == "sub01" and alpha == 1.4 and ch == 0:

                figure_four(
                    subject,
                    x,
                    m,
                    s,
                    noise,
                    d,
                    algorithms["NLMS"][1],
                    algorithms["IPNLMS"][1],
                    algorithms["ILL"][1],
                )

                plot_weights(algorithms["ILL"][3], subject)

            # -----------------------------
            # Paper Figure 3
            # -----------------------------
            if subject == "sub01" and ch == 0:

                if alpha == 2.0:

                    amse_gaussian = {
                        "NLMS": amse_curve(ideal, algorithms["NLMS"][1]),
                        "IPNLMS": amse_curve(ideal, algorithms["IPNLMS"][1]),
                        "ILL": amse_curve(ideal, algorithms["ILL"][1]),
                    }

                if alpha == 1.4:

                    amse_alpha = {
                        "NLMS": amse_curve(ideal, algorithms["NLMS"][1]),
                        "IPNLMS": amse_curve(ideal, algorithms["IPNLMS"][1]),
                        "ILL": amse_curve(ideal, algorithms["ILL"][1]),
                    }

                    figure_three(
                        amse_gaussian,
                        amse_alpha,
                        "sub01",
                    )

        df_channel = pd.DataFrame(channel_results)

        summary = df_channel.groupby("Algorithm")[["RMSE", "PRD", "SNR", "AMSE"]].mean()

        print(summary)

        for algo, row in summary.iterrows():

            rows.append(
                {
                    "Subject": subject,
                    "Alpha": alpha,
                    "Algorithm": algo,
                    "RMSE": row["RMSE"],
                    "PRD": row["PRD"],
                    "SNR": row["SNR"],
                    "AMSE": row["AMSE"],
                }
            )

# ==========================================================
# Final Tables
# ==========================================================

final_table = pd.DataFrame(rows)

print("\nFINAL TABLE")
print(final_table)

csv_path = os.path.join(PAPER1_DIR, "Paper_TableII.csv")
xlsx_path = os.path.join(PAPER1_DIR, "Paper_TableII.xlsx")

final_table.to_csv(csv_path, index=False)

pivot = final_table.pivot_table(
    index=["Subject", "Alpha"],
    columns="Algorithm",
    values=["RMSE", "PRD", "SNR", "AMSE"],
)

pivot.to_excel(xlsx_path)

# ==========================================================
# Done
# ==========================================================

print("\nDone.")
print(f"All Paper-1 results saved in: {PAPER1_DIR}")
print("Generated:")
print(f"  - {csv_path}")
print(f"  - {xlsx_path}")
print("  - Figure3_sub01.png")
print("  - Figure4_sub01.png")
print("  - Weights_sub01.png")
