import ezr
import step01
import step04

def flow(header, row, seen):
    """
    Decide if the current row is 'good enough' to stop.
    We use the logic from step04, which checks if the current row
    is in the top 5% of the distribution of rows seen so far.
    """
    return step04.flow(header, row, seen)

if __name__ == "__main__":
    file_path = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(file_path))
    header = all_data[0]
    rows = all_data[1:]
    
    seen = []
    found = False
    print("Monitoring incoming configurations for optimal performance...")
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Stopping criteria met at row {i} (index {i}).")
            print(f"This configuration is in the top 5% of all seen so far.")
            print(f"Values: {row}")
            found = True
            break
        seen.append(row)
    
    if not found:
        print("Processed all rows; no configuration met the quality threshold.")
    
    exit(0)
