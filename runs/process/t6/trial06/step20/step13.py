import ezr
import step03

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically indistinguishable 
    (same apart from noise), False if they differ.
    """
    return step03.certify(xs, ys)

if __name__ == "__main__":
    # Load the data
    filename = "pom3a.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # The customer asks if results shifted after changing how teams decide what to build.
    # In the pom3a dataset, 'Plan' (index 7) represents the planning/decision strategy.
    # We compare the distribution of the primary goal 'Cost-' (index 9) 
    # between low-plan and high-plan configurations.
    plan_idx = 7
    cost_idx = 9
    
    plans = [r[plan_idx] for r in rows]
    median_plan = sum(plans) / len(plans)
    
    low_plan_costs = [r[cost_idx] for r in rows if r[plan_idx] < median_plan]
    high_plan_costs = [r[cost_idx] for r in rows if r[plan_idx] >= median_plan]
    
    # Check if the distributions are statistically the same
    is_same = certify(low_plan_costs, high_plan_costs)
    
    print("Analysis: Did changing the team decision strategy (Plan) shift the results?")
    if not is_same:
        print("Result: Yes, the results shifted significantly (not just noise).")
    else:
        print("Result: No, the results are statistically the same as before.")
    
    print(f"Average Cost- (Low Plan):  {sum(low_plan_costs)/len(low_plan_costs):.4f}")
    print(f"Average Cost- (High Plan): {sum(high_plan_costs)/len(high_plan_costs):.4f}")
    
    exit(0)
