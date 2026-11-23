import ezr
import random

def flow(header, row, seen):
    """
    Detects if a new row is an outlier compared to the 'seen' population.
    We use the distance from the centroid of the input columns (xdist)
    as a measure of how 'unusual' a row is. If the distance is 
    significantly higher than the average distance seen so far, 
    we flag it as a team shift.
    """
    if len(seen) < 20:
        return False
    
    # Create a table to handle column definitions and distance calculations
    # We use the 'seen' rows to establish the current population norm
    tbl = ezr.Tbl([header] + seen)
    
    # Calculate the centroid (mids) of the input columns for the seen population
    centroid = ezr.mids(tbl)
    
    # Calculate the distance of the current row from the centroid
    current_dist = ezr.xdist(tbl, row, centroid)
    
    # Calculate the average distance of all seen rows from the centroid
    seen_distances = [ezr.xdist(tbl, r, centroid) for r in seen]
    avg_dist = sum(seen_distances) / len(seen_distances)
    
    # If the current row's distance is more than 2 standard deviations 
    # above the mean distance, we flag it as a shift in team composition.
    # We use a simple standard deviation approximation.
    variance = sum((d - avg_dist)**2 for d in seen_distances) / len(seen_distances)
    std_dev = variance**0.5
    
    return current_dist > (avg_dist + 2 * std_dev)

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Simulate arrival of rows one by one
    seen = []
    shifts = 0
    for row in rows:
        if flow(header, row, seen):
            shifts += 1
        seen.append(row)
        
    print("Team Composition Shift Analysis")
    print("-" * 50)
    print(f"Total employees processed: {len(rows)}")
    print(f"Number of detected team shifts: {shifts}")
    print("-" * 50)
    print("Logic: Flagged rows that deviate significantly (2+ std devs)")
    print("from the running average input-space centroid.")
