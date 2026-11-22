import ezr
import random

def remember(header, rows):
    """
    Finds the people most like the 'average' employee and reports their tenure.
    The 'best' rows are those that are most representative of the population 
    (closest to the centroid) while having high tenure (YearsAtCompany+).
    """
    # Create a table to use library utilities
    tbl = ezr.Tbl([header] + rows)
    
    # Identify the index of the primary tenure goal
    tenure_idx = header.index('YearsAtCompany+')
    
    # Calculate the centroid of the dataset to find "typical" employees
    centroid = ezr.mids(tbl)
    
    # Score rows based on two criteria:
    # 1. Similarity to the average employee (low xdist to centroid)
    # 2. High tenure (YearsAtCompany+)
    # We want to minimize xdist and maximize tenure.
    # Score = xdist - (normalized_tenure * weight)
    
    # Get max tenure for normalization
    tenures = [r[tenure_idx] for r in rows if isinstance(r[tenure_idx], (int, float))]
    max_tenure = max(tenures) if tenures else 1
    
    scored = []
    for i, row in enumerate(rows):
        dist_to_avg = ezr.xdist(tbl, row, centroid)
        tenure = row[tenure_idx] if isinstance(row[tenure_idx], (int, float)) else 0
        # Lower score is better (closer to average, higher tenure)
        score = dist_to_avg - (tenure / max_tenure)
        scored.append((score, i))
    
    # Sort by score ascending
    scored.sort()
    
    # Return top 5% of rows (or at least 1)
    limit = max(1, len(rows) // 20)
    return [idx for score, idx in scored[:limit]]

if __name__ == "__main__":
    filename = "WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv"
    data = list(ezr.csv(filename))
    header = data[0]
    rows = data[1:]
    
    best_indices = remember(header, rows)
    
    print("--- Analysis: Employees most like the average ---")
    print(f"Identified {len(best_indices)} employees who are representative and have high tenure.")
    
    tenure_idx = header.index('YearsAtCompany+')
    total_tenure = 0
    for idx in best_indices:
        tenure = rows[idx][tenure_idx]
        total_tenure += tenure
        
    print(f"Average tenure of these representative employees: {total_tenure / len(best_indices):.2f} years.")
    print(f"Indices of these employees: {best_indices}")
    
    exit(0)
