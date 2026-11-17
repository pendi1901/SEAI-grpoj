import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


def guess(header, train, test):
    # Identify the first '+' goal column (target) and all other columns (features).
    plus_goals = [c for c in header if c.endswith('+')]
    target_col = plus_goals[0]  # YearsAtCompany+

    feature_cols = [c for c in header if c != target_col]

    le = LabelEncoder()
    X_train = []
    y_train = []
    for row in train:
        x = []
        for col in feature_cols:
            val = row[header.index(col)]
            try:
                x.append(float(val))
            except ValueError:
                le.fit([val])
                x.append(le.transform([val])[0])
        y_train.append(float(row[header.index(target_col)]))
        X_train.append(x)

    X_test = []
    for row in test:
        x = []
        for col in feature_cols:
            val = row[header.index(col)]
            try:
                x.append(float(val))
            except ValueError:
                le.transform([val])[0] if len(le.classes_) > 0 else float('nan')
        X_test.append(x)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    return [float(model.predict([x])[0]) for x in X_test]


if __name__ == "__main__":
    import numpy as np

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

    train_rows = rows[:-1]
    test_row = rows[-1:]
    result = guess(header, train_rows, test_row)
    print(f"Estimated YearsAtCompany+ for the new hire: {result[0]:.2f} years")
