import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (same apart from noise), False if they differ.
    Uses Welch's t-test for independent samples.
    """
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    # Welch's t-test does not assume equal variance
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

def analyze_shift(header, rows):
    """
    Splits data into two halves (before/after spring change) and compares 
    the aggregate performance of the goal columns.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    # Calculate a composite score for each row
    # Normalize goals: 1 - (val - min)/(max - min) for '-'
    # (val - min)/(max - min) for '+'
    scores = []
    for row in rows:
        row_score = 0
        for idx in goal_indices:
            col_vals = [r[idx] for r in rows]
            min_v, max_v = min(col_vals), max(col_vals)
            rng = max_v - min_v if max_v != min_v else 1
            norm = (row[idx] - min_v) / rng
            row_score += (1 - norm) if header[idx].endswith('-') else norm
        scores.append(row_score / len(goal_indices))
    
    # Split into two halves (assuming chronological order)
    mid = len(scores) // 2
    before = scores[:mid]
    after = scores[mid:]
    
    is_same = certify(before, after)
    return is_same, sum(before)/len(before), sum(after)/len(after)

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
        
        is_same, mean_before, mean_after = analyze_shift(header, rows)
        
        print("Customer Inquiry: Did the spring process change yield different results?")
        print("-" * 70)
        print(f"Mean Performance (Before): {mean_before:.4f}")
        print(f"Mean Performance (After):  {mean_after:.4f}")
        
        if is_same:
            print("\nConclusion: The results are statistically indistinguishable.")
            print("The shift in team decision-making did not produce a significant change.")
        else:
            print("\nConclusion: The results are statistically different.")
            print("The change in process has had a measurable impact on project outcomes.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
