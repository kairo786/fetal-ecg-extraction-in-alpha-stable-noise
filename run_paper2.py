# import numpy as np
# import pandas as pd

# from utils.loader import load_subject
# from utils.noise import generate_alpha_noise
# from utils.filters import (
#     nlms_filter,
#     ipnlms_filter,
#     ill_filter,
#     llncosh_filter,
#     lhsaf_filter,
#     ilhsaf_filter,
# )

# from utils.metrics import (
#     rmse,
#     prd,
#     snr,
#     amse,
#     amse_curve,
# )

# from utils.plotting import (
#     figure5_paper2,
#     figure7_paper2,
#     plot_weights,
#     plot_weights_paper_two,
# )

# subjects = ["sub01", "sub03", "sub05", "sub07"]
# alphas = [2.0, 1.8, 1.6, 1.4]

# rows = []


# def choose_best_reference(mecg, m):

#     ref33 = mecg[:, 32]
#     ref34 = mecg[:, 33]

#     c33 = abs(np.corrcoef(ref33, m)[0, 1])
#     c34 = abs(np.corrcoef(ref34, m)[0, 1])

#     if c33 >= c34:
#         return ref33 - np.mean(ref33)

#     return ref34 - np.mean(ref34)


# for subject in subjects:

#     print("=" * 60)
#     print(subject.upper())
#     print("=" * 60)

#     data = load_subject(subject)

#     fecg = data["fecg"]
#     mecg = data["mecg"]

#     fig5_gaussian = {}
#     fig5_alpha = {}

#     for alpha in alphas:

#         channel_results = []

#         print(f"alpha={alpha}")

#         for ch in range(4):

#             s = fecg[:, ch]
#             m = mecg[:, ch]

#             x = choose_best_reference(mecg, m)

#             clean = s + m

#             noise, _ = generate_alpha_noise(clean, alpha, 15)

#             d = clean + noise

#             algorithms = {  # (y,e,w,h)
#                 "NLMS": nlms_filter(
#                     x,
#                     d,
#                     filter_len=180,
#                     mu=0.1,
#                 ),
#                 "IPNLMS": ipnlms_filter(
#                     x,
#                     d,
#                     filter_len=200,
#                     mu=0.04,
#                     alpha=0.2,
#                 ),
#                 "Llncosh": llncosh_filter(
#                     x,
#                     d,
#                     filter_len=7,
#                     mu=0.01,
#                     lam=10,
#                 ),
#                 "LHSAF": lhsaf_filter(
#                     x,
#                     d,
#                     filter_len=7,
#                     mu=0.02,
#                     lam=8,
#                 ),
#                 "ILHSAF": ilhsaf_filter(
#                     x,
#                     d,
#                     m,
#                     filter_len=7,
#                     mu=0.03,
#                 ),
#             }

#             skip = 5000

#             ideal = s + noise

#             for name, (y, e, w, h) in algorithms.items():

#                 channel_results.append(
#                     {
#                         "Subject": subject,
#                         "Alpha": alpha,
#                         "Channel": ch + 1,
#                         "Algorithm": name,
#                         "RMSE": rmse(ideal[skip:], e[skip:]),
#                         "PRD": prd(s[skip:], e[skip:]),
#                         "SNR": snr(ideal[skip:], e[skip:]),
#                         "AMSE": amse(s[skip:], e[skip:]),
#                     }
#                 )

#             # -------- Figure7 --------

#             if subject == "sub01" and alpha in [2.0, 1.4] and ch == 0:

#                 figure7_paper2(
#                     subject,
#                     alpha,
#                     x,
#                     m,
#                     algorithms["NLMS"][1],
#                     algorithms["IPNLMS"][1],
#                     algorithms["Llncosh"][1],
#                     algorithms["LHSAF"][1],
#                     algorithms["ILHSAF"][1],
#                 )

#             # -------- Figure5 --------

#             if subject == "sub01" and ch == 0:

#                 curves = {
#                     "NLMS": amse_curve(ideal, algorithms["NLMS"][1]),
#                     "IPNLMS": amse_curve(ideal, algorithms["IPNLMS"][1]),
#                     "Llncosh": amse_curve(ideal, algorithms["Llncosh"][1]),
#                     "LHSAF": amse_curve(ideal, algorithms["LHSAF"][1]),
#                     "ILHSAF": amse_curve(ideal, algorithms["ILHSAF"][1]),
#                 }

#                 if alpha == 2.0:
#                     fig5_gaussian = curves

#                 if alpha == 1.4:
#                     fig5_alpha = curves

#                 if alpha == 1.4:

#                     figure5_paper2(
#                         fig5_gaussian,
#                         fig5_alpha,
#                         subject,
#                     )

#                     plot_weights_paper_two(
#                         algorithms["ILHSAF"][3],
#                         f"Paper2_Weights_ILHSAF_{subject}",
#                     )

#         df = pd.DataFrame(channel_results)

#         summary = df.groupby("Algorithm")[["RMSE", "PRD", "SNR", "AMSE"]].mean()

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

# final_table.to_csv("Paper2_TableIII.csv", index=False)

# pivot = final_table.pivot_table(
#     index=["Subject", "Alpha"],
#     columns="Algorithm",
#     values=["RMSE", "PRD", "SNR", "AMSE"],
# )

