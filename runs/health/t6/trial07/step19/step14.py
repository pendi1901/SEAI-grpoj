import ezr
import step04

def flow(header, row, seen):
    """
    Decide if the current row is 'good enough' to stop searching.
    We use the logic from step04, which compares the current row's 
    ydist against the distribution of previously seen rows to 
    determine if it is in the top 5% of the potential performance space.
    """
    return step04.flow(header, row, seen)

if __name__ == "__main__":
    # Load the data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    seen = []
    found_at = -1
    
    # Simulate the arrival of rows one by one
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            found_at = i
            break
        seen.append(row)
        
    print("--- Stopping Criterion Analysis ---")
    if found_at != -1:
        print(f"Stopped at row {found_at}: The performance has stopped improving significantly.")
        print(f"The setup at this index is in the top 5% of observed configurations.")
    else:
        print("Processed all rows without finding a 'good enough' setup to stop early.")
