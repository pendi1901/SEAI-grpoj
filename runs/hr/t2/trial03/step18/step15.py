import csv
import step05

def blame(header, rows):
    """
    Identifies input columns that have the least correlation with tenure.
    We identify the 'worst' rows (bottom 25% by tenure) and compare the 
    distribution of input columns against the population. Columns with 
    the smallest deviation from the population mean are considered 
    'irrelevant' to the outcome.
    """
    years_idx = header.index('YearsAtCompany+')
    
    # Identify input columns (excluding goals)
    input_indices = [
        i for i, h in enumerate(header) 
        if not (h.endswith('+') or h.endswith('-'))
    ]
    
    # Sort rows by tenure to find the bottom 25%
    sorted_rows = sorted(rows, key=lambda r: r[years_idx])
    worst_rows = sorted_rows[:len(rows) // 4]
    
    # Calculate deviation scores for each input column
    scores = []
    for i in input_indices:
        col_data = [r[i] for r in rows if isinstance(r[i], (int, float))]
        if not col_data:
            continue
            
        pop_mean = sum(col_data) / len(col_data)
        worst_mean = sum(r[i] for r in worst_rows if isinstance(r[i], (int, float))) / len(worst_rows)
        
        # Score based on absolute difference from population mean
        # Smaller difference = less influence on the 'worst' group
        if pop_mean != 0:
            diff = abs(worst_mean - pop_mean) / pop_mean
            scores.append((diff, header[i]))
        else:
            scores.append((0.0, header[i]))
            
    # Return columns with the lowest deviation scores (least explanatory)
    scores.sort(key=lambda x: x[0])
    return [s[1] for s in scores[:5]]

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
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
                        processed_row.append(0.0)
                else:
                    processed_row.append(val)
            rows.append(processed_row)

    irrelevant = blame(header, rows)
    
    print("Analysis: Which columns have little impact on tenure?")
    print(f"The following columns show the least correlation with short tenure and may be candidates for removal: {', '.join(irrelevant)}.")
    print("Logic: These columns show the smallest statistical deviation in the bottom 25% of employees compared to the general population.")
