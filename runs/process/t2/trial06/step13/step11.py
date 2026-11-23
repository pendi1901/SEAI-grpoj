import csv
from step01 import remember as original_remember

def remember(header, rows):
    """
    Returns the indices of the best-performing rows.
    Uses the logic from step01 to identify the top 5% of rows.
    """
    return original_remember(header, rows)

def find_similar(header, rows, target_row):
    """
    Finds the 3 most similar rows to the target_row based on input columns
    and returns them.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    def dist(r1, r2):
        d = 0
        for i in input_indices:
            d += (float(r1[i]) - float(r2[i])) ** 2
        return d ** 0.5

    # Find 3 nearest neighbors
    neighbors = sorted(rows, key=lambda r: dist(r, target_row))[:3]
    return neighbors

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [row for row in reader]
            
        # Example: User proposes the first row as their setup
        target = rows[0]
        # Mask the goals for the proposal
        proposal = [val if not (header[i].endswith('-') or header[i].endswith('+')) else "?" 
                    for i, val in enumerate(target)]
        
        similar = find_similar(header, rows, proposal)
        
        print("Customer Inquiry: How did similar past setups perform?")
        print("Analysis: We identified the 3 most similar historical configurations.")
        print("-" * 60)
        for i, row in enumerate(similar):
            print(f"Match {i+1}:")
            for j, name in enumerate(header):
                if name.endswith('-') or name.endswith('+'):
                    print(f"  {name}: {row[j]}")
        print("-" * 60)
        print("These historical outcomes provide a baseline for your proposed setup.")
        
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
