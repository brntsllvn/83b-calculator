import numpy_financial as npf


def get_npv(tax_diff_process, discount_rate):
    npv = round(npf.npv(discount_rate, tax_diff_process), 2)
    return npv
