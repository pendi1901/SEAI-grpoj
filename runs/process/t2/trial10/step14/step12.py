import csv
import step01
import step02

def guess(header, train, test):
    """
    Estimates the first goal column for test rows.
    The customer asks about a scenario where requirements change twice as fast
    halfway through the data. We model this by splitting the training data
    into two halves and weighting the second half (the 'faster' change period)
    more heavily when calculating the average for the estimate.
    """
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith('-') or name.endswith('+'):
            goal_idx = i
            break
    
    # Split training data into two halves
    mid = len(train) // 2
    first_half = train[:mid]
    second_half = train[mid:]
    
    # Identify best rows in each half using step01
    best_first = step01.remember(header, first_half)
    best_second = step01.remember(header, second_half)
    
    # Calculate weighted average: second half (faster changes) counts for 2x
    vals_first = [float(first_half[i][goal_idx]) for i in best_first]
    vals_second = [float(second_half[i][goal_idx]) for i in best_second]
    
    avg_first = sum(vals_first) / len(vals_first) if vals_first else 0
    avg_second = sum(vals_second) / len(vals_second) if vals_second else 0
    
    # Weighted estimate
    estimate = (avg_first + (2 * avg_second)) / 3
    
    return [estimate for _ in test]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
            # Use 800 rows for training, 100 for testing
            train = rows[:800]
            test = rows[800:900]
            
            estimates = guess(header, train, test)
            
            print("Customer Inquiry: What happens to cost/idle time if requirements change twice as fast?")
            print(f"Estimated value for the first goal column: {estimates[0]:.4f}")
            print("Analysis: By weighting the second half of the data (representing accelerated change) "
                  "more heavily, we project the impact on performance goals.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
