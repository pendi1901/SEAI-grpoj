import ezr
import random

def certify(xs, ys):
    """
    Returns True if the distributions of xs and ys are statistically 
    indistinguishable (the same apart from noise), False otherwise.
    Uses the statistical tests provided in ezr.
    """
    # The ezr.same function performs cliffs delta and KS tests.
    # We use eps=0.35 as a standard effect size for Cohen's d.
    return ezr.same(xs, ys, eps=0.35)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # To answer the customer's question about whether results shifted in spring,
    # we split the data chronologically (assuming the file order represents time).
    # We compare the first half (pre-spring) to the second half (post-spring).
    mid = len(rows) // 2
    pre_spring = rows[:mid]
    post_spring = rows[mid:]
    
    # We evaluate performance based on the 'Cost-' goal column.
    cost_idx = header.index('Cost-')
    
    pre_costs = [r[cost_idx] for r in pre_spring]
    post_costs = [r[cost_idx] for r in post_spring]
    
    # Perform certification
    is_same = certify(pre_costs, post_costs)
    
    print("Statistical Analysis: Pre-Spring vs Post-Spring Performance (Cost-)")
    print("-" * 60)
    print(f"Pre-spring sample size:  {len(pre_costs)}")
    print(f"Post-spring sample size: {len(post_costs)}")
    print(f"Pre-spring mean cost:    {sum(pre_costs)/len(pre_costs):.4f}")
    print(f"Post-spring mean cost:   {sum(post_costs)/len(post_costs):.4f}")
    print("-" * 60)
    
    if is_same:
        print("Result: The difference in costs is statistically insignificant.")
        print("Conclusion: The change in team decision-making did not result in a")
        print("            statistically significant shift in performance.")
    else:
        print("Result: The difference in costs is statistically significant.")
        print("Conclusion: The change in team decision-making has caused a real")
        print("            and measurable shift in performance.")
        
    exit(0)
