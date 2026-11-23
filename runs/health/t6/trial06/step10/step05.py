import ezr
import step01

def blame(header, rows):
    """
    Identify input columns that best explain why the worst rows are bad.
    We compare the distribution of input values in the worst 25% of rows
    against the rest, using the tree's ability to find splits that 
    separate 'bad' from 'good'.
    """
    data = [header] + rows
    tbl = ezr.Tbl(data)
    
    # Sort rows by ydist (ascending: lower is better)
    # The worst rows are those with the highest ydist
    sorted_rows = sorted(rows, key=lambda r: ezr.ydist(tbl, r), reverse=True)
    
    # Focus on the worst 25%
    n_worst = len(rows) // 4
    worst = sorted_rows[:n_worst]
    
    # We look for input columns that are most frequently used in the 
    # top levels of a tree built to distinguish 'worst' from 'rest'.
    # A simple proxy: which input columns have the highest variance 
    # or entropy difference between the 'worst' subset and the rest.
    # Here, we use the tree's cut logic to find the most discriminative splits.
    
    # Create a temporary table for the 'worst' subset
    worst_tbl = ezr.clone(tbl, worst)
    
    # Find the best cut to separate the worst rows
    # The 'at' index of the best cut is the most influential column
    found = ezr.cut(tbl, worst)
    
    if found:
        at, _, _ = found
        return [header[at]]
    
    return []

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data_gen = ezr.csv(filename)
    
    try:
        header = next(data_gen)
        rows = list(data_gen)
        
        influential_cols = blame(header, rows)
        
        print("Analysis of bad configurations:")
        if influential_cols:
            print(f"The setting that most contributes to poor performance is: {influential_cols[0]}")
            print("This column shows the highest divergence in the worst-performing setups.")
        else:
            print("No single setting clearly explains the poor performance.")
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    
    exit(0)
