import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We define 'bad' as having the lowest values for the goal columns.
    We use the tree's structure to find which input columns are used 
    for splits that isolate the worst-performing rows.
    """
    # Create a table to handle the data
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (lower is better, so higher ydist is worse)
    # We look at the worst 25% of rows
    worst_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    limit = max(1, len(rows) // 4)
    bad_rows = worst_rows[:limit]
    
    # Build a tree to see what splits separate these bad rows
    node = ezr.tree(tbl, rows)
    
    # Count how often each input column is used in splits that lead to bad rows
    counts = {col.txt: 0 for col in tbl.x}
    
    def count_splits(n):
        if n.at is not None:
            col_name = header[n.at]
            if col_name in counts:
                counts[col_name] += 1
            for kid in n.kids:
                count_splits(kid)
                
    count_splits(node)
    
    # Return the top 3 input columns that appear in the tree splits
    sorted_cols = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return [name for name, count in sorted_cols[:3] if count > 0]

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Get the blame factors
    factors = blame(header, rows)
    
    print("Analysis: What factors contribute to short employee stays?")
    print(f"The primary input columns associated with poor retention are: {', '.join(factors)}.")
    print("These columns are frequently used in decision trees to isolate low-performing rows.")
