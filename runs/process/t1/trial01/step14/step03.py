import csv
import math

def certify(xs, ys):
    """
    Returns True if xs and ys are statistically similar (same distribution),
    False if they differ significantly. Uses a simple A12 effect size test.
    """
    def a12(lst1, lst2):
        m, n = len(lst1), len(lst2)
        greater = 0
        for x in lst1:
            for y in lst2:
                if x > y: greater += 1
                elif x == y: greater += 0.5
        return greater / (m * n)

    # If A12 is near 0.5, they are the same. 
    # Thresholds for small/medium/large effects are often 0.56/0.64/0.71.
    # We return True if the effect size is small (not significantly different).
    score = a12(xs, ys)
    return 0.44 <= score <= 0.56

def analyze_teams(header, rows):
    """
    Splits data into small vs big teams and compares their 'Cost-' values.
    """
    team_size_idx = header.index('Team Size')
    cost_idx = header.index('Cost-')
    
    # Median split for Team Size
    sizes = [row[team_size_idx] for row in rows]
    median = sorted(sizes)[len(sizes) // 2]
    
    small_teams = [row[cost_idx] for row in rows if row[team_size_idx] <= median]
    big_teams = [row[cost_idx] for row in rows if row[team_size_idx] > median]
    
    is_same = certify(small_teams, big_teams)
    
    return is_same, sum(small_teams)/len(small_teams), sum(big_teams)/len(big_teams)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    rows = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                rows.append([float(x) for x in row])
        
        same, avg_small, avg_big = analyze_teams(header, rows)
        
        print("Customer Inquiry Analysis:")
        print(f"Small team average cost: {avg_small:.4f}")
        print(f"Big team average cost:   {avg_big:.4f}")
        
        if same:
            print("Conclusion: The difference is likely due to noise/luck. The team size does not significantly impact cost.")
        else:
            print("Conclusion: The difference is statistically significant. Team size appears to impact cost.")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
