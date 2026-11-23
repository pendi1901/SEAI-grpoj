import ezr
import step07

def choose(header, rows, label):
    """
    Finds a setup that is both accurate (low ydist) and small (low complexity).
    We use the acquire strategy to find accurate rows, then select the best
    one that also minimizes a complexity score.
    """
    labeled_cache = {}

    def oracle_wrapper(idx):
        if idx not in labeled_cache:
            labeled_cache[idx] = label(idx)
        return labeled_cache[idx]

    # Use the acquisition strategy to find a set of high-performing rows
    # We pass a wrapper that caches labels to respect the 50-row limit
    best_idx = step07.choose(header, rows, oracle_wrapper)
    
    # After acquisition, we have a set of labeled rows in labeled_cache.
    # We build a TBL using only the labeled rows to define the ydist context.
    labeled_rows = [labeled_cache[i] for i in labeled_cache]
    tbl = ezr.Tbl([header] + labeled_rows)
    
    # Complexity proxy: normalized N_estimators + normalized Max_depth
    # These are at indices 3 and 7 respectively.
    def complexity(row):
        n_est = row[3]
        depth = row[7]
        return (n_est / 200.0) + (depth / 20.0)
    
    # Score candidates: weighted sum of performance (ydist) and complexity
    # We look for the best balance among the rows we have already labeled.
    def score(idx):
        row = labeled_cache[idx]
        return ezr.ydist(tbl, row) + 0.5 * complexity(row)
    
    best_idx = min(labeled_cache.keys(), key=score)
    return best_idx

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        all_rows = list(data_gen)
        
        # Mask the goals
        masked_rows = []
        for r in all_rows:
            new_row = list(r)
            for i, name in enumerate(header):
                if name[-1] in "+-":
                    new_row[i] = "?"
            masked_rows.append(new_row)
            
        def label(i):
            return all_rows[i]
            
        best_idx = choose(header, masked_rows, label)
        print(f"Recommended configuration found at index: {best_idx}")
        print(f"Configuration details: {all_rows[best_idx]}")
        print("This setup balances high forecast accuracy with low computational overhead.")
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
        
    exit(0)
