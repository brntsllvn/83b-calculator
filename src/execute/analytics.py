def calculate_npv(tax_diff_process, discount_rate):
    total = 0.0
    for i, cash_flow in enumerate(tax_diff_process):
        if cash_flow is None or isinstance(cash_flow, str):
            raise TypeError('Invalid input')
        total += 1.0 * (cash_flow / ((1 + discount_rate) ** i))
    return round(total)
