import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (noise), False if they are significantly different.
    """
    return step03.certify(xs, ys)

def get_tenure_by_training(header, rows):
    """
    Splits the data into two groups: those with high training (>= 3 days)
    and those with low training (< 3 days). Returns the 'YearsWithCurrManager+' 
    values for both groups.
    """
    training_idx = header.index('TrainingTimesLastYear')
    manager_idx = header.index('YearsWithCurrManager+')
    
    high_training = []
    low_training = []
    
    for row in rows:
        t_val = row[training_idx]
        m_val = row[manager_idx]
        if isinstance(t_val, (int, float)) and isinstance(m_val, (int, float)):
            if t_val >= 3:
                high_training.append(m_val)
            else:
                low_training.append(m_val)
                
    return high_training, low_training

if __name__ == "__main__":
    file_path = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    high_group, low_group = get_tenure_by_training(header, rows)
    
    is_noise = certify(high_group, low_group)
    
    print("Analysis: Do people with more training (>=3 days) stay longer with their manager?")
    print(f"Average years with manager (High Training): {sum(high_group)/len(high_group):.2f} years")
    print(f"Average years with manager (Low Training) : {sum(low_group)/len(low_group):.2f} years")
    
    if is_noise:
        print("Result: The difference is statistically insignificant (noise).")
    else:
        print("Result: The difference is statistically significant (real).")
