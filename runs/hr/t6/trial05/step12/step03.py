import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (i.e., the difference is just noise), False if they really differ.
    """
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Map column names to indices
    col_map = {name: i for i, name in enumerate(header)}
    overtime_idx = col_map['overTime']
    tenure_idx = col_map['YearsAtCompany+']
    
    # Separate tenure data based on overtime status
    yes_overtime = [r[tenure_idx] for r in rows if r[overtime_idx] == 'Yes']
    no_overtime = [r[tenure_idx] for r in rows if r[overtime_idx] == 'No']
    
    # Perform statistical test
    # certify returns True if they are the same (noise), False if they differ
    is_noise = certify(yes_overtime, no_overtime)
    
    print("Analysis: Do people who work overtime leave their role sooner?")
    if is_noise:
        print("Result: The difference is statistically insignificant (just noise).")
    else:
        print("Result: There is a statistically significant difference in tenure.")
        avg_yes = sum(yes_overtime) / len(yes_overtime)
        avg_no = sum(no_overtime) / len(no_overtime)
        print(f"Average tenure for Overtime: {avg_yes:.2f} years")
        print(f"Average tenure for No Overtime: {avg_no:.2f} years")
    
    exit(0)
