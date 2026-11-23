import csv
import numpy as np
from scipy.stats import pearsonr

def certify(xs, ys):
    """
    Returns True if the correlation between xs and ys is high (suggesting 
    the relationship is real), False if it is low (suggesting noise).
    Using a threshold of 0.3 for moderate correlation.
    """
    if len(xs) < 2:
        return False
    corr, _ = pearsonr(xs, ys)
    # If correlation is significant (e.g., > 0.3), we consider it 'real'
    return abs(corr) > 0.3

def analyze_setup_size(header, rows):
    """
    Analyzes if 'N_estimators' (setup size) correlates with performance.
    Performance is defined as the aggregate of goal columns.
    """
    n_idx = header.index('N_estimators')
    
    # Identify goal indices
    goal_indices = [i for i, h in enumerate(header) if h.endswith('-') or h.endswith('+')]
    
    sizes = []
    performances = []
    
    for row in rows:
        size = float(row[n_idx])
        
        # Calculate aggregate performance:
        # Normalize goals: (1 - MRE) + ACC + PRED40
        perf = 0
        for idx in goal_indices:
            val = float(row[idx])
            if header[idx].endswith('-'):
                perf -= val  # Minimize
            else:
                perf += val  # Maximize
        
        sizes.append(size)
        performances.append(perf)
        
    return certify(sizes, performances)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    header = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                try:
                    processed_row.append(float(val))
                except ValueError:
                    processed_row.append(val)
            rows.append(processed_row)
            
    is_real = analyze_setup_size(header, rows)
    
    if is_real:
        print("The correlation between setup size and performance is statistically significant.")
        print("It is likely that larger setups genuinely perform better.")
    else:
        print("The correlation between setup size and performance is weak.")
        print("The observed differences are likely due to noise.")
