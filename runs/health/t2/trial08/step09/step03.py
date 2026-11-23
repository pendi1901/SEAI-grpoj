import csv
import math

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically similar 
    (i.e., the difference is likely noise), False if they are significantly different.
    Uses a simple T-test approach for independent samples.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    mean1, mean2 = sum(xs) / n1, sum(ys) / n2
    var1 = sum((x - mean1) ** 2 for x in xs) / (n1 - 1)
    var2 = sum((y - mean2) ** 2 for y in ys) / (n2 - 1)
    
    # Pooled standard error
    se = math.sqrt((var1 / n1) + (var2 / n2))
    if se == 0:
        return mean1 == mean2
    
    t_stat = abs(mean1 - mean2) / se
    # For a 95% confidence level, t-critical is approx 1.96
    return t_stat < 1.96

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    try:
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

        # "Big" vs "Small" setups based on N_estimators
        n_est_idx = header.index('N_estimators')
        acc_idx = header.index('ACC+')
        
        median_n = sum(r[n_est_idx] for r in rows) / len(rows)
        
        small = [r[acc_idx] for r in rows if r[n_est_idx] <= median_n]
        big = [r[acc_idx] for r in rows if r[n_est_idx] > median_n]
        
        is_noise = certify(small, big)
        
        print("Analysis: Is the difference between big and small setups real or noise?")
        if is_noise:
            print("Result: The observed difference is likely just noise.")
        else:
            print("Result: The difference is statistically significant.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
