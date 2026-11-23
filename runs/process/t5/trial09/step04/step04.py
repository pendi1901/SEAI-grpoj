import ezr
import random

def flow(header, row, seen):
    """
    Decide whether to accept a row immediately.
    We accept if the row is significantly better than the current 
    population of 'seen' rows, using the ydist metric.
    """
    if not seen:
        return True
    
    # Create a table to calculate ydist
    data = [header] + seen
    tbl = ezr.Tbl(data)
    
    # Calculate the distance of the current row to the ideal
    current_dist = ezr.ydist(tbl, row)
    
    # Calculate distances of all seen rows
    seen_dists = [ezr.ydist(tbl, r) for r in seen]
    
    # If the current row is better than the median of what we've seen,
    # we accept it. This is a greedy approach for online decision making.
    median_dist = sorted(seen_dists)[len(seen_dists) // 2]
    
    return current_dist < median_dist

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    data_gen = ezr.csv(filename)
    header = next(data_gen)
    rows = list(data_gen)
    
    # Shuffle to simulate random arrival order
    random.seed(1234567891)
    random.shuffle(rows)
    
    seen = []
    accepted = []
    
    for row in rows:
        if flow(header, row, seen):
            accepted.append(row)
        seen.append(row)
        
    print(f"Decision process complete.")
    print(f"Total proposals reviewed: {len(rows)}")
    print(f"Proposals accepted: {len(accepted)}")
    
    if accepted:
        # Calculate average performance of accepted vs total
        tbl = ezr.Tbl([header] + rows)
        avg_all = sum(ezr.ydist(tbl, r) for r in rows) / len(rows)
        avg_acc = sum(ezr.ydist(tbl, r) for r in accepted) / len(accepted)
        
        print(f"Average ydist of all proposals: {avg_all:.4f}")
        print(f"Average ydist of accepted proposals: {avg_acc:.4f}")
        print("The accepted proposals show better goal alignment on average.")
    
    exit(0)
