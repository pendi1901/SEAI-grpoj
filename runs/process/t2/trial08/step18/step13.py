import csv
import step03

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically similar
    (i.e., the difference is likely noise), False if they differ significantly.
    Uses the A12 effect size check from step03.
    """
    return step03.certify(xs, ys)

def get_score(row, header):
    """Calculates a normalized score for a row."""
    total = 0
    for i, name in enumerate(header):
        if name.endswith('-'):
            total += row[i]
        elif name.endswith('+'):
            total += (1.0 - row[i])
    return total

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # Split the data into two halves to represent "before" and "after" the change
        # The prompt implies a temporal shift or a split in the data
        mid = len(rows) // 2
        before = rows[:mid]
        after = rows[mid:]
        
        scores_before = [get_score(r, header) for r in before]
        scores_after = [get_score(r, header) for r in after]
        
        is_noise = certify(scores_before, scores_after)
        
        print("Customer Inquiry: In spring we changed how teams decide what to build first. Did results really shift, or are they the same as before?")
        if is_noise:
            print("Answer: The results are statistically the same; the observed differences are likely just noise.")
        else:
            avg_before = sum(scores_before) / len(scores_before)
            avg_after = sum(scores_after) / len(scores_after)
            print(f"Answer: The results have shifted significantly. The average performance score changed from {avg_before:.4f} to {avg_after:.4f}.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
