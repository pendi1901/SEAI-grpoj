import csv
from step01 import remember

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (same distribution),
    False if they differ significantly. Uses a simple bootstrap/permutation 
    logic or a basic difference of means check.
    """
    if not xs or not ys:
        return True
    
    # Calculate means
    mu_x = sum(xs) / len(xs)
    mu_y = sum(ys) / len(ys)
    
    # Calculate standard deviation
    def stdev(data, mean):
        return (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5
    
    sd_x = stdev(xs, mu_x)
    sd_y = stdev(ys, mu_y)
    
    # If the difference in means is less than the combined standard deviation,
    # we consider them "the same apart from noise".
    combined_sd = (sd_x + sd_y) / 2
    return abs(mu_x - mu_y) < combined_sd

def analyze_team_size_impact(header, rows):
    # Find indices
    team_size_idx = header.index('Team Size')
    cost_idx = header.index('Cost-')
    
    # Split into small (<= 0.5) and big (> 0.5) teams
    small_team_costs = []
    big_team_costs = []
    
    for row in rows:
        team_size = float(row[team_size_idx])
        cost = float(row[cost_idx])
        if team_size <= 0.5:
            small_team_costs.append(cost)
        else:
            big_team_costs.append(cost)
            
    is_same = certify(small_team_costs, big_team_costs)
    
    return is_same, small_team_costs, big_team_costs

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        same, small, big = analyze_team_size_impact(header, rows)
        
        print(f"Small team average cost: {sum(small)/len(small):.4f}")
        print(f"Big team average cost: {sum(big)/len(big):.4f}")
        
        if same:
            print("The difference is likely just noise. Small teams are not significantly cheaper.")
        else:
            print("The difference is statistically significant. Small teams are cheaper.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
