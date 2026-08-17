import wfdb


def load_subject(subject):

    base = f"data/{subject}_snr06dB_l1_c0"

    fecg, _ = wfdb.rdsamp(base + "_fecg1")
    mecg, _ = wfdb.rdsamp(base + "_mecg")

    return {"fecg": fecg, "mecg": mecg}


def load_record(path_without_extension):

    signal, fields = wfdb.rdsamp(path_without_extension)

    return signal, fields


def load_all():

    fecg, f_info = load_record("data/sub01_snr06dB_l1_c0_fecg1")
    mecg, m_info = load_record("data/sub01_snr06dB_l1_c0_mecg")
    noise1, _ = load_record("data/sub01_snr06dB_l1_c0_noise1")
    noise2, _ = load_record("data/sub01_snr06dB_l1_c0_noise2")

    return {
        "fecg": fecg,
        "mecg": mecg,
        "noise1": noise1,
        "noise2": noise2,
        "fs": f_info["fs"],
    }
