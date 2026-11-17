import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


def justify(header, rows, row):
    # Goals are columns ending in '+' (maximise) or '-' (minimise).
    plus_goals = [c for c in header if c.endswith('+')]
    target_col = plus_goals[0]  # YearsAtCompany+

    feature_cols = [c for c in header if c != target_col]

    le = LabelEncoder()
    X_train, y_train = [], []
    for r in rows:
        x = []
        for col in feature_cols:
            val = r[header.index(col)]
            try:
                x.append(float(val))
            except ValueError:
                le.fit([val])
                x.append(le.transform([val])[0])
        y_train.append(float(r[header.index(target_col)]))
        X_train.append(x)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # Predict the hidden goals for the new row.
    x_new = []
    for col in feature_cols:
        val = row[header.index(col)]
        try:
            x_new.append(float(val))
        except ValueError:
            le.transform([val])[0] if len(le.classes_) > 0 else float('nan')

    pred = model.predict([x_new])[0]

    # Fraction of existing rows that our prediction beats.
    n_better = sum(1 for y in y_train if y < pred)
    p = n_better / len(y_train)

    return (p, f"Better than {n_better} of {len(rows)} employees on tenure")


if __name__ == "__main__":
    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            parsed = []
            for cell in row:
                try:
                    parsed.append(float(cell))
                except ValueError:
                    parsed.append(cell)
            rows.append(parsed)

    new_row = rows[-1]
    p, reason = justify(header, rows[:-1], new_row)
    print(f"Ranking: better than {p:.2%} of employees")
    print(reason)
