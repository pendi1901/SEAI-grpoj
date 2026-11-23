import ezr
import random

def blame(header, rows):
    """
    Identify input columns that have the least impact on performance.
    We define 'bad' as having high ydist (distance from ideal goals).
    We compare the distribution of input values in the worst 25% 
    against the rest of the population. Columns with the smallest
    difference between these groups are candidates for removal.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (distance from ideal goals)
    # Higher ydist means 'worse' performance
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    
    # Take the worst 25% to analyze
    n = len(sorted_rows) // 4
    worst = sorted_rows[:n]
    rest = sorted_rows[n:]
    
    scores = {}
    for col in tbl.x:
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        r_vals = [r[col.at] for r in rest if r[col.at] != "?"]
        
        if not w_vals or not r_vals:
            scores[col.txt] = 0
            continue
            
        if isinstance(col, ezr.Sym):
            # For symbols, compare frequency distributions (entropy)
            w_col = ezr.adds(w_vals)
            r_col = ezr.adds(r_vals)
            # Score based on how much the entropy changes
            scores[col.txt] = abs(ezr.div(w_col) - ezr.div(r_col))
        else:
            # For numbers, compare normalized mean difference
            w_mu = sum(w_vals) / len(w_vals)
            r_mu = sum(r_vals) / len(r_vals)
            # Normalize by the range of the column to make scores comparable
            col_div = ezr.div(col) if ezr.div(col) > 0 else 1.0
            scores[col.txt] = abs(w_mu - r_mu) / col_div
            
    # Return columns with the lowest scores (least impact on performance)
    sorted_cols = sorted(scores.items(), key=lambda x: x[1])
    return [name for name, score in sorted_cols]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the columns that have the least impact
    factors = blame(header, rows)
    
    print("Analysis: Which columns have little impact on retention?")
    print("-" * 60)
    print("The following input columns show the least difference between")
    print("the worst-performing employees and the rest of the population.")
    print("These are candidates for removal from data collection:")
    for i, factor in enumerate(factors[:5], 1):
        print(f"{i}. {factor}")
    print("-" * 60)
    print("These columns are statistically least relevant to performance.")
