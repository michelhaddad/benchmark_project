import numpy as np


def get_spec_ratio(ref_time, measured_time):
    return round(ref_time / measured_time, 5)


# Geometric mean of spec ratios
def avg_spec_ratio(spec_ratios):
    a = np.log(spec_ratios)
    return float(round(np.exp(a.sum() / len(a)), 5))
