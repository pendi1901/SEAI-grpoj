import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (same population),
    False if they differ significantly. Uses Welch's t-test.
    """
    # If the samples are too small, we cannot reliably reject the null hypothesis
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    # Welch's t-test (does not assume equal variance)
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_shift(header, rows):
    """
    Splits the data into two halves (before and after the change in spring)
    and compares the aggregate performance of the goals.
    """
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    def get_score(row):
        # Normalize goals to [0, 1] based on the whole dataset
        scores = []
        for i in goal_indices:
            col_vals = [r[i] for r in rows]
            c_min, c_max = min(col_vals), max(col_vals)
            norm = (row[i] - c_min) / (c_max - c_min + 1e-9)
            scores.append(1 - norm if header[i].endswith('-') else norm)
        return sum(scores) / len(scores)

    # Split the data into two halves
    mid = len(rows) // 2
    before = [get_score(row) for row in rows[:mid]]
    after = [get_score(row) for row in rows[mid:]]
    
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
                rows.append([float(val) for val in row])
        
        is_same, mean_before, mean_after = analyze_shift(header, rows)
        
        print("Customer Inquiry Analysis: Did results shift in spring?")
        print(f"Average performance score before change: {mean_before:.4f}")
        print(f"Average performance score after change:  {mean_after:.4f}")
        
        if is_same:
            print("Conclusion: The difference in results is statistically insignificant.")
            print("The change in how teams decide what to build has not resulted in a measurable shift.")
        else:
            print("Conclusion: The difference in results is statistically significant.")
            print("The change in decision-making has had a real impact on project outcomes.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
