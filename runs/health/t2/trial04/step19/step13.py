import csv
import math
import step03

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (no significant difference),
    False if they differ significantly. Uses the T-test approach from step03.
    """
    return step03.certify(xs, ys)

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [val if header[i] == 'criterion' else float(val) for i, val in enumerate(row)]
            rows.append(processed_row)

    # The customer asks about the choice between the tool's two built-in rules.
    # In this dataset, 'criterion' is the symbolic parameter that defines the rule.
    # We compare 'absolute_error' vs 'squared_error' (the two most common).
    crit_idx = header.index('criterion')
    acc_idx = header.index('ACC+')
    
    abs_err_accs = [r[acc_idx] for r in rows if r[crit_idx] == 'absolute_error']
    sq_err_accs = [r[acc_idx] for r in rows if r[crit_idx] == 'squared_error']
    
    is_similar = certify(abs_err_accs, sq_err_accs)
    
    print("Customer Inquiry: Does the choice between 'absolute_error' and 'squared_error' matter?")
    if is_similar:
        print("Result: The performance difference between these rules is statistically insignificant.")
        print("Advice: You can stop arguing about it; the choice does not impact your results.")
    else:
        print("Result: The performance difference is statistically significant.")
        print("Advice: The choice of rule does matter for your outcomes.")
