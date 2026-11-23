import csv
import math
import step03

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (null hypothesis),
    False if they differ significantly. Uses the t-test logic from step03.
    """
    return step03.certify(xs, ys)

def analyze_shift(header, rows):
    """
    Splits the data into two halves (before and after the 'spring' change)
    and compares the performance goals to see if results shifted.
    """
    # We use the first goal column as a proxy for 'results'
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_idx = i
            break
            
    mid = len(rows) // 2
    before = [float(row[goal_idx]) for row in rows[:mid]]
    after = [float(row[goal_idx]) for row in rows[mid:]]
    
    is_same = certify(before, after)
    return before, after, is_same

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            before, after, is_same = analyze_shift(header, rows)
            
            print("Customer Inquiry: Did results shift after the spring change?")
            print(f"Average result before: {sum(before)/len(before):.4f}")
            print(f"Average result after: {sum(after)/len(after):.4f}")
            
            if is_same:
                print("Conclusion: The results are statistically the same. The change had no significant impact.")
            else:
                print("Conclusion: The results have shifted significantly. The change had a measurable impact.")
                
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
