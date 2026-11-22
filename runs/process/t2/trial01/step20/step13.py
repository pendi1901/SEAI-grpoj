import csv
from step03 import certify

def analyze_shift(header, rows):
    """
    Splits the data into two halves (before and after the 'spring' change)
    and checks if the goal distributions are statistically similar.
    """
    # We assume the data is chronological. We split into two halves.
    mid = len(rows) // 2
    before = rows[:mid]
    after = rows[mid:]
    
    # We evaluate the 'Cost-' goal as a proxy for the overall result shift
    goal_idx = header.index('Cost-')
    
    xs = [row[goal_idx] for row in before]
    ys = [row[goal_idx] for row in after]
    
    return certify(xs, ys), xs, ys

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        is_same, xs, ys = analyze_shift(header, rows)
        
        print("Customer Inquiry: In spring we changed how teams decide what to build first. Did results really shift?")
        if is_same:
            print("Answer: No, the results are statistically similar. The change did not cause a significant shift.")
        else:
            print("Answer: Yes, the results shifted significantly. The change had a measurable impact.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
