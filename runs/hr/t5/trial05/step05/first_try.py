import ezr
import random

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are 'bad'.
    We define 'bad' as having low values for columns ending in '+' 
    and high values for columns ending in '-'.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (distance from ideal goals)
    # Higher ydist means 'worse' performance
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    
    # Take the worst 25% to analyze
    n = len(sorted_rows) // 4
    worst = sorted_rows[:n]
    rest = sorted_rows[n:]
    
    # Calculate the 'importance' of each input column by checking
    # how much the distribution of values in 'worst' differs from 'rest'.
    # We use a simple heuristic: for symbols, entropy difference;
    # for numbers, the difference in means.
    scores = {}
    for col in tbl.x:
        w_vals = [r[col.at] for r in worst if r[col.at] != "?"]
        r_vals = [r[col.at] for r in rest if r[col.at] != "?"]
        
        if not w_vals or not r_vals:
            scores[col.txt] = 0
            continue
            
        if isinstance(col, ezr.Sym):
            # Entropy difference
            w_col = ezr.adds(w_vals)
            r_col = ezr.adds(r_vals)
            scores[col.txt] = abs(ezr.div(w_col) - ezr.div(r_col))
        else:
            # Normalized mean difference
            w_mu = sum(w_vals) / len(w_vals)
            r_mu = sum(r_vals) / len(r_vals)
            scores[col.txt] = abs(w_mu - r_mu)
            
    # Return top 3 columns that explain the bad performance
    sorted_cols = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [name for name, score in sorted_cols[:3]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get the top 3 factors
    factors = blame(header, rows)
    
    print("Analysis: What factors contribute to short stays?")
    print("-" * 50)
    print("The following input columns most strongly differentiate")
    print("the employees with the shortest tenure from the rest:")
    for i, factor in enumerate(factors, 1):
        print(f"{i}. {factor}")
    print("-" * 50)
    print("These factors are the primary drivers of retention risk.")
