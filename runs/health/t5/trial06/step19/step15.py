import ezr
import random

def blame(header, rows):
    """
    Identify input columns that have the least impact on performance.
    We compare the distribution of input values in the worst 10% of rows
    against the rest of the data. Columns with the smallest difference
    between these groups are safe to leave at factory defaults.
    """
    # Create a table to handle column roles and ydist calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the "worst" ones
    indexed_rows = []
    for i, row in enumerate(rows):
        indexed_rows.append((ezr.ydist(tbl, row), row))
    
    # Sort by ydist descending to get the worst performers
    indexed_rows.sort(key=lambda x: x[0], reverse=True)
    
    # Define the worst 10%
    n_worst = max(1, len(rows) // 10)
    worst_rows = [x[1] for x in indexed_rows[:n_worst]]
    other_rows = [x[1] for x in indexed_rows[n_worst:]]
    
    # For each input column, check if the distribution of values in the 
    # worst rows is significantly different from the rest.
    # A column is "safe" if its values in the worst rows are NOT 
    # significantly different from the rest.
    scores = []
    for col in tbl.x:
        # Extract values for this column
        worst_vals = [r[col.at] for r in worst_rows if r[col.at] != "?"]
        other_vals = [r[col.at] for r in other_rows if r[col.at] != "?"]
        
        if not worst_vals or not other_vals:
            continue
            
        # If numeric, compare means. If symbolic, compare frequency of modes.
        if isinstance(col, ezr.Num):
            m_worst = sum(worst_vals) / len(worst_vals)
            m_other = sum(other_vals) / len(other_vals)
            # Normalize difference by range to make it comparable
            diff = abs(m_worst - m_other) / (ezr.div(col) + 1e-32)
        else:
            # Simple heuristic for symbolic: difference in mode frequency
            diff = 1.0 if (max(worst_vals, key=worst_vals.count) != 
                           max(other_vals, key=other_vals.count)) else 0.0
            
        scores.append((diff, col.txt))
    
    # Return the names of the columns with the smallest difference (most "safe")
    scores.sort(key=lambda x: x[0])
    return [name for diff, name in scores]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    
    if not data:
        print("No data found.")
        exit(1)
        
    header = data[0]
    rows = data[1:]
    
    safe_settings = blame(header, rows)
    
    print("Analysis: Which settings can I leave at factory defaults?")
    print("The following settings have the least impact on performance, "
          "making them safe to leave at default values:")
    for i, name in enumerate(safe_settings[:3]):
        print(f"{i+1}. {name}")
    
    print("\nThese columns show the least divergence between poor-performing "
          "setups and the rest of the population.")
    
    exit(0)
