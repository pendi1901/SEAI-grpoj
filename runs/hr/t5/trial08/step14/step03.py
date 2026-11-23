import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (i.e., the difference is likely just noise), False if they differ.
    Uses the same logic as ezr.same (cliffs and ks tests).
    """
    # Sort the lists as required by the statistical tests
    xs_sorted = sorted(xs)
    ys_sorted = sorted(ys)
    
    # Use the statistical tests provided in ezr
    # We use the default thresholds defined in ezr.same
    return ezr.cliffs(xs_sorted, ys_sorted) and ezr.ks(xs_sorted, ys_sorted)

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Identify column indices
    # 'overTime' is symbolic, 'YearsInCurrentRole+' is numeric
    col_names = {name: i for i, name in enumerate(header)}
    overtime_idx = col_names['overTime']
    tenure_idx = col_names['YearsInCurrentRole+']
    
    # Split data into two groups: Overtime vs No Overtime
    # We only care about rows where the goal column is not "?"
    yes_overtime = []
    no_overtime = []
    
    for row in rows:
        val = row[tenure_idx]
        if val != "?":
            if row[overtime_idx] == "Yes":
                yes_overtime.append(val)
            elif row[overtime_idx] == "No":
                no_overtime.append(val)
                
    # Perform the certification
    is_same = certify(yes_overtime, no_overtime)
    
    print("Analysis: Does working overtime affect years in current role?")
    print(f"Average years (Overtime): {sum(yes_overtime)/len(yes_overtime):.2f}")
    print(f"Average years (No Overtime): {sum(no_overtime)/len(no_overtime):.2f}")
    
    if is_same:
        print("Result: The difference is statistically insignificant (noise).")
    else:
        print("Result: The difference is statistically significant (real).")
    
    exit(0)
