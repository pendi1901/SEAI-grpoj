import csv
import pandas as pd
import numpy as np
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is statistically 
    insignificant (p > 0.05), False if they are significantly different.
    """
    # Use Welch's t-test (equal_var=False) to compare two independent samples
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        df = pd.DataFrame(rows, columns=header)
        
        # Define 'small' vs 'big' based on median Team Size
        median_team = df['Team Size'].median()
        small_teams = df[df['Team Size'] <= median_team]['Cost-']
        big_teams = df[df['Team Size'] > median_team]['Cost-']
        
        # Check if the difference is statistically significant
        is_luck = certify(small_teams.tolist(), big_teams.tolist())
        
        print("Customer Inquiry: Are small-team setups cheaper than big-team ones?")
        if is_luck:
            print("Answer: The observed difference is likely due to luck (not statistically significant).")
        else:
            print("Answer: The difference is real and statistically significant.")
            print(f"Small team average cost: {small_teams.mean():.4f}")
            print(f"Big team average cost: {big_teams.mean():.4f}")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
