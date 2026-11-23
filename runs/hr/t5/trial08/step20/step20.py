import ezr
import random

def race(header, rows, label):
    """
    Compare three strategies for finding the best employee arrangement.
    Budget: 50 labels total.
    """
    labeled_data = {}
    
    def oracle_wrapper(i):
        if i not in labeled_data:
            if len(labeled_data) >= 50:
                return None
            labeled_data[i] = label(i)
        return labeled_data[i]

    # We use the full dataset to build the table structure for distance metrics.
    # Note: The table needs the full rows to calculate norms correctly.
    # We use the original rows to build the table context.
    full_tbl = ezr.Tbl([header] + rows)

    def get_ydist(row_idx):
        if row_idx not in labeled_data:
            return 1e30
        # We must ensure the row passed to ydist is the fully labeled version
        return ezr.ydist(full_tbl, labeled_data[row_idx])

    # 1. Random strategy
    def strategy_random(rows):
        indices = random.sample(range(len(rows)), 16)
        for i in indices: oracle_wrapper(i)
        return min(indices, key=get_ydist)

    # 2. Rule of thumb: Newest staff (YearsAtCompany+ is low)
    def strategy_rule_of_thumb(rows):
        tenure_idx = header.index("YearsAtCompany+")
        # Sort by tenure ascending (newest first)
        # We use a safe lookup for the tenure value
        candidates = sorted(range(len(rows)), 
                            key=lambda i: rows[i][tenure_idx] if rows[i][tenure_idx] != "?" else 999)
        indices = candidates[:16]
        for i in indices: oracle_wrapper(i)
        return min(indices, key=get_ydist)

    # 3. Intelligent acquisition (ezr.acquire)
    def strategy_acquire(rows):
        # We need a local oracle that maps rows back to indices for our shared budget
        def local_oracle(row):
            for i, r in enumerate(rows):
                if r is row: 
                    return oracle_wrapper(i)
            return row
        
        # Use a subset of the budget
        labeled = ezr.acquire(full_tbl, cap=17, label=local_oracle)
        # Find index of best labeled row
        best_row = min(labeled, key=lambda r: ezr.ydist(full_tbl, r))
        for i, r in enumerate(rows):
            if r is best_row: return i
        return 0

    results = {
        "random": strategy_random(rows),
        "rule_of_thumb": strategy_rule_of_thumb(rows),
        "acquire": strategy_acquire(rows)
    }
    
    winner = min(results, key=lambda k: get_ydist(results[k]))
    
    return {
        "winner": winner,
        "row": results[winner],
        "tried": list(results.keys())
    }

if __name__ == "__main__":
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Mask goals for the race
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    masked_rows = []
    for row in rows:
        new_row = list(row)
        for idx in goal_indices: new_row[idx] = "?"
        masked_rows.append(new_row)
        
    def label(i): return rows[i]
    
    result = race(header, masked_rows, label)
    
    print("Analysis: Is the 'newest staff' rule of thumb effective?")
    print(f"Winner: {result['winner']}")
    print(f"Best row found at index: {result['row']}")
    print(f"Strategies compared: {', '.join(result['tried'])}")
    
    if result['winner'] == "rule_of_thumb":
        print("Conclusion: The rule of thumb is effective.")
    else:
        print("Conclusion: The rule of thumb is outperformed by more intelligent search strategies.")
    
    exit(0)
