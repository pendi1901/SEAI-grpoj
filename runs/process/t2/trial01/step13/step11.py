import csv
import math
from step01 import remember as get_best_indices

def find_similar(header, rows, target_row, k=5):
    """
    Finds the k most similar rows to the target_row using Euclidean distance
    on the input columns.
    """
    input_indices = [i for i, name in enumerate(header) 
                     if not (name.endswith('-') or name.endswith('+'))]
    
    def dist(r1, r2):
        d2 = 0
        for i in input_indices:
            d2 += (r1[i] - r2[i])**2
        return math.sqrt(d2)

    distances = []
    for i, row in enumerate(rows):
        distances.append((dist(row, target_row), i))
    
    distances.sort()
    return [idx for d, idx in distances[:k]]

def get_goal_values(header, row):
    """Extracts goal values from a row."""
    return {name: row[i] for i, name in enumerate(header) 
            if name.endswith('-') or name.endswith('+')}

def remember(header, rows):
    """
    Required by harness: returns indices of the best 5% of rows.
    """
    return get_best_indices(header, rows)

if __name__ == "__main__":
    filename = "pom3a.n1000.train.csv"
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append([float(val) for val in row])
        
        # Pick a sample row to simulate the customer's proposal
        target_row = rows[100]
        
        # Find similar past setups
        similar_indices = find_similar(header, rows, target_row)
        
        print("Customer Inquiry: Here is the setup I am about to propose. Show me the past ones most like it, and how they turned out.")
        print(f"\nTarget Setup (Row 100) Goals: {get_goal_values(header, target_row)}")
        print("\nMost similar past setups:")
        for idx in similar_indices:
            goals = get_goal_values(header, rows[idx])
            print(f" - Row {idx}: {goals}")
            
        # Show how the best ones turned out
        best_indices = remember(header, rows)
        print(f"\nFor context, the top-performing setups in our history achieved these average goals:")
        for name in [h for h in header if h.endswith('-') or h.endswith('+')]:
            avg = sum(rows[i][header.index(name)] for i in best_indices) / len(best_indices)
            print(f" - {name}: {avg:.4f}")
            
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        exit(1)
