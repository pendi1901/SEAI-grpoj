import ezr
import random

def choose(header, rows, label):
    """
    Find the best working arrangement using at most 50 labels.
    We use a manual acquisition loop to avoid the unhashable type error 
    in the library's internal set operations.
    """
    # Create a table object. The goal columns are marked with + or -
    # We mask the goals in the rows passed to the table
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    
    def mask(row):
        new_row = list(row)
        for i in goal_indices:
            new_row[i] = "?"
        return new_row

    masked_rows = [mask(r) for r in rows]
    tbl = ezr.Tbl([header] + masked_rows)
    
    # We need to track original indices because the library shuffles/sorts
    indexed_rows = list(enumerate(rows))
    random.shuffle(indexed_rows)
    
    # Budget: 50 labels
    budget = 50
    labeled_data = []
    
    # Initial random sample
    start_n = min(budget, 4)
    for _ in range(start_n):
        idx, row = indexed_rows.pop()
        labeled_data.append((idx, label(row)))
        
    # Build a model to guide the rest of the search
    # We use the labeled data to find the best row
    def get_ydist(row):
        # Create a temporary table with the labeled data to calculate ydist
        temp_tbl = ezr.clone(tbl, [r for _, r in labeled_data])
        return ezr.ydist(temp_tbl, row)

    # Greedy search for the remaining budget
    while len(labeled_data) < budget and indexed_rows:
        # Find the best and worst in current labeled set
        labeled_data.sort(key=lambda x: ezr.ydist(tbl, x[1]))
        best = labeled_data[0][1]
        worst = labeled_data[-1][1]
        
        # Pick the next row that is most like 'best' and least like 'worst'
        # We look at a small window of the remaining rows to save time
        sample_size = min(len(indexed_rows), 20)
        candidates = [indexed_rows.pop() for _ in range(sample_size)]
        
        best_idx, best_row = min(candidates, key=lambda x: ezr.xdist(tbl, x[1], best) - ezr.xdist(tbl, x[1], worst))
        
        labeled_data.append((best_idx, label(best_row)))
        
        # Put the others back
        for c in candidates:
            if c[0] != best_idx:
                indexed_rows.append(c)
                
    # Return the index of the best row found
    best_final = min(labeled_data, key=lambda x: ezr.ydist(tbl, x[1]))
    return best_final[0]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    def oracle(row):
        return row

    best_idx = choose(header, rows, oracle)
    best_row = rows[best_idx]
    
    print("Optimal Working Arrangement Found")
    print("-" * 50)
    print(f"Best Employee Record Index: {best_idx}")
    print(f"YearsAtCompany+: {best_row[header.index('YearsAtCompany+')]}")
    print(f"YearsInCurrentRole+: {best_row[header.index('YearsInCurrentRole+')]}")
    print(f"JobRole: {best_row[header.index('jobRole')]}")
    print("-" * 50)
    print("This arrangement was identified using 50 targeted interviews.")
