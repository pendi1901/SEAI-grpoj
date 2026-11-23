import ezr
import random

def remember(header, rows):
    """
    Finds the setups most similar to the current team's setup (the first row)
    and evaluates their performance.
    """
    # Create a table to manage column roles and distance metrics
    tbl = ezr.Tbl([header] + rows)
    
    # The team's current setup is the first row
    team_setup = rows[0]
    
    # Calculate distance from the team's setup for all rows
    # We use xdist to find rows with similar input configurations
    distances = []
    for i, row in enumerate(rows):
        # Skip the team's own row
        if i == 0:
            continue
        d = ezr.xdist(tbl, row, team_setup)
        distances.append((d, i))
    
    # Sort by distance (ascending) to find the most similar setups
    distances.sort(key=lambda x: x[0])
    
    # Return the top 5% of rows (800 rows * 0.05 = 40)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in distances[:limit]]

if __name__ == "__main__":
    filename = "Health-ClosedIssues0000.n1000.train.csv"
    data = list(ezr.csv(filename))
    
    if not data:
        print("No data found.")
        exit(1)
        
    header = data[0]
    rows = data[1:]
    
    # Get the indices of the most similar setups
    similar_indices = remember(header, rows)
    
    # Create a table for scoring
    tbl = ezr.Tbl([header] + rows)
    
    print(f"Found {len(similar_indices)} setups most similar to the team's current configuration.")
    print(f"{'Index':<10} | {'Y-Dist (Performance)':<20}")
    print("-" * 35)
    
    for idx in similar_indices:
        # ydist measures how close the goals are to the ideal (lower is better)
        score = ezr.ydist(tbl, rows[idx])
        print(f"{idx:<10} | {score:.4f}")
        
    print("\nNote: Y-Dist represents the distance to the ideal goal values.")
    print("Lower Y-Dist indicates better performance.")
    
    exit(0)
