import csv
import pandas as pd
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is not statistically 
    significant (i.e., they are the same apart from noise), False otherwise.
    Uses Welch's t-test.
    """
    # If the p-value is greater than 0.05, we fail to reject the null hypothesis
    # (meaning the difference is likely due to noise/luck).
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_team_size_impact(header, rows):
    """
    Compares Cost- for small-team setups vs big-team setups.
    """
    df = pd.DataFrame(rows, columns=header)
    
    # Define small vs big based on the median of 'Team Size'
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
                processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
                rows.append(processed_row)
        
        is_same, mean_small, mean_big = analyze_team_size_impact(header, rows)
        
        print("Customer Inquiry: Is the difference in cost between small and big teams real?")
        print("-" * 70)
        print(f"Average Cost- (Small Teams): {mean_small:.4f}")
        print(f"Average Cost- (Big Teams):   {mean_big:.4f}")
        
        if is_same:
            print("\nConclusion: The observed difference is likely due to noise (luck).")
            print("The setups are statistically similar.")
        else:
            print("\nConclusion: The difference is statistically significant.")
            print("Small-team setups are genuinely different in cost compared to big-team ones.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
