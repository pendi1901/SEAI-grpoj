import csv
import step01

def flow(header, row, seen):
    """
    Decides whether to accept a row based on whether it is better than
    the best rows seen so far. We use the scoring logic from step01.
    If the row is in the top 5% of all rows seen so far, we accept it.
    """
    if not seen:
        return True
    
    # Combine current row with seen rows to evaluate relative performance
    all_rows = seen + [row]
    best_indices = step01.remember(header, all_rows)
    
    # If the current row (the last one) is among the best, accept it
    return (len(all_rows) - 1) in best_indices

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(x) for x in row])
            
    accepted_count = 0
    seen = []
    
    # Simulate the arrival process
    for row in rows:
        if flow(header, row, seen):
            accepted_count += 1
        seen.append(row)
        
    print("Customer Inquiry: Sequential Approval Process")
    print(f"Total proposals reviewed: {len(rows)}")
    print(f"Proposals approved: {accepted_count}")
    print("Decision strategy: Approved if the proposal ranks in the top 5% of all seen so far.")
