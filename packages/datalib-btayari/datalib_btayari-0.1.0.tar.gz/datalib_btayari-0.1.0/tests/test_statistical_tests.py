import pandas as pd
from scipy.stats import ttest_ind
from src.datalib.stats.statistical_tests import t_test, chi_square_test

def test_t_test():
    sample1 = [1, 2, 3]
    sample2 = [4, 5, 6]
    stat, p_value = t_test(sample1, sample2)
    assert round(stat, 2) == -3.67, "t_test ne fonctionne pas correctement."

def test_chi_square_test():
    contingency_table = [[10, 20], [30, 40]]
    chi2, p, _, _ = chi_square_test(contingency_table)
    assert round(chi2, 2) == 0.45, "chi_square_test ne fonctionne pas correctement."
