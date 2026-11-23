import csv
import numpy as np

def flow(header, row, seen):
    """
    Implements the Secretary Problem strategy:
    1. Observe a sample (the first 37% of the data).
    2. Establish the best performance seen in that sample.
    3. Accept the first subsequent row that is better than the sample best.
    """
    # Identify goal columns
    goal_indices = [i for i, col in enumerate(header) if col.endswith(('-', '+'))]
    
    def get_score(r):
        # Calculate a normalized score for a row
        # Since we don't have global min/max, we use the current 'seen' data
        # to estimate relative performance.
        scores = []
        for i in goal_indices:
            val = r[i]
            # Simple heuristic: if we don't have enough data, return 0
            # Otherwise, we treat lower '-' and higher '+' as better
            scores.append(val if header[i].endswith('+') else -val)
        return sum(scores)

    # If this is the first row, we can't decide yet
    if not seen:
        return False
    
    # Strategy: Use the first 37% of the total expected data (approx 300 rows)
    # as the 'rejection' phase to learn the baseline.
    sample_size = 300
    
    if len(seen) < sample_size:
        return False
    
    # Find the best score in the sample
    sample_scores = [get_score(r) for r in seen[:sample_size]]
    best_sample_score = max(sample_scores)
    
    # If current row is better than the best in the sample, accept it
    current_score = get_score(row)
    if current_score > best_sample_score:
        return True
    
    # If we reach the end, we must accept the last one
    return False

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Simulate the flow
        seen = []
        chosen = None
        for i, row in enumerate(rows):
            if flow(header, row, seen):
                chosen = (i, row)
                break
            seen.append(row)
            
        print("Customer Inquiry: Online Selection Strategy")
        if chosen:
            print(f"Approved proposal at index {chosen[0]}.")
            print(f"Row data: {chosen[1]}")
        else:
            print("No proposal met the criteria during the selection window.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
