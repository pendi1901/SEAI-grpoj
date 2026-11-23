import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (same apart from noise), False if they significantly differ.
    Uses the same logic as ezr.same.
    """
    # Ensure lists are sorted for the statistical tests
    xs, ys = sorted(xs), sorted(ys)
    # Use ezr's statistical tests: cliffs delta and Kolmogorov-Smirnov
    # We use the default thresholds defined in ezr.py
    return ezr.cliffs(xs, ys) and ezr.ks(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    # Identify columns
    # 'overTime' is at index 22
    # 'YearsInCurrentRole+' is at index 32
    overtime_idx = 22
    years_role_idx = 32

    # Collect data for the two groups
    yes_overtime = []
    no_overtime = []

    for row in rows:
        val = row[years_role_idx]
        if isinstance(val, (int, float)):
            if row[overtime_idx] == "Yes":
                yes_overtime.append(val)
            elif row[overtime_idx] == "No":
                no_overtime.append(val)

    # Perform the certification
    # If certify returns True, they are the same (noise). 
    # If False, they are different (real effect).
    is_noise = certify(yes_overtime, no_overtime)

    print("Analysis: Do people who work overtime leave their role sooner?")
    print(f"Average years in role (Overtime): {sum(yes_overtime)/len(yes_overtime):.2f}")
    print(f"Average years in role (No Overtime): {sum(no_overtime)/len(no_overtime):.2f}")
    
    if not is_noise:
        print("Result: The difference is statistically significant. The effect is real.")
    else:
        print("Result: The difference is not statistically significant. It is likely just noise.")

    exit(0)
