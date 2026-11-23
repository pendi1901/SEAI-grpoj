import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the distributions are statistically indistinguishable 
    (same apart from noise), False if they really differ.
    """
    return step03.certify(xs, ys)

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify indices
    # 'TrainingTimesLastYear' is numeric (index 29)
    # 'YearsWithCurrManager+' is numeric (index 34)
    train_idx = header.index('TrainingTimesLastYear')
    mgr_idx = header.index('YearsWithCurrManager+')
    
    # Split data into two groups: low training (0-2) vs high training (3-6)
    low_train = [r[mgr_idx] for r in rows if r[train_idx] <= 2]
    high_train = [r[mgr_idx] for r in rows if r[train_idx] > 2]
    
    # Perform certification
    is_same = certify(low_train, high_train)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    if is_same:
        print("Result: The difference is statistically insignificant (noise).")
        print("Conclusion: Training frequency does not appear to impact tenure with managers.")
    else:
        print("Result: There is a statistically significant difference.")
        avg_low = sum(low_train) / len(low_train)
        avg_high = sum(high_train) / len(high_train)
        print(f"Average years with manager (Low Training): {avg_low:.2f}")
        print(f"Average years with manager (High Training): {avg_high:.2f}")
        if avg_high > avg_low:
            print("Conclusion: Yes, more training is associated with longer tenure with managers.")
        else:
            print("Conclusion: Training is associated with a change in tenure, but not necessarily an increase.")
    
    exit(0)
