import csv
import pandas as pd
import numpy as np
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (null hypothesis 
    not rejected), False if they are significantly different.
    Uses Welch's t-test for independent samples with unequal variances.
    """
    # Use a significance level of 0.05
    # If p > 0.05, we fail to reject the null hypothesis (they are the same)
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_shift(header, rows):
    """
    Splits the data into two halves (before and after the change in spring)
    and compares the performance (aggregate goal score) to see if results shifted.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal columns
    goals = [c for c in header if c.endswith('-') or c.endswith('+')]
    
    # Normalize goals to [0, 1] range to create a single performance metric
    normalized_goals = pd.DataFrame(index=df.index)
    for goal in goals:
        col = df[goal].astype(float)
        if goal.endswith('-'):
            normalized_goals[goal] = (col - col.min()) / (col.max() - col.min() + 1e-9)
        else:
            normalized_goals[goal] = (col.max() - col) / (col.max() - col.min() + 1e-9)
            
    df['score'] = normalized_goals.sum(axis=1)
    
    # Split data into two halves (assuming chronological order)
    mid = len(df) // 2
    before = df.iloc[:mid]['score'].tolist()
    after = df.iloc[mid:]['score'].tolist()
    
    is_same = certify(before, after)
    return is_same, np.mean(before), np.mean(after)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if val.replace('.', '', 1).isdigit() or 
                                 (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                                 else val for val in row]
                rows.append(processed_row)
        
        is_same, mean_before, mean_after = analyze_shift(header, rows)
        
        print("Customer Inquiry: Did the results shift after the change in how teams decide what to build?")
        print(f"Average performance score before: {mean_before:.4f}")
        print(f"Average performance score after:  {mean_after:.4f}")
        
        if is_same:
            print("Answer: The results are statistically the same; the change did not have a significant impact.")
        else:
            print("Answer: The results are statistically different; the change in decision-making has shifted performance.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
