import numpy as np


def ill_filter(x, d, m, filter_len=32, mu=0.005):

    N = len(x)

    w = np.zeros(filter_len)

    y = np.zeros(N)

    e = np.zeros(N)

    history = np.zeros((N, filter_len))

    H = np.max(np.abs(m))

    for n in range(filter_len - 1, N):

        x_vec = x[n - filter_len + 1 : n + 1][::-1]

        y[n] = np.dot(w, x_vec)

        e[n] = d[n] - y[n]

        # H = np.max(np.abs(x_vec))

        phi = np.tanh((0.84 * e[n]) / H)

        w += mu * H * phi * x_vec

        history[n] = w

    return y, e, w, history


def nlms_filter(x, d, filter_len=32, mu=0.8):

    N = len(x)

    w = np.zeros(filter_len)

    y = np.zeros(N)

    e = np.zeros(N)

    history = np.zeros((N, filter_len))

    delta = 1e-8

    for n in range(filter_len - 1, N):

        x_vec = x[n - filter_len + 1 : n + 1][::-1]

        y[n] = np.dot(w, x_vec)

        e[n] = d[n] - y[n]

        norm = np.dot(x_vec, x_vec) + delta

        w += mu * e[n] * x_vec / norm

        history[n] = w

    return y, e, w, history


def ipnlms_filter(x, d, filter_len=32, mu=0.8, alpha=-0):

    N = len(x)

    w = np.zeros(filter_len)

    y = np.zeros(N)

    e = np.zeros(N)

    history = np.zeros((N, filter_len))

    delta = 1e-8

    for n in range(filter_len - 1, N):

        x_vec = x[n - filter_len + 1 : n + 1][::-1]

        y[n] = np.dot(w, x_vec)

        e[n] = d[n] - y[n]

        absw = np.abs(w)

        g = ((1 - alpha) / (2 * filter_len)) + (1 + alpha) * absw / (
            2 * np.sum(absw) + delta
        )

        denom = np.sum(g * x_vec * x_vec) + delta

        w += mu * g * x_vec * e[n] / denom

        history[n] = w

    return y, e, w, history


def lhsaf_filter(x, d, filter_len=7, mu=0.02, lam=8):

    N = len(x)

    w = np.zeros(filter_len)

    y = np.zeros(N)

    e = np.zeros(N)

    history = np.zeros((N, filter_len))

    for n in range(filter_len - 1, N):

        x_vec = x[n - filter_len + 1 : n + 1][::-1]

        y[n] = np.dot(w, x_vec)

        e[n] = d[n] - y[n]
        den = 1e-12;
        sech = 1 / (np.cosh(lam * e[n])+ den)

        phi = np.tanh(lam * e[n]) * sech / (1 + sech)

        w += mu * phi * x_vec

        history[n] = w.copy()

    return y, e, w, history


def ilhsaf_filter(x, d, m, filter_len=7, mu=0.03):

    N = len(x)

    w = np.zeros(filter_len)

    y = np.zeros(N)

    e = np.zeros(N)

    history = np.zeros((N, filter_len))

    H = np.max(np.abs(m))

    if H == 0:
        H = 1e-8

    for n in range(filter_len - 1, N):

        x_vec = x[n - filter_len + 1 : n + 1][::-1]

        y[n] = np.dot(w, x_vec)

        e[n] = d[n] - y[n]

        u = 0.35 * e[n] / H

        sech = 1 / np.cosh(u)

        phi = np.tanh(u) * sech / (1 + sech)

        w += mu * phi * x_vec

        history[n] = w.copy()

    return y, e, w, history


def llncosh_filter(x, d, filter_len=7, mu=0.01, lam=10):

    N = len(x)

    w = np.zeros(filter_len)

    y = np.zeros(N)

    e = np.zeros(N)

    history = np.zeros((N, filter_len))

    for n in range(filter_len - 1, N):

        x_vec = x[n - filter_len + 1 : n + 1][::-1]

        y[n] = np.dot(w, x_vec)

        e[n] = d[n] - y[n]

        phi = np.tanh(lam * e[n])

        w += mu * phi * x_vec

        history[n] = w.copy()

    return y, e, w, history
