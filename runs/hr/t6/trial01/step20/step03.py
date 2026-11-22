import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable
    (i.e., the difference is just noise), False if they really differ.
    Uses the same() function from ezr.stats.
    """
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]

    # Identify indices
    # 'overTime' is symbolic, 'YearsInCurrentRole+' is numeric (goal to maximize)
    ot_idx = header.index('overTime')
    tenure_idx = header.index('YearsInCurrentRole+')

    # Split data into two groups: those who work overtime and those who don't
    overtime_yes = []
    overtime_no = []

    for row in rows:
        val = row[tenure_idx]
        if val == "?":
            continue
        if row[ot_idx] == "Yes":
            overtime_yes.append(val)
        elif row[ot_idx] == "No":
            overtime_no.append(val)

    # Perform statistical test
    # If same() returns True, they are the same (noise).
    # If False, they differ significantly.
    is_noise = certify(overtime_yes, overtime_no)

    print("Analysis: Do people who work overtime leave their role sooner?")
    print(f"Average tenure (Overtime=Yes): {sum(overtime_yes)/len(overtime_yes):.2f} years")
    print(f"Average tenure (Overtime=No):  {sum(overtime_no)/len(overtime_no):.2f} years")
    
    if is_noise:
        print("Result: The difference is statistically insignificant (just noise).")
    else:
        print("Result: The difference is statistically significant (not just noise).")
