import csv
from scipy import stats
from step01 import remember

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they are statistically different. Uses a t-test.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    # If p-value > 0.05, we fail to reject the null hypothesis (it's noise)
    return p_value > 0.05

def analyze_correlation(header, rows):
    """
    Checks if 'N_estimators' (size) correlates with 'ACC+' (accuracy).
    """
    # Find indices
    size_idx = header.index('N_estimators')
    acc_idx = header.index('ACC+')
    
    # Split data into small and large setups based on median size
    sizes = [row[size_idx] for row in rows]
    median_size = sum(sizes) / len(sizes)
    
    small_acc = [row[acc_idx] for row in rows if row[size_idx] <= median_size]
    large_acc = [row[acc_idx] for row in rows if row[size_idx] > median_size]
    
    is_noise = certify(small_acc, large_acc)
    
    print(f"Analysis of Accuracy vs Setup Size:")
    print(f"Small setups mean accuracy: {sum(small_acc)/len(small_acc):.4f}")
    print(f"Large setups mean accuracy: {sum(large_acc)/len(large_acc):.4f}")
    
    if is_noise:
        print("Conclusion: The difference is likely just noise.")
    else:
        print("Conclusion: The difference is statistically significant.")
    return not is_noise

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed_row = []
                for val in row:
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                rows.append(processed_row)
        
        analyze_correlation(header, rows)
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
