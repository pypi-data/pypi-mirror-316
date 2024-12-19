from scipy.stats import ttest_ind, chi2_contingency

def t_test(sample1, sample2):
    """Effectuer un test t."""
    return ttest_ind(sample1, sample2)

def chi_square_test(contingency_table):
    """Effectuer un test du chi-carré."""
    return chi2_contingency(contingency_table)
