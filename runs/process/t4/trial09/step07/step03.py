import csv
import pandas as pd
import numpy as np
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is statistically 
    insignificant (p > 0.05), False otherwise.
    """
    # Using Welch's t-test (equal_var=False) to compare two independent samples
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_team_size_impact(header, rows):
    """
    Compares 'Cost-' for small vs big teams.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Define small vs big based on median split of 'Team Size'
    median_team = df['Team Size'].median()
    small_teams = df[df['Team Size'] <= median_team]['Cost-']
    big_teams = df[df['Team Size'] > median_team]['Cost-']
    
    is_same = certify(small_teams.tolist(), big_teams.tolist())
    
    return is_same, small_teams.mean(), big_teams.mean()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        is_same, mean_small, mean_big = analyze_team_size_impact(header, rows)
        
        print("Customer Inquiry: Are small-team setups cheaper than big-team ones?")
        print(f"  Mean Cost (Small Teams): {mean_small:.4f}")
        print(f"  Mean Cost (Big Teams):   {mean_big:.4f}")
        
        if is_same:
            print("Conclusion: The difference is statistically insignificant. It was likely luck.")
        else:
            print("Conclusion: The difference is statistically significant. The trend is real.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
