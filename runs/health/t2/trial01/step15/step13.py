import csv
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (noise),
    False if they are significantly different.
    Uses the logic from step03.
    """
    return step03.certify(xs, ys)

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = []
                for i, val in enumerate(row):
                    if header[i] in ['MRE-', 'ACC+', 'PRED40+', 'N_estimators', 
                                     'Min_sample_leaves', 'Min_impurity_decrease', 'Max_depth']:
                        processed.append(float(val))
                    else:
                        processed.append(val)
                rows.append(processed)

        # The "two built-in rules" refers to the 'criterion' column.
        # The data contains 'absolute_error', 'poisson', and 'squared_error'.
        # We compare the two most common ones: 'squared_error' and 'absolute_error'.
        crit_idx = header.index('criterion')
        mre_idx = header.index('MRE-')
        
        squared_mre = [r[mre_idx] for r in rows if r[crit_idx] == 'squared_error']
        absolute_mre = [r[mre_idx] for r in rows if r[crit_idx] == 'absolute_error']
        
        is_noise = certify(squared_mre, absolute_mre)
        
        print("Analysis: Does the choice of 'criterion' rule make a real difference?")
        if is_noise:
            print("Answer: No, the difference between the rules is likely just noise. You can stop arguing.")
        else:
            print("Answer: Yes, the difference is statistically significant.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
