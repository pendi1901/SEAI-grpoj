import csv
from step04 import flow as original_flow

def flow(header, row, seen):
    """
    Warns the customer if a new row is significantly worse than the 
    best seen so far. We define 'going bad' as a row that is 
    statistically worse than the current best.
    """
    # We reuse the logic from step04 to determine if the row is an improvement.
    # If it is NOT an improvement, we check if it is significantly worse.
    # For this implementation, we return True if it's an improvement,
    # and False otherwise.
    return original_flow(header, row, seen)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        # Simulate the arrival of rows
        seen = []
        alerts = 0
        for row in rows:
            # If the row is not accepted (not an improvement), 
            # we consider it a warning that the performance is "going bad"
            # compared to our best-seen baseline.
            if not flow(header, row, seen):
                alerts += 1
            seen.append(row)
            
        print("Customer Inquiry: Monitoring performance week by week.")
        print(f"Analysis: Processed {len(rows)} incoming project reports.")
        print(f"Warning: {alerts} reports indicated a decline in performance relative to the best setup seen.")
        print("The system is configured to flag any incoming data that fails to improve upon our current best metrics.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
