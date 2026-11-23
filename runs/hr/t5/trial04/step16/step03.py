import ezr

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable
    (i.e., the difference is just noise), False if they are significantly different.
    Uses the same logic as ezr.same.
    """
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    # Identify indices
    # 'overTime' is at index 22
    # 'YearsInCurrentRole+' is at index 32
    overtime_idx = 22
    years_role_idx = 32

    # Separate data into two groups: those who work overtime and those who don't
    yes_overtime = []
    no_overtime = []

    for row in rows:
        val = row[years_role_idx]
        if isinstance(val, (int, float)):
            if row[overtime_idx] == "Yes":
                yes_overtime.append(val)
            elif row[overtime_idx] == "No":
                no_overtime.append(val)

    # Sort for statistical tests
    yes_overtime.sort()
    no_overtime.sort()

    # Perform certification
    is_noise = certify(yes_overtime, no_overtime)

    # Output results
    print("Analysis: Do people who work overtime leave their role sooner?")
    print(f"Group 'Yes' (Overtime) count: {len(yes_overtime)}, mean: {sum(yes_overtime)/len(yes_overtime):.2f}")
    print(f"Group 'No' (No Overtime) count: {len(no_overtime)}, mean: {sum(no_overtime)/len(no_overtime):.2f}")
    
    if not is_noise:
        print("Result: The difference is statistically significant (not just noise).")
    else:
        print("Result: The difference is statistically indistinguishable (likely just noise).")
