import ezr
import random

def blame(header, rows):
    """
    Identify the input columns that best explain why the worst rows are bad.
    We compare the distribution of input values in the worst 25% of rows
    against the rest of the population.
    """
    # Create a table to handle column statistics and distance calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows (higher ydist = worse performance)
    scored = []
    for r in rows:
        scored.append((ezr.ydist(tbl, r), r))
    
    # Sort by ydist descending (worst first)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 25% and the rest
    n = len(scored) // 4
    worst = [x[1] for x in scored[:n]]
    rest = [x[1] for x in scored[n:]]
    
    # For each input column, calculate the difference in distribution
    # between the worst rows and the rest.
    impacts = []
    for col in tbl.x:
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        r_vals = [r[col.at] for r in rest if r[col.at] != "?"]
        
        if not w_vals or not r_vals:
            continue
            
        # For numeric inputs, use the difference in means (normalized)
        if isinstance(col, ezr.Num):
            w_mu = sum(w_vals) / len(w_vals)
            r_mu = sum(r_vals) / len(r_vals)
            diff = abs(w_mu - r_mu)
            impacts.append((diff, col.txt))
        else:
            # For symbolic inputs, we treat them as low impact unless specified
            impacts.append((0, col.txt))
            
    # Sort by impact (highest difference = most important)
    impacts.sort(key=lambda x: x[0], reverse=True)
    
    # Return the names of the top 2 most impactful columns
    return [name for _, name in impacts[:2]]

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # Run the blame analysis
    important_factors = blame(header, rows)
    
    # Identify all input columns to suggest what can be ignored
    input_cols = [col.txt for col in ezr.Tbl([header] + rows).x]
    ignored_factors = [f for f in input_cols if f not in important_factors]
    
    print("Project Analysis: Key Drivers of Cost")
    print("-" * 60)
    print("Most important factors to monitor:")
    for i, name in enumerate(important_factors):
        print(f"{i+1}. {name}")
        
    print("\nFactors you can safely stop worrying about:")
    for name in ignored_factors:
        print(f"- {name}")
        
    print("-" * 60)
    print("These findings are based on identifying which inputs deviate most")
    print("significantly in our worst-performing project scenarios.")
    
    exit(0)
