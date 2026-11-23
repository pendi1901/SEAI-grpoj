import csv

def blame(header, rows):
    """
    Identifies input columns that have little to no correlation with tenure.
    We define 'tenure' as the sum of normalized goal columns.
    We then calculate the correlation between each input column and this tenure score.
    Columns with very low correlation are candidates to stop collecting.
    """
    goal_indices = [i for i, col in enumerate(header) if col.endswith('+') or col.endswith('-')]
    input_indices = [i for i, col in enumerate(header) if not (col.endswith('+') or col.endswith('-'))]
    
    # Calculate a normalized tenure score for each row
    # Goals ending in + are maximized, - are minimized.
    scores = []
    for row in rows:
        score = 0
        for i in goal_indices:
            val = row[i]
            if header[i].endswith('+'):
                score += val
            else:
                score -= val
        scores.append(score)
    
    # Calculate correlation between each input column and the tenure score
    # We use a simple difference in means approach:
    # If the mean of the column for the top 25% of tenure is similar to the 
    # mean for the bottom 25%, the column has little impact.
    sorted_indices = sorted(range(len(rows)), key=lambda i: scores[i])
    n = len(rows) // 4
    bottom_rows = [rows[i] for i in sorted_indices[:n]]
    top_rows = [rows[i] for i in sorted_indices[-n:]]
    
    useless_columns = []
    for i in input_indices:
        col_name = header[i]
        
        if isinstance(rows[0][i], float):
            # Numeric: compare means
            vals_bottom = [row[i] for row in bottom_rows]
            vals_top = [row[i] for row in top_rows]
            mean_bottom = sum(vals_bottom) / len(vals_bottom)
            mean_top = sum(vals_top) / len(vals_top)
            
            # If means are very close (within 5% of the range), it's likely useless
            all_vals = [row[i] for row in rows]
            col_range = max(all_vals) - min(all_vals)
            if col_range > 0 and abs(mean_top - mean_bottom) < (0.05 * col_range):
                useless_columns.append(col_name)
        else:
            # Symbolic: compare distribution
            categories = set(row[i] for row in rows)
            is_useless = True
            for cat in categories:
                prob_bottom = sum(1 for row in bottom_rows if row[i] == cat) / n
                prob_top = sum(1 for row in top_rows if row[i] == cat) / n
                if abs(prob_top - prob_bottom) > 0.1: # 10% threshold
                    is_useless = False
                    break
            if is_useless:
                useless_columns.append(col_name)
                
    return useless_columns

if __name__ == "__main__":
    filename = 'WA_Fn-UseC_-HR-Employee-Attrition.n1000.train.csv'
    rows = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            processed_row = [float(val) if header[i][0].isupper() else val for i, val in enumerate(row)]
            rows.append(processed_row)
    
    useless = blame(header, rows)
    
    print("Analysis: Columns that have little to no impact on employee tenure.")
    print("These columns could potentially be removed from data collection:")
    for col in useless:
        print(f"- {col}")
