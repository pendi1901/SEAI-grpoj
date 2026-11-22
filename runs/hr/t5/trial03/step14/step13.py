import ezr
import random

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (i.e., the difference is just noise), False if they are significantly different.
    """
    return ezr.same(xs, ys)

def analyze_training_impact(header, rows):
    """
    Splits the data into two groups: those with low training (0-2 days) 
    and those with high training (3+ days). Compares the 
    'YearsWithCurrManager+' column for both groups.
    """
    # Find indices
    train_idx = header.index('TrainingTimesLastYear')
    manager_idx = header.index('YearsWithCurrManager+')
    
    low_training = []
    high_training = []
    
    for row in rows:
        t_val = row[train_idx]
        m_val = row[manager_idx]
        
        if isinstance(t_val, (int, float)) and isinstance(m_val, (int, float)):
            if t_val <= 2:
                low_training.append(m_val)
            else:
                high_training.append(m_val)
                
    # Sort for statistical tests
    low_training.sort()
    high_training.sort()
    
    # Perform certification
    is_noise = certify(low_training, high_training)
    
    avg_low = sum(low_training) / len(low_training) if low_training else 0
    avg_high = sum(high_training) / len(high_training) if high_training else 0
    
    return is_noise, avg_low, avg_high

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    is_noise, avg_low, avg_high = analyze_training_impact(header, rows)
    
    print("--- Training Days vs Years With Current Manager Analysis ---")
    print(f"Average years with manager (Low Training, <=2 days): {avg_low:.2f}")
    print(f"Average years with manager (High Training, >2 days): {avg_high:.2f}")
    
    if is_noise:
        print("\nConclusion: The difference is statistically insignificant (noise).")
        print("More training does not appear to significantly change tenure with the manager.")
    else:
        print("\nConclusion: The difference is statistically significant (not just noise).")
        print("There is a measurable difference in tenure with the manager based on training levels.")
    
    exit(0)
