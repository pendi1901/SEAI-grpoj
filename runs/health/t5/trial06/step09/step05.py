import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We compare the distribution of input values in the worst 10% of rows
    against the rest of the data.
    """
    # Create a table to handle column roles and ydist calculations
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the "worst" ones
    # Higher ydist means further from the ideal goals
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
    # We use the 'div' (spread) and 'mid' (central tendency) as proxies.
    # A column is "blameworthy" if its values in the worst rows are 
    # consistently different from the rest.
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
            diff = abs(m_worst - m_other)
        else:
            # Simple heuristic for symbolic: difference in mode frequency
            # or just presence of unique values
            diff = 1.0 if (max(worst_vals, key=worst_vals.count) != 
                           max(other_vals, key=other_vals.count)) else 0.0
            
        scores.append((diff, col.txt))
    
    # Return the names of the top 3 columns that contribute most to the difference
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for diff, name in scores[:3]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    
    if not data:
        print("No data found.")
        exit(1)
        
    header = data[0]
    rows = data[1:]
    
    blame_list = blame(header, rows)
    
    print("Analysis: Which settings are causing the worst performance?")
    print(f"The settings most associated with poor outcomes are: {', '.join(blame_list)}")
    print("\nThese columns show the greatest divergence in values between the "
          "worst-performing setups and the rest of the population.")
    
    exit(0)
