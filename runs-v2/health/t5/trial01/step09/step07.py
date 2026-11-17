import ezr


def choose(header, rows, label):
    tbl = ezr.Tbl(rows)
    goals = [c for c in header if c[-1] in "+-"]
    
    def ydist_row(row):
        return ezr.ydist(tbl, row)

    # Label the first Start rows to seed our knowledge.
    start_rows = list(range(min(5, len(rows))))
    labelled = {}
    for i in start_rows:
        labelled[i] = label(i)

    # Now iteratively pick the best unlabelled row by ydist using current labels.
    # We'll use a greedy approach: at each step, compute ydist for all rows (using
    # known labels where available), and if any are still "?" we label them.
    
    def get_ydist(row):
        """Compute ydist using labelled data; return None if row is unlabelled."""
        if row in labelled:
            return ydist_row(labelled[row])
        return None

    # First pass: compute ydist for all rows that have labels.
    scored = []
    for i, row in enumerate(rows):
        d = get_ydist(row)
        if d is not None:
            scored.append((d, i))
    
    # If we don't have enough labelled rows yet, label more.
    while len(scored) < 5 and len(labelled) < the.Stop:
        # Pick the row with lowest ydist among unlabelled ones (using current knowledge).
        # For now, just label a few random rows to get started.
        unlabelled = [i for i in range(len(rows)) if i not in labelled]
        if not unlabelled:
            break
        pick_idx = unlabelled[0]
        labelled[pick_idx] = label(pick_idx)
    
    # Re-score with all labels.
    scored = []
    for i, row in enumerate(rows):
        d = get_ydist(row)
        if d is not None:
            scored.append((d, i))
    
    best_score = min(s[0] for s in scored) if scored else 1e30
    
    # Now greedily label rows that would improve our understanding.
    # Strategy: at each step, find the unlabelled row whose ydist (estimated by
    # comparing to labelled neighbors) is best. We'll use a simple approach:
    # compute ydist for all currently labelled rows, then pick the unlabelled
    # row closest to the best labelled one in feature space.
    
    while len(labelled) < 50 and scored:
        best_d = min(s[0] for s in scored)
        
        # Find the best labelled row's features
        best_row_idx = [i for d, i in scored if d == best_d][0]
        best_row = rows[best_row_idx]
        
        # For unlabelled rows, estimate their ydist by comparing to labelled rows.
        # We'll use a simple heuristic: pick the unlabelled row whose features
        # are closest (in input space) to any labelled row.
        best_unlabelled = None
        best_est_d = 1e30
        
        for i, row in enumerate(rows):
            if i not in labelled:
                # Estimate ydist by comparing to nearest labelled row
                min_dist = 1e30
                for j, lr in labelled.items():
                    d_feat = ezr.xdist(tbl, row, rows[lr])
                    if d_feat < min_dist:
                        min_dist = d_feat
                
                # Heuristic: lower feature distance to best row suggests better ydist
                est_d = 1 - min_dist / (min_dist + 1e-32)
                if est_d < best_est_d:
                    best_est_d = est_d
                    best_unlabelled = i
        
        if best_unlabelled is not None and len(labelled) < 50:
            labelled[best_unlabelled] = label(best_unlabelled)
    
    # Final scoring with all labels.
    scored = []
    for i, row in enumerate(rows):
        d = get_ydist(row)
        if d is not None:
            scored.append((d, i))
    
    if scored:
        best_score = min(s[0] for s in scored)
        # Return the index of the best row.
        return [i for d, i in scored if d == best_score][0]
    
    # Fallback: return 0 if no labels were obtained.
    return 0


if __name__ == "__main__":
    import os
    csv_path = "Health-ClosedIssues0000.train.csv"
    with open(csv_path, encoding="utf-8-sig") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    header = list(lines[0].split(","))
    rows = [[ezr.atom(s) for s in line.split(",")] for line in lines[1:]]
    
    best_idx = choose(header, rows, label)
    print(f"Best row index: {best_idx}")
