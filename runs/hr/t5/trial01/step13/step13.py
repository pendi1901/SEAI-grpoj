import ezr
import random

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

    # Find indices for 'TrainingTimesLastYear' and 'YearsWithCurrManager+'
    # 'TrainingTimesLastYear' is numeric, 'YearsWithCurrManager+' is numeric
    ttly_idx = header.index('TrainingTimesLastYear')
    ywcm_idx = header.index('YearsWithCurrManager+')

    # Split data into two groups: those with low training (0-2 days) 
    # and those with high training (3-6 days)
    low_train = []
    high_train = []

    for row in rows:
        val = row[ywcm_idx]
        if isinstance(val, (int, float)):
            if row[ttly_idx] <= 2:
                low_train.append(val)
            else:
                high_train.append(val)

    # Perform the certification
    # If certify returns True, the difference is noise (they are the same).
    # If certify returns False, the difference is real.
    is_noise = certify(low_train, high_train)

    print("Analysis: Do people with more training stay longer with their manager?")
    print(f"  Average years with manager (Low Training, <=2 days): {sum(low_train)/len(low_train):.2f}")
    print(f"  Average years with manager (High Training, >2 days): {sum(high_train)/len(high_train):.2f}")
    
    if is_noise:
        print("Result: The difference is statistically insignificant (just noise).")
        print("Conclusion: Training frequency does not appear to significantly impact tenure with managers.")
    else:
        print("Result: The difference is statistically significant (it is real).")
        print("Conclusion: There is a real difference in tenure with managers based on training frequency.")
