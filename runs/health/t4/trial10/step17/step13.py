import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they are statistically different. Uses a t-test.
    """
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    # If p-value > 0.05, we fail to reject the null hypothesis (it's noise)
    return p_value > 0.05

def compare_rules(header, rows):
    """
    Compares the performance of the two main criteria: 'absolute_error' and 'squared_error'.
    """
    criterion_idx = header.index('criterion')
    # We use the first goal column (MRE-) as the performance metric to minimize
    mre_idx = 0
    
    # Filter rows by criterion
    abs_err_mre = [row[mre_idx] for row in rows if row[criterion_idx] == 'absolute_error']
    sq_err_mre = [row[mre_idx] for row in rows if row[criterion_idx] == 'squared_error']
    
    is_noise = certify(abs_err_mre, sq_err_mre)
    
    return is_noise, abs_err_mre, sq_err_mre

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
        
        is_noise, abs_err, sq_err = compare_rules(header, rows)
        
        print(f"Comparison of 'absolute_error' vs 'squared_error':")
        print(f"Mean MRE- (absolute): {sum(abs_err)/len(abs_err):.4f}")
        print(f"Mean MRE- (squared):  {sum(sq_err)/len(sq_err):.4f}")
        
        if is_noise:
            print("Conclusion: The difference is statistically insignificant. You can stop arguing.")
        else:
            print("Conclusion: The difference is statistically significant. The choice matters.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
