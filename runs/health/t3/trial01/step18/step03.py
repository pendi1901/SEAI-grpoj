import csv
from scipy import stats

def certify(xs, ys):
    """
    Determines if two distributions are statistically different.
    Uses the Mann-Whitney U test to check if the distributions of 
    accuracies for 'big' vs 'small' setups are significantly different.
    Returns True if they are the same (p > 0.05), False if they differ.
    """
    # Null hypothesis: The two samples are drawn from the same distribution.
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same).
    stat, p_value = stats.mannwhitneyu(xs, ys, alternative='two-sided')
    return p_value > 0.05

def analyze_setups(header, rows):
    """
    Divides data into 'big' and 'small' based on N_estimators 
    and compares their ACC+ performance.
    """
    n_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    # Define 'big' as above the median N_estimators
    n_values = [row[n_idx] for row in rows]
    median_n = sum(n_values) / len(n_values)
    
    big_acc = [row[acc_idx] for row in rows if row[n_idx] > median_n]
    small_acc = [row[acc_idx] for row in rows if row[n_idx] <= median_n]
    
    is_same = certify(big_acc, small_acc)
    
    if is_same:
        return "The difference in accuracy between big and small setups is likely just noise."
    else:
        return "There is a statistically significant difference in accuracy between big and small setups."

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                # Numeric columns are those that don't contain 'criterion'
                if header[i] == 'criterion':
                    processed_row.append(val)
                else:
                    processed_row.append(float(val))
            rows.append(processed_row)
    
    result = analyze_setups(header, rows)
    print(result)
