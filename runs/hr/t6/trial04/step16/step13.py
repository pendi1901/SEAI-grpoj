import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the distributions are the same (noise), 
    False if they really differ.
    """
    return step03.certify(xs, ys)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Identify columns
    idx_train = header.index("TrainingTimesLastYear")
    idx_ywcm = header.index("YearsWithCurrManager+")
    
    # Split data into two groups: low training (0-2) vs high training (3-6)
    low_train = [r[idx_ywcm] for r in rows if r[idx_train] <= 2]
    high_train = [r[idx_ywcm] for r in rows if r[idx_train] > 2]
    
    # Check if the difference is statistically significant
    is_noise = certify(low_train, high_train)
    
    print("Analysis: Do people with more training stay longer with their manager?")
    print(f"Mean YearsWithCurrManager (Low Training): {sum(low_train)/len(low_train):.2f}")
    print(f"Mean YearsWithCurrManager (High Training): {sum(high_train)/len(high_train):.2f}")
    
    if is_noise:
        print("Result: The difference is statistically indistinguishable (noise).")
    else:
        print("Result: There is a statistically significant difference.")
