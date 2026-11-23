import csv
import pandas as pd
import numpy as np
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is statistically 
    insignificant (likely noise), False if they are significantly different.
    Uses Welch's t-test for independent samples with unequal variances.
    """
    # If the samples are too small, we cannot reliably reject the null hypothesis
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    # Perform Welch's t-test
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

def analyze_team_size_impact(header, rows):
    df = pd.DataFrame(rows, columns=header)
    
    # Identify goal column (Cost-)
    # We want to see if Cost- differs between small and large teams
    # 'Team Size' is a numeric column
    median_team_size = df['Team Size'].median()
    
    small_teams = df[df['Team Size'] <= median_team_size]['Cost-']
    large_teams = df[df['Team Size'] > median_team_size]['Cost-']
    
    is_same = certify(small_teams.tolist(), large_teams.tolist())
    
    return is_same, small_teams.mean(), large_teams.mean()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if i < len(row) - 3 or i < 9 else val 
                                 for i, val in enumerate(row)]
                # Ensure numeric conversion for all columns
                rows.append([float(x) for x in row])
        
        is_same, mean_small, mean_large = analyze_team_size_impact(header, rows)
        
        print("Customer Report: Team Size vs Cost")
        print(f"Average Cost (Small Teams): {mean_small:.4f}")
        print(f"Average Cost (Large Teams): {mean_large:.4f}")
        
        if is_same:
            print("Conclusion: The difference in cost is statistically insignificant.")
            print("It is likely that the observed difference was just luck/noise.")
        else:
            print("Conclusion: The difference in cost is statistically significant.")
            print("The team size has a real impact on the project cost.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
