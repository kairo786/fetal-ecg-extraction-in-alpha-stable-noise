import pandas as pd

from utils.loader import load_all
from utils.noise import generate_alpha_noise, verify_gsnr
from utils.filters import ill_filter, nlms_filter, ipnlms_filter
from utils.metrics import *
from utils.plotting import *
from utils.preprocess import *
from scipy.stats import levy_stable

data = load_all()

fecg = data["fecg"]
mecg = data["mecg"]

CHANNEL = 0

# Reference
x = mecg[:, 32]

x1 = mecg[:, 32]
x2 = mecg[:, 33]

# m = mecg[:,0]
# x, delay = align_reference(x, m)
# print("Delay:", delay)

x = x - np.mean(x)

# True signals
s = fecg[:, CHANNEL]
m = mecg[:, CHANNEL]

corr1 = np.corrcoef(x1, m)[0, 1]
corr2 = np.corrcoef(x2, m)[0, 1]

print("correlation coff1 : ", corr1, "correlation coff2 : ", corr2)


# Clean abdominal
# m = m - np.mean(m)

# s = s - np.mean(s)

clean = s + m

alphas = [2.0, 1.8, 1.6, 1.4]

rows = []

for alpha in alphas:

    target = 15; 
    noise, gamma = generate_alpha_noise(clean, alpha, 15)

    actual = verify_gsnr(clean,noise)
    print(
      "Target GSNR:",
       15,
       "Actual:",
       actual
    )    
    gamma *= 10**((actual-target)/20)

    noise = levy_stable.rvs(
     alpha,
     0,
     loc=0,
     scale=gamma,
     size=clean.shape,
     random_state=42,
    )

    d = clean + noise

    algorithms = {
        "ILL": ill_filter(x, d, m), # y , e, w, history
        "NLMS": nlms_filter(x, d),
        "IPNLMS": ipnlms_filter(x, d),
    }

    for name, (y, e, w, h) in algorithms.items():
        skip = 5000;
        # ideal=s+noise
        ideal = d - m;

        rows.append(
            {
                "Alpha": alpha,
                "Algorithm": name,
                "RMSE": rmse(ideal[skip:], (e)[skip:]),
                "PRD": prd(s[skip:], (e)[skip:]),
                "SNR s vs e":snr(s[skip],e[skip]),
                "SNR s+n vs e": snr(ideal[skip:], (e)[skip:]),
                "AMSE": amse(s[skip:], (e)[skip:]),
            }
        )

    if alpha == 1.4:

        # plot_result(x,s,noise, d, algorithms["ILL"][0], algorithms["ILL"][1], "ILL alpha=1.4")
        # plot_result(x,s,noise, d, s+noise, algorithms["ILL"][1]-noise, "ILL alpha=1.4")
        figure_four(
            x,
            m,
            s,
            noise,
            d,
            algorithms["NLMS"][1] - np.mean(algorithms["NLMS"][1]),
            algorithms["IPNLMS"][1]-np.mean(algorithms["IPNLMS"][1]),
            algorithms["ILL"][1] - np.mean(algorithms["ILL"][1]),
        )
        # plot_result(x,s,noise, d, algorithms["NLMS"][0], algorithms["NLMS"][1], "NLMS alpha=1.4")

        # plot_result(x,s,noise, d, algorithms["IPNLMS"][0], algorithms["IPNLMS"][1], "IPNLMS alpha=1.4")

        plot_weights(algorithms["ILL"][3], "ILL Weight Convergence")

table = pd.DataFrame(rows)

print(table)

table.to_csv("results_step7.csv", index=False)
