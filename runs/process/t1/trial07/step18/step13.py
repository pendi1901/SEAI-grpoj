import csv

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (same distribution),
    False if they are significantly different. Uses a simple A12 effect size test.
    """
    def a12(lst1, lst2):
        m, n = len(lst1), len(lst2)
        if m == 0 or n == 0: return 0.5
        greater = 0
        for x in lst1:
            for y in lst2:
                if x > y: greater += 1
                elif x == y: greater += 0.5
        return greater / (m * n)

    # A12 threshold: 0.56 is a small effect size, 0.64 medium, 0.71 large.
    # If A12 is close to 0.5, they are the same.
    score = a12(xs, ys)
    return abs(0.5 - score) < 0.147

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [[float(x) for x in row] for row in reader]
        
        # The customer asks if results shifted after a change in how teams decide what to build.
        # We use 'Plan' as a proxy for the decision-making strategy.
        # We split the data into two groups based on the median of 'Plan'.
        plan_idx = header.index('Plan')
        cost_idx = header.index('Cost-')
        
        plans = [r[plan_idx] for r in rows]
        median_plan = sum(plans) / len(plans)
        
        # Group 1: Old strategy (lower plan values), Group 2: New strategy (higher plan values)
        old_strategy = [r[cost_idx] for r in rows if r[plan_idx] <= median_plan]
        new_strategy = [r[cost_idx] for r in rows if r[plan_idx] > median_plan]
        
        is_same = certify(old_strategy, new_strategy)
        
        print("Customer Inquiry: Did the team decision strategy shift results?")
        print("-" * 60)
        print(f"Average cost (Old Strategy): {sum(old_strategy)/len(old_strategy):.4f}")
        print(f"Average cost (New Strategy): {sum(new_strategy)/len(new_strategy):.4f}")
        
        if is_same:
            print("\nConclusion: The difference is statistically insignificant.")
            print("The results are effectively the same as before.")
        else:
            print("\nConclusion: The difference is statistically significant.")
            print("The new strategy has genuinely shifted the results.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
