import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (i.e., the difference is just noise), False otherwise.
    """
    # Use the same logic as ezr.same, which checks cliffs and ks tests.
    return ezr.same(xs, ys)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify column indices
    # 'overTime' is the condition, 'YearsInCurrentRole+' is the goal
    idx_overtime = header.index("overTime")
    idx_role = header.index("YearsInCurrentRole+")
    
    # Separate data into two groups based on overtime
    yes_overtime = []
    no_overtime = []
    
    for row in rows:
        val = row[idx_role]
        if val != "?":
            if row[idx_overtime] == "Yes":
                yes_overtime.append(float(val))
            else:
                no_overtime.append(float(val))
    
    # Run the certification
    # If certify returns True, they are the same (noise). 
    # If False, they are different (real effect).
    is_noise = certify(yes_overtime, no_overtime)
    
    print("Analysis: Do people who work overtime leave their role sooner?")
    print(f"Average years in role (Overtime): {sum(yes_overtime)/len(yes_overtime):.2f}")
    print(f"Average years in role (No Overtime): {sum(no_overtime)/len(no_overtime):.2f}")
    
    if is_noise:
        print("Result: The observed difference is statistically indistinguishable from noise.")
    else:
        print("Result: The difference is statistically significant; overtime is linked to role tenure.")
