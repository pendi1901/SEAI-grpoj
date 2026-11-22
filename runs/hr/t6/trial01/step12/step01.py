import ezr
import random

def remember(header, rows):
    """
    Find rows that stay 'unusually long'.
    'YearsAtCompany+' is a goal to maximize.
    We identify the top 5% of rows based on this goal.
    """
    # Identify index for 'YearsAtCompany+'
    idx = header.index('YearsAtCompany+')
    
    # Create a list of (index, value) pairs
    # Filter out '?' if any exist
    indexed_rows = []
    for i, row in enumerate(rows):
        val = row[idx]
        if val != "?":
            indexed_rows.append((i, val))
            
    # Sort by value descending (maximize)
    indexed_rows.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 5% (max 40 rows for 800 total)
    limit = max(1, len(rows) // 20)
    return [item[0] for item in indexed_rows[:limit]]

if __name__ == "__main__":
    # Load data
    data = list(ezr.csv("WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"))
    header = data[0]
    rows = data[1:]
    
    # Get best rows
    best_indices = remember(header, rows)
    
    # Print summary for the customer
    print(f"Found {len(best_indices)} employees with the longest tenure.")
    print("Top 3 examples of their working arrangements:")
    
    # Display a few columns of interest for the top 3
    cols_to_show = ['Age', 'department', 'JobRole', 'YearsAtCompany+', 'MonthlyIncome']
    indices_to_show = [header.index(c) for c in cols_to_show if c in header]
    
    for i in best_indices[:3]:
        row = rows[i]
        details = ", ".join([f"{header[idx]}: {row[idx]}" for idx in indices_to_show])
        print(f" - {details}")
