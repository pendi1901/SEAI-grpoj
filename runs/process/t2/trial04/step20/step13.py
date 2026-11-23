import csv
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar 
    (i.e., the difference is likely noise), False if they differ.
    Uses the A12 effect size check from step03.
    """
    return step03.certify(xs, ys)

def get_data():
    filename = "pom3a.n1000.train.csv"
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [[float(val) for val in row] for row in reader]
    return header, rows

if __name__ == "__main__":
    header, rows = get_data()
    
    # The customer asks if results shifted after changing how teams decide what to build.
    # We interpret this as comparing the performance of the first half of the data 
    # (pre-change) vs the second half (post-change).
    
    goal_indices = [i for i, name in enumerate(header) 
                    if name.endswith('-') or name.endswith('+')]
    
    def get_score(row):
        total = 0
        for i in goal_indices:
            val = row[i]
            if header[i].endswith('-'):
                total += val
            else:
                total += (1.0 - val)
        return total

    scores = [get_score(r) for r in rows]
    mid = len(scores) // 2
    pre_change = scores[:mid]
    post_change = scores[mid:]
    
    is_same = certify(pre_change, post_change)
    
    print("Analysis: Did the team's decision-making change shift results?")
    if is_same:
        print("Conclusion: The results are statistically similar; the change did not significantly impact performance.")
    else:
        print("Conclusion: The results differ significantly; the change in decision-making had a measurable effect.")
