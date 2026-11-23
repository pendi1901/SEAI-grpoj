import ezr
import random

def blame(header, rows):
    """
    Identifies input columns that best explain why the worst rows are bad.
    We define 'bad' as having a high ydist (far from optimal goals).
    We compare the distribution of input values in the worst 25% of rows
    against the best 25% of rows to find the most significant differences.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (ascending: best to worst)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r))
    
    n = len(sorted_rows) // 4
    best = sorted_rows[:n]
    worst = sorted_rows[-n:]
    
    # Score columns by how much they differ between best and worst
    # For numeric: difference in means. For symbolic: difference in entropy/distribution.
    scores = []
    for col in tbl.x:
        at = col.at
        if isinstance(col, ezr.Num):
            mu_best = sum(r[at] for r in best) / n
            mu_worst = sum(r[at] for r in worst) / n
            diff = abs(mu_best - mu_worst)
        else:
            # Symbolic: count frequency of most common value
            def freq(subset):
                counts = {}
                for r in subset:
                    v = r[at]
                    counts[v] = counts.get(v, 0) + 1
                return max(counts.values()) / n if counts else 0
            diff = abs(freq(best) - freq(worst))
        
        scores.append((diff, header[at]))
    
    # Return top 3 columns that explain the difference
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for score, name in scores[:3]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Run the blame analysis
    factors = blame(header, rows)
    
    print("Analysis: What factors correlate with short stays (worst performance)?")
    print(f"The top factors identified are: {', '.join(factors)}.")
    print("These columns show the greatest divergence between the best and worst performing employees.")
    
    exit(0)
