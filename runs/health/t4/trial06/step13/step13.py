import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they are statistically significantly different.
    Uses Welch's t-test.
    """
    # If the variance is zero or lists are empty, they are effectively the same
    if len(xs) < 2 or len(ys) < 2:
        return True
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    # If p_value > 0.05, we fail to reject the null hypothesis (it's noise)
    return p_value > 0.05

def compare_criteria(header, rows):
    """
    Compares the performance (MRE-) of different 'criterion' settings.
    """
    crit_idx = header.index('criterion')
    mre_idx = 0  # MRE- is the first column
    
    # Group MRE- values by criterion
    groups = {}
    for row in rows:
        crit = row[crit_idx]
        if crit not in groups:
            groups[crit] = []
        groups[crit].append(row[mre_idx])
    
    # Compare each pair of criteria
    criteria = list(groups.keys())
    results = {}
    for i in range(len(criteria)):
        for j in range(i + 1, len(criteria)):
            c1, c2 = criteria[i], criteria[j]
            is_noise = certify(groups[c1], groups[c2])
            results[(c1, c2)] = is_noise
            
    return results, groups

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)

    comparisons, groups = compare_criteria(header, rows)
    
    print("Comparison of 'criterion' settings (MRE-):")
    for (c1, c2), is_noise in comparisons.items():
        status = "statistically indistinguishable (noise)" if is_noise else "significantly different"
        print(f"- {c1} vs {c2}: {status}")
    
    print("\nConclusion:")
    if all(comparisons.values()):
        print("You can stop arguing; the choice of criterion does not make a real difference.")
    else:
        print("The choice of criterion does make a real difference; choose carefully.")
