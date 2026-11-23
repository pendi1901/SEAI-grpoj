import ezr
import random

def blame(header, rows):
    """
    Identifies input columns that have the least impact on the goal metrics.
    We define 'impact' by how much the distribution of a column changes
    between the 'best' and 'worst' performing rows. Columns with the 
    smallest difference (low impact) are candidates for removal.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (ascending: best to worst)
    # Best rows are at the start, worst rows are at the end
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r))
    n = len(sorted_rows)
    
    # Compare the top 25% (best) vs bottom 25% (worst)
    best = sorted_rows[:int(0.25 * n)]
    worst = sorted_rows[int(0.75 * n):]
    
    # Identify input columns (not goals)
    input_cols = [c for c in tbl.x]
    
    impacts = []
    for col in input_cols:
        if isinstance(col, ezr.Sym):
            # For symbols, compare the entropy of the distribution
            b_col = ezr.adds([r[col.at] for r in best if r[col.at] != "?"])
            w_col = ezr.adds([r[col.at] for r in worst if r[col.at] != "?"])
            # Small difference in entropy means the column doesn't distinguish well
            score = abs(ezr.div(b_col) - ezr.div(w_col))
            impacts.append((score, col.txt))
        else:
            # For numbers, compare the normalized means
            b_vals = [ezr.norm(col, r[col.at]) for r in best if r[col.at] != "?"]
            w_vals = [ezr.norm(col, r[col.at]) for r in worst if r[col.at] != "?"]
            if b_vals and w_vals:
                b_mu = sum(b_vals) / len(b_vals)
                w_mu = sum(w_vals) / len(w_vals)
                score = abs(b_mu - w_mu)
                impacts.append((score, col.txt))
            else:
                impacts.append((0, col.txt))
            
    # Sort by impact ascending (lowest impact first)
    impacts.sort(key=lambda x: x[0])
    
    # Return the names of the columns with the lowest impact
    return [s[1] for s in impacts]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    results = blame(header, rows)
    
    print("Analysis: Which columns have the least impact on retention metrics?")
    print("The following input columns show the weakest correlation with performance outcomes.")
    print("You may consider stopping the collection of these columns:")
    for i, name in enumerate(results[:5], 1):
        print(f"{i}. {name}")
    
    print("\nThese were identified by comparing the best and worst performing rows.")
