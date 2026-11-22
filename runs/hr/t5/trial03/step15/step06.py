import ezr
import random

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and reason is a sentence explaining why the arrangement is ranked there.
    """
    # Create a table to handle the data
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goal values for the input row using the tree-based ranker
    # The ranker builds a tree on the known rows and predicts the ydist
    ranker = ezr.ranker(tbl)
    
    # Calculate predicted ydist for the target row
    # Lower ydist is better (closer to ideal goals)
    predicted_ydist = ranker(row)
    
    # Calculate ydist for all existing rows
    all_ydists = [ezr.ydist(tbl, r) for r in rows]
    
    # Calculate p: fraction of rows that are worse (have higher ydist) than our row
    # If our row has a lower ydist, it is "better"
    better_than = [d for d in all_ydists if d > predicted_ydist]
    p = len(better_than) / len(all_ydists)
    
    # Generate a reason based on the rank
    rank_percentile = int(p * 100)
    reason = (f"This arrangement is in the top {100 - rank_percentile}% of all teams "
              "based on its predicted ability to retain staff.")
    
    return p, reason

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Pick a random row from the dataset to justify
    # Mask its goal columns to simulate an unknown arrangement
    target_idx = random.randint(0, len(rows) - 1)
    target_row = list(rows[target_idx])
    
    goal_indices = [i for i, name in enumerate(header) if name.endswith(("+", "-"))]
    for idx in goal_indices:
        target_row[idx] = "?"
        
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification Analysis:")
    print(f"Rank: {p:.2f}")
    print(f"Reason: {reason}")
    
    exit(0)
