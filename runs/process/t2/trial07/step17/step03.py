import csv
import math

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (same population),
    False if they differ significantly. Uses a simple t-test approach.
    """
    n1, n2 = len(xs), len(ys)
    if n1 < 2 or n2 < 2:
        return True
    
    mu1, mu2 = sum(xs) / n1, sum(ys) / n2
    var1 = sum((x - mu1) ** 2 for x in xs) / (n1 - 1)
    var2 = sum((y - mu2) ** 2 for y in ys) / (n2 - 1)
    
    # Pooled standard deviation
    pooled_std = math.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    if pooled_std == 0:
        return mu1 == mu2
    
    t_stat = (mu1 - mu2) / (pooled_std * math.sqrt(1/n1 + 1/n2))
    # For a 95% confidence level, critical t-value is approx 1.96
    return abs(t_stat) < 1.96

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append([float(x) for x in row])
            
    team_size_idx = header.index('Team Size')
    cost_idx = header.index('Cost-')
    
    # Split into small (bottom 50%) and big (top 50%) team sizes
    team_sizes = [r[team_size_idx] for r in rows]
    median_size = sum(sorted(team_sizes)) / len(team_sizes)
    
    small_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] < median_size]
    big_team_costs = [r[cost_idx] for r in rows if r[team_size_idx] >= median_size]
    
    is_same = certify(small_team_costs, big_team_costs)
    
    print("Customer Inquiry: Are small-team setups cheaper than big-team ones?")
    if not is_same:
        print("Result: The difference is statistically significant. Small teams are indeed cheaper.")
    else:
        print("Result: The difference is not statistically significant. The observation was likely luck.")
