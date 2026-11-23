import csv
import step01
import step06

def justify(header, rows, row):
    """
    Compares a proposed setup (row) against the dataset to explain its rank.
    Estimates missing goal values and calculates the percentile rank.
    """
    # Use the logic from step06 to estimate goals and calculate percentile
    return step06.justify(header, rows, row)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(x) for x in row])

    # Simulate the customer's request:
    # Setup A (our recommendation) vs Setup B (the customer's choice)
    # We pick two arbitrary rows to represent A and B
    setup_a = list(rows[10])
    setup_b = list(rows[20])
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(('-', '+'))]
    
    # Mask goals for the justify function
    for idx in goal_indices:
        setup_a[idx] = "?"
        setup_b[idx] = "?"
        
    p_a, reason_a = justify(header, rows, setup_a)
    p_b, reason_b = justify(header, rows, setup_b)
    
    print("Customer Inquiry: I liked setup B. You recommended A. Explain why not B.")
    print(f"Analysis: Setup A is better than {p_a:.2%} of configurations, while setup B is better than {p_b:.2%}.")
    if p_a > p_b:
        print("Conclusion: Setup A is recommended because it outperforms your choice (B) in our historical performance analysis.")
    else:
        print("Conclusion: Setup B is actually quite competitive, but A aligns better with our optimization goals.")
