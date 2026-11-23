import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is statistically 
    insignificant (likely noise), False if they are significantly different.
    Uses Welch's t-test for independent samples.
    """
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    # Welch's t-test (does not assume equal variance)
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

def analyze_shift(header, rows):
    """
    Compares the first half of the data (pre-change) with the second half (post-change)
    across all goal columns to see if the results shifted significantly.
    """
    goal_indices = [i for i, col in enumerate(header) if col.endswith(('-', '+'))]
    
    # Split data into two halves
    mid = len(rows) // 2
    first_half = rows[:mid]
    second_half = rows[mid:]
    
    results = {}
    for idx in goal_indices:
        col_name = header[idx]
        xs = [row[idx] for row in first_half]
        ys = [row[idx] for row in second_half]
        
        is_same = certify(xs, ys)
        results[col_name] = is_same
        
    return results

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        shift_analysis = analyze_shift(header, rows)
        
        print("Customer Inquiry: Did results shift after the team process change?")
        all_same = True
        for col, is_same in shift_analysis.items():
            if not is_same:
                print(f"- Significant shift detected in: {col}")
                all_same = False
        
        if all_same:
            print("Conclusion: No statistically significant shift was detected across any goal.")
            print("The results appear to be the same as before; the change did not impact performance.")
        else:
            print("\nConclusion: The results have shifted significantly in the metrics listed above.")
            print("The team process change had a measurable impact on project outcomes.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
