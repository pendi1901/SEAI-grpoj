import csv

def certify(xs, ys):
    """
    Determines if two distributions are significantly different using the 
    A12 effect size statistic. Returns True if they are the same (noise), 
    False if they really differ.
    """
    if not xs or not ys:
        return True

    def a12(lst1, lst2):
        m, n = len(lst1), len(lst2)
        count = 0
        for x in lst1:
            for y in lst2:
                if x > y: count += 1
                elif x == y: count += 0.5
        return count / (m * n)

    # A12 threshold: 0.56 is small, 0.64 medium, 0.71 large.
    # We use 0.6 as a conservative threshold for "really differ".
    score = a12(xs, ys)
    return 0.4 <= score <= 0.6

if __name__ == "__main__":
    filename = 'Health-ClosedIssues0000.n1000.train.csv'
    try:
        rows = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                processed = [float(val) if header[i] not in ['criterion'] else val 
                             for i, val in enumerate(row)]
                rows.append(processed)

        # The customer asks about the choice of 'criterion' (the tool's built-in rule).
        # We compare the performance (ACC+) of 'absolute_error' vs 'squared_error'.
        crit_idx = header.index('criterion')
        acc_idx = header.index('ACC+')
        
        abs_err_acc = [r[acc_idx] for r in rows if r[crit_idx] == 'absolute_error']
        sq_err_acc = [r[acc_idx] for r in rows if r[crit_idx] == 'squared_error']
        
        is_noise = certify(abs_err_acc, sq_err_acc)
        
        print("Analysis: Does the choice of 'criterion' (absolute_error vs squared_error) impact accuracy?")
        if is_noise:
            print("Result: The difference is statistically insignificant. You can stop arguing about it.")
        else:
            print("Result: There is a statistically significant difference. The choice of rule matters.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
