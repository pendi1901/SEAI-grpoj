import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (i.e., the difference is just noise), False if they are significantly different.
    Uses the same logic as ezr.same.
    """
    return ezr.same(xs, ys)

def analyze_overtime_impact(header, rows):
    """
    Splits the data into two groups: those who work overtime and those who don't.
    Compares the 'YearsInCurrentRole+' column for both groups.
    """
    # Find indices
    overtime_idx = header.index('overTime')
    role_idx = header.index('YearsInCurrentRole+')
    
    # Separate data
    with_overtime = []
    without_overtime = []
    
    for row in rows:
        val = row[role_idx]
        if isinstance(val, (int, float)):
            if row[overtime_idx] == 'Yes':
                with_overtime.append(val)
            elif row[overtime_idx] == 'No':
                without_overtime.append(val)
                
    # Sort for statistical tests
    with_overtime.sort()
    without_overtime.sort()
    
    # Perform certification
    is_noise = certify(with_overtime, without_overtime)
    
    avg_yes = sum(with_overtime) / len(with_overtime)
    avg_no = sum(without_overtime) / len(without_overtime)
    
    return is_noise, avg_yes, avg_no

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    is_noise, avg_yes, avg_no = analyze_overtime_impact(header, rows)
    
    print("--- Overtime vs Years in Current Role Analysis ---")
    print(f"Average years in role (Overtime): {avg_yes:.2f}")
    print(f"Average years in role (No Overtime): {avg_no:.2f}")
    
    if is_noise:
        print("\nConclusion: The difference is statistically insignificant (noise).")
    else:
        print("\nConclusion: The difference is statistically significant (not just noise).")
