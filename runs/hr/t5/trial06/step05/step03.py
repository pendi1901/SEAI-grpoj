import ezr

def certify(xs, ys):
    """
    Returns True if the distributions are statistically indistinguishable 
    (i.e., the difference is just noise), False if they significantly differ.
    """
    # Using the same logic as ezr.same, which checks for statistical significance
    # using Cliff's Delta and Kolmogorov-Smirnov tests.
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    # Identify column indices
    # 'overTime' is symbolic, 'YearsInCurrentRole+' is numeric
    ot_idx = header.index('overTime')
    tenure_idx = header.index('YearsInCurrentRole+')

    # Split data into two groups: those who work overtime and those who don't
    overtime_yes = []
    overtime_no = []

    for row in rows:
        val = row[tenure_idx]
        if val != "?":
            if row[ot_idx] == 'Yes':
                overtime_yes.append(val)
            elif row[ot_idx] == 'No':
                overtime_no.append(val)

    # Perform the certification
    is_noise = certify(overtime_yes, overtime_no)

    print("Analysis: Do employees who work overtime leave their roles sooner?")
    print(f"Overtime group (n={len(overtime_yes)}): mean tenure = {sum(overtime_yes)/len(overtime_yes):.2f} years")
    print(f"No-overtime group (n={len(overtime_no)}): mean tenure = {sum(overtime_no)/len(overtime_no):.2f} years")
    
    if is_noise:
        print("Result: The observed difference is statistically indistinguishable from noise.")
        print("Conclusion: There is no significant evidence that overtime affects tenure.")
    else:
        print("Result: The difference is statistically significant.")
        print("Conclusion: Overtime is a real factor in how long employees stay in their roles.")
