import csv

def blame(header, rows):
    """
    Identifies input columns that have the least correlation with the goal 
    'YearsAtCompany+'. We define 'least relevant' as columns whose values 
    show the smallest statistical difference between the top 20% and 
    bottom 20% of employees by tenure.
    """
    # Identify goal column
    goal_idx = next(i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-'))
    
    # Identify input columns (not goals)
    input_indices = [i for i, col in enumerate(header) if not (col.endswith('+') or col.endswith('-'))]
    
    # Sort rows by tenure to find the top 20% and bottom 20%
    sorted_rows = sorted(rows, key=lambda r: r[goal_idx])
    limit = max(1, int(len(rows) * 0.2))
    bottom_20 = sorted_rows[:limit]
    top_20 = sorted_rows[-limit:]
    
    # Calculate difference in distribution between top and bottom groups
    # Small difference means the column has little impact on tenure
    scores = []
    for i in input_indices:
        col_name = header[i]
        vals_bottom = [r[i] for r in bottom_20]
        vals_top = [r[i] for r in top_20]
        
        if isinstance(vals_bottom[0], (int, float)):
            # Numeric: use absolute difference of means
            m_bottom = sum(vals_bottom) / len(vals_bottom)
            m_top = sum(vals_top) / len(vals_top)
            diff = abs(m_top - m_bottom)
        else:
            # Symbolic: use Jaccard-like distance (percentage of overlap)
            set_bottom = set(vals_bottom)
            set_top = set(vals_top)
            intersection = set_bottom.intersection(set_top)
            union = set_bottom.union(set_top)
            diff = 1.0 - (len(intersection) / len(union) if union else 0)
            
        scores.append((diff, col_name))
    
    # Sort by difference ascending (smallest difference = least impact)
    scores.sort(key=lambda x: x[0])
    
    # Return the names of the 5 columns with the least impact
    return [s[1] for s in scores[:5]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    header = None
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = []
            for i, val in enumerate(row):
                if header[i][0].isupper():
                    try:
                        processed_row.append(float(val))
                    except ValueError:
                        processed_row.append(val)
                else:
                    processed_row.append(val)
            rows.append(processed_row)
            
    irrelevant_cols = blame(header, rows)
    
    print("Data Collection Optimization:")
    print("The following columns show the least correlation with employee tenure.")
    print("You may consider stopping the collection of these fields:")
    for col in irrelevant_cols:
        print(f"- {col}")
    
    exit(0)
