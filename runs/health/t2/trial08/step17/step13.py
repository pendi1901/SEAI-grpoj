import csv
import math
from step03 import certify

def compare_criteria(header, rows):
    """
    Compares the performance (ACC+) of two different criteria: 
    'absolute_error' vs 'squared_error'.
    """
    crit_idx = header.index('criterion')
    acc_idx = header.index('ACC+')
    
    abs_err_accs = [r[acc_idx] for r in rows if r[crit_idx] == 'absolute_error']
    sq_err_accs = [r[acc_idx] for r in rows if r[crit_idx] == 'squared_error']
    
    # Use the certify function from step03 to check if the difference is significant
    is_noise = certify(abs_err_accs, sq_err_accs)
    
    return is_noise, abs_err_accs, sq_err_accs

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
                rows.append(processed)
        
        is_noise, abs_accs, sq_accs = compare_criteria(header, rows)
        
        print("Analysis: Does the choice between 'absolute_error' and 'squared_error' matter?")
        if is_noise:
            print("Result: The difference is statistically insignificant. You can stop arguing.")
        else:
            print("Result: The difference is statistically significant. The choice of criterion matters.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
