import csv

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (the difference is noise), False otherwise.
    Uses the Vargha-Delaney A12 effect size test.
    """
    n_x = len(xs)
    n_y = len(ys)
    if n_x == 0 or n_y == 0:
        return True

    greater = 0
    less = 0
    for x in xs:
        for y in ys:
            if x > y:
                greater += 1
            elif x < y:
                less += 1
    
    equal = (n_x * n_y) - greater - less
    a12 = (greater + 0.5 * equal) / (n_x * n_y)
    
    # A12 threshold: if between 0.4 and 0.6, the difference is negligible (noise).
    return 0.4 <= a12 <= 0.6

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [val if header[i] == 'criterion' else float(val) 
                                 for i, val in enumerate(row)]
                rows.append(processed_row)
        
        # The customer asks about the choice of 'criterion' (the tool's built-in rule).
        # We compare the performance (ACC+) of the two most common criteria.
        crit_idx = header.index('criterion')
        acc_idx = header.index('ACC+')
        
        # Identify the two most frequent criteria
        criteria = {}
        for r in rows:
            c = r[crit_idx]
            criteria[c] = criteria.get(c, 0) + 1
        
        top_two = sorted(criteria.keys(), key=lambda x: criteria[x], reverse=True)[:2]
        
        group1 = [r[acc_idx] for r in rows if r[crit_idx] == top_two[0]]
        group2 = [r[acc_idx] for r in rows if r[crit_idx] == top_two[1]]
        
        is_noise = certify(group1, group2)
        
        print(f"Comparing performance (ACC+) between '{top_two[0]}' and '{top_two[1]}':")
        if is_noise:
            print("Answer: The difference is statistically insignificant. You can stop arguing about it.")
        else:
            print("Answer: There is a statistically significant difference. The choice of rule matters.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
