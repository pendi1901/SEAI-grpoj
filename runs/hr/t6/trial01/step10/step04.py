import ezr
from step01 import remember


def flow(header, row, seen):
    """Return True if this employee needs a retention conversation."""
    # Identify goal columns (names ending in +)
    goals = [header[i] for i, h in enumerate(header) if h.endswith("+")]

    # Build column summaries from training data using ezr.Tbl
    tbl = ezr.Tbl(open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", encoding="utf-8-sig"))
    
    # Compute ydist for the current row and all seen rows
    def compute_yd(r):
        return ezr.ydist(tbl, r)

    # Track which rows we've seen (including this one)
    all_rows = seen + [row]
    
    # For each row, compute its ydist
    row_ys = [compute_yd(r) for r in all_rows]
    
    # The current row's ydist
    cur_yd = row_ys[-1]
    
    # If this is the first row, just return False (no decision needed yet)
    if len(all_rows) == 1:
        return False
    
    # Compute mean ydist of all seen rows so far
    mean_yd = sum(row_ys[:-1]) / len(row_ys[:-1])
    
    # If current row is significantly worse than average, flag it
    # A "what would keep you here" conversation is needed for at-risk employees
    if cur_yd > mean_yd + 0.5:
        return True
    
    return False


if __name__ == "__main__":
    tbl = ezr.Tbl(open("WA_Fn-UseC_-HR-Employee-Attrition.train.csv", encoding="utf-8-sig"))
    
    # Process rows one at a time to demonstrate the flow function
    flagged = []
    for i, row in enumerate(tbl.rows):
        if flow(tbl.names, row, [tbl.rows[j] for j in range(i)]):
            flagged.append(row)
    
    print(f"Employees needing retention conversations: {len(flagged)}")