# pivot.to_excel("Paper2_TableIII.xlsx")

# print("Done.")

import os
import numpy as np
import pandas as pd

from utils.loader import load_subject
from utils.noise import generate_alpha_noise
from utils.filters import (
    nlms_filter,
    ipnlms_filter,
    ill_filter,
    llncosh_filter,
    lhsaf_filter,
    ilhsaf_filter,
)

from utils.metrics import (
    rmse,
    prd,
    snr,
    amse,
    amse_curve,
)

from utils.plotting import (
    figure5_paper2,
    figure7_paper2,
    plot_weights_paper_two,
)

# ==========================================================
# Result Folder
# ==========================================================

PAPER2_DIR = "Paper2_Results"
os.makedirs(PAPER2_DIR, exist_ok=True)

subjects = ["sub01", "sub03", "sub05", "sub07"]
alphas = [2.0, 1.8, 1.6, 1.4]

rows = []


def choose_best_reference(mecg, m):

    ref33 = mecg[:, 32]
    ref34 = mecg[:, 33]

    c33 = abs(np.corrcoef(ref33, m)[0, 1])
    c34 = abs(np.corrcoef(ref34, m)[0, 1])

    if c33 >= c34:
        return ref33 - np.mean(ref33)

    return ref34 - np.mean(ref34)


for subject in subjects:

    print("=" * 60)
    print(subject.upper())
    print("=" * 60)

    data = load_subject(subject)

    fecg = data["fecg"]
    mecg = data["mecg"]

    fig5_gaussian = {}
    fig5_alpha = {}

    for alpha in alphas:

        print(f"alpha={alpha}")

        channel_results = []

        for ch in range(4):

            s = fecg[:, ch]
            m = mecg[:, ch]

            x = choose_best_reference(mecg, m)

            clean = s + m

            noise, _ = generate_alpha_noise(clean, alpha, 15)

            d = clean + noise

            algorithms = {  # (y, e, w, h)
                "NLMS": nlms_filter(
                    x,
                    d,
                    filter_len=180,
                    mu=0.1,
                ),
                "IPNLMS": ipnlms_filter(
                    x,
                    d,
                    filter_len=200,
                    mu=0.04,
                    alpha=0.2,
                ),
                "Llncosh": llncosh_filter(
                    x,
                    d,
                    filter_len=7,
                    mu=0.01,
                    lam=10,
                ),
                "LHSAF": lhsaf_filter(
                    x,
                    d,
                    filter_len=7,
                    mu=0.02,
                    lam=8,
                ),
                "ILHSAF": ilhsaf_filter(
                    x,
                    d,
                    m,
                    filter_len=7,
                    mu=0.03,
                ),
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
                        "RMSE": rmse(ideal[skip:], e[skip:]),
                        "PRD": prd(s[skip:], e[skip:]),
                        "SNR": snr(ideal[skip:], e[skip:]),
                        "AMSE": amse(s[skip:], e[skip:]),
                    }
                )

            # -------------------------------------------------
            # Figure 7
            # -------------------------------------------------

            if subject == "sub01" and alpha in [2.0, 1.4] and ch == 0:

                figure7_paper2(
                    subject,
                    alpha,
                    x,
                    m,
                    algorithms["NLMS"][1],
                    algorithms["IPNLMS"][1],
                    algorithms["Llncosh"][1],
                    algorithms["LHSAF"][1],
                    algorithms["ILHSAF"][1],
                )

            # -------------------------------------------------
            # Figure 5 + Weights
            # -------------------------------------------------

            if subject == "sub03" and ch == 0:

                curves = {
                    "NLMS": amse_curve(s, algorithms["NLMS"][1]),
                    "IPNLMS": amse_curve(s, algorithms["IPNLMS"][1]),
                    "Llncosh": amse_curve(s, algorithms["Llncosh"][1]),
                    "LHSAF": amse_curve(s, algorithms["LHSAF"][1]),
                    "ILHSAF": amse_curve(s, algorithms["ILHSAF"][1]),
                }

                if alpha == 2.0:
                    fig5_gaussian = curves

                if alpha == 1.4:

                    fig5_alpha = curves

                    figure5_paper2(
                        fig5_gaussian,
                        fig5_alpha,
                        subject,
                    )

                    plot_weights_paper_two(
                        algorithms["ILHSAF"][3],
                        f"ILHSAF_{subject}",
                    )

        df = pd.DataFrame(channel_results)

        summary = df.groupby("Algorithm")[["RMSE", "PRD", "SNR", "AMSE"]].mean()

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

csv_path = os.path.join(PAPER2_DIR, "Paper2_TableIII.csv")
xlsx_path = os.path.join(PAPER2_DIR, "Paper2_TableIII.xlsx")

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
print(f"All Paper-2 results saved in: {PAPER2_DIR}")
print("Generated:")
print(f"  - {csv_path}")
print(f"  - {xlsx_path}")
print("  - Paper2_Fig5_sub01.png")
print("  - Paper2_Fig7_sub01_a.png")
print("  - Paper2_Fig7_sub01_b.png")
print("  - Paper2_Weights_ILHSAF_sub01.png")
