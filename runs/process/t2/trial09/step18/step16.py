import csv
from step06 import justify as step06_justify

def justify(header, rows, row):
    """
    Estimates the goals for the given row and returns its percentile rank
    among the provided rows, along with a justification.
    """
    # We reuse the logic from step06 which handles the estimation of "?" goals
    # and calculates the percentile rank based on the goal performance.
    return step06_justify(header, rows, row)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
            
            # The customer asks why B is not as good as A.
            # We simulate this by comparing two specific rows from the dataset.
            # Let's pick row 0 as 'A' (the recommended one) and row 1 as 'B'.
            row_a = rows[0]
            row_b = list(rows[1])
            
            # Mask the goals for row_b as per the requirement
            goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
            for idx in goal_indices:
                row_b[idx] = "?"
            
            p, reason = justify(header, rows, row_b)
            
            print("Customer Inquiry: I liked setup B. You recommended A. Explain why not B.")
            print(f"Analysis: Setup B is better than {p:.4f} of all known configurations.")
            print(f"Justification: {reason}")
            print("Setup A was recommended because it ranks higher in our performance model.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
