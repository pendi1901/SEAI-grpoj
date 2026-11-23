import csv
import pandas as pd
from scipy import stats

def certify(xs, ys):
    """
    Returns True if the difference between two distributions is statistically 
    insignificant (p > 0.05), False otherwise.
    """
    # Use Welch's t-test (equal_var=False) to compare two independent samples
    t_stat, p_value = stats.ttest_ind(xs, ys, equal_var=False)
    return p_value > 0.05

def analyze_team_size_impact(header, rows):
    df = pd.DataFrame(rows, columns=header)
    
    # Identify the 'Team Size' column and the 'Cost-' goal
    # Team Size is numeric, Cost- is the goal to minimize
    # We split into small vs big based on the median of Team Size
    median_team = df['Team Size'].median()
    
    small_team_costs = df[df['Team Size'] <= median_team]['Cost-']
    big_team_costs = df[df['Team Size'] > median_team]['Cost-']
    
    # Check if they are statistically different
    is_same = certify(small_team_costs.tolist(), big_team_costs.tolist())
    
    return is_same, small_team_costs.mean(), big_team_costs.mean()

if __name__ == "__main__":
    filename = 'pom3a.n1000.train.csv'
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                processed_row = [float(val) if val.replace('.', '', 1).isdigit() or 
                                 (val.startswith('-') and val[1:].replace('.', '', 1).isdigit()) 
                                 else val for val in row]
                rows.append(processed_row)
        
        is_same, mean_small, mean_big = analyze_team_size_impact(header, rows)
        
        print("Customer Inquiry: Are small-team setups cheaper than big-team ones?")
        print(f"  Average Cost (Small Teams): {mean_small:.4f}")
        print(f"  Average Cost (Big Teams):   {mean_big:.4f}")
        
        if is_same:
            print("Conclusion: The difference is statistically insignificant. It was likely luck.")
        else:
            print("Conclusion: The difference is statistically significant. It is a real trend.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
