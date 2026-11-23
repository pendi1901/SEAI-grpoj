import csv

def blame(header, rows):
    """
    Identifies input columns that have the least correlation with the goal columns.
    We define 'least correlation' as columns where the distribution of values
    is statistically similar between the 'best' and 'worst' performers.
    
    Returns a list of column names that are candidates for removal.
    """
    goal_indices = [i for i, h in enumerate(header) if h.endswith('+') or h.endswith('-')]
    input_indices = [i for i, h in enumerate(header) if i not in goal_indices]
    
    # Define 'best' and 'worst' rows based on the first goal column
    goal_idx = goal_indices[0]
    is_max = header[goal_idx].endswith('+')
    
    sorted_rows = sorted(rows, key=lambda r: r[goal_idx], reverse=is_max)
    n = len(sorted_rows)
    # Compare top 25% vs bottom 25%
    top_25 = sorted_rows[:max(1, n // 4)]
    bot_25 = sorted_rows[-max(1, n // 4):]
    
    def get_dist_diff(col_idx):
        vals_top = [r[col_idx] for r in top_25]
        vals_bot = [r[col_idx] for r in bot_25]
        
        if isinstance(vals_top[0], (int, float)):
            m_top = sum(vals_top) / len(vals_top)
            m_bot = sum(vals_bot) / len(vals_bot)
            # Normalize difference by range
            all_vals = [r[col_idx] for r in rows]
            r_range = max(all_vals) - min(all_vals)
            return abs(m_top - m_bot) / (r_range if r_range != 0 else 1.0)
        else:
            # For symbolic, check if the distribution of categories is similar
            set_top = set(vals_top)
            set_bot = set(vals_bot)
            # Jaccard-like distance
            intersection = set_top.intersection(set_bot)
            union = set_top.union(set_bot)
            return 1.0 - (len(intersection) / len(union) if union else 0)

    # Calculate scores for all inputs
    scores = []
    for i in input_indices:
        scores.append((get_dist_diff(i), header[i]))
    
    # Sort by score ascending (lowest difference = least impact)
    scores.sort(key=lambda x: x[0])
    
    # Return the bottom 5 columns that have the least impact
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

    candidates = blame(header, rows)
    print("Columns with minimal impact on tenure (candidates for removal):")
    for col in candidates:
        print(f"- {col}")
