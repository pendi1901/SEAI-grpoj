import csv


def remember(header, rows):
    years_at_company_idx = header.index('YearsAtCompany+')
    years_in_current_role_idx = header.index('YearsInCurrentRole+')
    years_with_curr_manager_idx = header.index('YearsWithCurrManager+')

    def safe(val):
        if val == '?':
            return 0.0
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    max_ac = max(safe(r[years_at_company_idx]) for r in rows) or 1
    max_icr = max(safe(r[years_in_current_role_idx]) for r in rows) or 1
    max_wcm = max(safe(r[years_with_curr_manager_idx]) for r in rows) or 1

    scored = []
    for i, row in enumerate(rows):
        score = (safe(row[years_at_company_idx]) / max_ac +
                 safe(row[years_in_current_role_idx]) / max_icr +
                 safe(row[years_with_curr_manager_idx]) / max_wcm) * 100.0
        scored.append((score, i))

    scored.sort(reverse=True)
    n = len(rows)
    limit = max(1, int(n * 0.05))
    return [pos for _, pos in scored[:limit]]


if __name__ == "__main__":
    path = 'WA_Fn-UseC_-HR-Employee-Attrition.train.csv'
    with open(path, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    positions = remember(header, rows)
    emp_idx = header.index('EmployeeNumber')
    print(f"Top {len(positions)} employees who stay unusually long:")
    for pos in positions[:5]:
        row = rows[pos]
        print(f"  Employee #{row[emp_idx]}, "
              f"At company: {row[years_at_company_idx]} years, "
              f"In current role: {row[years_in_current_role_idx]} years")
