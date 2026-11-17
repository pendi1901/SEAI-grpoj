import pandas as pd
import numpy as np
from scipy import stats
from step01 import remember
import csv

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is not statistically 
    significant (p > 0.05), False otherwise.
    """
    # Use Welch's t-test (equal_var=False) to compare means
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

if __name__ == "__main__":
    filename = 'pom3a.train.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(rows, columns=header)
    # Convert numeric columns to float
    for col in header:
        if col[0].isupper():
            df[col] = df[col].astype(float)

    # Identify Team Size column and Cost- column
    # Based on the provided header: 'Team Size' is index 8, 'Cost-' is index 9
    team_size_col = 'Team Size'
    cost_col = 'Cost-'

    # Define small vs big teams based on median split
    median_size = df[team_size_col].median()
    small_teams = df[df[team_size_col] <= median_size][cost_col].tolist()
    big_teams = df[df[team_size_col] > median_size][cost_col].tolist()

    # Check if the difference is statistically significant
    is_same = certify(small_teams, big_teams)

    print("Customer Inquiry: Are small-team setups cheaper than big-team ones?")
    if not is_same and np.mean(small_teams) < np.mean(big_teams):
        print("Answer: Yes, the difference is statistically significant and small teams are indeed cheaper.")
    elif not is_same:
        print("Answer: There is a statistically significant difference, but small teams are not cheaper.")
    else:
        print("Answer: No, the observed difference is likely due to luck (not statistically significant).")
