import ezr
import step01

def certify(xs, ys):
    """
    Returns True if the distributions are statistically indistinguishable,
    False if they are significantly different.
    """
    return ezr.same(xs, ys)

def get_costs_by_team_size(header, rows):
    """
    Splits the data into 'small' (Team Size < 0.5) and 'big' (Team Size >= 0.5)
    and returns the Cost- values for each.
    """
    # 'Team Size' is at index 8, 'Cost-' is at index 9
    small_costs = []
    big_costs = []
    
    for row in rows:
        team_size = row[8]
        cost = row[9]
        if team_size < 0.5:
            small_costs.append(cost)
        else:
            big_costs.append(cost)
            
    return small_costs, big_costs

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_iter = ezr.csv(filename)
    
    try:
        header = next(data_iter)
        rows = list(data_iter)
    except StopIteration:
        exit(0)
        
    small, big = get_costs_by_team_size(header, rows)
    
    is_same = certify(small, big)
    
    print("Analysis: Are small-team setups cheaper than big-team ones?")
    if is_same:
        print("Result: The difference is statistically insignificant (it was likely luck).")
    else:
        print("Result: The difference is statistically significant (it is real).")
        
    print(f"Small team count: {len(small)}, Mean cost: {sum(small)/len(small):.4f}")
    print(f"Big team count: {len(big)}, Mean cost: {sum(big)/len(big):.4f}")
    
    exit(0)
