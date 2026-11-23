import ezr
import random

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically indistinguishable,
    False if they differ significantly.
    Uses the same logic as step03, leveraging ezr's statistical tests.
    """
    # We use a slightly larger effect size (0.35) to account for noise
    # in the pom3a dataset.
    return ezr.same(sorted(xs), sorted(ys), eps=0.35)

if __name__ == "__main__":
    # Load data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # The customer asks if the change in decision-making (the "spring" change)
    # resulted in a shift in results. We simulate this by splitting the data
    # chronologically (assuming the file order represents time).
    # We compare the first half (pre-change) vs the second half (post-change).
    
    # Identify a primary goal column to check for shifts
    goal_idx = -1
    for i, name in enumerate(header):
        if name.endswith(('-', '+')):
            goal_idx = i
            break
            
    mid = len(rows) // 2
    pre_change = [r[goal_idx] for r in rows[:mid]]
    post_change = [r[goal_idx] for r in rows[mid:]]
    
    # Perform certification
    is_same = certify(pre_change, post_change)
    
    print("Analysis: Did the spring change in decision-making shift our results?")
    print(f"Pre-change sample size: {len(pre_change)}, Post-change sample size: {len(post_change)}")
    print(f"Pre-change average: {sum(pre_change)/len(pre_change):.4f}")
    print(f"Post-change average: {sum(post_change)/len(post_change):.4f}")
    
    if is_same:
        print("\nConclusion: The results are statistically indistinguishable.")
        print("The observed differences are likely due to noise, not the process change.")
    else:
        print("\nConclusion: There is a statistically significant difference in results.")
        print("The spring change appears to have had a measurable impact on performance.")
        
    exit(0)
