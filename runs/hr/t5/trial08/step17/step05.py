import ezr
import random

def blame(header, rows):
    """
    Identifies input columns that best explain why the worst rows are bad.
    We define 'bad' as having a high ydist (distance from ideal goals).
    We compare the distribution of values in the worst 25% of rows 
    against the best 25% of rows for each input column.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Sort rows by ydist (lower is better)
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r))
    
    n = len(sorted_rows) // 4
    best = sorted_rows[:n]
    worst = sorted_rows[-n:]
    
    # Score columns by how much their distributions differ between best and worst
    # We use a simple heuristic: for numeric, difference in means; 
    # for symbolic, difference in frequency of the most common value.
    scores = []
    for col in tbl.x:
        at = col.at
        if isinstance(col, ezr.Num):
            best_vals = [r[at] for r in best if r[at] != "?"]
            worst_vals = [r[at] for r in worst if r[at] != "?"]
            if best_vals and worst_vals:
                diff = abs((sum(worst_vals)/len(worst_vals)) - (sum(best_vals)/len(best_vals)))
                scores.append((diff, header[at]))
        else:
            # Symbolic: compare frequency of the most common value in 'worst'
            worst_vals = [r[at] for r in worst if r[at] != "?"]
            if worst_vals:
                counts = {}
                for v in worst_vals: counts[v] = counts.get(v, 0) + 1
                mode = max(counts, key=counts.get)
                # Score is how much more common this value is in worst vs best
                best_vals = [r[at] for r in best if r[at] != "?"]
                b_count = best_vals.count(mode) / len(best_vals) if best_vals else 0
                w_count = counts[mode] / len(worst_vals)
                scores.append((w_count - b_count, header[at]))
    
    # Return top 3 columns that correlate with being 'bad'
    scores.sort(key=lambda x: x[0], reverse=True)
    return [name for score, name in scores[:3]]

if __name__ == "__main__":
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    top_blame = blame(header, rows)
    
    print("Analysis: What factors correlate with short stays (worst retention)?")
    print(f"The top factors identified are: {', '.join(top_blame)}.")
    print("These columns show the largest divergence between high-retention and low-retention employees.")
    
    exit(0)
