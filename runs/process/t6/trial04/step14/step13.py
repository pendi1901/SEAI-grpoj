import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    # Reuse the statistical certification logic from step03
    return step03.certify(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    rows_gen = ezr.csv(filename)
    header = next(rows_gen)
    rows = list(rows_gen)
    
    # The customer asks if results shifted after a change in decision-making.
    # We simulate this by splitting the data chronologically (first half vs second half).
    n = len(rows)
    first_half = rows[:n // 2]
    second_half = rows[n // 2:]
    
    # We evaluate the primary goal (Cost-) to see if the distribution shifted.
    cost_idx = header.index("Cost-")
    xs = [r[cost_idx] for r in first_half]
    ys = [r[cost_idx] for r in second_half]
    
    is_same = certify(xs, ys)
    
    print("Analysis: Did the results shift after the change in decision-making?")
    print("-" * 60)
    print(f"First half average cost:  {sum(xs)/len(xs):.4f}")
    print(f"Second half average cost: {sum(ys)/len(ys):.4f}")
    print("-" * 60)
    
    if is_same:
        print("Result: The difference is statistically insignificant.")
        print("Conclusion: The results are effectively the same as before.")
    else:
        print("Result: The difference is statistically significant.")
        print("Conclusion: The results have genuinely shifted.")
    print("-" * 60)
