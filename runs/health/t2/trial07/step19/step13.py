import csv
import step03

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable (noise),
    False if they differ significantly (real effect).
    Uses the A12 effect size test from step03.
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
                processed = [val if header[i] == 'criterion' else float(val) 
                             for i, val in enumerate(row)]
                rows.append(processed)

        # The customer asks about the choice between the tool's built-in rules.
        # In this dataset, the 'criterion' column represents the choice of rule.
        # We compare the performance (ACC+) of the two most common criteria.
        crit_idx = header.index('criterion')
        acc_idx = header.index('ACC+')
        
        # Identify the two most frequent criteria
        criteria = {}
        for r in rows:
            c = r[crit_idx]
            criteria[c] = criteria.get(c, []) + [r[acc_idx]]
        
        sorted_crit = sorted(criteria.keys(), key=lambda k: len(criteria[k]), reverse=True)
        
        if len(sorted_crit) >= 2:
            c1, c2 = sorted_crit[0], sorted_crit[1]
            xs, ys = criteria[c1], criteria[c2]
            
            is_noise = certify(xs, ys)
            
            print(f"Comparing the two most common rules: '{c1}' vs '{c2}'.")
            if is_noise:
                print("Result: The difference is likely noise. You can stop arguing about it.")
            else:
                print("Result: The difference is real. The choice of rule matters.")
        else:
            print("Not enough distinct rules to compare.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
