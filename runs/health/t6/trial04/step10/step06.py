import ezr
import step01
import step02

def justify(header, rows, row):
    """
    Returns (p, reason): p is the fraction of rows that 'row' is better than,
    and a sentence explaining why.
    """
    # Create a table to establish the goal space
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the goals for the target row
    # We use the tree-based ranker to predict the performance of the target row
    # based on the training data (all rows)
    ranker = ezr.ranker(tbl)
    predicted_score = ranker(row)
    
    # Calculate scores for all existing rows
    # Lower ydist is better, so we negate it to get a "goodness" score
    all_scores = [-ezr.ydist(tbl, r) for r in rows]
    
    # The target row's score is estimated by the ranker (which returns mean ydist)
    # We negate it to match the "higher is better" logic of our scores
    target_score = -predicted_score
    
    # Calculate fraction of rows that are worse than the target row
    better_than_count = sum(1 for s in all_scores if s < target_score)
    p = better_than_count / len(rows)
    
    # Generate a reason based on the performance
    reason = (f"This configuration is estimated to outperform {int(p * 100)}% "
              "of the known setups based on its input parameters.")
    
    return p, reason

if __name__ == "__main__":
    file_path = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(file_path))
    header = all_data[0]
    rows = all_data[1:]
    
    # Pick a sample row to justify (e.g., the 10th row)
    target_row = list(rows[10])
    # Mask the goals
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for idx in goal_indices:
        target_row[idx] = "?"
        
    p, reason = justify(header, rows, target_row)
    
    print(f"Justification for configuration:")
    print(f"  {reason}")
    print(f"  (Score percentile: {p:.4f})")
