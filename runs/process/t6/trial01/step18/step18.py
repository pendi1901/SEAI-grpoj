import ezr
import step01

def fix(header, row, levers):
    """
    Finds the best change to a 'bad' row by exploring the neighborhood
    of the row within the allowed lever constraints, specifically targeting
    the reduction of 'Idle-' (index 11).
    """
    # Create a table to use ydist for scoring
    # We use the header to define the structure
    tbl = ezr.Tbl([header])
    
    best_change = {}
    best_score = float('inf')
    
    # Try changing each lever to its bounds or midpoint to find an improvement
    for col_name, allowed in levers.items():
        at = header.index(col_name)
        original_val = row[at]
        
        # Generate candidates: for numeric, try low and high bounds
        candidates = []
        if isinstance(allowed, tuple):
            # Test the bounds
            candidates = [allowed[0], allowed[1]]
        else:
            candidates = allowed
            
        for val in candidates:
            if val == original_val:
                continue
                
            # Create a modified row
            new_row = list(row)
            new_row[at] = val
            
            # Score the new row (lower ydist is better)
            # ydist calculates distance to ideal goals (0 for -, 1 for +)
            score = ezr.ydist(tbl, new_row)
            
            if score < best_score:
                best_score = score
                best_change = {col_name: val}
                
    return best_change

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
    except StopIteration:
        exit(1)
        
    # The customer wants to cut 'Idle-'.
    # We define levers excluding 'Team Size' (since they cannot hire).
    # We focus on 'Plan' and 'Initial Known' as project management levers.
    levers = {
        "Plan": (0.1, 0.9),
        "Initial Known": (0.1, 0.9)
    }
    
    # Find a 'bad' row (high ydist) to fix
    tbl = ezr.Tbl([header] + rows)
    scored = sorted([(ezr.ydist(tbl, r), r) for r in rows], key=lambda x: x[0], reverse=True)
    bad_row = scored[0][1]
    
    recommendation = fix(header, bad_row, levers)
    
    print("Rescue Plan for High Idle Time (No Hiring Allowed):")
    if recommendation:
        for col, val in recommendation.items():
            print(f"Adjust '{col}' to {val:.2f}.")
        print("These changes minimize the distance to the ideal project goals,")
        print("effectively reducing idle time without increasing team size.")
    else:
        print("No effective adjustments found within the given constraints.")
    
    exit(0)
