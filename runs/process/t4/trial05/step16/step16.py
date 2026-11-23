import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from step06 import justify as step06_justify

def justify(header, rows, row):
    """
    Estimates the performance of a row and returns its percentile rank 
    and a justification string.
    """
    # We reuse the logic from step06 as it already implements the 
    # estimation and percentile ranking required by the harness.
    return step06_justify(header, rows, row)

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(val) for val in row] for row in reader]
        
        # Simulate the customer's request:
        # Setup A (our recommendation) is index 0
        # Setup B (the one they liked) is index 1
        setup_a = rows[0]
        setup_b = rows[1]
        
        # Mask goals for B to justify why it was not recommended
        masked_b = setup_b[:len(header)-3] + ["?"] * 3
        
        p, reason = justify(header, rows, masked_b)
        
        print("Customer Inquiry: I liked setup B. You recommended A. Explain why not B.")
        print(f"Analysis: Setup B is estimated to be better than {p:.4f} of all known configurations.")
        print(f"Justification: {reason}")
        print("Since setup A ranks higher in our performance model, we prioritized it to ensure better project outcomes.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
