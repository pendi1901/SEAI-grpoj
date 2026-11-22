import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the distributions are statistically indistinguishable 
    (noise), False if they are significantly different.
    """
    # ezr.same uses cliffs and ks tests to check if two distributions are the same.
    return ezr.same(xs, ys)

def analyze_overtime_impact(header, rows):
    """
    Splits the data into two groups based on 'overTime' (Yes vs No)
    and compares their 'YearsAtCompany+' values.
    """
    ot_idx = header.index("overTime")
    tenure_idx = header.index("YearsAtCompany+")
    
    yes_ot = [r[tenure_idx] for r in rows if r[ot_idx] == "Yes"]
    no_ot = [r[tenure_idx] for r in rows if r[ot_idx] == "No"]
    
    is_noise = certify(yes_ot, no_ot)
    
    return is_noise, yes_ot, no_ot

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    is_noise, yes_ot, no_ot = analyze_overtime_impact(header, rows)
    
    avg_yes = sum(yes_ot) / len(yes_ot)
    avg_no = sum(no_ot) / len(no_ot)
    
    print(f"Analysis of Overtime impact on 'YearsAtCompany+':")
    print(f"Average tenure (Overtime=Yes): {avg_yes:.2f} years")
    print(f"Average tenure (Overtime=No):  {avg_no:.2f} years")
    
    if is_noise:
        print("Conclusion: The observed difference is statistically indistinguishable from noise.")
    else:
        print("Conclusion: The difference is statistically significant; overtime is linked to tenure.")
    
    exit(0)
