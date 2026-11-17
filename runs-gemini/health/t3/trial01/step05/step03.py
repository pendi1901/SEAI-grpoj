import csv
import pandas as pd
import numpy as np
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they are statistically significantly different.
    Uses Welch's t-test.
    """
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    # If p_value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

def analyze_setup_size(df):
    """
    Determines if 'big' setups (high N_estimators) perform better than 'small' ones.
    """
    # Identify goal columns
    min_cols = [c for c in df.columns if c.endswith('-')]
    max_cols = [c for c in df.columns if c.endswith('+')]
    
    # Normalize goals to a single performance score [0, 1]
    scores = pd.DataFrame(index=df.index)
    for col in min_cols:
        c_min, c_max = df[col].min(), df[col].max()
        scores[col] = (c_max - df[col]) / (c_max - c_min + 1e-9)
    for col in max_cols:
        c_min, c_max = df[col].min(), df[col].max()
        scores[col] = (df[col] - c_min) / (c_max - c_min + 1e-9)
    
    df['score'] = scores.mean(axis=1)
    
    # Split by N_estimators (median split)
    median_n = df['N_estimators'].median()
    small = df[df['N_estimators'] <= median_n]['score']
    big = df[df['N_estimators'] > median_n]['score']
    
    is_same = certify(small.tolist(), big.tolist())
    
    return is_same, small.mean(), big.mean()

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.train.csv'
    df = pd.read_csv(filename)
    
    # Ensure numeric columns are treated as such
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = pd.to_numeric(df[col], errors='ignore')
            
    is_same, small_avg, big_avg = analyze_setup_size(df)
    
    print("--- Analysis of Setup Size vs Performance ---")
    print(f"Average score for small setups: {small_avg:.4f}")
    print(f"Average score for big setups:   {big_avg:.4f}")
    
    if is_same:
        print("Conclusion: The difference in performance is likely just noise.")
    else:
        print("Conclusion: The difference in performance is statistically significant.")
