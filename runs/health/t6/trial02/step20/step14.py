import ezr
import step04

def flow(header, row, seen):
    """
    Decides whether to stop at the current row.
    We stop if the current row is in the top 5% of all potential rows,
    estimated by comparing it against the distribution of seen rows.
    """
    return step04.flow(header, row, seen)

if __name__ == "__main__":
    # Load data
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    all_data = list(ezr.csv(filename))
    header = all_data[0]
    rows = all_data[1:]
    
    seen = []
    stopped = False
    for i, row in enumerate(rows):
        if flow(header, row, seen):
            print(f"Optimization stopped at row {i+1} (1-based index).")
            print("The current configuration is in the top 5% of all seen setups.")
            print(f"Row values: {row}")
            stopped = True
            break
        seen.append(row)
    
    if not stopped:
        print("No row met the stopping criteria; processed all 800 rows.")
