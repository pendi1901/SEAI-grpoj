import csv


def remember(header, rows):
    goal_cols = [c for c in header if c.endswith('+')]

    best_positions = []
    for i, row in enumerate(rows):
        score = 0
        valid = True
        for col in goal_cols:
            val = row[header.index(col)]
            if val == '?':
                valid = False
                break
            try:
                score += float(val)
            except ValueError:
                valid = False
                break
        if not valid:
            continue
        best_positions.append((score, i))

    best_positions.sort(reverse=True)

    max_count = max(1, int(len(rows) * 0.05))
    return [int(pos) for _, pos in best_positions[:max_count]]


if __name__ == "__main__":
    with open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    positions = remember(header, rows)

    print(f"Top {len(positions)} employees who stay longest:")
    for pos in positions[:5]:
        row = rows[pos]
        years_at_company = row[header.index('YearsAtCompany+')]
        years_in_role = row[header.index('YearsInCurrentRole+')]
        years_with_manager = row[header.index('YearsWithCurrManager+')]
        print(f"  Employee {row[header.index('EmployeeNumber')]}, "
              f"At company: {years_at_company} yrs, "
              f"In current role: {years_in_role} yrs, "
              f"With manager: {years_with_manager} yrs")
