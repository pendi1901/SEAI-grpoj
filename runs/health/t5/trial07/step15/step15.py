import ezr
import random

def blame(header, rows):
    """
    Identifies input columns that have the least impact on performance (ydist).
    Columns with low impact are candidates for factory defaults.
    We rank columns by how little they differentiate the 'worst' rows from the 'rest'.
    """
    tbl = ezr.Tbl([header] + rows)
    
    # Calculate ydist for all rows to identify the "worst"
    # Higher ydist means worse performance
    scored = []
    for row in rows:
        scored.append((ezr.ydist(tbl, row), row))
    
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Split into worst 25% and the rest
    n = len(scored) // 4
    worst = [x[1] for x in scored[:n]]
    rest = [x[1] for x in scored[n:]]
    
    # Score columns by how much they differ between 'worst' and 'rest'
    # Smaller difference means the column is less relevant to poor performance
    impacts = []
    for col in tbl.x:
        at = col.at
        if isinstance(col, ezr.Sym):
            # Entropy difference
            def get_entropy(r_list):
                counts = {}
                for row in r_list:
                    val = row[at]
                    counts[val] = counts.get(val, 0) + 1
                total = len(r_list)
                return -sum((c/total) * (ezr.log2(c/total)) for c in counts.values() if c > 0)
            
            diff = abs(get_entropy(worst) - get_entropy(rest))
        else:
            # Normalized mean difference
            mu_w = sum(r[at] for r in worst) / len(worst)
            mu_r = sum(r[at] for r in rest) / len(rest)
            diff = abs(mu_w - mu_r) / (ezr.div(col) + 1e-32)
            
        impacts.append((diff, header[at]))
    
    # Sort by impact ascending (lowest impact first)
    impacts.sort(key=lambda x: x[0])
    return [name for _, name in impacts]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    # Get columns ranked by least impact
    candidates = blame(header, rows)
    
    print("Analysis: Which settings can be left at factory defaults?")
    print("The following input columns have the least impact on performance,")
    print("making them the safest candidates to leave at factory defaults:")
    for i, name in enumerate(candidates[:3]):
        print(f"{i+1}. {name}")
    
    print("\nThese settings are least associated with poor outcomes.")
