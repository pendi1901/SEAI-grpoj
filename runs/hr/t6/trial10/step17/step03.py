import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable
    (i.e., the difference is just noise), False if they really differ.
    Uses ezr.same which checks Cohen's d, Cliff's delta, and KS test.
    """
    return ezr.same(xs, ys)

def analyze_overtime_impact(header, rows):
    """
    Splits the data into two groups: those who work overtime and those who don't.
    Compares their 'YearsInCurrentRole+' (a goal to maximize).
    """
    # Find indices
    overtime_idx = header.index('overTime')
    tenure_idx = header.index('YearsInCurrentRole+')
    
    yes_overtime = []
    no_overtime = []
    
    for row in rows:
        val = row[tenure_idx]
        if val == "?": continue
        if row[overtime_idx] == "Yes":
            yes_overtime.append(val)
        else:
            no_overtime.append(val)
            
    # Check if they are the same
    is_same = certify(yes_overtime, no_overtime)
    
    return is_same, yes_overtime, no_overtime

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    is_same, yes_ot, no_ot = analyze_overtime_impact(header, rows)
    
    avg_yes = sum(yes_ot) / len(yes_ot)
    avg_no = sum(no_ot) / len(no_ot)
    
    print("Analysis: Does working overtime affect tenure in current role?")
    print(f"  Average tenure (Overtime): {avg_yes:.2f} years")
    print(f"  Average tenure (No Overtime): {avg_no:.2f} years")
    
    if is_same:
        print("Result: The difference is statistically insignificant (noise).")
    else:
        print("Result: The difference is statistically significant (real).")
