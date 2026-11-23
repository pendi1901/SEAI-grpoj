import ezr
import step01

def blame(header, rows):
    """
    Identifies input columns that best explain why the worst rows are 'bad'.
    We define 'bad' as having a high ydist (distance from ideal goals).
    We compare the distribution of input values in the worst 25% of rows
    against the best 25% of rows to find the most significant differences.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (distance from ideal)
    # Higher ydist = worse performance/tenure
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    
    n = len(sorted_rows) // 4
    worst = sorted_rows[:n]
    best = sorted_rows[-n:]
    
    # Score columns by how much their distribution differs between worst and best
    # For numeric: difference in means. For symbolic: difference in entropy/frequency.
    scores = []
    for col in tbl.x:
        if isinstance(col, ezr.Num):
            mu_worst = sum(r[col.at] for r in worst) / n
            mu_best = sum(r[col.at] for r in best) / n
            scores.append((abs(mu_worst - mu_best), col.txt))
        else:
            # For symbols, check if the most common value in 'worst' is different
            # or if the distribution is skewed compared to 'best'
            w_vals = [r[col.at] for r in worst]
            b_vals = [r[col.at] for r in best]
            # Simple heuristic: difference in frequency of the most common item
            w_mode = max(set(w_vals), key=w_vals.count)
            b_mode = max(set(b_vals), key=b_vals.count)
            diff = 1.0 if w_mode != b_mode else 0.0
            scores.append((diff, col.txt))
            
    # Return top 3 columns that explain the difference
    scores.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scores[:3]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    explanations = blame(header, rows)
    
    print("Analysis: What factors correlate with short stays (worst performance)?")
    print(f"The primary drivers identified are: {', '.join(explanations)}.")
    print("These columns show the most significant variance between our top-performing "
          "long-term staff and those with the shortest tenures.")
