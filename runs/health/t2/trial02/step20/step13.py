import csv
import step03

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is likely noise,
    False if they really differ. Uses the T-test logic from step03.
    """
    return step03.certify(xs, ys)

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

    # The customer asks about the 'criterion' column (the tool's built-in rules).
    # We compare the performance (MRE-) of the two most common criteria.
    crit_idx = header.index('criterion')
    mre_idx = header.index('MRE-')
    
    # Get unique criteria
    criteria = list(set(r[crit_idx] for r in rows))
    
    # Compare the two most frequent criteria
    c1, c2 = criteria[0], criteria[1]
    
    xs = [r[mre_idx] for r in rows if r[crit_idx] == c1]
    ys = [r[mre_idx] for r in rows if r[crit_idx] == c2]
    
    is_noise = certify(xs, ys)
    
    print("Customer Inquiry: 'Does the choice between the tool's two built-in rules make any real difference, or can I stop arguing about it?'")
    if is_noise:
        print(f"Answer: The difference in performance between '{c1}' and '{c2}' is statistically insignificant; you can stop arguing about it.")
    else:
        print(f"Answer: There is a statistically significant difference between '{c1}' and '{c2}'. The choice of rule matters.")
