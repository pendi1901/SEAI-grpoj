import ezr
import step01

def flow(header, row, seen):
    """
    Warn the customer if a new row is significantly worse than the 
    performance trend established by the 'seen' rows.
    
    We define 'going bad' as the current row's ydist being significantly 
    higher (worse) than the mean ydist of the previously seen rows.
    """
    if not seen:
        return False
    
    # Create a table from seen rows to calculate performance metrics
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the mean performance of the history
    seen_ydists = [ezr.ydist(tbl, r) for r in seen]
    mean_ydist = sum(seen_ydists) / len(seen_ydists)
    
    # Calculate performance of the current row
    # Note: ydist handles '?' by normalizing based on the table's columns
    current_ydist = ezr.ydist(tbl, row)
    
    # If the current row is worse than the mean by more than 1 standard deviation,
    # we flag it as "going bad".
    # Standard deviation calculation:
    variance = sum((d - mean_ydist) ** 2 for d in seen_ydists) / len(seen_ydists)
    std_dev = variance ** 0.5
    
    # Return True if the row is significantly worse (higher ydist) than the mean
    return current_ydist > (mean_ydist + std_dev)

if __name__ == "__main__":
    file_path = "pom3a.n1000.train.csv"
    data = list(ezr.csv(file_path))
    header = data[0]
    rows = data[1:]
    
    warnings = 0
    seen = []
    
    # Simulate arrival one by one
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            warnings += 1
            # Print a warning for the first few occurrences
            if warnings <= 5:
                print(f"Warning: Row {i} is performing significantly worse than the trend.")
        seen.append(row)
        
    print("-" * 40)
    print(f"Total rows processed: {len(rows)}")
    print(f"Total 'bad' performance warnings: {warnings}")
    print("Decision logic: Flagged rows that are > 1 std dev worse than the mean ydist of history.")
    exit(0)
