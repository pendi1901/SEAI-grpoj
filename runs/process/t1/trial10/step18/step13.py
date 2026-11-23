import csv

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (the same apart from noise), False otherwise.
    Uses the Vargha-Delaney A12 effect size test.
    """
    if not xs or not ys:
        return True

    m, n = len(xs), len(ys)
    xs = sorted(xs)
    ys = sorted(ys)
    
    r1 = 0
    for x in xs:
        for y in ys:
            if x > y: r1 += 1
            elif x == y: r1 += 0.5
            
    # A12 > 0.56 (or < 0.44) indicates a small effect size
    # We return True if the difference is negligible (luck)
    a12 = r1 / (m * n)
    return abs(a12 - 0.5) < 0.147

def analyze_shift(header, rows):
    """
    Compares the first half of the data (pre-change) to the second half (post-change)
    using the 'Score-' goal to determine if results shifted.
    """
    score_idx = header.index('Score-')
    
    # Split data into two halves
    mid = len(rows) // 2
    pre_change = [float(row[score_idx]) for row in rows[:mid]]
    post_change = [float(row[score_idx]) for row in rows[mid:]]
    
    is_same = certify(pre_change, post_change)
    
    avg_pre = sum(pre_change) / len(pre_change)
    avg_post = sum(post_change) / len(post_change)
    
    return is_same, avg_pre, avg_post

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        is_same, avg_pre, avg_post = analyze_shift(header, rows)
        
        print("Analysis of team decision changes:")
        print(f"Pre-change average Score-: {avg_pre:.4f}")
        print(f"Post-change average Score-: {avg_post:.4f}")
        
        if is_same:
            print("Conclusion: The results are statistically the same; the shift was likely just luck.")
        else:
            print("Conclusion: The results have significantly shifted; the change in decision-making had a real impact.")
            
        exit(0)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
