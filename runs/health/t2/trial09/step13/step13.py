import csv
from step03 import certify

def analyze_criterion(header, rows):
    """
    Compares the performance (ACC+) of the two most common criteria:
    'absolute_error' and 'squared_error'.
    """
    crit_idx = header.index('criterion')
    acc_idx = header.index('ACC+')
    
    abs_err_accs = [r[acc_idx] for r in rows if r[crit_idx] == 'absolute_error']
    sq_err_accs = [r[acc_idx] for r in rows if r[crit_idx] == 'squared_error']
    
    is_noise = certify(abs_err_accs, sq_err_accs)
    
    return is_noise, abs_err_accs, sq_err_accs

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
            rows.append(processed_row)

    is_noise, abs_accs, sq_accs = analyze_criterion(header, rows)
    
    print("Analysis of ACC+ by criterion (absolute_error vs squared_error):")
    print(f"Mean ACC+ (absolute_error): {sum(abs_accs)/len(abs_accs):.4f}")
    print(f"Mean ACC+ (squared_error):  {sum(sq_accs)/len(sq_accs):.4f}")
    
    if is_noise:
        print("\nConclusion: The difference between these criteria is statistically insignificant.")
        print("You can stop arguing about it; the choice does not make a real difference.")
    else:
        print("\nConclusion: The difference is statistically significant.")
        print("The choice of criterion does impact performance.")
