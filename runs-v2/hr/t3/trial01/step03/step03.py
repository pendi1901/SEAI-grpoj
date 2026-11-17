import pandas as pd
import numpy as np


def certify(xs, ys):
    """Returns True if xs and ys are the same apart from noise, False if they really differ."""
    n_x = len(xs)
    n_y = len(ys)
    
    mean_x = sum(xs) / n_x if n_x else 0.0
    mean_y = sum(ys) / n_y if n_y else 0.0
    
    var_x = sum((x - mean_x)**2 for x in xs) / (n_x - 1) if n_x > 1 else 0.0
    var_y = sum((y - mean_y)**2 for y in ys) / (n_y - 1) if n_y > 1 else 0.0
    
    pooled_var = ((n_x - 1) * var_x + (n_y - 1) * var_y) / (n_x + n_y - 2)
    pooled_std = pooled_var ** 0.5
    
    se = pooled_std * (1.0 / n_x + 1.0 / n_y) ** 0.5 if pooled_std > 0 else 1.0
    t_stat = abs(mean_x - mean_y) / se if se > 0 else 999.0
    
    return t_stat < 2.0


def main():
    df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.train.csv')
    
    header = list(df.columns)
    rows = []
    for _, row in df.iterrows():
        r = []
        for col, val in zip(header, row):
            if pd.isna(val):
                r.append(float('nan'))
            elif isinstance(val, (int, float)):
                r.append(float(val))
            else:
                r.append(str(val))
        rows.append(r)

    # Attrition rate for overtime workers vs non-overtime workers
    attrition_col = header.index('attrition')
    
    ot_yes_rows = []
    ot_no_rows = []
    
    for row in rows:
        if row[header.index('overTime')] == 'Y':
            attr_val = 1.0 if str(row[attrition_col]) == 'Yes' else 0.0
            ot_yes_rows.append(attr_val)
        elif row[header.index('overTime')] == 'N':
            attr_val = 1.0 if str(row[attrition_col]) == 'Yes' else 0.0
            ot_no_rows.append(attr_val)

    mean_ot_yes = sum(ot_yes_rows) / len(ot_yes_rows) * 100
    mean_ot_no = sum(ot_no_rows) / len(ot_no_rows) * 100
    
    print(f"Attrition rate: Overtime workers={mean_ot_yes:.1f}%, Non-overtime workers={mean_ot_no:.1f}%")
    
    if certify(ot_yes_rows, ot_no_rows):
        print("Conclusion: The difference is noise - overtime does not significantly affect attrition.")
    else:
        print("Conclusion: Overtime workers leave sooner than non-overtime workers (real effect).")


if __name__ == "__main__":
    main()
