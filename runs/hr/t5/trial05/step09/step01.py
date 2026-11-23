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
    
    # Extract values, ignoring '?'
    data = []
    for i, row in enumerate(rows):
        val = row[idx]
        if val != "?":
            data.append((val, i))
    
    # Sort by YearsAtCompany+ descending
    data.sort(key=lambda x: x[0], reverse=True)
    
    # Return top 5% (max 40 rows for 800 input rows)
    limit = max(1, int(len(rows) * 0.05))
    return [item[1] for item in data[:limit]]

if __name__ == "__main__":
    # Load data
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    # Get best rows
    best_indices = remember(header, rows)
    
    # Print summary for the customer
    print(f"Found {len(best_indices)} employees with the longest tenure.")
    print("-" * 50)
    print(f"{'YearsAtCompany':<20} | {'JobRole':<20} | {'Department'}")
    print("-" * 50)
    
    idx_tenure = header.index('YearsAtCompany+')
    idx_role = header.index('jobRole')
    idx_dept = header.index('department')
    
    for i in best_indices[:10]: # Show top 10
        row = rows[i]
        print(f"{row[idx_tenure]:<20} | {row[idx_role]:<20} | {row[idx_dept]}")
    
    print("-" * 50)
    print("These employees represent the top tier of company tenure.")
