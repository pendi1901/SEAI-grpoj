import csv
import pandas as pd
import numpy as np
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (p > 0.05),
    False if they are significantly different.
    """
    # Use Welch's t-test (does not assume equal variance)
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_teams(header, rows):
    """
    Compares 'Cost-' for small vs large teams.
    Small teams: Team Size < median. Large teams: Team Size >= median.
    """
    df = pd.DataFrame(rows, columns=header)
    median_team_size = df['Team Size'].median()
    
    small_teams = df[df['Team Size'] < median_team_size]['Cost-']
    large_teams = df[df['Team Size'] >= median_team_size]['Cost-']
    
    is_same = certify(small_teams.tolist(), large_teams.tolist())
    
    return small_teams.mean(), large_teams.mean(), is_same

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        small_mean, large_mean, is_same = analyze_teams(header, rows)
        
        print("Customer Inquiry: Are small-team setups cheaper than big-team ones?")
        print(f"Average Cost (Small Teams): {small_mean:.4f}")
        print(f"Average Cost (Large Teams): {large_mean:.4f}")
        
        if is_same:
            print("Conclusion: The difference is statistically insignificant. It was likely luck.")
        else:
            print("Conclusion: The difference is statistically significant. Small teams are genuinely cheaper.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
