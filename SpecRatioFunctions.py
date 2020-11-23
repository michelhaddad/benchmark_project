import numpy as np


def get_spec_ratio(ref_time, measured_time):
    return ref_time / measured_time


def avg_spec_ratio(spec_ratios):
    a = np.log(spec_ratios)
    return np.exp(a.sum() / len(a))
