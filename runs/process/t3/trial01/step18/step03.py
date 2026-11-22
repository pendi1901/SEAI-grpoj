import csv
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the two distributions are statistically similar (null hypothesis 
    not rejected), False if they are significantly different.
    Uses Welch's t-test to compare means.
    """
    # If the samples are too small, we cannot reliably reject the null hypothesis
    if len(xs) < 2 or len(ys) < 2:
        return True
    
    # Welch's t-test (does not assume equal variance)
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    
    # If p-value > 0.05, we fail to reject the null hypothesis (they are the same)
    return p_value > 0.05

def analyze_team_size_impact(header, rows):
    """
    Splits data into small and big teams based on the median Team Size
    and compares their Cost- values.
    """
    team_size_idx = header.index('Team Size')
    cost_idx = header.index('Cost-')
    
    team_sizes = [row[team_size_idx] for row in rows]
    median_size = sum(team_sizes) / len(team_sizes)
    
    small_team_costs = [row[cost_idx] for row in rows if row[team_size_idx] <= median_size]
    big_team_costs = [row[cost_idx] for row in rows if row[team_size_idx] > median_size]
    
    is_same = certify(small_team_costs, big_team_costs)
    
    return is_same, small_team_costs, big_team_costs

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        is_same, small_costs, big_costs = analyze_team_size_impact(header, rows)
        
        print("Analysis of Team Size vs Cost:")
        print(f"Small team average cost: {sum(small_costs)/len(small_costs):.4f}")
        print(f"Big team average cost:   {sum(big_costs)/len(big_costs):.4f}")
        
        if is_same:
            print("\nConclusion: The difference is not statistically significant.")
            print("It is likely that the observed difference was due to luck/noise.")
        else:
            print("\nConclusion: The difference is statistically significant.")
            print("The team size truly impacts the cost.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
