import ezr
import random

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they are significantly different.
    Uses the same logic as ezr.same (cliffs and ks tests).
    """
    return ezr.same(xs, ys)

def analyze():
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # The customer asks if results shifted after a change in how teams decide what to build.
    # In the pom3a dataset, 'Plan' is the column representing the planning strategy.
    # We compare the 'Score-' goal for rows with low 'Plan' values vs high 'Plan' values
    # to see if the planning strategy change resulted in a statistically significant shift.
    
    plan_idx = header.index("Plan")
    score_idx = header.index("Score-")
    
    # Median split on Plan
    plan_values = [r[plan_idx] for r in rows]
    median_plan = sorted(plan_values)[len(plan_values) // 2]
    
    low_plan_scores = [r[score_idx] for r in rows if r[plan_idx] <= median_plan]
    high_plan_scores = [r[score_idx] for r in rows if r[plan_idx] > median_plan]
    
    # Perform certification
    is_same = certify(low_plan_scores, high_plan_scores)
    
    print("Analysis: Did the change in planning strategy shift results?")
    print(f"Comparing 'Score-' for low-plan vs high-plan configurations.")
    print(f"Low-plan count: {len(low_plan_scores)}, High-plan count: {len(high_plan_scores)}")
    print(f"Mean Score (Low):  {sum(low_plan_scores)/len(low_plan_scores):.4f}")
    print(f"Mean Score (High): {sum(high_plan_scores)/len(high_plan_scores):.4f}")
    
    if is_same:
        print("Result: The difference is statistically insignificant. The results are effectively the same.")
    else:
        print("Result: The difference is statistically significant. The change in strategy had a real impact.")

if __name__ == "__main__":
    analyze()
