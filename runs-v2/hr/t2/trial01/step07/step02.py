import csv
import math


def guess(header, train, test):
    years_idx = header.index('YearsAtCompany+')
    goal_cols = ['YearsAtCompany+', 'YearsInCurrentRole+',
                 'YearsSinceLastPromotion', 'YearsWithCurrManager+']

    numeric_cols = []
    for col in header:
        if col not in goal_cols and '+' not in col \
                and col != 'EmployeeNumber' and col != 'EmployeeCount':
            numeric_cols.append(col)

    n_train = len(train)
    if n_train == 0:
        return [0.0] * len(test)

    def safe_float(val):
        if val == '?':
            return 0.0
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    col_idx = {col: header.index(col) for col in numeric_cols}

    means = {}
    stds = {}
    for col in numeric_cols:
        vals = [safe_float(r[col_idx[col]]) for r in train]
        mean_val = sum(vals) / len(vals)
        variance = sum((v - mean_val) ** 2 for v in vals) / len(vals)
        means[col] = mean_val
        stds[col] = max(math.sqrt(variance), 1e-6)

    y_vals = [safe_float(r[years_idx]) for r in train]
    y_mean = sum(y_vals) / len(y_vals)

    correlations = {}
    for col in numeric_cols:
        x_vals = [safe_float(r[col_idx[col]]) for r in train]
        x_mean = means[col]
        numerator = sum((x - x_mean) * (y - y_mean)
                        for x, y in zip(x_vals, y_vals))
        denom_x = math.sqrt(sum((x - x_mean) ** 2 for x in x_vals))
        denom_y = math.sqrt(sum((y - y_mean) ** 2 for y in y_vals))
        if denom_x * denom_y > 0:
            correlations[col] = numerator / (denom_x * denom_y)
        else:
            correlations[col] = 0.0

    predictions = []
    for t_row in test:
        pred = y_mean
        for col in numeric_cols:
            val = safe_float(t_row[col_idx[col]])
            z_score = (val - means[col]) / stds[col]
            pred += correlations[col] * z_score
        predictions.append(pred)

    return predictions


if __name__ == "__main__":
    path = 'WA_Fn-UseC_-HR-Employee-Attrition.train.csv'
    with open(path, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    predictions = guess(header, rows, [])
    print(f"Predicted YearsAtCompany+ for {len(predictions)} new hires:")
    for i, p in enumerate(predictions[:5]):
        print(f"  Hire #{i+1}: ~{p:.1f} years")
