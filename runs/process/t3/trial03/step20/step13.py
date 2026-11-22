import csv
import numpy as np
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is statistically 
    insignificant (likely noise), False if they are significantly different.
    Uses Welch's t-test for independent samples with unequal variances.
    """
    # If the distributions are identical or have zero variance, they are the same
    if len(set(xs)) == 1 and len(set(ys)) == 1 and xs[0] == ys[0]:
        return True
        
    # Welch's t-test (equal_var=False)
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False, nan_policy='omit')
    
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

def get_aggregate(row, header, goal_indices, mins, maxs):
    """Calculates a normalized aggregate score for a row."""
    scores = []
    for i in goal_indices:
        val = row[i]
        col_min = mins[i]
        col_max = maxs[i]
        # Normalize to [0, 1]
        norm = (val - col_min) / (col_max - col_min + 1e-9)
        # '-' is minimized, '+' is maximized
        if header[i].endswith('-'):
            scores.append(1.0 - norm)
        else:
            scores.append(norm)
    return sum(scores) / len(scores)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Split data into two halves to represent "before" and "after" the change
        mid = len(rows) // 2
        before = rows[:mid]
        after = rows[mid:]
        
        # Identify goal columns and their ranges for normalization
        goal_indices = [i for i, name in enumerate(header) if name.endswith('-') or name.endswith('+')]
        all_vals = np.array(rows)
        mins = np.min(all_vals, axis=0)
        maxs = np.max(all_vals, axis=0)
        
        # Calculate aggregate scores for both periods
        scores_before = [get_aggregate(r, header, goal_indices, mins, maxs) for r in before]
        scores_after = [get_aggregate(r, header, goal_indices, mins, maxs) for r in after]
        
        # Determine if they are statistically different
        is_same = certify(scores_before, scores_after)
        
        print("Analysis: Did the team's process change result in a real shift?")
        if is_same:
            print("Result: The performance distributions are statistically indistinguishable.")
            print("Conclusion: The observed differences are likely just noise; no real shift occurred.")
        else:
            print("Result: The performance distributions are statistically different.")
            print("Conclusion: The process change had a genuine impact on project outcomes.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
