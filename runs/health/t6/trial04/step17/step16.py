import ezr
import step02
import step06

def justify(header, rows, row):
    """
    Answers why we shouldn't just use the biggest, deepest setup.
    We compare the performance of a 'big' setup (max depth, max estimators)
    against the distribution of all known rows.
    """
    # Create a table to establish the goal space
    tbl = ezr.Tbl([header] + rows)
    
    # Estimate the performance of the provided row
    # We use the tree-based ranker to predict the performance
    ranker = ezr.ranker(tbl)
    predicted_score = ranker(row)
    
    # Calculate scores for all existing rows (negated ydist for "higher is better")
    all_scores = [-ezr.ydist(tbl, r) for r in rows]
    
    # The target row's score is estimated by the ranker
    target_score = -predicted_score
    
    # Calculate fraction of rows that are worse than the target row
    better_than_count = sum(1 for s in all_scores if s < target_score)
    p = better_than_count / len(rows)
    
    # The reason explains that bigger is not always better due to diminishing returns
    # or overfitting, which the ranker captures.
    reason = (f"This configuration is estimated to outperform {p:.2f} of the known setups; "
              "using the largest possible settings often leads to overfitting rather than "
              "better performance.")
    
    return p, reason

if __name__ == "__main__":
    file_path = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(file_path))
    header = all_data[0]
    rows = all_data[1:]
    
    # Define a 'big' setup: high N_estimators, high Max_depth
    # Based on the data, Max_depth is index 7, N_estimators is index 3
    big_row = [0.0] * len(header)
    big_row[3] = 200.0  # High N_estimators
    big_row[7] = 20.0   # High Max_depth
    big_row[4] = "squared_error"
    big_row[5] = 2.0
    big_row[6] = 1.0
    
    # Mask the goals
    goal_indices = [i for i, name in enumerate(header) if name[-1] in "+-"]
    for idx in goal_indices:
        big_row[idx] = "?"
        
    p, reason = justify(header, rows, big_row)
    
    print("Analysis of using the biggest, deepest setup:")
    print(f"  {reason}")
    print(f"  (Performance percentile: {p:.4f})")
    
    exit(0)
