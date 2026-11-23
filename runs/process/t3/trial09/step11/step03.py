import csv
import pandas as pd
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (same apart from noise), False if they differ.
    Uses Welch's t-test for independent samples.
    """
    # If samples are too small, we cannot reject the null hypothesis
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    # Perform Welch's t-test (does not assume equal variance)
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

def analyze_team_size_impact(header, rows):
    """
    Splits data into small and big team setups and compares their costs.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Identify 'Team Size' and 'Cost-'
    # Team Size is an input, Cost- is a goal
    median_team_size = df['Team Size'].median()
    
    small_teams = df[df['Team Size'] <= median_team_size]['Cost-']
    big_teams = df[df['Team Size'] > median_team_size]['Cost-']
    
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
                processed_row = [float(val) if i < len(header) - 3 or (i >= len(header) - 3 and val.replace('.','',1).isdigit()) else val for i, val in enumerate(row)]
                rows.append(processed_row)
        
        is_same, mean_small, mean_big = analyze_team_size_impact(header, rows)
        
        print("Customer Inquiry: Are small-team setups cheaper than big-team ones?")
        print("-" * 60)
        print(f"Mean Cost (Small Teams): {mean_small:.4f}")
        print(f"Mean Cost (Big Teams):   {mean_big:.4f}")
        
        if is_same:
            print("\nConclusion: The difference is statistically insignificant.")
            print("It appears the observed difference was likely due to luck/noise.")
        else:
            print("\nConclusion: The difference is statistically significant.")
            print("Small-team setups are genuinely different in cost compared to big-team ones.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
