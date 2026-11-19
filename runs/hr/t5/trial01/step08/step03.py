import ezr

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable
    (i.e., the difference is just noise), False if they are significantly different.
    """
    # We use the same logic as ezr.same, which checks for statistical 
    # significance using Cliff's Delta and the Kolmogorov-Smirnov test.
    return ezr.same(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]

    # Find indices for 'overTime' and 'YearsInCurrentRole+'
    # 'overTime' is at index 22, 'YearsInCurrentRole+' is at index 32
    ot_idx = header.index('overTime')
    yicr_idx = header.index('YearsInCurrentRole+')

    # Separate data into two groups: those who work overtime and those who don't
    yes_ot = []
    no_ot = []

    for row in rows:
        val = row[yicr_idx]
        if isinstance(val, (int, float)):
            if row[ot_idx] == 'Yes':
                yes_ot.append(val)
            elif row[ot_idx] == 'No':
                no_ot.append(val)

    # Perform the certification
    # If certify returns True, the difference is noise (they are the same).
    # If certify returns False, the difference is real.
    is_noise = certify(yes_ot, no_ot)

    print("Analysis: Do people who work overtime leave their role sooner?")
    print(f"  Average years in role (Overtime): {sum(yes_ot)/len(yes_ot):.2f}")
    print(f"  Average years in role (No Overtime): {sum(no_ot)/len(no_ot):.2f}")
    
    if is_noise:
        print("Result: The difference is statistically insignificant (just noise).")
    else:
        print("Result: The difference is statistically significant (it is real).")
