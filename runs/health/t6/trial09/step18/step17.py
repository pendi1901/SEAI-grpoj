import ezr

def choose(header, rows, label):
    """
    Find a setup that forecasts well (low ydist) and is small.
    We define 'small' as having low N_estimators and low Max_depth.
    We use the acquire strategy to find good setups, then filter for 
    those that are also 'small' to satisfy the nightly run constraint.
    """
    # Track labeled indices using a set of integers
    labeled_indices = set()

    def oracle_wrapper(row):
        # Find the index of this row in the original list
        # Since rows are passed by reference, we can find the index
        for i, r in enumerate(rows):
            if r is row:
                if i not in labeled_indices:
                    labeled_indices.add(i)
                    revealed = label(i)
                    for j, val in enumerate(revealed):
                        row[j] = val
                return row
        return row

    # Use acquire to find good candidates
    tbl = ezr.Tbl([header] + rows)
    # acquire returns the rows that were labeled
    labeled_rows = ezr.acquire(tbl, cap=50, label=oracle_wrapper)
    
    # Define 'small' as being below the median for N_estimators and Max_depth
    n_est_idx = header.index('N_estimators')
    max_depth_idx = header.index('Max_depth')
    
    all_n_est = [r[n_est_idx] for r in rows]
    all_depth = [r[max_depth_idx] for r in rows]
    
    med_n = sorted(all_n_est)[len(all_n_est) // 2]
    med_d = sorted(all_depth)[len(all_depth) // 2]
    
    # Filter for rows that are both high-performing and 'small'
    candidates = []
    for i in labeled_indices:
        row = rows[i]
        if row[n_est_idx] <= med_n and row[max_depth_idx] <= med_d:
            candidates.append((ezr.ydist(tbl, row), i))
    
    # If no small rows were found in the labeled set, return the best overall
    if not candidates:
        # Return the best labeled row
        return min(labeled_indices, key=lambda i: ezr.ydist(tbl, rows[i]))
    
    # Return the index of the best small row
    candidates.sort(key=lambda x: x[0])
    return candidates[0][1]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    all_rows = data[1:]
    
    # Mask goals
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = [list(r) for r in all_rows]
    for row in masked_rows:
        for idx in goal_indices:
            row[idx] = "?"
            
    def label_func(i):
        return all_rows[i]
        
    best_idx = choose(header, masked_rows, label_func)
    
    print(f"Analysis complete. Found a high-performing, small setup at index: {best_idx}")
    print(f"Setup details: N_estimators={all_rows[best_idx][header.index('N_estimators')]}, "
          f"Max_depth={all_rows[best_idx][header.index('Max_depth')]}")
    exit(0)
