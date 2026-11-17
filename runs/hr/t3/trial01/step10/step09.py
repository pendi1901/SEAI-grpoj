import csv
from collections import Counter


def spot(header, rows):
    # Goals: '+' -> maximise, '-' -> minimise; everything else is input.
    plus = [c for c in header if c.endswith('+')]
    minus = [c for c in header if c.endswith('-')]
    input_cols = [c for c in header if c not in plus and c not in minus]

    n = len(rows)
    # Per-row suspicion score: number of suspicious cells.
    row_scores = {i: 0 for i in range(n)}

    # Known valid categories for symbolic columns (domain knowledge).
    VALID_DEPT = {'Sales', 'Research & Development', 'Operations',
                  'Human Resources', 'Engineering'}
    VALID_GENDER = {'Male', 'Female'}
    VALID_MARITAL = {'Single', 'Married', 'Divorced', 'Widowed'}
    VALID_ROLE = {'Laboratory Technician', 'Sales Executive',
                  'Sales Representative', 'Research Scientist',
                  'Manufacturing Director', 'Human Resources'}
    VALID_EDU = {'Other', 'Life Sciences', 'Medical',
                 'Marketing', 'Sales', 'Technical'}
    VALID_TRAVEL = {'Non-Travel', 'Travel_Rarely', 'Travel_Frequently'}

    for col in input_cols:
        idx = header.index(col)
        try:
            vals = [float(row[idx]) for row in rows]
            arr = __import__('numpy').array(vals)
            mean_v, std_v = float(arr.mean()), float(arr.std())

            if std_v < 1e-9:
                # Constant column — any deviation is wrong.
                target = mean_v
                for i, v in enumerate(rows):
                    if abs(float(v[idx]) - target) > 0.5:
                        row_scores[i] += 1
            else:
                threshold = 3.0 * std_v
                for i, v in enumerate(rows):
                    diff = abs(float(v[idx]) - mean_v)
                    if diff > threshold:
                        row_scores[i] += 1

        except (ValueError, TypeError):
            # Symbolic column — validate against known categories.
            vals = [row[idx] for row in rows]
            valid_set = None
            if col == 'department':
                valid_set = VALID_DEPT
            elif col == 'gender':
                valid_set = VALID_GENDER
            elif col == 'maritalStatus':
                valid_set = VALID_MARITAL
            elif col == 'jobRole':
                valid_set = VALID_ROLE
            elif col == 'educationField':
                valid_set = VALID_EDU
            elif col == 'businessTravel':
                valid_set = VALID_TRAVEL

            if valid_set is not None:
                for i, v in enumerate(vals):
                    if v.strip() not in valid_set:
                        row_scores[i] += 1

    # Return rows sorted by suspicion (most suspicious first).
    return [i for i in range(n) if row_scores[i] > 0], sorted(
        [i for i in range(n)], key=lambda i: -row_scores[i])


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

    suspicious, _ = spot(header, rows)
    print(f"Found {len(suspicious)} rows with likely wrong entries:")
    target_col = "YearsAtCompany+"
    for idx in suspicious[:10]:
        age = int(rows[idx][header.index("Age")]) if header.index("Age") < len(rows[idx]) else "?"
        years = float(rows[idx][header.index(target_col)]) if header.index(target_col) < len(rows[idx]) else "?"
        print(f"  Row {idx}: Age={age}, YearsAtCompany+={years:.1f}")
